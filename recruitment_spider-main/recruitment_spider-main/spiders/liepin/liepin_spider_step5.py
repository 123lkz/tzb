#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
猎聘网爬虫 - 第五步
功能：对step4生成的4个part数据进行去重处理，合并到统一的集合中

主要步骤：
1. 从MongoDB读取4个part的数据
2. 根据job_link进行去重
3. 将去重后的数据保存到统一的集合中，并按照数量拆分成4个部分

数据存储：
- 输入集合：
  * liepin_job_raw_part1
  * liepin_job_raw_part2
  * liepin_job_raw_part3
  * liepin_job_raw_part4
- 输出集合：
  * liepin_step3_urls（总集合）
  * liepin_step3_urls_part1
  * liepin_step3_urls_part2
  * liepin_step3_urls_part3
  * liepin_step3_urls_part4
"""

import os
import sys
import logging
from datetime import datetime
from pymongo import MongoClient
from tqdm import tqdm
import math

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "liepin_spider_step5")
except ImportError:
    # 如果无法导入log_manager，则使用基本配置
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("spiders.liepin_spider")

class LiepinSpiderStep5:
    """猎聘网数据去重处理"""
    
    def __init__(self):
        # MongoDB配置
        self.mongo_uri = "mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test"
        self.mongo_db = "da_test"
        self.input_collections = [
            "liepin_job_raw_part1",
            "liepin_job_raw_part2",
            "liepin_job_raw_part3",
            "liepin_job_raw_part4"
        ]
        self.output_collection = "liepin_step3_urls"
        self.output_part_collections = [
            "liepin_step3_urls_part1",
            "liepin_step3_urls_part2",
            "liepin_step3_urls_part3",
            "liepin_step3_urls_part4"
        ]
        
        # MongoDB连接
        self.mongo_client = None
        self.db = None
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
    def _init_mongodb(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            logger.info("MongoDB连接成功")
        except Exception as e:
            logger.error(f"MongoDB连接失败: {str(e)}")
            raise
    
    def get_url_key(self, doc):
        """生成URL的唯一键，用于比较"""
        return (
            doc.get('industry_parent_code', ''),
            doc.get('industry_child_code', ''),
            doc.get('job_type_name', ''),
            doc.get('province_code', '')
        )
    
    def analyze_collection_group(self, url_collection, log_collection):
        """分析单个集合组的数据差异"""
        logger.info(f"分析集合组: {url_collection} vs {log_collection}")
        
        # 获取url_part数据
        url_docs = list(self.db[url_collection].find({}))
        url_keys = {self.get_url_key(doc): doc for doc in url_docs}
        
        # 获取log_part数据
        log_docs = list(self.db[log_collection].find({}))
        log_keys = {self.get_url_key(doc): doc for doc in log_docs}
        
        logger.info(f"URL集合数量: {len(url_docs)}")
        logger.info(f"LOG集合数量: {len(log_docs)}")
        
        # 找出只在log_part中存在的数据
        only_in_log = []
        for key, doc in log_keys.items():
            if key not in url_keys:
                only_in_log.append(doc)
        
        # 找出只在url_part中存在的数据
        only_in_url = []
        for key, doc in url_keys.items():
            if key not in log_keys:
                only_in_url.append(doc)
        
        # 找出共同存在的数据
        common_keys = set(url_keys.keys()) & set(log_keys.keys())
        
        logger.info(f"只在LOG中存在的数据数量: {len(only_in_log)}")
        logger.info(f"只在URL中存在的数据数量: {len(only_in_url)}")
        logger.info(f"共同存在的数据数量: {len(common_keys)}")
        
        return {
            'url_collection': url_collection,
            'log_collection': log_collection,
            'url_count': len(url_docs),
            'log_count': len(log_docs),
            'only_in_log': only_in_log,
            'only_in_url': only_in_url,
            'common_count': len(common_keys)
        }
    
    def validate_collections(self):
        """验证所有集合组的数据一致性"""
        logger.info("开始验证step2集合数据一致性...")
        
        collection_groups = [
            {
                'url_part': 'liepin_step2_urls_part1',
                'log_part': 'liepin_step2_urls_202504_log_part1'
            },
            {
                'url_part': 'liepin_step2_urls_part2', 
                'log_part': 'liepin_step2_urls_202504_log_part2'
            },
            {
                'url_part': 'liepin_step2_urls_part3',
                'log_part': 'liepin_step2_urls_202504_log_part3'
            },
            {
                'url_part': 'liepin_step2_urls_part4',
                'log_part': 'liepin_step2_urls_202504_log_part4'
            }
        ]
        
        all_valid = True
        results = []
        
        for group in collection_groups:
            result = self.analyze_collection_group(
                group['url_part'], 
                group['log_part']
            )
            results.append(result)
            
            # 检查是否有不一致的数据
            if result['only_in_log'] or result['only_in_url']:
                all_valid = False
                logger.error(f"集合组 {group['url_part']} vs {group['log_part']} 数据不一致！")
                logger.error(f"  只在LOG中的数据: {len(result['only_in_log'])}")
                logger.error(f"  只在URL中的数据: {len(result['only_in_url'])}")
            else:
                logger.info(f"集合组 {group['url_part']} vs {group['log_part']} 数据一致 ✓")
        
        # 汇总统计
        total_url_count = sum(r['url_count'] for r in results)
        total_log_count = sum(r['log_count'] for r in results)
        total_only_in_log = sum(len(r['only_in_log']) for r in results)
        total_only_in_url = sum(len(r['only_in_url']) for r in results)
        total_common = sum(r['common_count'] for r in results)
        
        logger.info(f"汇总统计:")
        logger.info(f"  总URL数据量: {total_url_count}")
        logger.info(f"  总LOG数据量: {total_log_count}")
        logger.info(f"  总只在LOG中的数据量: {total_only_in_log}")
        logger.info(f"  总只在URL中的数据量: {total_only_in_url}")
        logger.info(f"  总共同数据量: {total_common}")
        
        if all_valid:
            logger.info("所有step2集合组数据验证通过！")
        else:
            logger.error("存在数据不一致的集合组，请先清理数据！")
        
        return all_valid
    
    def process_data(self):
        """处理数据去重"""
        try:
            # 首先验证step2集合组的数据一致性
            if not self.validate_collections():
                logger.error("step2数据验证失败，程序退出！请先清理不一致的数据。")
                return
            
            logger.info("step2数据验证通过，开始处理数据去重...")
            
            # 用于存储所有数据的字典，以job_link为键
            all_jobs = {}
            total_processed = 0
            total_duplicates = 0
            
            # 处理每个part的数据
            for collection_name in self.input_collections:
                collection = self.db[collection_name]
                total_docs = collection.count_documents({})
                
                logger.info(f"开始处理集合 {collection_name}，共 {total_docs} 条记录")
                
                # 使用tqdm显示进度
                for doc in tqdm(collection.find({}, {'job_link': 1, 'job_id': 1,'job_data_prom_id':1, 'title': 1, 'company': 1}), total=total_docs):
                    job_link = doc.get('job_link')
                    if job_link:
                        if job_link not in all_jobs:
                            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            temp = {
                                'detail_url': job_link,
                                'collection_name': collection_name,
                                'job_id': doc.get('job_id'),
                                'job_data_prom_id': doc.get('job_data_prom_id'),
                                'collection_id': doc.get('_id'),
                                'crawl_time': current_time
                            }
                            all_jobs[job_link] = temp
                        else:
                            total_duplicates += 1
                    total_processed += 1
            
            # 将去重后的数据写入总集合
            output_collection = self.db[self.output_collection]
            output_collection.delete_many({})
            
            jobs_list = list(all_jobs.values())
            if jobs_list:
                output_collection.insert_many(jobs_list)
                output_collection.create_index("detail_url", unique=True)
            
            # 清空所有分片集合
            for collection_name in self.output_part_collections:
                self.db[collection_name].delete_many({})
            
            # 将数据分成4份并写入分片集合
            total_jobs = len(jobs_list)
            chunk_size = math.ceil(total_jobs / 4)
            
            for i in range(4):
                start_idx = i * chunk_size
                end_idx = min((i + 1) * chunk_size, total_jobs)
                chunk = jobs_list[start_idx:end_idx]
                
                if chunk:
                    collection = self.db[self.output_part_collections[i]]
                    collection.insert_many(chunk)
                    collection.create_index("detail_url", unique=True)
                    logger.info(f"分片集合 {self.output_part_collections[i]} 写入完成，共 {len(chunk)} 条记录")
            
            logger.info(f"数据处理完成:")
            logger.info(f"总处理记录数: {total_processed}")
            logger.info(f"重复记录数: {total_duplicates}")
            logger.info(f"去重后记录数: {total_jobs}")
            
        except Exception as e:
            logger.error(f"数据处理失败: {str(e)}")
            raise
    
    def close(self):
        """关闭MongoDB连接"""
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("MongoDB连接已关闭")

def main():
    """主函数"""
    spider = LiepinSpiderStep5()
    try:
        spider.process_data()
    finally:
        spider.close()

if __name__ == "__main__":
    main() 
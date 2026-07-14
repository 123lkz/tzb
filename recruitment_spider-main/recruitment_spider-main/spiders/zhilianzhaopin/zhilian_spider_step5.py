#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智联招聘爬虫 - 第五步
功能：对step4生成的4个part数据进行去重处理，合并到统一的集合中

主要步骤：
1. 从MongoDB读取4个part的数据
2. 根据positionUrl进行去重
3. 将去重后的数据保存到统一的集合中，并按照数量拆分成4个部分

数据存储：
- 输入集合：
  * zhilian_job_raw_part1
  * zhilian_job_raw_part2
  * zhilian_job_raw_part3
  * zhilian_job_raw_part4
- 输出集合：
  * zhilian_step3_urls（总集合）
  * zhilian_step3_urls_part1
  * zhilian_step3_urls_part2
  * zhilian_step3_urls_part3
  * zhilian_step3_urls_part4
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
    logger = get_logger(__name__, "zhilian_spider")
except ImportError:
    # 如果无法导入log_manager，则使用基本配置
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("spiders.zhilian_spider")

class ZhilianSpiderStep5:
    """智联招聘数据去重处理"""
    
    def __init__(self):
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.input_collections = [
            "zhilian_job_raw_part1",
            "zhilian_job_raw_part2",
            "zhilian_job_raw_part3",
            "zhilian_job_raw_part4"
        ]
        self.output_collection = "zhilian_step3_urls"
        self.output_part_collections = [
            "zhilian_step3_urls_part1",
            "zhilian_step3_urls_part2",
            "zhilian_step3_urls_part3",
            "zhilian_step3_urls_part4"
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
    
    def process_data(self):
        """处理数据去重"""
        try:
            # 检查数据一致性
            logger.info("开始检查数据一致性...")
            
            # 检查每个分片的数据一致性
            for i in range(1, 5):
                url_collection = f"zhilian_step2_urls_part{i}"
                log_collection = f"zhilian_step2_urls_202504_log_part{i}"
                
                # 获取URL集合数据
                url_data = list(self.db[url_collection].find(
                    {},
                    {'city_code': 1, 'industry_code': 1, 'job_type_code': 1, '_id': 0}
                ))
                # 获取日志集合数据
                log_data = list(self.db[log_collection].find(
                    {},
                    {'city_code': 1, 'industry_code': 1, 'job_type_code': 1, '_id': 0}
                ))
                
                url_count = len(url_data)
                log_count = len(log_data)
                
                logger.info(f"集合 {url_collection} 中的URL数量: {url_count}")
                logger.info(f"集合 {log_collection} 中的日志数量: {log_count}")
                
                # 检查数量是否一致
                if url_count != log_count:
                    logger.error(f"数据不一致！{url_collection}中的URL数量({url_count})与{log_collection}中的日志数量({log_count})不匹配")
                    logger.error("请检查数据后再运行程序")
                    return
                
                # 验证字段组合是否完全匹配
                url_combinations = {(item['city_code'], item['industry_code'], item['job_type_code']) for item in url_data}
                log_combinations = {(item['city_code'], item['industry_code'], item['job_type_code']) for item in log_data}
                
                # 检查是否有不匹配的组合
                if url_combinations != log_combinations:
                    # 找出不匹配的组合
                    url_only = url_combinations - log_combinations
                    log_only = log_combinations - url_combinations
                    
                    if url_only:
                        logger.error(f"part{i} url集合中存在但log集合中不存在的组合: {url_only}")
                    if log_only:
                        logger.error(f"part{i} log集合中存在但url集合中不存在的组合: {log_only}")
                    logger.error("请检查数据后再运行程序")
                    return
                
                logger.info(f"part{i} 数据一致性检查通过")
            
            logger.info("所有分片数据一致性检查通过，开始处理...")
            
            # 用于存储所有数据的字典，以positionUrl为键
            all_jobs = {}
            total_processed = 0
            total_duplicates = 0
            
            # 处理每个part的数据
            for collection_name in self.input_collections:
                collection = self.db[collection_name]
                total_docs = collection.count_documents({})
                
                logger.info(f"开始处理集合 {collection_name}，共 {total_docs} 条记录")
                
                # 使用tqdm显示进度
                for doc in tqdm(collection.find({},{'positionUrl':1}), total=total_docs):
                    position_url = doc.get('positionUrl')
                    if position_url:
                        if position_url not in all_jobs:
                            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            temp = {
                                'positionUrl':position_url,                                
                                'crawl_time':current_time,
                                'collection_name':collection_name,
                                'collection_id':doc.get('_id'),
                            }
                            all_jobs[position_url] = temp
                        else:
                            total_duplicates += 1
                    total_processed += 1
            
            # 将去重后的数据写入总集合
            output_collection = self.db[self.output_collection]
            output_collection.delete_many({})
            
            jobs_list = list(all_jobs.values())
            if jobs_list:
                output_collection.insert_many(jobs_list)
                output_collection.create_index("positionUrl", unique=True)
            
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
                    collection.create_index("positionUrl", unique=True)
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
    spider = ZhilianSpiderStep5()
    try:
        spider.process_data()
    finally:
        spider.close()

if __name__ == "__main__":
    main()
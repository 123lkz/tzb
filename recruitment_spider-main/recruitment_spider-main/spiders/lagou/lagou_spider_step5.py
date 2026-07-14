#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
拉勾网爬虫 - 第五步
功能：根据step4获取的职位列表，生成职位详情页URL

主要步骤：
1. 从MongoDB加载step4生成的所有part职位列表数据
2. 根据positionId生成职位详情页URL并保存到总集合
3. 将总URL列表分成4份保存

数据存储：
- 输入集合：lagou_job_raw_part1-4
- 输出总集合：lagou_step3_urls
- 输出分片集合：lagou_step3_urls_part1-4
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from tqdm import tqdm
import sys
import os
import math
import random

# 将项目根目录添加到Python路径中
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent  # 从当前文件向上找三层到项目根目录
sys.path.append(str(project_root))

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "lagou_spider_step5")
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class LagouSpiderStep5:
    """拉勾网爬虫 - 第五步"""
    
    def __init__(self):
        """初始化爬虫"""
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.mongo_client = None
        self.db = None
        self.collection = None
        
        # 输入输出集合名称
        self.input_collections = [
            'lagou_job_raw_part1',
            'lagou_job_raw_part2',
            'lagou_job_raw_part3',
            'lagou_job_raw_part4'
        ]
        self.output_collection = 'lagou_step3_urls'
        self.output_part_collections = [
            'lagou_step3_urls_part1',
            'lagou_step3_urls_part2',
            'lagou_step3_urls_part3',
            'lagou_step3_urls_part4'
        ]
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        logger.info(f"初始化完成")
    
    def _init_mongodb(self) -> None:
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            self.collection = self.db[self.output_collection]
            
            # 创建索引
            self.collection.create_index('positionId', unique=True)
            self.collection.create_index('crawl_time')
            self.collection.create_index('collection_name')
            self.collection.create_index('collection_id')
            
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise

    def _clear_collections(self) -> None:
        """清空目标集合"""
        try:
            # 清空总集合
            self.collection.delete_many({})
            logger.info(f"已清空总集合: {self.output_collection}")
            
            # 清空分片集合
            for collection_name in self.output_part_collections:
                self.db[collection_name].delete_many({})
                logger.info(f"已清空分片集合: {collection_name}")
                
        except Exception as e:
            logger.error(f"清空集合失败: {str(e)}")
            raise

    def _split_and_save_urls(self) -> None:
        """将总URL列表分成4份并保存"""
        try:
            # 获取所有URL
            all_urls = list(self.collection.find({}, {'_id': 0}))
            total_urls = len(all_urls)
            logger.info(f"获取到 {total_urls} 个URL")
            
            # 计算每份的大小
            chunk_size = math.ceil(total_urls / 4)
            
            # 分成4份并保存
            for i in range(4):
                start_idx = i * chunk_size
                end_idx = min((i + 1) * chunk_size, total_urls)
                chunk = all_urls[start_idx:end_idx]
                
                # 保存到对应的分片集合
                collection = self.db[self.output_part_collections[i]]
                if chunk:
                    result = collection.insert_many(chunk)
                    logger.info(f"分片 {i+1} 保存成功，共 {len(result.inserted_ids)} 条数据")
                
        except Exception as e:
            logger.error(f"分片保存失败: {str(e)}")
            raise

    def close(self) -> None:
        """关闭所有连接"""
        if self.mongo_client:
            try:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")
            except Exception as e:
                logger.error(f"关闭MongoDB连接失败: {str(e)}")

    def run(self) -> None:
        """运行爬虫"""
        try:
            # 检查数据一致性
            logger.info("开始检查数据一致性...")
            
            # 检查每个分片的数据一致性
            for i in range(1, 5):
                url_collection = f"lagou_step2_urls_part{i}"
                log_collection = f"lagou_step2_urls_202504_log_part{i}"
                
                # 获取URL集合数据
                url_data = list(self.db[url_collection].find(
                    {},
                    {'city_code': 1, 'industry_name': 1, 'job_type_code': 1, '_id': 0}
                ))
                # 获取日志集合数据
                log_data = list(self.db[log_collection].find(
                    {},
                    {'city_code': 1, 'industry_name': 1, 'job_type_code': 1, '_id': 0}
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
                url_combinations = {(item['city_code'], item['industry_name'], item['job_type_code']) for item in url_data}
                log_combinations = {(item['city_code'], item['industry_name'], item['job_type_code']) for item in log_data}
                
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
            
            # 清空目标集合
            self._clear_collections()
            
            processed_position_ids = set()  # 用于记录已处理的positionId
            # 处理每个输入集合
            for input_collection in self.input_collections:
                # 获取职位列表数据
                jobs = list(self.db[input_collection].find({}, {'positionId': 1,'positionName':1}))
                total_jobs = len(jobs)
                logger.info(f"从 {input_collection} 获取到 {total_jobs} 个职位数据")
                
                # 创建进度条
                pbar = tqdm(total=total_jobs, 
                           desc=f"处理 {input_collection}", 
                           unit="职位",
                           ncols=100,
                           bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
                           position=0,  # 固定位置
                           leave=True)  # 保留进度条
                
                # 批量处理职位
                batch_size = 1000
                url_batch = []
                
                
                for job in jobs:
                    try:
                        # 更新进度条描述
                        current_desc = f"正在处理: {job.get('positionName', '未知职位')}"
                        pbar.set_description(current_desc)                        
                        # 更新进度条
                        pbar.update(1)
                        # 生成职位详情页URL
                        position_id = job.get('positionId')
                        if not position_id:
                            logger.error(f"职位缺少positionId: {job}")
                            continue
                            
                        # 检查positionId是否已处理
                        if position_id in processed_position_ids:
                            continue
                            
                        position_url = f"https://www.lagou.com/wn/jobs/{position_id}.html"
                        
                        # 添加到批次
                        url_data = {
                            'positionId': position_id,
                            'positionUrl': position_url,
                            'crawl_time': datetime.now(),
                            'collection_name': input_collection,
                            'collection_id': job.get('_id')
                        }
                        url_batch.append(url_data)
                        processed_position_ids.add(position_id)
                        
                        # 当批次达到指定大小时，批量插入
                        if len(url_batch) >= batch_size:
                            try:
                                self.collection.insert_many(url_batch)
                                url_batch = []
                            except BulkWriteError as bwe:
                                # 如果发生重复键错误，说明有些positionId已经存在
                                # 清空批次，继续处理下一个
                                print("有些positionId已经存在")
                                url_batch = []
                                continue
                            
                    except Exception as e:
                        logger.error(f"处理职位失败: {position_url}, 错误: {str(e)}")
                        continue
                                        
                
                # 处理剩余的批次
                if url_batch:
                    try:
                        self.collection.insert_many(url_batch)
                    except BulkWriteError:
                        pass  # 忽略重复键错误
                
                # 关闭进度条
                pbar.close()
            
            # 将总URL列表分成4份并保存
            logger.info("开始分片保存URL")
            self._split_and_save_urls()
            logger.info("所有职位处理完成")
            
        except Exception as e:
            logger.error(f"运行出错: {str(e)}")
            raise
        finally:
            self.close()

def main():
    """主函数"""
    try:                
        # 创建爬虫实例
        spider = LagouSpiderStep5()
        # 运行爬虫
        spider.run()
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main() 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
58同城招聘爬虫 - 第五步
严格按照以下格式保存数据：
{
    "_id": ObjectId("自动生成"),
    "job_url": "原集合中的job_url",
    "crawl_time": "从原集合读取",
    "collection_name": "来源集合名称",
    "collection_id": "原集合中的_id"
}
"""

import os
import sys
import logging
from datetime import datetime
from pymongo import MongoClient
from tqdm import tqdm
import math
from bson import ObjectId

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("58_spider_step5")

class Job58SpiderStep5:
    def __init__(self):
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.input_collections = [
            "58_job_raw_part1",
            "58_job_raw_part2",
            "58_job_raw_part3",
            "58_job_raw_part4"
        ]
        self.output_collection = "58_step3_urls"
        self.output_part_collections = [
            "58_step3_urls_part1",
            "58_step3_urls_part2",
            "58_step3_urls_part3",
            "58_step3_urls_part4"
        ]
        # 需要检查的日志集合
        self.log_collections = [
            "58_step2_urls_202504_log_part1",
            "58_step2_urls_202504_log_part2",
            "58_step2_urls_202504_log_part3",
            "58_step2_urls_202504_log_part4"
        ]
        # 需要检查的数据集合
        self.step2_collections = [
            "58_step2_urls_part1",
            "58_step2_urls_part2",
            "58_step2_urls_part3",
            "58_step2_urls_part4"
        ]
        
        # 初始化MongoDB连接
        self.client = None
        self.db = None
        self._connect_mongodb()

    def _connect_mongodb(self):
        """连接MongoDB数据库"""
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            logger.info("MongoDB连接成功")
        except Exception as e:
            logger.error(f"MongoDB连接失败: {str(e)}")
            raise

    def _check_collections_count(self):
        """检查step2集合和日志集合的数据量是否匹配"""
        logger.info("开始检查集合数据量是否匹配...")
        
        for i in range(4):
            step2_col = self.db[self.step2_collections[i]]
            log_col = self.db[self.log_collections[i]]
            
            step2_count = step2_col.count_documents({})
            log_count = log_col.count_documents({})
            
            logger.info(f"检查集合 {self.step2_collections[i]}({step2_count}条) 和 {self.log_collections[i]}({log_count}条)")
            
            if log_count < step2_count:
                error_msg = f"错误: {self.log_collections[i]} 数据量({log_count}) 少于 {self.step2_collections[i]}({step2_count})"
                logger.error(error_msg)
                raise ValueError(error_msg)
        
        logger.info("所有集合数据量检查通过，符合要求(log数据量 ≥ step2数据量)")

    def _process_data(self):
        """核心处理逻辑（严格按格式处理）"""
        unique_data = {}  # {job_url: document}
        total_processed = 0
        total_duplicates = 0

        for col_name in self.input_collections:
            collection = self.db[col_name]
            total = collection.count_documents({})
            logger.info(f"正在处理集合 {col_name} (共 {total} 条数据)")

            # 只查询必要的字段：job_url, crawl_time, _id
            for doc in tqdm(collection.find({}, {'job_url': 1, 'crawl_time': 1, '_id': 1}),
                          total=total, desc=f"Processing {col_name}"):
                job_url = doc.get('job_url')
                if job_url:
                    if job_url not in unique_data:
                        unique_data[job_url] = {
                            'job_url': job_url,  # 直接使用原job_url字段
                            'crawl_time': doc.get('crawl_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                            'collection_name': col_name,
                            'collection_id': str(doc.get('_id'))  # 原集合的_id转为字符串
                        }
                    else:
                        total_duplicates += 1
                total_processed += 1

        return unique_data, total_processed, total_duplicates

    def _save_to_mongodb(self, data):
        """保存数据到MongoDB"""
        # 主集合操作
        main_collection = self.db[self.output_collection]
        main_collection.delete_many({})
        
        if data:
            # 转换为列表时自动生成新的_id
            documents = [doc for doc in data.values()]
            result = main_collection.insert_many(documents)
            main_collection.create_index("job_url", unique=True)
            logger.info(f"主集合 {self.output_collection} 已写入 {len(result.inserted_ids)} 条数据")

        # 分片存储
        data_list = list(data.values())
        total = len(data_list)
        chunk_size = math.ceil(total / 4)
        
        for i in range(4):
            part_collection = self.db[self.output_part_collections[i]]
            part_collection.delete_many({})
            
            start = i * chunk_size
            end = min((i + 1) * chunk_size, total)
            chunk = data_list[start:end]
            
            if chunk:
                part_collection.insert_many(chunk)
                part_collection.create_index("job_url", unique=True)
                logger.info(f"分片集合 {self.output_part_collections[i]} 已写入 {len(chunk)} 条数据")

    def run(self):
        """执行入口"""
        try:
            logger.info("开始58同城数据去重处理")
            logger.info("输入字段要求：job_url, crawl_time, _id")
            
            # 首先检查集合数据量是否匹配
            self._check_collections_count()
            
            # 处理数据
            unique_data, total_processed, total_duplicates = self._process_data()
            
            # 保存结果
            self._save_to_mongodb(unique_data)
            
            # 打印统计信息
            logger.info("处理结果统计:")
            logger.info(f"总处理记录数: {total_processed}")
            logger.info(f"重复记录数: {total_duplicates}")
            logger.info(f"有效去重后记录数: {len(unique_data)}")
            
            logger.info("数据处理完成！")
        except Exception as e:
            logger.error(f"处理过程中发生错误: {str(e)}")
            raise
        finally:
            if self.client:
                self.client.close()
                logger.info("MongoDB连接已关闭")

if __name__ == "__main__":
    spider = Job58SpiderStep5()
    spider.run()
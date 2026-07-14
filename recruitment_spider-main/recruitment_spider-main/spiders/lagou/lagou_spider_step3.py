#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
拉勾网爬虫 - 第三步：URL验证和分配

功能说明：
1. 验证第二步生成的URL集合文档数量是否一致
2. 根据验证结果生成新的URL组合
3. 将URL平均分配到4个部分

处理流程：
1. 验证所有part集合的文档数量
2. 加载城市配置文件
3. 构建新的URL组合（包含城市信息）
4. 将URL保存到lagou_step2_urls集合
5. 将URL平均分配到4个part集合

数据验证：
- 检查lagou_step1_urls_202504_log_part1~4的文档数量
- 检查lagou_step1_urls_part1~4的文档数量
- 确保所有part的文档数量一致

URL生成规则：
1. 基于已验证的URL组合
2. 为每个组合添加所有城市信息
3. 生成新的URL数据结构

数据存储：
- lagou_step2_urls：存储所有新生成的URL
- lagou_step2_urls_part1~4：存储分配后的URL

索引设计：
1. 联合唯一索引：
   - job_type_name
   - industry_name
   - city_name
2. 时间索引：
   - create_time
3. 分区索引：
   - part

注意事项：
1. 验证失败时直接退出程序
2. 确保URL分配均匀
3. 处理余数分配问题
4. 维护数据一致性
"""

import sys
import json
import logging
import os
from datetime import datetime
from typing import Dict, List
from pymongo import MongoClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("spiders.lagou_spider_step3")

class LagouSpiderStep3:
    """拉勾网爬虫 - 第三步：验证和分配URL"""
    
    def __init__(self):
        # 设置MongoDB连接
        self.client = MongoClient('mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA')
        self.db = self.client['MOOC123_DA']
        
        # 数据文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        if root_dir not in sys.path:
            sys.path.append(root_dir)
        self.city_file = os.path.join(root_dir, 'recruitment_spider/data/lagou/city.json')

    def verify_collections(self) -> bool:
        """
        验证所有集合的文档数量是否一致，以及job_type_code和industry_name是否完全匹配
        """
        try:            
            for i in range(1, 5):
                # 获取log集合数据
                log_data = list(self.db[f'lagou_step1_urls_202504_log_part{i}'].find(
                    {},
                    {'job_type_code': 1, 'industry_name': 1, '_id': 0}
                ))
                # 获取url集合数据
                url_data = list(self.db[f'lagou_step1_urls_part{i}'].find(
                    {},
                    {'job_type_code': 1, 'industry_name': 1, '_id': 0}
                ))
                
                log_count = len(log_data)
                url_count = len(url_data)
                
                logger.info(f"part{i} log集合文档数量: {log_count}")
                logger.info(f"part{i} url集合文档数量: {url_count}")
                
                # 验证数量是否一致
                if log_count != url_count:
                    logger.error(f"part{i} log集合文档数量与url集合不一致")
                    return False
                
                # 验证job_type_code和industry_name是否完全匹配
                log_combinations = {(item['job_type_code'], item['industry_name']) for item in log_data}
                url_combinations = {(item['job_type_code'], item['industry_name']) for item in url_data}
                
                # 检查是否有不匹配的组合
                if log_combinations != url_combinations:
                    # 找出不匹配的组合
                    log_only = log_combinations - url_combinations
                    url_only = url_combinations - log_combinations
                    
                    if log_only:
                        logger.error(f"part{i} log集合中存在但url集合中不存在的组合: {log_only}")
                    if url_only:
                        logger.error(f"part{i} url集合中存在但log集合中不存在的组合: {url_only}")
                    return False
                
                logger.info(f"part{i} job_type_code和industry_name验证通过")
            
            logger.info("所有集合文档数量和字段验证通过")
            return True
            
        except Exception as e:
            logger.error(f"验证集合时发生错误: {str(e)}")
            return False

    def load_json_file(self, file_path: str) -> dict:
        """
        加载JSON文件
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载JSON文件 {file_path} 失败: {str(e)}")
            return {}

    def run(self):
        """
        运行验证和分配
        """
        # 首先验证所有集合的文档数量
        if not self.verify_collections():
            logger.error("集合验证失败，退出程序")
            return

        # 加载城市配置文件
        cities = self.load_json_file(self.city_file)
        if not cities:
            logger.error("城市配置文件加载失败，退出程序")
            return

        # 构建所有需要访问的URL
        logger.info("开始构建URL列表...")        
        total_urls = []
        for i in range(1, 5):
            step_urls = []
            log_urls = list(self.db[f'lagou_step1_urls_202504_log_part{i}'].find(
                {'status': "success"},
                {"_id": 0, "status": 0, "update_time": 0, "crawl_time": 0, "first_crawl_time": 0}
            ))
            for city in cities.get('city', []):
                for log_url in log_urls:
                    url_data = {
                        'job_type_code': log_url['job_type_code'],
                        'job_type_name': log_url['job_type_name'],
                        'industry_name': log_url['industry_name'],
                        'city_code': city['code'],
                        'city_name': city['name'],
                        'create_time': datetime.now(),
                        'part': i
                    }
                    step_urls.append(url_data)
            total_urls.extend(step_urls)
            logger.info(f"part{i} 构建URL完成，共 {len(step_urls)} 个URL组合")

        # 保存到lagou_step2_urls集合            
        self.db['lagou_step2_urls'].delete_many({})
        self.db['lagou_step2_urls'].insert_many(total_urls)
        logger.info(f"lagou_step2_urls集合保存完成")

        # 创建索引
        self.db['lagou_step2_urls'].create_index(
            [
                ('job_type_name', 1),
                ('industry_name', 1), 
                ('city_name', 1)
            ],
            unique=True,
            name='unique_job_industry_city'
        )
        self.db['lagou_step2_urls'].create_index(
            [('part', 1)],
            name='idx_part'
        )
        logger.info(f"创建索引完成")
        logger.info(f"URL构建完成，共 {len(total_urls)} 个URL组合")

        # 将数据平均分配到4个part集合中
        total_count = len(total_urls)
        part_size = total_count // 4
        remainder = total_count % 4
        
        logger.info(f"总数据量: {total_count}, 每个part基础大小: {part_size}, 余数: {remainder}")
        
        start_index = 0
        for i in range(1, 5):
            self.db[f'lagou_step2_urls_part{i}'].delete_many({})
            current_part_size = part_size + (1 if i <= remainder else 0)
            part_data = total_urls[start_index:start_index + current_part_size]
            start_index += current_part_size
            
            if part_data:
                self.db[f'lagou_step2_urls_part{i}'].insert_many(part_data)
                logger.info(f"part{i} 保存到lagou_step2_urls_part{i}集合完成，共 {len(part_data)} 条数据")
                
                self.db[f'lagou_step2_urls_part{i}'].create_index(
                    [
                        ('job_type_name', 1),
                        ('industry_name', 1), 
                        ('city_name', 1)
                    ],
                    unique=True,
                    name='unique_job_industry_city'
                )
                self.db[f'lagou_step2_urls_part{i}'].create_index(
                    [('create_time', 1)],
                    name='idx_create_time'
                )
                logger.info(f"part{i} 创建索引完成")
            else:
                logger.warning(f"part{i} 没有数据需要保存")

if __name__ == '__main__':
    spider = LagouSpiderStep3()
    spider.run()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
猎聘网爬虫 - 第一步
功能：生成行业类型和岗位类型的URL组合

主要步骤：
1. 从job_type.json和industry.json加载行业代码和岗位代码
2. 生成所有可能的行业类型和岗位类型组合
3. 将组合保存到MongoDB的liepin_step1_urls集合中

数据存储：
- 集合名称：liepin_step1_urls
- 索引：
  * (industry_parent_code, industry_child_code, job_industry, job_category, job_type_name) - 唯一索引
  * status - 状态索引
  * create_time - 创建时间索引
  * job_type_name - 岗位代码索引
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from pymongo import MongoClient
import re

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "liepin_spider")
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class LiepinSpiderStep1:
    """猎聘网爬虫 - Requests版本"""
    
    def __init__(self):                
        # 基础数据文件路径
        self.job_type_path = Path("recruitment_spider/data/liepin/job_type.json")
        self.industry_path = Path("recruitment_spider/data/liepin/industry.json")
        
        # 基础URL
        self.base_url = "https://www.liepin.com/zhaopin/"
        
        # 加载基础数据
        self.job_type_codes = self.load_job_type_codes()
        self.industry_codes = self.load_industry_codes()
        
        # MongoDB配置
        self.mongo_uri = "mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test"
        self.mongo_db = "da_test"
        self.mongo_client = None
        self.db = None
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        logger.info(f"初始化完成: {len(self.job_type_codes)} 个岗位类型, {len(self.industry_codes)} 个行业")
    
    def load_job_type_data(self) -> dict:
        """加载岗位类型数据文件"""
        try:
            if not self.job_type_path.exists():
                logger.error(f"岗位类型数据文件不存在: {self.job_type_path}")
                return {}
                
            with open(self.job_type_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载岗位类型数据失败: {str(e)}")
            return {}

    def load_industry_data(self) -> dict:
        """加载行业数据文件"""
        try:
            if not self.industry_path.exists():
                logger.error(f"行业数据文件不存在: {self.industry_path}")
                return {}
                
            with open(self.industry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载行业数据失败: {str(e)}")
            return {}

    def load_industry_codes(self) -> List[dict]:
        """从industry.json加载行业代码"""
        try:
            data = self.load_industry_data()
            industry_codes = []
            
            def extract_industry_codes(industry_list):
                for parent in industry_list:
                    parent_code = parent.get('code')
                    parent_name = parent.get('name')
                    if 'children' in parent:
                        # 添加子行业
                        for child in parent['children']:
                            industry_codes.append({
                                'parent_code': parent_code,
                                'parent_name': parent_name,
                                'child_code': child['code'],
                                'child_name': child['name']
                            })
                    else:
                        # 添加当前行业
                        industry_codes.append({
                            'parent_code': parent_code,
                            'parent_name': parent_name,
                            'child_code': parent_code,
                            'child_name': parent_name
                        })
            
            extract_industry_codes(data)
            logger.info(f"成功加载 {len(industry_codes)} 个行业")
            return industry_codes
            
        except Exception as e:
            logger.error(f"加载行业代码失败: {str(e)}")
            return []

    def load_job_type_codes(self) -> List[dict]:
        """从job_type.json加载岗位代码"""
        try:
            data = self.load_job_type_data()
            job_codes = []
            
            # 遍历每个一级分类
            for industry, categories in data.items():
                # 遍历每个二级分类
                for category, jobs in categories.items():
                    # 遍历具体岗位
                    for job in jobs:
                        job_codes.append({
                            'name': job.get('name', ''),
                            'industry': industry,  # 一级分类
                            'category': category   # 二级分类
                        })
            
            logger.info(f"成功加载 {len(job_codes)} 个岗位代码")
            return job_codes
        
        except Exception as e:
            logger.error(f"加载岗位代码失败: {str(e)}")
            return []
    
    def _init_mongodb(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise

    def close(self):
        """关闭MongoDB连接"""
        if self.mongo_client:
            try:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")
            except Exception as e:
                logger.error(f"关闭MongoDB连接失败: {str(e)}")

    def run(self):
        """运行爬虫"""
        try:
            self.all_urls = []
            seen_combinations = set()  # 用于去重的集合，基于关键参数
            for job_type in self.job_type_codes:                
                for industry in self.industry_codes:                    
                    # 构建去重的关键参数组合
                    key_combination = (
                        job_type['name'],
                        industry['parent_code'],
                        industry['child_code']
                    )
                    
                    # 检查关键参数组合是否已存在，避免重复
                    if key_combination not in seen_combinations:
                        seen_combinations.add(key_combination)  # 添加到已见集合
                        
                        # 构建URL，格式：https://www.liepin.com/zhaopin/?key=岗位名称&industry=父级行业代码$子级行业代码
                        url = f"{self.base_url}?key={job_type['name']}&industry={industry['parent_code']}${industry['child_code']}"
                        
                        # 将构建的URL添加到集合中
                        self.all_urls.append({
                            'url': url,
                            'industry_parent_code': industry['parent_code'],
                            'industry_parent_name': industry['parent_name'],
                            'industry_child_code': industry['child_code'],
                            'industry_child_name': industry['child_name'],
                            'job_type_name': job_type['name'],
                            'job_industry': job_type['industry'],  # 一级分类
                            'job_category': job_type['category'],  # 二级分类
                            'status': 'pending',
                            'create_time': datetime.now(),
                        })
            
            # 批量保存到MongoDB
            try:
                # 清空原有的URL集合
                self.db['liepin_step1_urls'].delete_many({})
                
                # 批量插入新的URL
                if self.all_urls:
                    self.db['liepin_step1_urls'].insert_many(self.all_urls)
                    
                # 创建索引
                self.db['liepin_step1_urls'].create_index([
                    ('industry_parent_code', 1),                    
                    ('industry_child_code', 1),
                    ('job_industry', 1),
                    ('job_category', 1),
                    ('job_type_name', 1)
                ], unique=True)
                self.db['liepin_step1_urls'].create_index([('status', 1)])
                self.db['liepin_step1_urls'].create_index([('create_time', 1)])
                self.db['liepin_step1_urls'].create_index([('job_type_name', 1)])
                
                logger.info(f"总共需要处理 {len(self.all_urls)} 个URL组合，已保存到MongoDB")

                # 将step1_urls拆分成4个part                
                total_urls = len(self.all_urls)
                # 计算每个part的大小
                part_size = total_urls // 4
                if total_urls % 4 != 0:
                    part_size += 1
                # 清空所有的part集合
                for i in range(1,5):
                    self.db[f'liepin_step1_urls_part{i}'].delete_many({})
                # 将数据分成多个part并保存
                for i in range(4):
                    start_idx = i*part_size
                    end_idx = min((i+1)*part_size,total_urls)
                    part_urls = self.all_urls[start_idx:end_idx]
                    if part_urls:
                        self.db[f'liepin_step1_urls_part{i+1}'].insert_many(part_urls)
                        # 创建索引
                        self.db[f'liepin_step1_urls_part{i+1}'].create_index([
                            ('industry_parent_code',1),
                            ('industry_child_code',1),
                            ('job_industry',1),
                            ('job_category',1),
                            ('job_type_name',1)
                        ],unique=True)
                        self.db[f'liepin_step1_urls_part{i+1}'].create_index([('create_time',1)])
                    logger.info(f"liepin_step1_urls_part{i+1} 已保存 {len(part_urls)}" )

            except Exception as e:
                logger.error(f"保存URL到MongoDB失败: {str(e)}")
                raise            
            
        except Exception as e:
            logger.error(f"爬虫运行出错: {str(e)}")
            raise
        finally:
            self.close()

def main():
    """主函数"""
    try:
        # 创建爬虫实例
        spider = LiepinSpiderStep1()        
        # 运行爬虫
        spider.run()        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()

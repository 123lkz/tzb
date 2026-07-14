#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
拉勾网爬虫 - 第一步：创建和划分URL
主要功能：
1. 从配置文件加载职位类型和行业信息
2. 生成所有可能的职位类型和行业组合
3. 将URL保存到MongoDB
4. 将URL平均分配到4个部分
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List
from pymongo import MongoClient

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("spiders.lagou_spider_create_step1_urls")

class LagouSpiderStep1:
    """
    拉勾网爬虫 - URL创建和划分类
    
    主要功能：
    1. 初始化MongoDB连接和配置文件路径
    2. 加载职位类型和行业配置文件
    3. 生成URL组合并保存到MongoDB
    4. 将URL平均分配到4个部分
    """
    
    def __init__(self):
        """
        初始化爬虫类
        设置MongoDB连接和配置文件路径
        """
        # 设置MongoDB连接
        self.client = MongoClient('mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA')
        self.db = self.client['MOOC123_DA']
        
        # 添加当前目录到工作路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        if project_root not in os.sys.path:
            os.sys.path.append(project_root)            
        # 数据文件路径
        self.job_type_file = os.path.join(project_root, 'recruitment_spider/data/lagou/job_type.json')
        self.industry_file = os.path.join(project_root, 'recruitment_spider/data/lagou/industry.json')

    def load_json_file(self, file_path: str) -> dict:
        """
        加载JSON配置文件
        
        Args:
            file_path: JSON文件的路径
            
        Returns:
            dict: 解析后的JSON数据，如果加载失败则返回空字典
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载JSON文件 {file_path} 失败: {str(e)}")
            return {}

    def save_urls_to_mongodb(self, url_list: List[Dict]) -> bool:
        """
        批量保存URL到MongoDB
        
        Args:
            url_list: 要保存的URL列表，每个URL包含职位类型和行业信息
            
        Returns:
            bool: 保存是否成功
        """
        try:
            if url_list:
                # 删除原有的集合
                self.db['lagou_step1_urls'].drop()
                logger.info("已删除原有的lagou_step1_urls集合")
                
                # 批量插入新的URL数据
                self.db['lagou_step1_urls'].insert_many(url_list, ordered=False)
                
                # 创建联合唯一索引,确保job_type和industry组合不重复
                self.db['lagou_step1_urls'].create_index(
                    [
                        ('job_type_code', 1),
                        ('job_type_name', 1),
                        ('industry_name', 1)
                    ],
                    unique=True
                )
                # 创建create_time索引用于时间查询
                self.db['lagou_step1_urls'].create_index([('create_time', 1)])
                logger.info(f"批量保存URL成功，共 {len(url_list)} 条")
                return True
            return False
        except Exception as e:
            logger.error(f"批量保存URL到MongoDB失败: {str(e)}")
            return False

    def divide_urls_into_parts(self):
        """
        将lagou_step1_urls中的URL平均划分到part1~part4
        
        处理流程：
        1. 删除原有的part集合
        2. 获取所有URL
        3. 计算每个部分应包含的URL数量
        4. 将URL平均分配到4个部分
        5. 为每个部分创建必要的索引
        
        Returns:
            bool: 划分是否成功
        """
        try:
            # 删除原有的part集合
            for part_num in range(1, 5):
                self.db[f'lagou_step1_urls_part{part_num}'].drop()
                logger.info(f"已删除原有的lagou_step1_urls_part{part_num}集合")
            
            # 获取所有的URL
            urls = list(self.db['lagou_step1_urls'].find({}))
            total_urls = len(urls)
            
            if total_urls == 0:
                logger.info("没有需要处理的URL")
                return True
                
            # 计算每个部分应该包含的URL数量
            urls_per_part = total_urls // 4  # 基础数量
            remainder = total_urls % 4  # 余数，需要平均分配
            
            # 划分URL到不同的部分
            start_idx = 0
            for part_num in range(1, 5):
                # 计算当前部分应该包含的URL数量（考虑余数）
                current_part_size = urls_per_part + (1 if remainder > 0 else 0)
                remainder -= 1
                
                # 获取当前部分的URL
                part_urls = urls[start_idx:start_idx + current_part_size]
                
                # 批量插入到对应的part集合
                if part_urls:
                    self.db[f'lagou_step1_urls_part{part_num}'].insert_many(part_urls)
                    # 创建create_time索引
                    self.db[f'lagou_step1_urls_part{part_num}'].create_index([('create_time', 1)])
                    # 创建联合唯一索引,确保job_type和industry组合不重复
                    self.db[f'lagou_step1_urls_part{part_num}'].create_index(
                        [
                            ('job_type_code', 1),
                            ('job_type_name', 1),
                            ('industry_name', 1)
                        ],
                        unique=True
                    )
                    logger.info(f"Part{part_num}处理完成，包含 {len(part_urls)} 条URL")
                
                start_idx += current_part_size
            
            logger.info("所有URL划分完成")
            return True
            
        except Exception as e:
            logger.error(f"划分URL时发生错误: {str(e)}")
            return False

    def run(self):
        """
        运行爬虫主流程
        
        处理流程：
        1. 加载职位类型和行业配置文件
        2. 生成所有可能的职位类型和行业组合
        3. 将URL保存到MongoDB
        4. 将URL平均分配到4个部分
        """
        # 加载配置文件
        job_types = self.load_json_file(self.job_type_file)
        industries = self.load_json_file(self.industry_file)

        if not all([job_types, industries]):
            logger.error("配置文件加载失败，退出程序")
            return

        # 构建所有需要访问的URL
        logger.info("开始构建URL列表...")
        url_list = []
        
        # 遍历所有职位类型和行业组合
        for job_type in job_types.get('job_type', []):
            for industry in industries.get('industry', []):
                # 构建URL数据
                url_data = {
                    'job_type_code': job_type['code'],  # 职位类型代码
                    'job_type_name': job_type['name'],  # 职位类型名称
                    'industry_name': industry['name'],  # 行业名称
                    'create_time': datetime.now(),      # 创建时间
                }
                url_list.append(url_data)
                
        # 批量保存到MongoDB
        if self.save_urls_to_mongodb(url_list):
            logger.info("所有URL保存完成")
            # 保存lagou_step1_urls成功后，将其划分到part1~part4
            if self.divide_urls_into_parts():
                logger.info("URL划分完成")
            else:
                logger.error("URL划分失败")
        else:
            logger.error("URL保存失败")

if __name__ == '__main__':
    # 创建爬虫实例并运行
    spider = LagouSpiderStep1()
    spider.run()
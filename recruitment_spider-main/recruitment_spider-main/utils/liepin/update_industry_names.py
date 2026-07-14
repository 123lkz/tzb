#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
猎聘网爬虫 - 行业名称更新补丁
功能：更新liepin_step2_urls_202504_log_part1集合中的行业名称信息

主要步骤：
1. 从industry.json加载行业数据
2. 从MongoDB加载日志数据
3. 根据行业代码匹配对应的名称
4. 更新MongoDB中的记录
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from pymongo import MongoClient
from tqdm import tqdm
from pymongo import UpdateOne

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class IndustryNameUpdater:
    """行业名称更新器"""
    
    def __init__(self):
        """初始化更新器"""
        # MongoDB配置
        self.mongo_uri = "mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test"
        self.mongo_db = "da_test"
        self.mongo_client = None
        self.db = None
        self.collection = None
        
        # 行业数据
        self.industry_data = None
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        # 加载行业数据
        self._load_industry_data()
        
        logger.info("初始化完成")
    
    def _init_mongodb(self) -> None:
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            self.collection = self.db['liepin_step2_urls_202504_log_part4']
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise

    def _load_industry_data(self) -> None:
        """加载行业数据"""
        try:
            # 获取项目根目录
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent.parent
            
            # 读取industry.json文件
            industry_file = project_root/ 'recruitment_spider' / 'data' / 'liepin' / 'industry.json'
            with open(industry_file, 'r', encoding='utf-8') as f:
                self.industry_data = json.load(f)
            
            logger.info("行业数据加载成功")
        except Exception as e:
            logger.error(f"加载行业数据失败: {str(e)}")
            raise

    def _find_industry_names(self, parent_code: str, child_code: str) -> tuple:
        """查找行业名称
        
        Args:
            parent_code: 父级行业代码
            child_code: 子级行业代码
            
        Returns:
            (parent_name, child_name): 行业名称元组
        """
        try:
            parent_name = None
            child_name = None
            
            # 遍历行业数据查找名称
            for parent in self.industry_data:
                if parent['code'] == parent_code:
                    parent_name = parent['name']
                    # 查找子行业名称
                    for child in parent['children']:
                        if child['code'] == child_code:
                            child_name = child['name']
                            break
                    break
            
            return parent_name, child_name
        except Exception as e:
            logger.error(f"查找行业名称失败: {str(e)}")
            return None, None

    def update_industry_names(self) -> None:
        """更新行业名称"""
        try:
            # 获取所有需要更新的记录
            # records = list(self.collection.find({
            #     'industry_parent_name': {'$exists': False},
            #     'industry_child_name': {'$exists': False}
            # }))
            records = list(self.collection.find({
                'industry_parent_name': None,
                'industry_child_name': None
            }))
            
            total_records = len(records)
            logger.info(f"找到 {total_records} 条需要更新的记录")
            
            # 创建进度条
            pbar = tqdm(total=total_records, 
                       desc="更新进度", 
                       unit="记录",
                       ncols=100)
            
            # 准备批量更新操作
            bulk_operations = []
            for record in records:
                parent_code = record.get('industry_parent_code')
                child_code = record.get('industry_child_code')
                
                if parent_code and child_code:
                    parent_name, child_name = self._find_industry_names(parent_code, child_code)
                    
                    if parent_name and child_name:
                        bulk_operations.append(
                            UpdateOne(
                                {'_id': record['_id']},
                                {'$set': {
                                    'industry_parent_name': parent_name,
                                    'industry_child_name': child_name
                                }}
                            )
                        )
                
                pbar.update(1)
            
            # 执行批量更新
            if bulk_operations:
                result = self.collection.bulk_write(bulk_operations, ordered=False)
                logger.info(f"批量更新完成 - 修改: {result.modified_count}, 总数: {len(bulk_operations)}")
            else:
                logger.info("没有需要更新的记录")
            
            pbar.close()
            
        except Exception as e:
            logger.error(f"更新行业名称失败: {str(e)}")
            raise
        finally:
            if self.mongo_client:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")

def main():
    """主函数"""
    try:
        updater = IndustryNameUpdater()
        updater.update_industry_names()
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main() 
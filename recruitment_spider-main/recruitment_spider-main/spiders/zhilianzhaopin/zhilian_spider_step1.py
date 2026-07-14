#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智联招聘爬虫 - 第一步
功能：生成行业类型和岗位类型的URL组合

主要步骤：
1. 从base_data.json加载行业代码和岗位代码
2. 生成所有可能的行业类型和岗位类型组合
3. 将组合保存到MongoDB的zhilian_step1_urls集合中

数据存储：
- 集合名称：zhilian_step1_urls
- 索引：
  * (industry_code, job_type_code) - 唯一索引
  * status - 状态索引
  * create_time - 创建时间索引
  * job_type_code - 岗位代码索引

"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from pymongo import MongoClient

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "zhilian_spider")
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class ZhilianSpiderStep1:
    """智联招聘爬虫 - Requests版本"""
    
    def __init__(self):
        # API配置
        self.base_url = "https://fe-api.zhaopin.com"
        self.search_api = "/c/i/search/positions"
        
        # 基础数据文件路径
        self.base_data_path = Path("recruitment_spider/data/zhilian/base_data.json")
        
        # 加载基础数据
        self.job_type_codes = self.load_job_type_codes()
        self.industry_codes = self.load_industry_codes()
        
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.mongo_client = None
        self.db = None
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        logger.info(f"初始化完成: {len(self.job_type_codes)} 个岗位类型, {len(self.industry_codes)} 个行业")
    
    def load_base_data(self) -> dict:
        """加载基础数据文件"""
        try:
            if not self.base_data_path.exists():
                logger.error(f"基础数据文件不存在: {self.base_data_path}")
                return {}
                
            with open(self.base_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载基础数据失败: {str(e)}")
            return {}

    def load_industry_codes(self) -> List[dict]:
        """从base_data.json加载行业代码"""
        try:
            data = self.load_base_data()
            industries = data.get('data', {}).get('industry', [])
            industry_codes = []
            
            def extract_last_level(industry_list):
                for item in industry_list:
                    sublist = item.get('sublist', [])
                    if not sublist:
                        code = item.get('code')
                        name = item.get('name')
                        if code and name:
                            industry_codes.append({
                                'code': code,
                                'name': name
                            })
                    else:
                        extract_last_level(sublist)
            
            extract_last_level(industries)
            logger.info(f"成功加载 {len(industry_codes)} 个行业")
            return industry_codes
            
        except Exception as e:
            logger.error(f"加载行业代码失败: {str(e)}")
            return []

    def load_job_type_codes(self) -> List[dict]:
        """从base_data.json加载岗位代码"""
        try:
            data = self.load_base_data()
            job_types = data.get('data', {}).get('jobType', [])
            combined_codes = []
            
            for level1 in job_types:
                level1_code = level1.get('code')
                if not level1_code:
                    continue
                    
                for level2 in level1.get('sublist', []):
                    level2_code = level2.get('code')
                    if not level2_code:
                        continue
                        
                    level3_list = level2.get('sublist', [])
                    if not level3_list:
                        combined_codes.append({
                            'code': level2_code,
                            'name': level2.get('name', '')
                        })
                        continue
                    
                    for level3 in level3_list:
                        level3_code = level3.get('code')
                        if level3_code:
                            combined_codes.append({
                                'code': level3_code,
                                'name': level3.get('name', '')
                            })
            
            logger.info(f"成功加载 {len(combined_codes)} 个岗位代码")
            return combined_codes
        
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
            for job_type in self.job_type_codes:                
                for industry in self.industry_codes:                    
                    url = f"{self.base_url}{self.search_api}"
                    # 将构建的URL添加到集合中
                    self.all_urls.append({
                        'url': url,
                        'industry_code': industry.get('code'),
                        'industry_name': industry.get('name'),
                        'job_type_code': job_type.get('code'),
                        'job_type_name': job_type.get('name'),
                        'status': 'pending',
                        'create_time': datetime.now(),
                    })
            
            # 批量保存到MongoDB
            try:
                # 清空原有的URL集合
                self.db['zhilian_step1_urls'].delete_many({})
                
                # 批量插入新的URL
                if self.all_urls:
                    self.db['zhilian_step1_urls'].insert_many(self.all_urls)
                    
                # 创建索引
                self.db['zhilian_step1_urls'].create_index([
                    ('industry_code', 1),                    
                    ('job_type_code', 1)
                ], unique=True)
                self.db['zhilian_step1_urls'].create_index([('status', 1)])
                self.db['zhilian_step1_urls'].create_index([('create_time', 1)])
                self.db['zhilian_step1_urls'].create_index([('job_type_code', 1)])
                
                logger.info(f"总共需要处理 {len(self.all_urls)} 个URL组合，已保存到MongoDB")

                # 将step1_urls拆分成4个part                
                total_urls = len(self.all_urls)
                # 计算每个part的大小
                part_size = total_urls // 4
                if total_urls % 4 != 0:
                    part_size += 1
                # 清空所有的part集合
                for i in range(1,5):
                    self.db[f'zhilian_step1_urls_part{i}'].delete_many({})
                # 将数据分成多个part并保存
                for i in range(4):
                    start_idx = i*part_size
                    end_idx = min((i+1)*part_size,total_urls)
                    part_urls = self.all_urls[start_idx:end_idx]
                    if part_urls:
                        self.db[f'zhilian_step1_urls_part{i+1}'].insert_many(part_urls)
                        # 创建索引
                        self.db[f'zhilian_step1_urls_part{i+1}'].create_index([
                            ('industry_code',1),
                            ('job_type_code',1)
                        ],unique=True)
                        self.db[f'zhilian_step1_urls_part{i+1}'].create_index([('create_time',1)])
                    logger.info(f"zhilian_step1_urls_part{i+1} 已保存 {len(part_urls)}" )

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
        spider = ZhilianSpiderStep1()        
        # 运行爬虫
        spider.run()        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()

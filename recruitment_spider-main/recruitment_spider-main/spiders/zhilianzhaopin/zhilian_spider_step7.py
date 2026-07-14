#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智联招聘爬虫 - 第七步
功能：从zhilian_job_raw集合中提取去重后的公司信息并分割
1. 从zhilian_job_raw提取去重公司信息到zhilian_company
2. 将zhilian_company分割为zhilian_company_part1和zhilian_company_part2
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, List
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "zhilian_spider_step7")
except ImportError:
    # 如果无法导入log_manager，则使用基本配置
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("zhilian_spider_step7")

class ZhilianSpiderStep7:
    """智联招聘公司信息处理爬虫 - 整合提取和分割功能"""
    
    def __init__(self, part_count=2):
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        
        # 集合名称
        self.source_collection = "zhilian_job_raw"  # 源集合
        self.target_collection = "zhilian_step4_urls"  # 目标集合
        
        # 分割配置
        self.part_count = part_count  # 控制生成多少个part
        self.part_collections = []  # 存储所有part集合名称
        
        # 生成part集合名称
        for i in range(1, part_count + 1):
            self.part_collections.append(f"zhilian_step4_urls_part{i}")
        
        # MongoDB连接
        self.mongo_client = None
        self.db = None
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        logger.info(f"智联招聘公司信息处理爬虫初始化完成，将生成 {part_count} 个part")
    
    def _init_mongodb(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            logger.info("MongoDB连接成功")
        except Exception as e:
            logger.error(f"MongoDB连接失败: {str(e)}")
            raise
    
    def extract_companies(self) -> List[Dict]:
        """从zhilian_job_raw集合中提取去重后的公司信息"""
        try:
            logger.info("开始从zhilian_job_raw集合中提取去重后的公司信息...")
            
            # 使用聚合管道获取去重后的公司信息
            pipeline = [
                {
                    "$match": {
                        "companyName": {"$exists": True, "$ne": ""},
                        "companyId": {"$exists": True, "$ne": None}
                    }
                },
                {
                    "$group": {
                        "_id": "$companyId",
                        "companyName": {"$first": "$companyName"},
                        "firstJobId": {"$first": "$_id"},
                        "jobCount": {"$sum": 1},
                        "firstPublishTime": {"$min": "$firstPublishTime"},
                        "lastPublishTime": {"$max": "$firstPublishTime"},
                        "originalJobIds": {"$push": "$_id"}
                    }
                }
            ]
            
            # 设置聚合选项，允许使用磁盘进行排序
            companies = list(self.db[self.source_collection].aggregate(
                pipeline, 
                allowDiskUse=True
            ))
            logger.info(f"成功获取 {len(companies)} 个不同的公司")
            
            # 在Python中进行排序，避免MongoDB内存限制
            companies.sort(key=lambda x: x.get("jobCount", 0), reverse=True)
            logger.info("已完成公司数据排序")
            
            return companies
            
        except Exception as e:
            logger.error(f"获取公司信息失败: {str(e)}")
            return []
    
    def save_companies_to_collection(self, companies: List[Dict]) -> bool:
        """将公司信息保存到zhilian_company集合"""
        try:
            logger.info("开始保存公司信息到zhilian_company集合...")
            
            # 准备要插入的数据
            company_docs = []
            current_time = datetime.now()
            
            for company in companies:
                company_doc = {
                    "company_id": company["_id"],  # 原companyId
                    "company_name": company["companyName"],
                    "job_count": company["jobCount"],
                    "original_job_ids": company["originalJobIds"],  # 原始job的_id列表
                    "create_time": current_time,
                }
                company_docs.append(company_doc)
            
            # 清空目标集合（可选）
            self.db[self.target_collection].drop()
            logger.info(f"已清空 {self.target_collection} 集合")
            
            # 批量插入数据
            if company_docs:
                result = self.db[self.target_collection].insert_many(company_docs)
                logger.info(f"成功插入 {len(result.inserted_ids)} 个公司记录")
                
                # 创建索引
                self.db[self.target_collection].create_index("company_id", unique=True)
                self.db[self.target_collection].create_index("company_name")
                self.db[self.target_collection].create_index("job_count")
                logger.info("已创建索引")
                
            return True

            
        except BulkWriteError as e:
            logger.error(f"批量写入失败: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"保存公司信息失败: {str(e)}")
            return False

    def get_all_companies(self) -> List[dict]:
        """获取所有公司数据"""
        try:
            logger.info(f"开始从 {self.target_collection} 集合中获取所有公司数据...")
            
            # 获取所有公司数据，按job_count降序排列
            companies = list(self.db[self.target_collection].find(
                {}, 
                {"_id": 0}  # 排除MongoDB的_id字段
            ).sort("job_count", -1))
            
            logger.info(f"成功获取 {len(companies)} 个公司记录")
            return companies
                
        except Exception as e:
            logger.error(f"获取公司数据失败: {str(e)}")
            return []

    def split_companies(self, companies: List[dict]) -> List[List[dict]]:
        """将公司数据分成多个部分"""
        try:
            total_count = len(companies)
            if total_count == 0:
                logger.warning("没有公司数据需要分割")
                return []
            
            # 计算每个part的大小
            part_size = total_count // self.part_count
            remainder = total_count % self.part_count
            
            parts = []
            start_index = 0
            
            for i in range(self.part_count):
                # 前remainder个part多分配一个元素
                current_part_size = part_size + (1 if i < remainder else 0)
                end_index = start_index + current_part_size
                
                part = companies[start_index:end_index]
                parts.append(part)
                
                logger.info(f"  第{i+1}部分: {len(part)} 个公司")
                start_index = end_index
            
            logger.info(f"数据分割完成，共分为 {self.part_count} 个部分")
            return parts
            
        except Exception as e:
            logger.error(f"分割公司数据失败: {str(e)}")
            return []

    def save_to_split_collections(self, parts: List[List[dict]]) -> bool:
        """保存数据到多个分割集合"""
        try:
            logger.info("开始保存数据到分割集合...")
            
            # 清空目标集合
            for collection in self.part_collections:
                self.db[collection].drop()
                logger.info(f"已清空 {collection} 集合")
            
            # 保存数据
            for i, part in enumerate(parts):
                result = self.db[self.part_collections[i]].insert_many(part)
                logger.info(f"成功插入 {len(result.inserted_ids)} 个公司记录到 {self.part_collections[i]}")
                
                # 创建索引
                self.db[self.part_collections[i]].create_index("company_id", unique=True)
                self.db[self.part_collections[i]].create_index("company_name")
                self.db[self.part_collections[i]].create_index("job_count")
                logger.info(f"已为 {self.part_collections[i]} 创建索引")
            
                return True
            
        except BulkWriteError as e:
            logger.error(f"批量写入失败: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"保存数据失败: {str(e)}")
            return False

    def get_collection_stats(self):
        """获取集合统计信息"""
        try:
            source_count = self.db[self.source_collection].count_documents({})
            target_count = self.db[self.target_collection].count_documents({})
            
            logger.info(f"源集合 {self.source_collection} 记录数: {source_count}")
            logger.info(f"目标集合 {self.target_collection} 记录数: {target_count}")
            
            # 显示所有part集合的统计信息
            for collection in self.part_collections:
                collection_count = self.db[collection].count_documents({})
                logger.info(f"{collection} 记录数: {collection_count}")
            
            # 获取前10个公司信息作为示例
            sample_companies = list(self.db[self.target_collection].find(
                {}, 
                {"company_name": 1, "job_count": 1, "_id": 0}
            ).limit(10))
            
            logger.info("前10个公司示例:")
            for i, company in enumerate(sample_companies, 1):
                logger.info(f"  {i}. {company['company_name']} (职位数: {company['job_count']})")
            
            # 获取每个部分的前5个公司信息作为示例
            for collection in self.part_collections:
                logger.info(f"\n{collection} 前5个公司示例:")
                sample_part = list(self.db[collection].find(
                    {}, 
                    {"company_name": 1, "job_count": 1, "_id": 0}
                ).limit(5))
                
                for i, company in enumerate(sample_part, 1):
                    logger.info(f"  {i}. {company['company_name']} (职位数: {company['job_count']})")
                
        except Exception as e:
            logger.error(f"获取统计信息失败: {str(e)}")

    def run(self):
        """运行完整的处理流程"""
        try:
            logger.info("开始智联招聘公司信息处理流程...")
            
            # 第一步：提取公司信息
            logger.info("=== 第一步：提取公司信息 ===")
            companies = self.extract_companies()
            if not companies:
                logger.error("未获取到任何公司信息")
                return False            
            
            # 第二步：保存到zhilian_step4_urls集合
            if not self.save_companies_to_collection(companies):
                logger.error("保存公司信息失败")
                return False
            
            # 第三步：分割数据
            logger.info("=== 第二步：分割公司数据 ===")
            parts = self.split_companies(companies)
            if not parts:
                logger.error("数据分割失败")
                return False
            
            # 第四步：保存到分割集合
            if not self.save_to_split_collections(parts):
                logger.error("保存分割数据失败")
            return False
            
            # 第五步：显示统计信息
            logger.info("=== 处理结果统计 ===")
            self.get_collection_stats()
            
            logger.info("智联招聘公司信息处理流程完成！")
            return True
            
        except Exception as e:
            logger.error(f"智联招聘公司信息处理流程失败: {str(e)}")
            return False
        finally:
            self.close()
    
    def close(self):
        """关闭MongoDB连接"""
        if hasattr(self, 'mongo_client'):
            self.mongo_client.close()
            logger.info("MongoDB连接已关闭")

def main():
    """主函数"""
    # 可以通过修改这个变量来控制生成多少个part
    part_count = 2  # 生成2个part
    
    logger.info(f"启动智联招聘公司信息处理程序，将生成 {part_count} 个part...")
    
    spider = ZhilianSpiderStep7(part_count=part_count)
    try:
        success = spider.run()
        if success:
            logger.info("智联招聘公司信息处理成功完成！")
        else:
            logger.error("智联招聘公司信息处理失败！")
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
    finally:
        spider.close()

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
智联招聘数据迁移脚本
功能：将zhilian_job_raw_all_job_type的数据迁移到zhilian_job_raw集合
"""

import logging
from datetime import datetime
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError
from tqdm import tqdm

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("data_migration")

class JobDataMigrator:
    """智联招聘数据迁移器"""
    
    def __init__(self):
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.source_collection = "zhilian_job_raw_all_job_type"
        self.target_collection = "zhilian_job_raw"
        
        # 初始化MongoDB连接
        self.mongo_client = None
        self.db = None
        self._init_mongodb()
        
        logger.info("数据迁移器初始化完成")
    
    def _init_mongodb(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise

    def migrate_data(self):
        """执行数据迁移"""
        try:
            # 获取源集合中的总记录数
            total_records = self.db[self.source_collection].count_documents({})
            logger.info(f"总共需要迁移 {total_records} 条记录")
            
            # 创建进度条
            pbar = tqdm(total=total_records, 
                       desc="数据迁移进度", 
                       unit="记录",
                       ncols=100,
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')
            
            # 使用批量处理
            batch_size = 1000
            processed = 0
            total_upserted = 0
            total_modified = 0
            
            while processed < total_records:
                # 获取一批数据
                batch = list(self.db[self.source_collection].find({}).skip(processed).limit(batch_size))
                
                # 准备批量操作
                operations = []
                for doc in batch:                                        
                    operation = UpdateOne(
                        {'jobId': doc['jobId']},  # 查询条件
                        {'$set': doc},  # 更新数据
                        upsert=True  # 如果不存在则插入
                    )
                    operations.append(operation)
                
                # 执行批量写入
                if operations:
                    try:
                        result = self.db[self.target_collection].bulk_write(operations, ordered=False)
                        total_upserted += result.upserted_count
                        total_modified += result.modified_count
                        
                        # 更新进度条描述
                        pbar.set_description(
                            f"迁移进度 - 新增: {total_upserted}, 更新: {total_modified}"
                        )
                    except BulkWriteError as bwe:
                        logger.error(f"批量写入出错: {str(bwe.details)}")
                
                # 更新进度
                processed += len(batch)
                pbar.update(len(batch))
            
            # 关闭进度条
            pbar.close()
            
            # 输出最终结果
            logger.info(f"数据迁移完成 - 总记录数: {total_records}, 新增: {total_upserted}, 更新: {total_modified}")
            
        except Exception as e:
            logger.error(f"数据迁移失败: {str(e)}")
            raise
        finally:
            self.close()
    
    def close(self):
        """关闭MongoDB连接"""
        if self.mongo_client:
            try:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")
            except Exception as e:
                logger.error(f"关闭MongoDB连接失败: {str(e)}")

def main():
    """主函数"""
    try:
        # 创建迁移器实例
        migrator = JobDataMigrator()
        
        # 执行数据迁移
        migrator.migrate_data()
        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main() 
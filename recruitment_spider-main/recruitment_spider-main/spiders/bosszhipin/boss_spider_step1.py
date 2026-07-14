import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

# 添加工作路径到系统路径
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BossSpider:
    """BOSS直聘URL生成器"""
    
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.mongo_client = None
        self.db = None
        self.boss_urls = None
        self.boss_step_urls = "boss_step1_urls"  # 定义集合名称
        
        # 基础数据文件路径
        self.job_type_path = Path("recruitment_spider/data/bosszhipin/job_type.json")
        self.industry_code_path = Path("recruitment_spider/data/bosszhipin/industry_code.json")
        logger.info(f"基础数据文件路径: {self.job_type_path.absolute()}")
        
        # 加载岗位代码和行业代码
        self.job_type_codes = self.load_job_codes()
        self.company_industry_codes = self.load_company_industry_codes()
    
    def load_job_codes(self) -> List[Dict]:
        """从JSON文件中加载职位代码"""
        job_code_groups = []
        try:
            data_dir = Path("recruitment_spider/data/bosszhipin")
            if not data_dir.exists():
                logger.error(f"数据目录不存在: {data_dir}")
                data_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"已创建数据目录: {data_dir}")
                return []
            
            if not self.job_type_path.exists():
                logger.error(f"职位类型文件不存在: {self.job_type_path}")
                return []
            
            with open(self.job_type_path, 'r', encoding='utf-8') as f:
                job_type_data = json.load(f)
            
            for first_level in job_type_data.get('zpData', {}).get('position', []):
                for second_level in first_level.get('subLevelModelList', []):
                    for third_level in second_level.get('subLevelModelList', []):
                        third_code = third_level.get('code')
                        if third_code:
                            tmp_data = {
                                "job_type_code": third_code,
                                "job_type_name": third_level.get('name')
                            }
                            job_code_groups.append(tmp_data)
            
            logger.info(f"成功加载 {len(job_code_groups)} 个第三级职位代码")
            return job_code_groups
        
        except Exception as e:
            logger.error(f"加载职位代码失败: {str(e)}")
            return []
    
    def load_company_industry_codes(self) -> List[Dict]:
        """从JSON文件中加载公司行业代码"""
        industry_code_groups = []
        try:
            data_dir = Path("recruitment_spider/data/bosszhipin")
            if not data_dir.exists():
                logger.error(f"数据目录不存在: {data_dir}")
                data_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"已创建数据目录: {data_dir}")
                return []
            
            if not self.industry_code_path.exists():
                logger.error(f"行业类型文件不存在: {self.industry_code_path}")
                return []
            
            with open(self.industry_code_path, 'r', encoding='utf-8') as f:
                industry_data = json.load(f)
            
            for parent_industry in industry_data.get('zpData', []):
                for sub_industry in parent_industry.get('subLevelModelList', []):
                    code = str(sub_industry.get('code'))
                    name = sub_industry.get('name')
                    if code and name:
                        industry_code_groups.append({'name': name, 'code': code})
            
            logger.info(f"成功加载 {len(industry_code_groups)} 个子行业代码")
            return industry_code_groups
            
        except Exception as e:
            logger.error(f"加载行业代码失败: {str(e)}")
            return []
    
    async def _init_mongodb(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            self.boss_urls = self.db[self.boss_step_urls]
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise
    
    def _build_search_url(self, industry_code: str, job_type_code: str) -> str:
        """构建搜索URL"""
        base_url = "https://www.zhipin.com"
        url = f"{base_url}/web/geek/job?city=100010000&position={job_type_code}&industry={industry_code}"
        logger.info(f"构建搜索URL: {url}")
        return url
    
    async def build_and_save_urls(self):
        """构建所有URL组合并保存到MongoDB"""
        try:
            # 构建所有URL组合
            all_urls = []
            for industry in self.company_industry_codes:
                for job_type in self.job_type_codes:
                    url = self._build_search_url(industry.get('code'), job_type.get('job_type_code'))
                    url_doc = {
                        'url': url,
                        'industry_code': str(industry.get('code')),
                        'industry_name': str(industry.get('name')),
                        'job_type_code': str(job_type.get('job_type_code')),
                        'job_type_name': str(job_type.get('job_type_name')),
                        'status': 'pending',  # pending, completed, failed
                        'create_time': datetime.now(),
                        'last_update_time': None,
                        'error_count': 0,
                        'last_error': None
                    }
                    all_urls.append(url_doc)
            
            # 使用drop删除原有的URL集合
            logger.info(f"删除原有的URL集合")
            await self.boss_urls.drop()
            
            # 批量插入新的URL
            if all_urls:
                await self.boss_urls.insert_many(all_urls)
            
            # 创建索引
            await self.boss_urls.create_index([('industry_code', 1)])
            await self.boss_urls.create_index([('job_type_code', 1)])
            await self.boss_urls.create_index([('url', 1)])
            await self.boss_urls.create_index([('status', 1)])
            await self.boss_urls.create_index([('create_time', 1)])
            
            logger.info(f"总共构建并保存了 {len(all_urls)} 个URL组合到MongoDB")
            # 计算每个部分的URL数量
            total_urls = len(all_urls)
            part_size = total_urls // 4  # 分成4个部分
            logger.info(f"总共生成 {total_urls} 个URL，每个部分约 {part_size} 个URL")
            
            # 将URL分成4个部分并保存
            for i in range(4):
                start_idx = i * part_size
                end_idx = start_idx + part_size if i < 3 else total_urls  # 最后一部分包含剩余的所有URL
                part_urls = all_urls[start_idx:end_idx]
                
                # 创建新的集合名称
                collection_name = f"boss_step1_urls_part{i+1}"
                collection = self.db[collection_name]
                
                # 删除原有的集合
                logger.info(f"删除原有的URL集合: {collection_name}")
                await collection.drop()
                
                # 批量插入新的URL
                if part_urls:
                    await collection.insert_many(part_urls)
                
                # 创建索引                
                await collection.create_index([('industry_code', 1)])
                await collection.create_index([('job_type_code', 1)])
                await collection.create_index([('url', 1)])
                await collection.create_index([('status', 1)])
                await collection.create_index([('create_time', 1)])
                
                logger.info(f"第 {i+1} 部分URL保存成功，共 {len(part_urls)} 个URL")

            
        except Exception as e:
            logger.error(f"构建和保存URL失败: {str(e)}")
            raise
    
    async def run(self):
        """运行主方法"""
        try:
            # 初始化MongoDB连接
            await self._init_mongodb()
            
            # 构建并保存所有URL组合到MongoDB
            await self.build_and_save_urls()
            
        except Exception as e:
            logger.error(f"运行出错: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            if self.mongo_client:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")

async def main():
    """主函数"""
    try:
        spider = BossSpider()
        await spider.run()
    except Exception as e:
        logger.error(f"运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main()) 
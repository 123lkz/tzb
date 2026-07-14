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
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "boss_spider")
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class BossSpiderStep3:
    """BOSS直聘爬虫 - 第三步
    功能：将step2生成的URL平均分配到4个部分，为并行爬取做准备
    """
    
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.mongo_client = None
        self.db = None
        
        # 加载城市代码
        self.city_codes = self.load_city_codes()
        logger.info(f"初始化完成: {len(self.city_codes)} 个城市")
    
    def load_city_codes(self) -> List[dict]:
        """从JSON文件中加载所有城市代码"""
        city_code_path = Path("recruitment_spider/data/bosszhipin/city_code.json")
        city_code_groups = []
        try:
            if not city_code_path.exists():
                logger.error(f"城市代码文件不存在: {city_code_path}")
                return []
            with open(city_code_path, 'r', encoding='utf-8') as f:
                city_data = json.load(f)
            for group in city_data:
                for city in group.get('cityList', []):
                    code = str(city.get('code'))
                    name = city.get('name')
                    if code and name:
                        city_code_groups.append({'name':name,'code': code})
            logger.info(f"成功加载 {len(city_code_groups)} 个城市代码")
            return city_code_groups
        except Exception as e:
            logger.error(f"加载城市代码失败: {str(e)}")
            return []
    
    async def init_db(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise
    
    def get_url_key(self, doc):
        """生成URL的唯一键，用于比较"""
        return (
            doc.get('industry_code', ''),
            doc.get('job_type_code', '')
        )
    
    async def analyze_collection_group(self, url_collection, log_collection):
        """分析单个集合组的数据差异"""
        logger.info(f"分析集合组: {url_collection} vs {log_collection}")
        
        # 获取url_part数据
        url_docs = await self.db[url_collection].find({}).to_list(length=None)
        url_keys = {self.get_url_key(doc): doc for doc in url_docs}
        
        # 获取log_part数据
        log_docs = await self.db[log_collection].find({}).to_list(length=None)
        log_keys = {self.get_url_key(doc): doc for doc in log_docs}
        
        logger.info(f"URL集合数量: {len(url_docs)}")
        logger.info(f"LOG集合数量: {len(log_docs)}")
        
        # 找出只在log_part中存在的数据
        only_in_log = []
        for key, doc in log_keys.items():
            if key not in url_keys:
                only_in_log.append(doc)
        
        # 找出只在url_part中存在的数据
        only_in_url = []
        for key, doc in url_keys.items():
            if key not in log_keys:
                only_in_url.append(doc)
        
        # 找出共同存在的数据
        common_keys = set(url_keys.keys()) & set(log_keys.keys())
        
        logger.info(f"只在LOG中存在的数据数量: {len(only_in_log)}")
        logger.info(f"只在URL中存在的数据数量: {len(only_in_url)}")
        logger.info(f"共同存在的数据数量: {len(common_keys)}")
        
        return {
            'url_collection': url_collection,
            'log_collection': log_collection,
            'url_count': len(url_docs),
            'log_count': len(log_docs),
            'only_in_log': only_in_log,
            'only_in_url': only_in_url,
            'common_count': len(common_keys)
        }
    
    async def validate_collections(self):
        """验证所有集合组的数据一致性"""
        logger.info("开始验证step1集合数据一致性...")
        
        collection_groups = [
            {
                'url_part': 'boss_step1_urls_part1',
                'log_part': 'boss_step1_urls_202504_log_part1'
            },
            {
                'url_part': 'boss_step1_urls_part2', 
                'log_part': 'boss_step1_urls_202504_log_part2'
            },
            {
                'url_part': 'boss_step1_urls_part3',
                'log_part': 'boss_step1_urls_202504_log_part3'
            },
            {
                'url_part': 'boss_step1_urls_part4',
                'log_part': 'boss_step1_urls_202504_log_part4'
            }
        ]
        
        all_valid = True
        results = []
        
        for group in collection_groups:
            result = await self.analyze_collection_group(
                group['url_part'], 
                group['log_part']
            )
            results.append(result)
            
            # 检查是否有不一致的数据
            if result['only_in_log'] or result['only_in_url']:
                all_valid = False
                logger.error(f"集合组 {group['url_part']} vs {group['log_part']} 数据不一致！")
                logger.error(f"  只在LOG中的数据: {len(result['only_in_log'])}")
                logger.error(f"  只在URL中的数据: {len(result['only_in_url'])}")
            else:
                logger.info(f"集合组 {group['url_part']} vs {group['log_part']} 数据一致 ✓")
        
        # 汇总统计
        total_url_count = sum(r['url_count'] for r in results)
        total_log_count = sum(r['log_count'] for r in results)
        total_only_in_log = sum(len(r['only_in_log']) for r in results)
        total_only_in_url = sum(len(r['only_in_url']) for r in results)
        total_common = sum(r['common_count'] for r in results)
        
        logger.info(f"汇总统计:")
        logger.info(f"  总URL数据量: {total_url_count}")
        logger.info(f"  总LOG数据量: {total_log_count}")
        logger.info(f"  总只在LOG中的数据量: {total_only_in_log}")
        logger.info(f"  总只在URL中的数据量: {total_only_in_url}")
        logger.info(f"  总共同数据量: {total_common}")
        
        if all_valid:
            logger.info("所有step1集合组数据验证通过！")
        else:
            logger.error("存在数据不一致的集合组，请先清理数据！")
        
        return all_valid
    
    async def run(self):
        """运行爬虫的主方法"""
        try:
            # 初始化数据库
            await self.init_db()
            logger.info("数据库初始化成功")
            
            # 首先验证所有集合组的数据一致性
            if not await self.validate_collections():
                logger.error("step1数据验证失败，程序退出！请先清理不一致的数据。")
                return
            
            logger.info("step1数据验证通过，开始生成step2 URL...")
            
            # 清空原有的step2 URL集合
            await self.db['boss_step2_urls'].delete_many({})
            
            # 为每个part生成step2的URL
            total_step2_urls = 0
            for part_num in range(1,5):
                self.all_urls = []
                part_urls = await self.db[f'boss_step1_urls_202504_log_part{part_num}'].find({'success':True}, {'_id': 0,'industry_code':1,'industry_name':1,'job_type_code':1,'job_type_name':1}).to_list(length=None)
                
                for city in self.city_codes:
                    for step1 in part_urls:
                        # 构建带参数的URL
                        url_params = {
                            'city': city.get('code'),
                            'position': step1.get('job_type_code'),
                            'industry': step1.get('industry_code')
                        }
                        url = f"https://www.zhipin.com/web/geek/jobs?city={url_params['city']}&position={url_params['position']}&industry={url_params['industry']}"
                        # 构建url
                        self.all_urls.append({
                            'url': url,
                            'industry_code': step1.get('industry_code'),
                            'industry_name': step1.get('industry_name'),
                            'city_code': city.get('code'),
                            'city_name': city.get('name'),
                            'job_type_code': step1.get('job_type_code'),
                            'job_type_name': step1.get('job_type_name'),
                            'create_time': datetime.now(),
                            'part': part_num
                        })
                
                # 批量保存到mongodb
                if self.all_urls:
                    await self.db['boss_step2_urls'].insert_many(self.all_urls)
                    total_step2_urls += len(self.all_urls)
                    logger.info(f"Part{part_num} 已生成 {len(self.all_urls)} 个step2 URL")
            
            # 创建索引
            await self.db['boss_step2_urls'].create_index([
                ('industry_code', 1),
                ('job_type_code', 1),
                ('city_code', 1)
            ], unique=True)
            await self.db['boss_step2_urls'].create_index([('create_time', 1)])
            await self.db['boss_step2_urls'].create_index([('part', 1)])
            
            logger.info(f"总共生成 {total_step2_urls} 个step2 URL组合，已保存到MongoDB")
            
            # 将boss_step2_urls中的数据平均分配到4个part集合中
            all_step2_urls = await self.db['boss_step2_urls'].find({}, {'_id': 0,'part':0}).to_list(length=None)
            part_size = len(all_step2_urls) // 4
            if len(all_step2_urls) % 4 != 0:
                part_size += 1
                
            # 清空原有的part集合
            for i in range(1, 5):
                await self.db[f'boss_step2_urls_part{i}'].delete_many({})
            
            # 将数据分成4个部分并保存
            for i in range(4):
                start_idx = i * part_size
                end_idx = min((i + 1) * part_size, len(all_step2_urls))
                part_urls = all_step2_urls[start_idx:end_idx]
                
                if part_urls:
                    await self.db[f'boss_step2_urls_part{i+1}'].insert_many(part_urls)
                    # 创建索引
                    await self.db[f'boss_step2_urls_part{i+1}'].create_index([
                        ('industry_code', 1),
                        ('job_type_code', 1),
                        ('city_code', 1)
                    ], unique=True)
                    await self.db[f'boss_step2_urls_part{i+1}'].create_index([('status', 1)])
                    await self.db[f'boss_step2_urls_part{i+1}'].create_index([('create_time', 1)])
                    await self.db[f'boss_step2_urls_part{i+1}'].create_index([('job_type_code', 1)])
                    await self.db[f'boss_step2_urls_part{i+1}'].create_index([('part', 1)])
                
                logger.info(f"Step2 Part{i+1} 已保存 {len(part_urls)} 个URL组合")
            
        except Exception as e:
            logger.error(f"爬虫运行出错: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            if self.mongo_client:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")

async def main():
    """主函数"""
    try:
        spider = BossSpiderStep3()
        await spider.run()
    except Exception as e:
        logger.error(f"运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main()) 
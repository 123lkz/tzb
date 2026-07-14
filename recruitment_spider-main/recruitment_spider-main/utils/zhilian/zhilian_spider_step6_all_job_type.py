# -*- coding: utf-8 -*-
"""
智联招聘爬虫 - 第二步
功能：验证step1生成的URL是否有数据，并标记状态

主要步骤：
1. 从MongoDB加载step1生成的URL组合
2. 对每个URL组合进行请求验证
3. 根据返回的职位数量判断URL是否有效
   - 职位数量 > 15：标记为success
   - 职位数量 <= 15：标记为failed
4. 将验证结果保存到MongoDB

数据存储：
- 输入集合：zhilian_step1_urls_part1
- 输出集合：zhilian_step1_urls_202504_log_part1
- 索引：
  * (job_type_code, industry_code) - 复合索引
  * status - 状态索引
  * crawl_time - 爬取时间索引

请求配置：
- 基础URL：https://fe-api.zhaopin.com
- API路径：/c/i/search/positions
- 请求方法：POST
- 请求头：包含必要的认证和浏览器信息
- 请求参数：包含职位类型、行业类型等搜索条件

注意事项：
1. 使用随机延迟(2-5秒)避免请求过快
2. 使用批量处理(1000条/批)提高效率
3. 记录详细的日志信息
4. 支持断点续传（通过检查已爬取记录）
"""

import json
import logging
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import requests
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError
from tqdm import tqdm

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "zhilian_spider")
except ImportError:
    # 如果无法导入log_manager，则使用基本配置
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("spiders.zhilian_spider")

class ZhilianSpiderStep2:
    """智联招聘爬虫 - Requests版本"""
    
    def __init__(self):
        # API配置
        self.base_url = "https://fe-api.zhaopin.com"
        self.search_api = "/c/i/search/positions"
        
        # 基础数据文件路径
        self.base_data_path = Path("recruitment_spider/data/zhilian/base_data.json")
        
        # 请求头配置
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.zhaopin.com',
            'referer': 'https://www.zhaopin.com/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'x-zp-business-system': '1',
            'x-zp-page-code': '0',
            'x-zp-platform': '13'
        }
        
        # 加载基础数据
        self.job_type_codes = self.load_job_type_codes()
        self.city_codes = self.load_city_codes()
        self.industry_codes = self.load_industry_codes()
        
        # 会话对象
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # 爬虫配置
        self.page_size = 20
        
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.mongo_progress_collection = "zhilian_step1_urls_202504_log_all_job_type"  # 新增进度记录集合        
        self.zhilian_url_202504_part = "zhilian_step1_urls"  # URL集合名称
        self.output_collection = "zhilian_job_raw_all_job_type"  # 输出集合名称
        self.mongo_client = None
        self.db = None
        self.progress_collection = None
        
        # URL缓存
        self.crawled_urls = {}
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        # 加载已爬取的URL
        self._load_crawled_urls()
        
        logger.info(f"初始化完成: {len(self.job_type_codes)} 个岗位类型, {len(self.city_codes)} 个城市, {len(self.industry_codes)} 个行业")
    
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

    def load_city_codes(self) -> List[dict]:
        """从base_data.json加载城市代码"""
        try:
            data = self.load_base_data()
            cities = data.get('data', {}).get('allCity', [])
            city_codes = []
            
            for city in cities:
                code = city.get('code')
                name = city.get('name')
                if code and name:
                    city_codes.append({
                        'code': code,
                        'name': name
                    })
            
            logger.info(f"成功加载 {len(city_codes)} 个城市")
            return city_codes
            
        except Exception as e:
            logger.error(f"加载城市代码失败: {str(e)}")
            return []

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
    
    def get_job_list(self, url: dict) -> List[Dict]:
        """
        获取职位列表
        :param url: URL信息字典，包含职位类型、城市、行业等信息
        :return: 职位列表
        """
        try:                        
            # 构造请求数据
            params = {
                "MmEwMD":"5WiIm3PrZlq0N8dSuxYPEKH2XL_2g_Y.XqKsBw0MjSVtrBhK4nZWbe18_jpLVcvJi2U8GSZw84EZYpMTBcFvBT3jGuGg6aVZkWN5J5fOWNbPzgXuK6jdeBFjg_Qh89KeWLodhdv.FzEZmRKdU.Ry3u9ptSHVRfagbonLX8RsMO9rwY.bJzIluzJiyN5nuO45TYjGspyb_jKihkqUeCB4wwahZnLO3o1p48qnlOJGWInIfxd9npUiT9PQua9wcwRlLCzyBp0uhgKY2dP0MwhNhOR.FivgnjfgM2Y8ipTYte3r3BkX13e8mLGJFS6tYMziwlP_Q5F2BL.snTGlPjH2lSaz0R9.zjeWG5hRsE.buZCsu4FWKvqbnPvv9lRmoKKgjfuc2nLiz0NXvu4ywimn1xA",
                "c1K5tw0w6_":"40ndbi7V3orvqvTD7XyTo8nNhZS.Q3QlPMJnqZJSXwhjyW8eHUDXcEjKWcxv6a7W31NbA9Mj7AS0EF3JVw1jE5fy0sHC03b6JbZb5AVs5dI0_wkCrkLdLIeD1PzHgugAXE1Rx3ogVnJi1__taxMBbMbhTE7ZF8hvQPoP36PHB2XNZ1dSPdIYyCect8Nxw624.ld9dvCnO9kxpCTqfXSiYOPzTV1IIBOMQwRjQGnLiHMwHk_q7D.tdArrS5vD2_AbLy7W8LE9CsuVTkImXIKXU2jxVksd5UGmq4QJKSLwAJq.cB_xC6VpHHTXB5QiOSpyJhGBpisnIqqNyoKVELBNBCVthGTTWNPE0z.aMB0J4xVtjD_ON6NnqB9HqJ7VK_hMSGpLbxKrPeY2oHw8IowE3wzGCL347ka2pK2vdkhs2t_VOCNGK_rbbXkg3uHF4xsPPExxgIjHYbsrIAYvfavZQHA"
            }
            data = {
                "S_SOU_JD_JOB_LEVEL3": url['job_type_code'],
                # "S_SOU_JD_INDUSTRY_LEVEL": url['industry_code'],
                "S_SOU_WORK_CITY": "489",
                "anonymous": 0,
                "cvNumber": "0B1FB7FA21E74B7837344A88A751A7495C2234C85637032AEA89700001C764F13C9CB5254267336053310C9146FDFAA3_A0001",
                "eventScenario": "pcSearchedSouSearch",
                "order": 4,
                "pageIndex": 1,
                "pageSize": self.page_size
            }

            # 发送请求
            url_path = f"{self.base_url}{self.search_api}"
            response = requests.post(url_path, params=params, json=data, headers=self.headers)
            response.raise_for_status()
            
            # 解析响应
            try:
                result = response.json()
            except json.JSONDecodeError:
                logger.warning(f"{url_path}不存在，参数{url}")
                raise Exception(f"{url_path}不存在，参数{url}")
                
            if result.get('code') != 200:                
                logger.error(f"请求失败: {result.get('message')}")
                raise Exception(f"请求失败: {result.get('message')}")
            
            jobs = result.get('data', {}).get('list', [])
            logger.info(f"获取到 {len(jobs)} 个职位")
            return jobs
            
        except Exception as e:
            logger.error(f"获取职位列表失败: {str(e)}")
            return []
    
    def _init_mongodb(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            self.progress_collection = self.db[self.mongo_progress_collection]                        
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise

    def _load_crawled_urls(self):
        """从MongoDB加载所有已爬取的URL到内存中"""
        try:
            cursor = self.progress_collection.find({}, {
                "job_type_code": 1,
                # "industry_code": 1,
            })
            
            for doc in cursor:                
                key = f"{doc['job_type_code']}"
                self.crawled_urls[key] = 1
                
            logger.info(f"已加载 {len(self.crawled_urls)} 个已爬取的URL组合")
        except Exception as e:
            logger.error(f"加载已爬取URL失败: {str(e)}")

    def is_combination_crawled(self, url: dict) -> bool:
        """检查指定的搜索组合是否已经爬取过"""
        try:            
            key = f"{url['job_type_code']}"            
            return bool(self.crawled_urls.get(key))
        except Exception as e:
            logger.error(f"检查爬取进度失败: {str(e)}")
            return False

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
            # 获取不同的job_type_code
            distinct_job_types = self.db[self.zhilian_url_202504_part].distinct("job_type_code")
            total_positions = len(distinct_job_types)
            logger.info(f"总共需要处理 {total_positions} 个不同的岗位类型")
            
            # 创建进度条
            pbar = tqdm(total=total_positions, 
                       desc="总体进度", 
                       unit="岗位类型",
                       ncols=100,
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')
            
            # 处理每个不同的job_type_code
            for job_type_code in distinct_job_types:
                try:
                    # 获取该job_type_code的第一条记录作为示例
                    url = self.db[self.zhilian_url_202504_part].find_one({"job_type_code": job_type_code})
                    if not url:
                        continue
                        
                    # 更新进度条描述
                    pbar.set_description(f"正在处理: {url['job_type_name']}")
                    
                    # 更新总进度条
                    pbar.update(1)
                    
                    # 检查是否已爬取
                    is_crawled = self.is_combination_crawled(url)
                    if is_crawled:
                        logger.info(f"跳过已爬取的岗位类型 - {url['job_type_name']}")
                        continue
                        
                    try:                                                        
                        # 随机延迟
                        time.sleep(random.uniform(2, 5))                            
                        # 获取职位列表
                        jobs = self.get_job_list(url)                            
                        # 保存数据到MongoDB
                        city = {}
                        industry = {}
                        job_type = {'code': url['job_type_code'], 'name': url['job_type_name']}
                        self.save_jobs_to_mongodb(jobs, job_type, city, industry)                        
                        # 标记URL为已爬取
                        self.mark_url_crawled(url, 'success', jobs)
                    except Exception as e:                            
                        logger.error(f"处理页面失败: {str(e)}")
                        continue                                                                        
                except Exception as e:                        
                    logger.error(f"处理岗位类型失败: {str(e)}")
                    continue
            
            # 关闭总进度条
            pbar.close()
            logger.info("爬虫运行完成")
            
        except Exception as e:
            logger.error(f"爬虫运行出错: {str(e)}")
            raise
        finally:
            self.close()

    def save_jobs_to_mongodb(self, jobs: List[Dict], job_type: dict, city: dict, industry: dict):
        """
        保存职位数据到MongoDB
        使用批量写入和更新操作
        """
        try:
            if not jobs:
                return
                
            # 准备批量操作
            operations = []
            current_time = datetime.now()
            
            for job in jobs:
                # 添加元数据
                job['_job_type'] = job_type
                job['_city'] = city
                job['_industry'] = industry
                job['_crawl_time'] = current_time
                
                # 创建更新操作
                operation = UpdateOne(
                    {'jobId': job['jobId']},  # 查询条件
                    {'$set': job},  # 更新数据
                    upsert=True  # 如果不存在则插入
                )
                operations.append(operation)
            
            # 执行批量写入
            if operations:
                result = self.db[self.output_collection].bulk_write(operations, ordered=False)
                logger.info(f"数据保存成功 - 插入: {result.upserted_count}, 修改: {result.modified_count}, 总数: {len(operations)}")
                
        except BulkWriteError as bwe:
            logger.error(f"批量写入出错: {str(bwe.details)}")
        except Exception as e:
            logger.error(f"保存数据到MongoDB失败: {str(e)}")
    
    def mark_url_crawled(self, url: dict, status: str, jobs: List[Dict]):
        """标记URL为已爬取，并根据是否有数据将其存入不同的集合"""
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 构造要保存的文档
            document = {
                "job_type_code": url['job_type_code'],
                "job_type_name": url['job_type_name'],
                # "industry_code": url['industry_code'],
                # "industry_name": url['industry_name'],
                "crawl_time": current_time,
                "status": status,
                "job_count": len(jobs)
            }
            
            # 更新数据库
            self.progress_collection.update_one(
                {
                    "job_type_code": url['job_type_code'],
                    # "industry_code": url['industry_code']
                },
                {"$set": document},
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"标记URL状态失败: {str(e)}")

def main():
    """主函数"""
    try:
        # 创建爬虫实例
        spider = ZhilianSpiderStep2()
        
        # 运行爬虫
        spider.run()
        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()

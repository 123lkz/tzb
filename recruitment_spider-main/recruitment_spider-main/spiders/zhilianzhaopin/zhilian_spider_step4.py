#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智联招聘爬虫 - 第四步
功能：爬取职位详情数据，并保存到MongoDB

主要步骤：
1. 从MongoDB加载step2生成的URL数据（part1部分）
2. 对每个URL组合进行分页爬取
3. 验证职位发布时间，只保存2025年的数据
4. 将职位数据保存到MongoDB

数据存储：
- 输入集合：zhilian_step2_urls_part1
- 输出集合：zhilian_job_raw_part1
- 进度记录集合：zhilian_step2_urls_202504_log_part1
- 索引配置：
  * jobId - 唯一索引
  * _job_type.code - 岗位代码索引
  * _city.code - 城市代码索引
  * _industry.code - 行业代码索引
  * _crawl_time - 爬取时间索引

请求配置：
- 基础URL：https://fe-api.zhaopin.com
- API路径：/c/i/search/positions
- 请求方法：POST
- 请求头：包含必要的认证和浏览器信息
- 请求参数：包含职位类型、行业类型、城市等搜索条件

数据过滤规则：
1. 只保存2025年发布的职位数据
2. 遇到2025年之前的职位数据时停止当前分页爬取
3. 每个职位数据添加元信息：
   * _job_type：岗位类型信息
   * _city：城市信息
   * _industry：行业信息
   * _crawl_time：爬取时间

注意事项：
1. 使用随机延迟(2-5秒)避免请求过快
2. 使用批量处理(1000条/批)提高效率
3. 支持断点续传（通过检查已爬取记录）
4. Cookie验证和自动更新机制
5. 详细的日志记录和进度显示
6. 异常处理和重试机制
"""


import os
import sys
import json
import logging
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import requests
from urllib.parse import urlencode
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError
from tqdm import tqdm
# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)
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

class ZhilianSpiderStep4:
    """智联招聘爬虫 - Requests版本"""
    
    def __init__(self):
        # API配置
        self.base_url = "https://fe-api.zhaopin.com"
        self.search_api = "/c/i/search/positions"
        self.cookie_validator_api = "http://210.14.140.52:10330"  # cookie验证API地址
        
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
        self.max_retries = 3
        self.retry_delay = 5
        
        # MongoDB配置
        self.mongo_uri = "mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test"
        self.mongo_db = "da_test"
        self.mongo_collection = "zhilian_job_raw_part1"
        self.mongo_progress_collection = "zhilian_step2_urls_202510_log_part1"  # 新增进度记录集合        
        self.zhilian_url_part1 = "zhilian_step2_urls_part1"  # URL集合名称
        self.zhilian_urls_data = None
        self.mongo_client = None
        self.db = None
        self.collection = None
        self.progress_collection = None
        
        # URL缓存
        self.crawled_urls = {}
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        # 加载已爬取的URL
        self._load_crawled_urls()
        
        logger.info(f"初始化完成: {len(self.job_type_codes)} 个岗位类型, {len(self.city_codes)} 个城市, {len(self.industry_codes)} 个行业")
        
    def _parse_cookie_string(self, cookie_string: str) -> Dict[str, str]:
        """解析cookie字符串为字典"""
        cookies = {}
        for item in cookie_string.split('; '):
            if '=' in item:
                name, value = item.split('=', 1)
                cookies[name] = value
        return cookies
    
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
    
    def check_cookie_validity(self) -> bool:
        """
        检查cookie是否有效并获取cookie
        通过调用验证API服务来验证和获取cookie
        """
        try:
            # 调用验证API
            response = requests.get(f"{self.cookie_validator_api}/api/validate/zhilian")
            
            if response.status_code != 200:
                logger.error(f"调用验证API失败，状态码: {response.status_code}")
                return False
                
            result = response.json()
            if not result.get('is_valid'):
                logger.error(f"Cookie验证失败: {result.get('message')}")
                return False
                
            api_data = result.get('data', {})
            if not api_data:
                logger.error("API返回数据为空")
                return False
                
            # 从API获取cookie、params和cvNumber
            cookies = api_data.get('cookies', {})
            params = api_data.get('params', {})
            cv_number = api_data.get('cvNumber')
            
            # 更新session的cookies
            self.session.cookies.update(cookies)
            
            # 保存params和cvNumber供后续使用
            self.request_params = params
            self.cv_number = cv_number
            
            logger.info("Cookie验证成功并已更新到session中")
            return True
            
        except Exception as e:
            logger.error(f"验证Cookie时发生错误: {str(e)}")
            return False

    def get_job_list(self, url: dict, page: int) -> List[Dict]:
        """
        获取职位列表
        :param url: URL信息字典，包含职位类型、城市、行业等信息
        :param page: 页码
        :return: 职位列表
        """
        try:
            # 从API获取cookie和params
            response = requests.get(f"{self.cookie_validator_api}/api/validate/zhilian")
            if response.status_code != 200:
                logger.error(f"获取cookie失败，状态码: {response.status_code}")
                raise Exception("获取cookie失败")
            
            api_result = response.json()
            if not api_result.get('is_valid'):
                logger.error(f"Cookie无效: {api_result.get('message')}")
                raise Exception("Cookie无效")
            
            api_data = api_result.get('data', {})
            if not api_data:
                logger.error("API返回数据为空")
                raise Exception("API返回数据为空")
            
            # 使用API返回的cookie和params
            cookies = api_data.get('cookies', {})
            params = api_data.get('params', {})
            cv_number = api_data.get('cvNumber')
            
            # 构造请求数据
            data = {
                "S_SOU_JD_JOB_LEVEL3": url['job_type_code'],
                "S_SOU_JD_INDUSTRY_LEVEL": url['industry_code'],
                "S_SOU_WORK_CITY": url['city_code'],
                "anonymous": 0,
                "cvNumber": cv_number,  # 使用API返回的cvNumber
                "eventScenario": "pcSearchedSouSearch",
                "order": 4,  # 4表示最新发布
                "pageIndex": page,
                "pageSize": self.page_size
            }

            # 发送请求
            url_path = f"{self.base_url}{self.search_api}"
            
            # 更新session的cookies
            self.session.cookies.update(cookies)
            
            response = self.session.post(url_path, params=params, json=data)
            response.raise_for_status()
            
            # 解析响应
            # 检查响应内容是否为压缩数据或无效数据
            try:
                # 尝试解析JSON
                result = response.json()
            except json.JSONDecodeError:
                # 如果解析失败，可能是压缩数据或无效响应
                logger.warning(f"{url_path}第{page}页不存在，参数{url}")
                return []
            if result.get('code') != 200:
                if result.get('code') in [401, 403] or 'token' in result.get('message', '').lower():
                    logger.error("Cookie已过期，需要更新")
                    raise Exception("Cookie已过期")
                logger.error(f"请求失败: {result.get('message')}")
                return []
            
            jobs = result.get('data', {}).get('list', [])
            logger.info(f"获取到 {len(jobs)} 个职位")
            return jobs
            
        except Exception as e:
            logger.error(f"获取职位列表失败: {str(e)}")
            if "Cookie".lower() in str(e).lower():
                raise  # 向上传递Cookie过期异常
            return []
    
    def _init_mongodb(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            self.collection = self.db[self.mongo_collection]
            self.progress_collection = self.db[self.mongo_progress_collection]                        
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise

    def _load_crawled_urls(self):
        """
        从MongoDB加载所有已爬取的URL到内存中
        格式: {f"{job_type_code}_{city_code}_{industry_code}_{page}": last_publish_time}
        """
        try:
            # logs_data = list(self.db['zhilian_step2_urls_202504_log_part1'].find({'jobs_count':0}))
            # for log in logs_data:
            #     key = f"{log['job_type_code']}_{log['city_code']}_{log['industry_code']}"
            #     self.crawled_urls[key] = 1
            
            cursor = self.progress_collection.find({}, {
                "job_type_code": 1,
                "city_code": 1,
                "industry_code": 1,
                "page": 1,
                "last_publish_time": 1
            })
            
            for doc in cursor:                
                # key = f"{doc['job_type_code']}_{doc['city_code']}_{doc['industry_code']}_{doc['page']}"
                key = f"{doc['job_type_code']}_{doc['city_code']}_{doc['industry_code']}"
                # self.crawled_urls[key] = doc.get('last_publish_time')
                self.crawled_urls[key] = 1
                
            
            logger.info(f"已加载 {len(self.crawled_urls)} 个已爬取的URL组合")
        except Exception as e:
            logger.error(f"加载已爬取URL失败: {str(e)}")

    def is_combination_crawled(self, url: dict, page: int) -> tuple:
        """
        检查指定的搜索组合是否已经爬取过
        返回 (是否爬取, 最后发布时间)
        """
        try:
            # key = f"{url['job_type_code']}_{url['city_code']}_{url['industry_code']}_{page}"
            key = f"{url['job_type_code']}_{url['city_code']}_{url['industry_code']}"
            last_publish_time = self.crawled_urls.get(key)
            # return bool(last_publish_time), last_publish_time
            return self.crawled_urls.get(key)
        except Exception as e:
            logger.error(f"检查爬取进度失败: {str(e)}")
            return False, None

    def mark_combination_crawled(self, url: dict, page: int, jobs_count: int, last_publish_time: str = None):
        """
        标记指定的搜索组合为已爬取
        """
        try:
            # 更新内存中的缓存
            key = f"{url['job_type_code']}_{url['city_code']}_{url['industry_code']}_{page}"
            self.crawled_urls[key] = last_publish_time
            
            # 更新数据库
            self.progress_collection.update_one(
                {
                    "job_type_code": url['job_type_code'],
                    "city_code": url['city_code'],
                    "industry_code": url['industry_code']                    
                },
                {
                    "$set": {
                        "job_type_name": url['job_type_name'],
                        "city_name": url['city_name'],
                        "industry_name": url['industry_name'],
                        "jobs_count": jobs_count,
                        "page": page,
                        "last_publish_time": last_publish_time,                        
                        "crawl_time": datetime.now()
                    }
                },
                upsert=True
            )
        except Exception as e:
            logger.error(f"记录爬取进度失败: {str(e)}")

    def get_crawl_progress(self) -> dict:
        """
        获取爬取进度统计
        """
        try:
            # 计算理论上的总组合数（每个组合假设最多50页）
            total_combinations = len(self.job_type_codes) * len(self.city_codes) * len(self.industry_codes) * 50
            
            # 从缓存中获取统计信息
            unique_combinations = set()
            total_jobs = 0
            
            for key in self.crawled_urls:
                job_type_code, city_code, industry_code, _ = key.split('_')
                unique_combinations.add(f"{job_type_code}_{city_code}_{industry_code}")
            
            return {
                "total_combinations": total_combinations,
                "crawled_combinations": len(unique_combinations),
                "total_pages_crawled": len(self.crawled_urls),
                "progress_percentage": (len(self.crawled_urls) / total_combinations) * 100 if total_combinations > 0 else 0
            }
        except Exception as e:
            logger.error(f"获取爬取进度失败: {str(e)}")
            return {}

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
                result = self.collection.bulk_write(operations, ordered=False)
                logger.info(f"数据保存成功 - 插入: {result.upserted_count}, 修改: {result.modified_count}, 总数: {len(operations)}")
                
        except BulkWriteError as bwe:
            logger.error(f"批量写入出错: {str(bwe.details)}")
        except Exception as e:
            logger.error(f"保存数据到MongoDB失败: {str(e)}")

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
            # 验证Cookie
            if not self.check_cookie_validity():
                raise Exception("Cookie无效，请更新Cookie后重试")
            
            # 获取数据库中的总职位数
            total_positions = self.db[self.zhilian_url_part1].count_documents({})
            logger.info(f"总共需要处理 {total_positions} 个岗位类型")
            
            # 创建进度条
            pbar = tqdm(total=total_positions, 
                       desc="总体进度", 
                       unit="组合",
                       ncols=100,
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')
            
            # 使用批量处理替代游标
            batch_size = 1000  # 每次处理100条记录
            processed = 0
            
            while processed < total_positions:
                try:
                    # 获取一批数据
                    urls_batch = list(self.db[self.zhilian_url_part1].find({}).skip(processed).limit(batch_size))                
                    
                    # 创建页面进度条
                    page_bar = tqdm(total=50, 
                                  desc="页面进度", 
                                  unit="页",
                                  leave=False,
                                  ncols=100,
                                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
                    
                    for url in urls_batch:                        
                        # 更新进度条描述
                        pbar.set_description(f"正在处理: {url['job_type_name']}-{url['city_name']}-{url['industry_name']}")
                        logger.info(f"处理搜索组合 - 职位: {url['job_type_name']}, 城市: {url['city_name']}, 行业: {url['industry_name']}")
                        
                        # 更新总进度条
                        pbar.update(1)
                        
                        # 检查是否已爬取
                        is_crawled = self.is_combination_crawled(url, 1)
                        if is_crawled:
                            logger.info(f"跳过已爬取的组合和页码 - 职位: {url['job_type_name']}, "
                                        f"城市: {url['city_name']}, 行业: {url['industry_name']}, 页码: {1}")
                            continue
                            
                        # 重置页面进度条
                        page_bar.reset()
                        clean_jobs = []
                        # 获取数据
                        # 标记是否已经处理过第一页无数据的情况
                        first_page_empty_handled = False
                        
                        for page in range(1, 50):
                            try:
                                # 更新页面进度条
                                page_bar.set_description(f"第{page}页")
                                page_bar.update(1)                                                                
                                # 获取职位列表
                                jobs = self.get_job_list(url, page)
                                # 随机延迟
                                time.sleep(random.uniform(2, 5))
                                # 检查是否有数据
                                if not jobs:
                                    if page == 1:
                                        # 有的行业一页数据也没有，这个时候需要标记为已爬取
                                        self.mark_combination_crawled(url, page, 0, None)
                                        first_page_empty_handled = True
                                    logger.info(f"没有更多数据，停止分页爬取")                                    
                                    break
                                
                                # 检查发布时间是否小于2025年8月1日
                                cutoff_date = datetime(2025, 9, 1)
                                should_break = False                                
                                last_job_time = None
                                
                                for job in jobs:
                                    publish_time = job.get('publishTime')
                                    if publish_time:
                                        try:
                                            job_time = datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
                                            if job_time < cutoff_date:
                                                logger.info(f"发现{job_time.strftime('%Y-%m-%d')}的数据，停止分页爬取")
                                                should_break = True
                                                break
                                            else:
                                                clean_jobs.append(job)
                                                last_job_time = publish_time
                                        except Exception as e:
                                            logger.warning(f"解析发布时间失败: {publish_time}, {str(e)}")                                                                
                                
                                if should_break:
                                    break
                                
                            except Exception as e:
                                if "Cookie已过期" in str(e):
                                    raise  # 向上传递Cookie过期异常
                                logger.error(f"处理页面失败: {str(e)}")
                                continue
                                    
                        # 保存数据到MongoDB
                        city = {'code': url['city_code'], 'name': url['city_name']}
                        industry = {'code': url['industry_code'], 'name': url['industry_name']}
                        job_type = {'code': url['job_type_code'], 'name': url['job_type_name']}
                        self.save_jobs_to_mongodb(clean_jobs, job_type, city, industry)
                        
                        # 标记当前页面为已爬取（避免重复标记第一页无数据的情况）
                        if not first_page_empty_handled:
                            self.mark_combination_crawled(url, page, len(clean_jobs), last_job_time)                        
                    # 关闭页面进度条
                    page_bar.close()
                    
                    # 更新已处理的数量
                    processed += len(urls_batch)
                    
                except Exception as e:
                    if "Cookie已过期" in str(e):
                        raise  # 继续向上传递Cookie过期异常
                    logger.error(f"处理搜索组合失败: {str(e)}")
                    continue
            
            # 关闭总进度条
            pbar.close()
            logger.info("爬虫运行完成")
            
        except Exception as e:
            if "Cookie已过期" in str(e):
                logger.error("Cookie已过期，请更新Cookie后重试")
            else:
                logger.error(f"爬虫运行出错: {str(e)}")
            raise
        finally:
            self.close()

def main():
    """主函数"""
    try:
        # 创建爬虫实例
        spider = ZhilianSpiderStep4()
        
        # 运行爬虫
        spider.run()
        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()

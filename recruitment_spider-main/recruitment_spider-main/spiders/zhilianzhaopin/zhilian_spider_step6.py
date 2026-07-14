#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智联招聘爬虫 - 第六步
功能：处理zhilian_step3_urls_part1集合中的URL，获取职位详情数据

主要步骤：
1. 从MongoDB读取zhilian_step3_urls_part1集合的URL数据
2. 使用GET请求获取每个URL的职位详情
3. 将职位详情数据保存到MongoDB

数据存储：
- 输入集合：zhilian_step3_urls_part1
- 输出集合：zhilian_job_detail_part1
- 进度记录集合：zhilian_step3_urls_part1_log

请求配置：
- 请求方法：GET
- 请求头：包含必要的认证和浏览器信息
- 请求参数：无

数据过滤规则：
1. 记录请求时间
2. 记录响应状态
3. 记录原始响应数据
"""

import os
import sys
import json
import logging
import random
import time
import requests
import http.client
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
from playwright.async_api import async_playwright
import asyncio

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

class ZhilianSpiderStep6:
    """智联招聘职位详情爬虫"""
    
    def __init__(self):
        # 请求头配置
        self.base_url = "jobs.zhaopin.com"                
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.input_collection = "zhilian_step3_urls_part1"
        self.output_collection = "zhilian_job_detail_part1"
        self.progress_collection = "zhilian_step3_urls_202504_log_part1"
        
        # 爬虫配置
        self.max_retries = 10
        self.retry_delay = 5
        self.request_delay = (2, 5)  # 随机延迟范围（秒）
        
        # MongoDB连接
        self.mongo_client = None
        self.db = None
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        # 加载已处理的URL
        self._load_processed_urls()
    
    def _init_mongodb(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            logger.info("MongoDB连接成功")
        except Exception as e:
            logger.error(f"MongoDB连接失败: {str(e)}")
            raise
    
    def _load_processed_urls(self):
        """加载已处理的URL"""
        try:
            self.processed_urls = set()
            cursor = self.db[self.progress_collection].find({}, {'positionUrl': 1})
            for doc in cursor:
                self.processed_urls.add(doc.get('positionUrl'))
            logger.info(f"已加载 {len(self.processed_urls)} 个已处理的URL")
        except Exception as e:
            logger.error(f"加载已处理URL失败: {str(e)}")
            self.processed_urls = set()
    
    def extract_jobinfo(self, content):
        soup = BeautifulSoup(content, "html.parser")
        scripts = soup.find_all("script")
        for script in scripts:
            script_text = script.string or script.text
            if script_text and "jobInfo" in script_text:
                idx = script_text.find("jobInfo")
                if idx == -1:
                    continue
                brace_start = script_text.find("{", idx)
                if brace_start == -1:
                    continue
                count = 0
                for i in range(brace_start, len(script_text)):
                    if script_text[i] == "{":
                        count += 1
                    elif script_text[i] == "}":
                        count -= 1
                        if count == 0:
                            brace_end = i
                            jobinfo_str = script_text[brace_start:brace_end+1]
                            # 去掉多余的逗号
                            jobinfo_str = re.sub(r',\s*}', '}', jobinfo_str)
                            jobinfo_str = re.sub(r',\s*]', ']', jobinfo_str)
                            try:
                                jobinfo_dict = json.loads(jobinfo_str)
                                return jobinfo_dict
                            except Exception as e:
                                logger.warning(f"jobInfo内容不是标准JSON，原始内容：{jobinfo_str}")
                                return jobinfo_str
                            break
        return None
    
    async def init_browser(self):
        logger.info("初始化Playwright浏览器...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            locale="zh-CN"
        )
        self.page = await self.context.new_page()
        logger.info("浏览器初始化完成")

    async def close_browser(self):
        logger.info("关闭Playwright浏览器...")
        await self.browser.close()
        await self.playwright.stop()
        logger.info("浏览器已关闭")

    async def get_job_detail(self, url: str) -> Dict:
        logger.info(f"开始访问职位详情页: {url}")
        doc_response = {'content': None, 'status': None, 'headers': None, 'url': None}

        async def handle_response(response):
            if (
                response.request.resource_type == "document"
                and doc_response['content'] is None
                and response.status == 200
            ):
                logger.info(f"捕获到文档类型响应: {response.url} 状态码: {response.status}")
                doc_response['status'] = response.status
                doc_response['headers'] = dict(await response.all_headers())
                doc_response['url'] = response.url
                try:
                    doc_response['content'] = await response.text()
                    logger.info(f"成功获取文档内容，长度: {len(doc_response['content'])}")
                except Exception as e:
                    logger.warning(f"获取文档内容失败: {e}")
                    doc_response['content'] = ""

        self.page.on("response", handle_response)

        # 重试逻辑
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await self.page.goto(url, wait_until="domcontentloaded")
                for _ in range(50):
                    if doc_response['content'] is not None:
                        break
                    await self.page.wait_for_timeout(100)
                content = doc_response['content']
                jobInfo = self.extract_jobinfo(content) if content else None
                if jobInfo is not None:
                    logger.info(f"成功提取jobInfo: {url}")
                else:
                    logger.warning(f"未能提取到jobInfo: {url}")
                return {
                    'status_code': doc_response['status'],
                    'content': content,
                    'headers': doc_response['headers'],
                    'url': doc_response['url'],
                    'jobinfo': jobInfo
                }
            except Exception as e:
                logger.warning(f"访问 {url} 失败，尝试次数 {attempt + 1}/{max_retries}，错误: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"访问 {url} 失败，跳过该URL")
                    return None
                await asyncio.sleep(2)  # 等待2秒后重试

    def save_job_detail(self, url: str, response_data: Dict, original_doc: Dict):
        """保存职位详情数据，只保存jobDetail下detailedCompany和detailedPosition，合并为一个扁平字典"""
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            jobinfo = response_data.get('jobinfo', {})
            jobdetail = jobinfo.get('jobDetail', {})
            detailed_company = jobdetail.get('detailedCompany', {})
            detailed_position = jobdetail.get('detailedPosition', {})

            # 合并两个字典（不加前缀，字段名保持原样）
            detail_doc = {
                'positionUrl': url,
                'crawl_time': current_time,
                **detailed_company,
                **detailed_position
            }
            logger.info(f"保存职位详情到MongoDB: {url}")
            self.db[self.output_collection].insert_one(detail_doc)
            logger.info(f"保存log到MongoDB: {url}")
            self.db[self.progress_collection].insert_one({
                'positionUrl': url,
                'status': 'success' if response_data else 'failed',
                'crawl_time': current_time
            })
            return True
        except Exception as e:
            logger.error(f"保存数据失败: {url}, 错误: {str(e)}")
            return False
    
    async def process_data(self):
        try:
            await self.init_browser()
            
            # 设置游标超时时间为10分钟
            cursor = self.db[self.input_collection].find({}).max_time_ms(600000)
            
            # 使用批量处理
            batch_size = 1000
            total_docs = self.db[self.input_collection].count_documents({})
            logger.info(f"开始处理数据，共 {total_docs} 条记录")
            
            processed_count = 0
            skip = 0
            
            # 创建总体进度条
            with tqdm(total=total_docs, desc="总体进度") as pbar:
                while skip < total_docs:
                    # 获取一批数据，使用skip和limit实现分页
                    batch = list(self.db[self.input_collection].find({})
                               .skip(skip)
                               .limit(batch_size)
                               .max_time_ms(600000))
                    
                    if not batch:
                        break
                        
                    for doc in tqdm(batch, total=len(batch), desc=f"处理批次 {skip//batch_size + 1}", leave=False):
                        url = doc.get('positionUrl')
                        if not url or url in self.processed_urls:
                            pbar.update(1)  # 更新总体进度
                            continue
                            
                        logger.info(f"处理URL: {url}")
                        response_data = await self.get_job_detail(url)
                        await asyncio.sleep(random.uniform(*self.request_delay))
                        
                        if self.save_job_detail(url, response_data, doc):
                            self.processed_urls.add(url)
                            processed_count += 1
                            pbar.update(1)  # 更新总体进度
                    
                    # 更新skip值
                    skip += batch_size
                    
            logger.info(f"数据处理完成，共处理 {processed_count} 条记录")
            
        except Exception as e:
            logger.error(f"数据处理失败: {str(e)}")
            raise
        finally:
            await self.close_browser()
    
    def close(self):
        """关闭MongoDB连接"""
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("MongoDB连接已关闭")

async def main():
    """主函数（异步）"""
    spider = ZhilianSpiderStep6()
    try:
        await spider.process_data()
    finally:
        spider.close()

if __name__ == "__main__":
    asyncio.run(main())
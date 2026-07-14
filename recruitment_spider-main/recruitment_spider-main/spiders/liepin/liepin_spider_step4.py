#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
猎聘网爬虫 - 第四步
功能：根据step3生成的URL，获取职位列表数据

主要步骤：
1. 从MongoDB加载step3生成的URL数据
2. 使用Playwright模拟浏览器访问URL
3. 解析职位列表数据
4. 保存到MongoDB

数据存储：
- 输入集合：liepin_step2_urls_part1-4
- 输出集合：liepin_step4_jobs
- 日志集合：liepin_step4_urls_202504_log_part1-4

注意事项：
1. 使用Playwright模拟真实浏览器行为
2. 需要处理反爬机制
3. 记录URL访问日志
4. 异常处理和重试机制
"""

import json
import logging
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError
from playwright.sync_api import sync_playwright, Page, Browser
from tqdm import tqdm
import sys
import os
from urllib.parse import unquote, urlparse, parse_qs

# 将项目根目录添加到Python路径中
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent  # 从当前文件向上找三层到项目根目录
sys.path.append(str(project_root))

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "liepin_spider_step4")
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class LiepinSpiderStep4:
    """猎聘网爬虫 - 第四步"""
    
    def __init__(self):
        """初始化爬虫
        """
 
        
        # MongoDB配置
        self.mongo_uri = "mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test"
        self.mongo_db = "da_test"
        self.mongo_client = None
        self.db = None
        self.collection = None
        self.progress_collection = None
        
        # 输入输出集合名称
        self.input_collection = f'liepin_step2_urls_part1'
        self.output_collection = 'liepin_job_raw_part1'
        self.log_collection = f'liepin_step2_urls_202504_log_part1'
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        # 初始化Playwright
        self.playwright = None
        self.browser = None
        self.page = None
        self._init_browser()
        
        # 已爬取URL缓存
        self.crawled_urls = {}
        self._load_crawled_urls()
        
        logger.info(f"初始化完成")
    
    def _init_mongodb(self) -> None:
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            self.collection = self.db[self.output_collection]
            self.progress_collection = self.db[self.log_collection]
            
            # 创建索引
            self.collection.create_index('job_id', unique=True)
            self.collection.create_index('_job_type.code')
            self.collection.create_index('_city.code')
            self.collection.create_index('_industry.code')
            self.collection.create_index('_crawl_time')
            
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise

    def _init_browser(self) -> None:
        """初始化浏览器"""
        try:
            self.playwright = sync_playwright().start()
            
            # 浏览器启动参数
            browser_args = [
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--window-size=1024,768',
                '--start-maximized',
                '--disable-notifications',
                '--disable-popup-blocking',
                '--disable-extensions',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials'
            ]
            
            # 启动浏览器
            self.browser = self.playwright.chromium.launch(
                headless=False,  # 有头模式，方便调试
                args=browser_args
            )
            
            # 创建上下文，增加常见请求头
            self.context = self.browser.new_context(
                viewport={'width': 1024, 'height': 768},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                locale='zh-CN',
                timezone_id='Asia/Shanghai',
                geolocation={'latitude': 39.9042, 'longitude': 116.4074},  # 北京坐标
                permissions=['geolocation'],
                color_scheme='light',
                device_scale_factor=1,
                is_mobile=False,
                has_touch=False,
                java_script_enabled=True,
                ignore_https_errors=True,
                extra_http_headers={
                    "accept": "application/json, text/plain, */*",
                    "accept-language": "zh-CN,zh;q=0.9",
                    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "x-client-type": "web",
                    "x-requested-with": "XMLHttpRequest"
                }
            )
            
            # 创建新页面
            self.page = self.context.new_page()
            
            # 注入反检测脚本
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh']});
                window.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
                Object.defineProperty(navigator, 'userAgent', {get: () => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'});
            """)
            
            # 设置页面超时
            self.page.set_default_timeout(30000)
            self.page.set_default_navigation_timeout(30000)
            
            logger.info("浏览器初始化成功")
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}")
            raise

    def _load_crawled_urls(self) -> None:
        """从MongoDB加载已爬取的URL到内存中"""
        try:
            cursor = self.progress_collection.find({}, {
                "url": 1,
                "status": 1,
                "job_count": 1
            })
            
            for doc in cursor:
                self.crawled_urls[doc['url']] = 1
            
            logger.info(f"已加载 {len(self.crawled_urls)} 个已爬取的URL")
        except Exception as e:
            logger.error(f"加载已爬取URL失败: {str(e)}")

    def _parse_job_card(self, card) -> Optional[Dict]:
        """解析单个职位卡片
        
        Args:
            card: 职位卡片元素
            
        Returns:
            解析后的职位信息字典，解析失败返回None
        """
        try:
            return {
                'job_id': card.get_attribute('data-job-id'),
                'title': card.query_selector(".job-title").inner_text().strip(),
                'company': card.query_selector(".company-name").inner_text().strip(),
                'salary': card.query_selector(".job-salary").inner_text().strip(),
                'location': card.query_selector(".job-area").inner_text().strip(),
                'education': card.query_selector(".job-education").inner_text().strip(),
                'experience': card.query_selector(".job-experience").inner_text().strip(),
                'company_type': card.query_selector(".company-type").inner_text().strip(),
                'company_size': card.query_selector(".company-size").inner_text().strip(),
                'create_time': datetime.now()
            }
        except Exception as e:
            logger.warning(f"解析职位卡片失败: {str(e)}")
            return None

    def _normalize_url(self, url: str) -> str:
        """标准化URL，处理编码问题
        
        Args:
            url: 原始URL
            
        Returns:
            标准化后的URL
        """
        try:
            # 解析URL
            parsed = urlparse(url)
            # 解码查询参数
            query_params = parse_qs(parsed.query)
            # 重新构建查询字符串
            normalized_query = '&'.join(f"{k}={v[0]}" for k, v in sorted(query_params.items()))
            # 重新组合URL
            normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{normalized_query}"
            return normalized_url
        except Exception as e:
            logger.error(f"URL标准化失败: {str(e)}, URL: {url}")
            return url

    def _get_job_list(self, url: str) -> Optional[List[Dict]]:
        """获取职位列表数据
        
        Args:
            url: 要访问的URL
            
        Returns:
            职位列表数据，获取失败返回None
        """
        try:
            # 设置必要的cookie
            cookies = [
                {
                    "name": "XSRF-TOKEN",
                    "value": "ArB1SMFrRZO18mxbOOdPOQ",
                    "domain": ".liepin.com",
                    "path": "/"
                },
                {
                    "name": "__gc_id",
                    "value": "3dad4c755de14778bdf9438f7a067a0e",
                    "domain": ".liepin.com",
                    "path": "/"
                },
                {
                    "name": "__uuid",
                    "value": "1748395987113.72",
                    "domain": ".liepin.com",
                    "path": "/"
                }
            ]
            self.context.add_cookies(cookies)
            
            # 创建响应监听器
            response_data = None
            def handle_response(response):
                nonlocal response_data
                if ("api-c.liepin.com/api/com.liepin.searchfront4c.pc-search-job" in response.url 
                    and response.status == 200):
                    try:
                        response_data = response.json()
                    except json.JSONDecodeError as e:
                        logger.error(f"解析API响应JSON失败: {str(e)}, URL: {response.url}")
                    except Exception as e:
                        logger.error(f"处理API响应时发生未知错误: {str(e)}, URL: {response.url}")

            # 添加响应监听器
            self.page.on("response", handle_response)
            
            try:
                # 访问目标页面
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        # 先尝试等待页面加载
                        response = self.page.goto(url, wait_until='domcontentloaded', timeout=60000)  # 增加超时时间到60秒
                        
                        # 检查响应状态
                        if response and response.status == 200:
                            # 等待页面加载完成，但使用更短的超时时间
                            try:
                                # 先等待页面基本元素加载
                                self.page.wait_for_selector('body', timeout=30000)
                                # 再等待网络请求完成
                                self.page.wait_for_load_state('networkidle', timeout=30000)
                            except TimeoutError as te:
                                # 如果networkidle超时，但页面基本内容已加载，继续执行
                                logger.warning(f"等待页面加载超时，但继续执行: {str(te)}, URL: {url}")
                            break
                        else:
                            logger.warning(f"页面响应状态码异常: {response.status if response else 'None'}, URL: {url}")
                            retry_count += 1
                            if retry_count == max_retries:
                                logger.error(f"页面加载失败(已重试{max_retries}次): {url}")
                                return None
                            time.sleep(10)  # 增加重试间隔到10秒
                            
                    except TimeoutError as te:
                        retry_count += 1
                        if retry_count == max_retries:
                            logger.error(f"页面加载超时(已重试{max_retries}次): {str(te)}, URL: {url}")
                            return None
                        logger.warning(f"页面加载超时,正在进行第{retry_count}次重试: {str(te)}, URL: {url}")
                        time.sleep(10)  # 增加重试间隔到10秒
                    except Exception as e:
                        logger.error(f"页面加载出错: {str(e)}, URL: {url}")
                        retry_count += 1
                        if retry_count == max_retries:
                            return None
                        time.sleep(10)
                        continue
                
                # 检查URL是否被重定向
                final_url = self.page.url
                normalized_original_url = self._normalize_url(url)
                normalized_final_url = self._normalize_url(final_url)
                
                if normalized_original_url != normalized_final_url:
                    logger.error(f"URL被重定向，可能被ban。原始URL: {url}, 重定向到: {final_url}")
                    return None
                
                # 模拟人类行为
                self._simulate_human_behavior()
                
                # 等待API响应
                time.sleep(2)  # 给API请求一些时间
                
                # 检查响应数据
                if response_data and 'pagination' in response_data['data']:                    
                    pagination_data = response_data['data'].get('pagination', {})
                    if pagination_data.get('totalCounts')>0:
                        job_list = response_data['data'].get('data', {}).get('jobCardList', [])
                        jobs = []
                        for job in job_list:
                            # 基础字段
                            job_info = {
                                # 基础信息
                                # '_id': job.get('job', {}).get('jobId'),  # 使用jobId作为主键
                                # 'create_time': datetime.now(),
                                # 'update_time': datetime.now(),
                                # 'source': 'liepin',                                
                                
                                # 公司信息
                                'company_id': job.get('comp', {}).get('compId'),
                                'company_name': job.get('comp', {}).get('compName', '').strip(),
                                'company_scale': job.get('comp', {}).get('compScale', '').strip(),
                                'company_stage': job.get('comp', {}).get('compStage', '').strip(),
                                'company_logo': job.get('comp', {}).get('compLogo', '').strip(),
                                'company_link': job.get('comp', {}).get('link', '').strip(),
                                'company_industry': job.get('comp', {}).get('compIndustry', '').strip(),
                                
                                # 职位信息
                                'job_id': job.get('job', {}).get('jobId', '').strip(),
                                'job_title': job.get('job', {}).get('title', '').strip(),
                                'job_salary': job.get('job', {}).get('salary', '').strip(),
                                'job_location': job.get('job', {}).get('dq', '').strip(),
                                'job_experience': job.get('job', {}).get('requireWorkYears', '').strip(),
                                'job_education': job.get('job', {}).get('requireEduLevel', '').strip(),
                                'job_kind': job.get('job', {}).get('jobKind', '').strip(),
                                'job_link': job.get('job', {}).get('link', '').strip(),
                                'job_refresh_time': job.get('job', {}).get('refreshTime', '').strip(),
                                'job_is_top': job.get('job', {}).get('topJob', False),
                                'job_labels': job.get('job', {}).get('labels', []),
                                'job_h5_outer_link': job.get('job', {}).get('h5OuterLink', '').strip(),
                                'job_pc_outer_link': job.get('job', {}).get('pcOuterLink', '').strip(),
                                'job_adv_view_flag': job.get('job', {}).get('advViewFlag', False),
                                'job_data_prom_id': job.get('job', {}).get('dataPromId', '').strip(),
                                
                                # 招聘者信息
                                'recruiter_id': job.get('recruiter', {}).get('recruiterId', '').strip(),
                                'recruiter_name': job.get('recruiter', {}).get('recruiterName', '').strip(),
                                'recruiter_title': job.get('recruiter', {}).get('recruiterTitle', '').strip(),
                                'recruiter_photo': job.get('recruiter', {}).get('recruiterPhoto', '').strip(),
                                'recruiter_im_id': job.get('recruiter', {}).get('imId', '').strip(),
                                'recruiter_im_status': job.get('recruiter', {}).get('imStatus', False),
                                'recruiter_im_show_text': job.get('recruiter', {}).get('imShowText', '').strip(),
                                'recruiter_im_user_type': job.get('recruiter', {}).get('imUserType', '').strip(),
                                'recruiter_chatted': job.get('recruiter', {}).get('chatted', False),
                                'recruiter_in_day': job.get('recruiter', {}).get('inDay', False),
                                
                                # 原始数据
                                # 'raw_data_info': job.get('dataInfo', '').strip(),
                                # 'raw_data_params': job.get('dataParams', '').strip(),
                                
                                # 元数据                            
                                # 'crawl_time': datetime.now(),                            
                            }
                            
                            jobs.append(job_info)
                        return (jobs,pagination_data)
                    else:
                        logger.warning(f"未获取到职位列表数据，URL: {url}")
                        return ([],pagination_data)
                
                # 检查是否被限制访问
                if response_data and 'code' in response_data and response_data['code'] != 0:
                    logger.error(f"API返回错误码: {response_data['code']}, 可能被ban")
                    return None
                
                logger.warning(f"未获取到职位列表数据，URL: {url}")
                return None
                
            finally:
                # 移除响应监听器
                self.page.remove_listener("response", handle_response)
                
        except Exception as e:
            logger.error(f"获取职位列表失败: {str(e)}")
            return None

    def _save_jobs(self, jobs: List[Dict], url_data: Dict) -> None:
        """保存职位数据到MongoDB
        
        Args:
            jobs: 职位列表数据
            url_data: URL相关信息
        """
        try:
            if not jobs:
                return
                
            # 准备批量操作
            operations = []
            current_time = datetime.now()
            
            for job in jobs:
                # 更新时间相关字段
                job.update({
                    'create_time': current_time,
                    'update_time': current_time,
                    'crawl_time': current_time
                })
                
                # 创建更新操作
                operation = UpdateOne(
                    {'job_id': job['job_id']},  # 查询条件
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

    def _save_url_log(self, url: str, status: str, pagination_data: Dict = None) -> None:
        """保存URL访问日志
        
        Args:
            url: 访问的URL
            status: 访问状态
            pagination_data: 分页信息
        """
        try:
            log_data = {
                "url": url['url'],
                "industry_parent_code": url['industry_parent_code'],
                "industry_parent_name": url['industry_parent_name'],
                "industry_child_code": url['industry_child_code'],
                "industry_child_name": url['industry_child_name'],
                "job_industry": url["job_industry"],
                "job_category": url["job_category"],
                "job_type_name": url["job_type_name"],
                "province_code": url["province_code"],
                "province_name": url["province_name"],                
                'status': status,
                'create_time': datetime.now(),
                'uploader': '单永旭'
            }
            
            # 添加分页信息
            if pagination_data:
                log_data.update({
                    'total_count': pagination_data.get('totalCounts', 0),
                    'current_page': pagination_data.get('currentPage', 0),
                    'page_size': pagination_data.get('pageSize', 0),
                    'total_pages': pagination_data.get('totalPage', 0),
                    'has_next': pagination_data.get('hasNext', False)
                })
            
            self.progress_collection.insert_one(log_data)
            
            # 更新内存中的缓存
            self.crawled_urls[url['url']] = 1
        except Exception as e:
            logger.error(f"保存URL访问日志失败: {str(e)}")

    def close(self) -> None:
        """关闭所有连接"""
        if self.mongo_client:
            try:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")
            except Exception as e:
                logger.error(f"关闭MongoDB连接失败: {str(e)}")
        
        if self.browser:
            try:
                self.browser.close()
                logger.info("浏览器已关闭")
            except Exception as e:
                logger.error(f"关闭浏览器失败: {str(e)}")
        
        if self.playwright:
            try:
                self.playwright.stop()
                logger.info("Playwright已关闭")
            except Exception as e:
                logger.error(f"关闭Playwright失败: {str(e)}")

    def run(self) -> None:
        """运行爬虫"""
        try:
            # 获取URL列表
            urls = list(self.db[self.input_collection].find({}, {'_id': 0,'create_time': 0}))
            total_urls = len(urls)
            logger.info(f"获取到 {total_urls} 个URL")
            
            # 创建进度条
            pbar = tqdm(total=total_urls, 
                       desc="总体进度", 
                       unit="URL",
                       ncols=100,
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
                       position=0,  # 固定位置
                       leave=True)  # 保留进度条
            
            # 处理每个URL
            for url_data in urls:
                url = url_data['url']
                try:
                    # 更新进度条描述
                    current_desc = f"正在处理: {url_data['job_type_name']}-{url_data['province_code']}-{url_data['industry_parent_code']}-{url_data['industry_child_code']}"
                    pbar.set_description(current_desc)
                    logger.info(f"开始处理URL: {current_desc}")
                    
                    # 检查是否已爬取
                    if url in self.crawled_urls:
                        logger.info(f"跳过已爬取的URL: {url}")
                        pbar.update(1)
                        continue
                    
                    # 获取职位列表
                    logger.info(f"开始获取职位列表: {url}")
                    res_data = self._get_job_list(url)
                    
                    # 处理返回数据
                    if res_data:
                        jobs, pagination_data = res_data
                        # 保存职位数据
                        if jobs:  # 只有在有职位数据时才保存
                            logger.info(f"获取到 {len(jobs)} 个职位数据")
                            self._save_jobs(jobs, url_data)
                        else:
                            logger.info("未获取到职位数据")
                            
                        # 记录URL访问日志（无论是否有职位数据）
                        self._save_url_log(
                            url=url_data,
                            status='success',
                            pagination_data=pagination_data
                        )
                        logger.info(f"URL处理完成: {url}")
                    else:
                        # 记录正常的URL访问失败（没有数据）
                        logger.warning(f"URL访问失败: {url}")
                        # self._save_url_log(
                        #     url=url_data,
                        #     status='failed'
                        # )
                    
                except Exception as e:
                    # 异常情况只记录错误日志，不记录URL访问日志
                    logger.error(f"处理URL失败: {url}, 错误: {str(e)}")
                    # 继续处理下一个URL
                    continue
                
                # 更新进度条
                pbar.update(1)
                
                # 随机等待
                wait_time = random.uniform(1, 2)
                logger.debug(f"等待 {wait_time:.2f} 秒")
                time.sleep(wait_time)
            
            # 关闭进度条
            pbar.close()
            logger.info("所有URL处理完成")
            
        except Exception as e:
            logger.error(f"运行出错: {str(e)}")
            raise
        finally:
            self.close()

    def _simulate_human_behavior(self) -> None:
        """模拟人类行为，包括随机滚动、鼠标移动和点击"""
        try:
            # 随机滚动
            for _ in range(random.randint(2, 4)):
                # 随机滚动距离
                scroll_distance = random.randint(100, 500)
                # 随机滚动方向（上下）
                direction = random.choice([-1, 1])
                self.page.mouse.wheel(0, scroll_distance * direction)
                # 随机等待
                time.sleep(random.uniform(0.2, 0.5))
            
            # 随机移动鼠标
            for _ in range(random.randint(2, 4)):
                # 随机位置
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                # 移动鼠标
                self.page.mouse.move(x, y)
                # 随机等待
                time.sleep(random.uniform(0.2, 0.5))
                               
            # 随机等待一段时间
            time.sleep(random.uniform(0.5, 1.5))
            
        except Exception as e:
            logger.warning(f"模拟人类行为时出错: {str(e)}")
            # 出错时简单等待
            time.sleep(random.uniform(0.5, 1.0))

def main():
    """主函数"""
    try:                
        # 创建爬虫实例
        spider = LiepinSpiderStep4()
        # 运行爬虫
        spider.run()
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()

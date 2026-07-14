#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
猎聘网爬虫 - 第六步
功能：处理liepin_step3_urls_part1集合中的URL，获取职位详情数据

主要步骤：
1. 从MongoDB读取liepin_step3_urls_part1集合的URL数据
2. 使用Playwright获取每个URL的职位详情
3. 将职位详情数据保存到MongoDB

数据存储：
- 输入集合：liepin_step3_urls_part1
- 输出集合：liepin_job_detail_part1
- 进度记录集合：liepin_step3_urls_202504_log_part1

请求配置：
- 请求方法：GET
- 请求头：包含必要的认证和浏览器信息
- 请求参数：无

数据过滤规则：
1. 记录请求时间
2. 记录响应状态
3. 记录原始响应数据
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
import uuid
import hashlib

# 将项目根目录添加到Python路径中
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent  # 从当前文件向上找三层到项目根目录
sys.path.append(str(project_root))

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "liepin_spider_step6")
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class LiepinSpiderStep6:
    """猎聘网爬虫 - 第六步"""
    
    def __init__(self):
        """初始化爬虫"""
        
        # MongoDB配置
        self.mongo_uri = "mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test"
        self.mongo_db = "da_test"
        self.mongo_client = None
        self.db = None
        self.collection = None
        self.progress_collection = None
        
        # 输入输出集合名称
        self.input_collection = 'liepin_step3_urls_part1'
        self.output_collection = 'liepin_job_detail_part1'
        self.log_collection = 'liepin_step3_urls_202504_log_part1'
        
        # 爬虫配置
        self.max_retries = 3
        self.retry_delay = 2
        self.request_delay = (3, 8)  # 随机延迟范围（秒），更符合人类行为
        
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
            
            # 设置索引
            self._setup_indexes()
            
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise

    def _setup_indexes(self) -> None:
        """设置MongoDB索引"""
        try:
            # 删除可能存在的job_id唯一索引（如果存在）
            try:
                self.collection.drop_index("job_id_1")
                logger.info("已删除旧的job_id唯一索引")
            except Exception:
                pass  # 索引不存在，忽略错误
            
            # 创建detail_url唯一索引
            self.collection.create_index("detail_url", unique=True)
            logger.info("已创建detail_url唯一索引")
            
            # 创建其他有用的索引
            self.collection.create_index("crawl_time")
            self.collection.create_index("status_code")
            self.collection.create_index("data_type")
            
            # 为日志集合创建索引
            self.progress_collection.create_index("detail_url")
            self.progress_collection.create_index("create_time")
            self.progress_collection.create_index("status")
            
            logger.info("MongoDB索引设置完成")
        except Exception as e:
            logger.error(f"设置MongoDB索引失败: {str(e)}")
            raise

    def _init_browser(self) -> None:
        """初始化浏览器 - 使用liepin_step4的配置"""
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
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "accept-encoding": "gzip, deflate, br, zstd",
                    "accept-language": "zh-CN,zh;q=0.9",
                    "cache-control": "max-age=0",
                    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1"
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
                "detail_url": 1,
                "status": 1
            })
            
            for doc in cursor:
                self.crawled_urls[doc['detail_url']] = 1
            
            logger.info(f"已加载 {len(self.crawled_urls)} 个已爬取的URL")
        except Exception as e:
            logger.error(f"加载已爬取URL失败: {str(e)}")

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

    def _get_job_detail(self, url: str, original_doc: Dict = None) -> Optional[Dict]:
        """获取职位详情数据
        
        Args:
            url: 要访问的URL
            original_doc: 原始文档数据，包含job_data_prom_id等信息
            
        Returns:
            职位详情数据，获取失败返回None
        """
        try:
            # 设置必要的cookie
            # cookies = [
            #     {
            #         "name": "__gc_id",
            #         "value": "3dad4c755de14778bdf9438f7a067a0e",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "__uuid",
            #         "value": "1748395987113.72",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "_ga",
            #         "value": "GA1.1.1769692972.1748395992",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "need_bind_tel",
            #         "value": "false",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "new_user",
            #         "value": "false",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "city_site",
            #         "value": "bj",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "user_roles",
            #         "value": "0",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "XSRF-TOKEN",
            #         "value": "JSxIrBe9QYmvdwd2R8IbMw",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "fe_se",
            #         "value": "-1750319814661",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "imApp_0",
            #         "value": "1",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "hpo_role-sec_project",
            #         "value": "sec_project_liepin",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "hpo_sec_tenant",
            #         "value": "0",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "HMACCOUNT",
            #         "value": "55B60FA1F020E7A1",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "access_system",
            #         "value": "C",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "__tlog",
            #         "value": "1750319814961.87%7C00000000%7C00000000%7Cs_o_009%7Cs_o_009",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "user_photo",
            #         "value": "5f8fa3a78dbe6273dcf85e2608u.png",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "user_name",
            #         "value": "%E5%8D%95%E6%B0%B8%E6%97%AD",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "c_flag",
            #         "value": "ec676dec31441fe291bee4461c62e98b",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "inited_user",
            #         "value": "d839c522a8be4432d8e08f02c3d60204",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "imId",
            #         "value": "49c1c923fe7c3a7a437681048d3c1212",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "imId_0",
            #         "value": "49c1c923fe7c3a7a437681048d3c1212",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "imClientId",
            #         "value": "49c1c923fe7c3a7aba1d6f1e55c3bc79",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "imClientId_0",
            #         "value": "49c1c923fe7c3a7aba1d6f1e55c3bc79",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "UniqueKey",
            #         "value": "57a41b2e81511df91a667e00ad0d9493",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "liepin_login_valid",
            #         "value": "0",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "lt_auth",
            #         "value": "vu8OMnBTx1qo4COKi2Ja5q9Mj42tVmXJ%2FShehBkG19ToCfGw4P3gQgOErbMBxAMhxEx0dMULNrX%2BMer%2FyHZJ6koXwG2uiZu2o%2Fyk0HgIdvRcN8W2vfj%2BkszYe58clUAB8mNbp34i",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "fe_im_connectJson_0",
            #         "value": "%7B%220_57a41b2e81511df91a667e00ad0d9493%22%3A%7B%22socketConnect%22%3A%221%22%2C%22connectDomain%22%3A%22liepin.com%22%7D%7D",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "__session_seq",
            #         "value": "305",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "fe_im_socketSequence_new_0",
            #         "value": "99_99_98",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "__tlg_event_seq",
            #         "value": "1064",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     },
            #     {
            #         "name": "fe_im_opened_pages",
            #         "value": "_1750419514122_1750419534023_1750417867406_1750421078965_1750421169262",
            #         "domain": ".liepin.com",
            #         "path": "/"
            #     }
            # ]
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
            
            # 构造完整的URL（包含所有参数）
            # full_url = self._construct_full_url(url, original_doc)
            full_url = url
            logger.info(f"构造完整URL: {full_url}")            
            try:
                # 访问目标页面
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        # 先尝试等待页面加载
                        response = self.page.goto(full_url, wait_until='domcontentloaded', timeout=60000)
                        
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
                                logger.warning(f"等待页面加载超时，但继续执行: {str(te)}, URL: {full_url}")
                            break
                        else:
                            logger.warning(f"页面响应状态码异常: {response.status if response else 'None'}, URL: {full_url}")
                            retry_count += 1
                            if retry_count == max_retries:
                                logger.error(f"页面加载失败(已重试{max_retries}次): {full_url}")
                                return None
                            time.sleep(10)
                            
                    except TimeoutError as te:
                        retry_count += 1
                        if retry_count == max_retries:
                            logger.error(f"页面加载超时(已重试{max_retries}次): {str(te)}, URL: {full_url}")
                            return None
                        logger.warning(f"页面加载超时,正在进行第{retry_count}次重试: {str(te)}, URL: {full_url}")
                        time.sleep(10)
                    except Exception as e:
                        logger.error(f"页面加载出错: {str(e)}, URL: {full_url}")
                        retry_count += 1
                        if retry_count == max_retries:
                            return None
                        time.sleep(10)
                        continue
                
                # 检查URL是否被重定向
                final_url = self.page.url
                normalized_original_url = self._normalize_url(full_url)
                normalized_final_url = self._normalize_url(final_url)
                
                if normalized_original_url != normalized_final_url:
                    logger.error(f"URL被重定向，可能被ban。原始URL: {full_url}, 重定向到: {final_url}")
                    return None
                
                # 模拟人类行为
                self._simulate_human_behavior()
                
                # 获取页面标题
                page_title = self.page.title()
                
                # 获取当前URL（可能经过重定向）
                current_url = self.page.url
                
                # 获取特定有用的HTML部分
                useful_html_parts = self._extract_useful_html_parts()
                page_title = self.page.title()

                # 判断5个字段都为空且page_title为空
                core_fields = [
                    'job_apply_container',
                    'recruiter_container',
                    'job_intro_container',
                    'company_intro_container',
                    'job_apply_container_desc'
                ]
                if all(not useful_html_parts.get(field, '').strip() for field in core_fields) and not page_title.strip():
                    logger.error("页面核心内容全部为空，且标题也为空，可能需要重新登录或已被ban，程序即将退出。")
                    import sys
                    sys.exit(1)
                
                # 检查是否被要求登录
                if "登录" in page_title or "login" in page_title.lower() or "请登录" in page_title:
                    logger.error("检测到需要登录，程序即将退出。")
                    import sys
                    sys.exit(1)
                
                logger.info(f"成功获取页面有用部分，总长度: {sum(len(part) for part in useful_html_parts.values())} 字符")
                
                return {
                    'status_code': 200,
                    'url': current_url,
                    'title': page_title,
                    'useful_html_parts': useful_html_parts,
                    'data_type': 'useful_html_parts'
                }
                
            except Exception as e:
                logger.error(f"获取页面内容失败: {str(e)}, URL: {full_url}")
                return None
                
        except Exception as e:
            logger.error(f"获取职位详情失败: {str(e)}")
            return None

    def _construct_full_url(self, base_url: str, original_doc: Dict) -> str:
        """构造完整的URL，包含所有必要的参数
        
        Args:
            base_url: 基础URL
            original_doc: 原始文档数据
            
        Returns:
            完整的URL
        """
        try:
            # 从原始文档中获取job_data_prom_id
            job_data_prom_id = original_doc.get('job_data_prom_id', '')
            job_id = original_doc.get('job_id', '')
            
            if not job_data_prom_id:
                logger.warning(f"未找到job_data_prom_id，使用原始URL: {base_url}")
                return base_url
            
            # 解析job_data_prom_id中的参数
            # 示例: "d_sfrom=search_prime&d_ckId=null&d_curPage=0&d_pageSize=40&d_headId=null&d_posi=2&skId=vw42luhjkqd98ylpm5icii1665a4trs9&fkId=vw42luhjkqd98ylpm5icii1665a4trs9&ckId=vw42luhjkqd98ylpm5icii1665a4trs9&sfrom=search_job_pc&curPage=0&pageSize=40&index=2"
            params = {}
            
            # 解析参数字符串
            param_pairs = job_data_prom_id.split('&')
            for pair in param_pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    params[key] = value
            
            # 构造pgRef参数（基于job_id和skId）
            # sk_id = params.get('skId', '')
            # if sk_id and job_id:
            #     # 根据真实案例构造pgRef格式: c_pc_search_page:c_pc_search_job_listcard@2_9970653:1:cc6ba9ea-9917-4e67-b266-cff8be81460a
            #     # job_id前面需要加上数字2，后面是固定值1，最后是完整的UUID
            #     # 从skId中提取前8位作为UUID的一部分，然后生成完整的UUID
            #     sk_id_prefix = sk_id[:8] if len(sk_id) >= 8 else sk_id
            #     # 生成一个基于skId前缀的UUID，确保一致性
            #     hash_obj = hashlib.md5(sk_id_prefix.encode())
            #     uuid_hex = hash_obj.hexdigest()
            #     # 构造标准UUID格式：8-4-4-4-12
            #     uuid_part = f"{uuid_hex[:8]}-{uuid_hex[8:12]}-{uuid_hex[12:16]}-{uuid_hex[16:20]}-{uuid_hex[20:32]}"
            pg_ref = f"c_pc_search_page:c_pc_search_job_listcard@2_{job_id}:1:cc6ba9ea-9917-4e67-b266-cff8be81460a"
            params['pgRef'] = pg_ref
            
            # 构造完整的URL
            if params:
                param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
                full_url = f"{base_url}?{param_string}"
                return full_url
            else:
                return base_url
                
        except Exception as e:
            logger.error(f"构造完整URL失败: {str(e)}")
            return base_url

    def _extract_useful_html_parts(self) -> Dict[str, str]:
        """提取页面中有用的HTML部分
        
        支持两种页面结构：
        1. 正常职位页面：包含完整的职位信息
        2. 下线职位页面：职位已下线，但仍有基本信息
        
        Returns:
            包含有用HTML部分的字典，如果部分不存在则返回空字符串
        """
        useful_parts = {}
        
        try:
            # 1. 职位应聘卡片 - 支持正常职位和下线职位两种结构
            job_apply_container = self.page.query_selector('section.job-apply-container')
            if job_apply_container:
                useful_parts['job_apply_container'] = job_apply_container.inner_html()
                logger.debug("成功提取职位应聘卡片（正常职位）")
            else:
                # 尝试获取下线职位的结构
                stop_job_apply_container = self.page.query_selector('section.stop-job-apply-container')
                if stop_job_apply_container:
                    useful_parts['job_apply_container'] = stop_job_apply_container.inner_html()
                    logger.debug("成功提取职位应聘卡片（下线职位）")
                else:
                    useful_parts['job_apply_container'] = ''
                    logger.debug("职位应聘卡片不存在")
            
            # 2. HR信息
            recruiter_container = self.page.query_selector('section.recruiter-container')
            if recruiter_container:
                useful_parts['recruiter_container'] = recruiter_container.inner_html()
                logger.debug("成功提取HR信息")
            else:
                useful_parts['recruiter_container'] = ''
                logger.debug("HR信息不存在")
            
            # 3. 职位介绍 - 支持正常职位和下线职位两种结构
            job_intro_container = self.page.query_selector('section.job-intro-container')
            if job_intro_container:
                useful_parts['job_intro_container'] = job_intro_container.inner_html()
                logger.debug("成功提取职位介绍")
            else:
                useful_parts['job_intro_container'] = ''
                logger.debug("职位介绍不存在")
            
            # 4. 公司介绍
            company_intro_container = self.page.query_selector('section.company-intro-container')
            if company_intro_container:
                useful_parts['company_intro_container'] = company_intro_container.inner_html()
                logger.debug("成功提取公司介绍")
            else:
                useful_parts['company_intro_container'] = ''
                logger.debug("公司介绍不存在")
            
            # 5. 职位应聘卡片描述部分 - 对于下线职位，包含操作区域和内容盒子
            job_apply_container_desc = self.page.query_selector('section.job-apply-container-desc')
            if job_apply_container_desc:
                useful_parts['job_apply_container_desc'] = job_apply_container_desc.inner_html()
                logger.debug("成功提取职位应聘卡片描述（正常职位）")
            else:
                # 对于下线职位，将操作区域和内容盒子合并到描述字段中
                desc_parts = []
                
                # 获取职位详情操作区域
                job_detail_operate = self.page.query_selector('div.job-detail-operate')
                if job_detail_operate:
                    desc_parts.append(job_detail_operate.inner_html())
                    logger.debug("成功提取职位详情操作区域")
                
                # 获取职位详情内容盒子
                job_detail_content_box = self.page.query_selector('div.job-detail-content-box')
                if job_detail_content_box:
                    desc_parts.append(job_detail_content_box.inner_html())
                    logger.debug("成功提取职位详情内容盒子")
                
                if desc_parts:
                    useful_parts['job_apply_container_desc'] = '\n'.join(desc_parts)
                    logger.debug("成功提取职位应聘卡片描述（下线职位）")
                else:
                    useful_parts['job_apply_container_desc'] = ''
                    logger.debug("职位应聘卡片描述不存在")
            
            # 统计成功提取的部分数量
            successful_parts = sum(1 for content in useful_parts.values() if content.strip())
            logger.info(f"成功提取 {successful_parts}/{len(useful_parts)} 个有用的HTML部分")
            
        except Exception as e:
            logger.error(f"提取有用HTML部分失败: {str(e)}")
            logger.error(f"返回的数据不对，有可能需要重新登录一下，或者被ban了")
            # 如果提取失败，直接退出吧
            raise e
            # 如果提取失败，确保所有字段都有默认值
            useful_parts = {
                'job_apply_container': '',
                'recruiter_container': '',
                'job_intro_container': '',
                'company_intro_container': '',
                'job_apply_container_desc': ''
            }
        
        return useful_parts

    def _save_job_detail(self, url: str, response_data: Dict, original_doc: Dict) -> None:
        """保存职位详情数据到MongoDB
        
        Args:
            url: 访问的URL
            response_data: 响应数据
            original_doc: 原始文档数据
        """
        try:
            if not response_data:
                return
                
            current_time = datetime.now()
            
            # 获取有用的HTML部分
            useful_html_parts = response_data.get('useful_html_parts', {})
            
            # 构造职位详情文档
            detail_doc = {
                'detail_url': url,
                'crawl_time': current_time,
                'source': 'liepin',
                'status_code': response_data.get('status_code'),
                'page_title': response_data.get('title'),
                'final_url': response_data.get('url'),  # 可能经过重定向的最终URL
                'data_type': 'useful_html_parts',
                'collection_name': original_doc.get('collection_name'),
                'collection_id': original_doc.get('collection_id'),
            }
            
            # 添加各个有用的HTML部分（即使为空字符串也要保存）
            for part_name, html_content in useful_html_parts.items():
                detail_doc[f'html_{part_name}'] = html_content
                detail_doc[f'html_{part_name}_length'] = len(html_content)
                # 标记是否为空
                detail_doc[f'html_{part_name}_empty'] = not bool(html_content.strip())
            
            # 计算总长度（包括空字符串）
            total_length = sum(len(content) for content in useful_html_parts.values())
            detail_doc['total_html_length'] = total_length
            detail_doc['parts_count'] = len(useful_html_parts)
            
            # 计算非空部分的数量
            non_empty_parts = sum(1 for content in useful_html_parts.values() if content.strip())
            detail_doc['non_empty_parts_count'] = non_empty_parts
            
            # 创建更新操作
            operation = UpdateOne(
                {'detail_url': url},  # 查询条件 - 使用detail_url作为唯一标识
                {'$set': detail_doc},  # 更新数据
                upsert=True  # 如果不存在则插入
            )
            
            # 执行写入
            result = self.collection.bulk_write([operation], ordered=False)
            logger.info(f"职位详情数据保存成功 - 插入: {result.upserted_count}, 修改: {result.modified_count}, 非空部分: {non_empty_parts}/{len(useful_html_parts)}")
                
        except BulkWriteError as bwe:
            logger.error(f"批量写入出错: {str(bwe.details)}")
        except Exception as e:
            logger.error(f"保存职位详情数据到MongoDB失败: {str(e)}")

    def _save_url_log(self, url_doc: Dict, status: str, response_data: Dict = None) -> None:
        """保存URL访问日志
        
        Args:
            url: 访问的URL
            status: 访问状态
            response_data: 响应数据
        """
        try:
            log_data = {
                "detail_url": url_doc.get('detail_url'),
                "collection_name": url_doc.get('collection_name'),
                "collection_id": url_doc.get('collection_id'),
                'status': status,
                'create_time': datetime.now(),
                'uploader': '单永旭'
            }
            
            # 添加响应信息
            if response_data:
                useful_html_parts = response_data.get('useful_html_parts', {})
                total_length = sum(len(content) for content in useful_html_parts.values())
                non_empty_parts = sum(1 for content in useful_html_parts.values() if content.strip())
                
                log_data.update({
                    'status_code': response_data.get('status_code'),
                    'page_title': response_data.get('title'),
                    'total_html_length': total_length,
                    'parts_count': len(useful_html_parts),
                    'non_empty_parts_count': non_empty_parts,
                    'data_type': 'useful_html_parts'
                })
            
            self.progress_collection.insert_one(log_data)
            
            # 更新内存中的缓存
            self.crawled_urls[url_doc.get('detail_url')] = 1
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
            urls = list(self.db[self.input_collection].find({}, {'_id': 0}))
            total_urls = len(urls)
            logger.info(f"获取到 {total_urls} 个URL")
            
            # 创建进度条
            pbar = tqdm(total=total_urls, 
                       desc="总体进度", 
                       unit="URL",
                       ncols=100,
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
                       position=0,
                       leave=True)
            
            # 处理每个URL
            for url_doc in urls:
                url = url_doc.get('detail_url')
                if not url:
                    logger.warning(f"跳过无效URL: {url_doc}")
                    pbar.update(1)
                    continue
                    
                try:
                    # 更新进度条描述
                    current_desc = f"正在处理: {url[:50]}..."
                    pbar.set_description(current_desc)
                    logger.info(f"开始处理URL: {url}")
                    
                    # 检查是否已爬取
                    if url in self.crawled_urls:
                        logger.info(f"跳过已爬取的URL: {url}")
                        pbar.update(1)
                        continue
                            
                    # 获取职位详情
                    logger.info(f"开始获取职位详情: {url}")
                    response_data = self._get_job_detail(url, url_doc)
                    
                    # 处理返回数据
                    if response_data:
                        # 保存职位详情数据
                        logger.info(f"获取到职位详情数据")
                        self._save_job_detail(url, response_data, url_doc)
                        
                        # 记录URL访问日志
                        self._save_url_log(
                            url_doc=url_doc,
                            status='success',
                            response_data=response_data
                        )
                        logger.info(f"URL处理完成: {url}")
                    else:
                        # 记录URL访问失败
                        logger.warning(f"URL访问失败: {url}")
                        self._save_url_log(
                            url_doc=url_doc,
                            status='failed'
                        )
                    
                except SystemExit:
                    # SystemExit是正常的程序退出，不是异常
                    logger.info("检测到需要重新登录或被ban，程序正常退出")
                    return
                except Exception as e:
                    # 异常情况记录错误日志
                    logger.error(f"处理URL失败: {url}, 错误: {str(e)}")
                    self._save_url_log(
                        url_doc=url_doc,
                        status='error'
                    )
                    continue
                
                # 更新进度条
                pbar.update(1)
                
                # 随机等待
                wait_time = random.uniform(*self.request_delay)
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
            # 获取页面尺寸
            page_size = self.page.viewport_size
            if not page_size:
                page_size = {'width': 1024, 'height': 768}
            
            # 随机滚动（更真实的滚动行为）
            for _ in range(random.randint(1, 3)):
                # 随机滚动距离（更小的距离，更真实）
                scroll_distance = random.randint(50, 300)
                # 随机滚动方向（上下）
                direction = random.choice([-1, 1])
                self.page.mouse.wheel(0, scroll_distance * direction)
                # 随机等待（更短的等待时间）
                time.sleep(random.uniform(0.1, 0.3))
            
            # 随机移动鼠标（更真实的移动轨迹）
            for _ in range(random.randint(1, 2)):
                # 随机位置（避免边缘区域）
                x = random.randint(100, page_size['width'] - 100)
                y = random.randint(100, page_size['height'] - 100)
                # 移动鼠标
                self.page.mouse.move(x, y)
                # 随机等待
                time.sleep(random.uniform(0.1, 0.2))                        
                               
            # 随机等待一段时间（更真实的等待时间）
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            logger.warning(f"模拟人类行为时出错: {str(e)}")
            # 出错时简单等待
            time.sleep(random.uniform(0.5, 1.0))

def main():
    """主函数"""
    try:                
        # 创建爬虫实例
        spider = LiepinSpiderStep6()
        # 运行爬虫
        spider.run()
    except SystemExit:
        # SystemExit是正常的程序退出，不是异常
        logger.info("程序正常退出")
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()

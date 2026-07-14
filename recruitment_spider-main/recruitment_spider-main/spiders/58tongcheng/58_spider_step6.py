#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
58同城职位详情爬虫 - 优化版本，解决distinct限制问题
增加对目标集合中已有数据的检查
"""

import re
import time
import random
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pymongo import MongoClient, errors
from pymongo.collection import Collection
from pymongo.database import Database
from playwright.sync_api import sync_playwright, Page, BrowserContext, TimeoutError as PlaywrightTimeoutError
from bson import ObjectId

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class JobDetailCrawler:
    def __init__(self, headless: bool = True) -> None:
        """初始化爬虫"""
        self.headless = headless
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        
        # MongoDB连接配置
        self.mongo_uri = "mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test"
        self.source_collection_name = "58_step3_urls_part3"
        self.log_collection_name = "58_step3_urls_202507_log_part3"
        self.target_collection_name = "58_job_detail_part3"
        
        # 初始化MongoDB连接
        self.client = self._get_mongo_client()
        self.db = self.client.get_database()
        self.source_collection = self.db[self.source_collection_name]
        self.log_collection = self.db[self.log_collection_name]
        self.target_collection = self.db[self.target_collection_name]
        
        # 确保集合存在
        self._ensure_collections_exist()
    
    def _get_mongo_client(self) -> MongoClient:
        """创建MongoDB客户端连接"""
        try:
            client = MongoClient(
                self.mongo_uri,
                serverSelectionTimeoutMS=3000,
                socketTimeoutMS=30000,
                connectTimeoutMS=3000
            )
            client.admin.command('ping')
            logger.info("成功连接到MongoDB")
            return client
        except Exception as e:
            logger.error(f"连接MongoDB失败: {e}")
            raise
    
    def _ensure_collections_exist(self) -> None:
        """确保所有需要的集合存在"""
        existing_collections = self.db.list_collection_names()
        
        if self.source_collection_name not in existing_collections:
            self.db.create_collection(self.source_collection_name)
            logger.info(f"创建集合: {self.source_collection_name}")
        
        if self.log_collection_name not in existing_collections:
            self.db.create_collection(self.log_collection_name)
            logger.info(f"创建集合: {self.log_collection_name}")
        
        if self.target_collection_name not in existing_collections:
            self.db.create_collection(self.target_collection_name)
            logger.info(f"创建集合: {self.target_collection_name}")
        
        # 创建索引
        self._create_indexes()
    
    def _create_indexes(self) -> None:
        """创建必要的索引"""
        try:
            self.source_collection.create_index("job_url", unique=True)
            self.log_collection.create_index("job_url")
            self.log_collection.create_index([("status", 1), ("job_url", 1)])  # 复合索引
            self.log_collection.create_index("timestamp")
            self.target_collection.create_index("source_url")
            logger.info("集合索引创建完成")
        except Exception as e:
            logger.error(f"创建索引失败: {e}")

    def _handle_slider_captcha(self, page: Page) -> bool:
        """处理滑动验证码"""
        try:
            logger.info("尝试处理滑动验证码...")
            for _ in range(7):
                try:
                    slider = page.locator(".geetest_slider_button")
                    if slider.is_visible():
                        slider.click(timeout=3000)
                        time.sleep(2)
                except:
                    pass
            
            try:
                retry_button = page.get_by_text("请点击此处重试")
                if retry_button.is_visible():
                    retry_button.click(timeout=3000)
                    logger.info("已点击重试按钮")
            except:
                pass
            
            return True
        except Exception as e:
            logger.error(f"处理滑动验证码时出错: {e}")
            return False

    def _check_and_handle_verification(self, page: Page, target_url: str) -> bool:
        """检查并处理验证码"""
        try:
            if "callback.58.com/antibot/verifycode" in page.url:
                logger.warning("检测到验证码页面，尝试处理...")
                try:
                    verify_button = page.get_by_role("button", name="点击按钮进行验证")
                    if verify_button.is_visible():
                        verify_button.click(timeout=3000)
                        logger.info("已点击验证按钮")
                        
                        try:
                            page.wait_for_url(target_url, timeout=3000)
                            logger.info("验证成功，已返回原页面")
                            return True
                        except PlaywrightTimeoutError:
                            if page.locator(".geetest_slider_button").is_visible():
                                self._handle_slider_captcha(page)
                            logger.warning("验证后未能返回目标页面")
                            return False
                except Exception as e:
                    logger.error(f"点击验证按钮失败: {e}")
                    return False
            
            captcha_elements = [
                page.locator(".geetest_slider_button"),
                page.locator("text=请点击此处重试"),
                page.locator("text=验证码"),
                page.locator("text=请完成验证")
            ]
            
            for element in captcha_elements:
                if element.is_visible(timeout=2000):
                    logger.warning("检测到验证码元素，尝试处理...")
                    return self._handle_slider_captcha(page)
            
            return True
            
        except Exception as e:
            logger.error(f"检查验证码时发生错误: {e}")
            return False
    
    def _navigate_with_verification_check(self, page: Page, url: str) -> bool:
        """导航到指定URL并检查验证码"""
        try:
            page.goto(url, timeout=5000)
            time.sleep(self.get_random_delay(1, 3))
            return self._check_and_handle_verification(page, url)
        except Exception as e:
            logger.error(f"导航到URL {url} 失败: {e}")
            return False

    @staticmethod
    def clean_text(text: Any) -> str:
        """清理文本中的非法字符"""
        if text is None:
            return ""
        text = str(text)
        return re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text).strip()

    def get_random_delay(self, min_sec: float = 1.0, max_sec: float = 3.0) -> float:
        """获取随机延迟时间"""
        return random.uniform(min_sec, max_sec)

    def _extract_element(self, page: Page, selector: str, attr: str = None, default: Any = "") -> Any:
        """通用元素提取方法"""
        try:
            element = page.locator(selector).first
            if not element.is_visible():
                return default
                
            if attr:
                return element.get_attribute(attr)
            return element.text_content().strip()
        except:
            return default

    def extract_job_detail(self, page: Page) -> Optional[Dict[str, Any]]:
        """提取职位详情数据"""
        try:
            # 1. 基础信息
            job_info = {
                "title": self._extract_element(page, ".pos_title"),
                "salary": self._extract_element(page, ".pos_salary"),
                "job_name": self._extract_element(page, ".pos_name"),
                "update_time": self._extract_element(page, ".pos_base_update span"),
                "view_count": self._extract_element(page, "#totalcount", default="0"),
                "apply_count": self._extract_element(page, "#apply_num", default="0"),
                "welfare": [
                    self.clean_text(item) 
                    for item in page.locator(".pos_welfare_item").all_text_contents()
                ],
                "hire_count": self._extract_element(page, ".item_condition:has-text('招')")
                          .replace("招", "").replace("人", "").strip(),
                "education": self._extract_element(page, ".item_condition:has-text('学历')")
                          .replace("学历", "").strip(),
                "experience": self._extract_element(page, ".item_condition:has-text('经验')"),
                "area": self._extract_element(page, ".pos_address").replace("查看地图", ""),
                "detail_address": self._extract_element(
                    page, 
                    ".pos-area > span:not(.pos_address):not(.pos_area_map)"
                ),
                "description": self._extract_element(page, ".posDes .des")
            }

            # 2. 公司信息
            company_info = {
                "name": self._extract_element(page, ".baseInfo_link a"),
                "industry": self._extract_element(page, ".comp_baseInfo_link"),
                "scale": self._extract_element(page, ".comp_baseInfo_scale"),
                "join_time": self._extract_element(page, ".join58_num"),
                "job_openings": self._extract_element(page, ".applyPos_num", default="0")
                              .replace("个", ""),
                "company_url": self._extract_element(page, ".baseInfo_link a", attr="href"),
                "description": self._extract_element(page, ".comIntro .intro")
            }

            # 3. 构建文档
            doc = {
                "_id": ObjectId(),
                **job_info,
                "company_info": company_info,
                "source_url": page.url,
                "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "58同城"
            }

            # 深度清理数据
            def clean_data(data):
                if isinstance(data, str):
                    return self.clean_text(data)
                elif isinstance(data, dict):
                    return {k: clean_data(v) for k, v in data.items()}
                elif isinstance(data, list):
                    return [clean_data(item) for item in data]
                return data

            return clean_data(doc)
            
        except Exception as e:
            logger.error(f"数据提取失败: {e}")
            return None

    def _get_pending_urls(self) -> List[Dict[str, Any]]:
        """获取所有待处理的URL列表（优化版本，解决distinct限制问题）"""
        try:
            logger.info("开始获取待处理URL列表...")
            
            # 方法1：使用聚合管道获取已成功处理的URL
            try:
                pipeline = [
                    {"$match": {"status": "success"}},
                    {"$group": {"_id": "$job_url"}},
                    {"$project": {"_id": 0, "job_url": "$_id"}}
                ]
                success_urls = {doc["job_url"] for doc in self.log_collection.aggregate(pipeline, allowDiskUse=True)}
                logger.info(f"通过聚合管道获取到 {len(success_urls)} 个已成功处理的URL")
            except Exception as e:
                logger.warning(f"使用聚合管道获取成功URL失败，尝试分批查询: {e}")
                # 方法2：分批查询
                success_urls = set()
                batch_size = 10000
                total = self.log_collection.count_documents({"status": "success"})
                logger.info(f"开始分批查询 {total} 条成功记录...")
                
                for i in range(0, total, batch_size):
                    batch = self.log_collection.find(
                        {"status": "success"},
                        {"job_url": 1, "_id": 0}
                    ).skip(i).limit(batch_size)
                    success_urls.update(doc["job_url"] for doc in batch)
                    if i % (batch_size * 10) == 0:  # 每10批报告一次进度
                        logger.info(f"已处理 {i}/{total} 条记录")
                
                logger.info(f"通过分批查询获取到 {len(success_urls)} 个已成功处理的URL")
            
            # 获取目标集合中已存在的URL
            try:
                pipeline = [
                    {"$group": {"_id": "$source_url"}},
                    {"$project": {"_id": 0, "source_url": "$_id"}}
                ]
                existing_urls = {doc["source_url"] for doc in self.target_collection.aggregate(pipeline, allowDiskUse=True)}
                logger.info(f"获取到 {len(existing_urls)} 个目标集合中已存在的URL")
            except Exception as e:
                logger.warning(f"获取目标集合URL失败，尝试分批查询: {e}")
                existing_urls = set()
                batch_size = 10000
                total = self.target_collection.count_documents({})
                logger.info(f"开始分批查询 {total} 条目标记录...")
                
                for i in range(0, total, batch_size):
                    batch = self.target_collection.find(
                        {},
                        {"source_url": 1, "_id": 0}
                    ).skip(i).limit(batch_size)
                    existing_urls.update(doc["source_url"] for doc in batch)
                    if i % (batch_size * 10) == 0:
                        logger.info(f"已处理 {i}/{total} 条目标记录")
                
                logger.info(f"通过分批查询获取到 {len(existing_urls)} 个目标集合中已存在的URL")
            
            # 合并需要跳过的URL
            skip_urls = success_urls.union(existing_urls)
            logger.info(f"共有 {len(skip_urls)} 个URL需要跳过处理")
            
            # 查询所有待处理URL（排除已成功处理的和目标集合中已存在的）
            query = {
                "job_url": {"$nin": list(skip_urls)},
                "job_url": {"$exists": True}
            }
            projection = {
                "job_url": 1,
                "collection_name": 1,
                "collection_id": 1,
                "_id": 0
            }
            
            logger.info("开始查询待处理URL...")
            pending_urls = list(self.source_collection.find(query, projection))
            logger.info(f"获取到 {len(pending_urls)} 个待处理URL")
            
            return pending_urls
        except Exception as e:
            logger.error(f"获取待处理URL失败: {e}")
            return []

    def _save_data(self, data: Dict[str, Any]) -> bool:
        """保存数据到目标集合"""
        try:
            # 检查是否已存在相同URL的数据
            existing = self.target_collection.find_one(
                {"source_url": data["source_url"]}
            )
            if existing:
                logger.info(f"数据已存在，跳过保存: {data['source_url']}")
                return True
                
            result = self.target_collection.insert_one(data)
            return result.acknowledged
        except Exception as e:
            logger.error(f"数据保存失败: {e}")
            return False

    def _save_log(self, record: Dict[str, Any], success: bool) -> None:
        """保存日志记录"""
        try:
            log_doc = {
                "_id": ObjectId(),
                "job_url": record["job_url"],
                "source_collection": record.get("collection_name"),
                "source_id": record.get("collection_id"),
                "status": "success" if success else "failed",
                "timestamp": datetime.now(),
                "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.log_collection.insert_one(log_doc)
        except Exception as e:
            logger.error(f"日志记录失败: {e}")

    def process_single_page(self, page: Page, url_record: Dict[str, Any]) -> bool:
        """处理单个页面（返回是否成功）"""
        url = url_record["job_url"]
        logger.info(f"开始处理: {url}")
        
        # 检查是否已有成功记录或目标集合中已有数据
        existing_success = self.log_collection.count_documents({
            "job_url": url,
            "status": "success"
        }) > 0
        
        existing_in_target = self.target_collection.count_documents({
            "source_url": url
        }) > 0
        
        if existing_success or existing_in_target:
            logger.info(f"URL已处理过或目标集合中已存在，跳过: {url}")
            return True
        
        # 导航到页面
        if not self._navigate_with_verification_check(page, url):
            logger.warning(f"页面导航失败: {url}")
            return False
            
        # 提取数据
        job_data = self.extract_job_detail(page)
        if not job_data:
            logger.warning(f"数据提取失败: {url}")
            return False
            
        # 补充元数据
        job_data.update({
            "source_collection": url_record.get("collection_name"),
            "source_id": url_record.get("collection_id")
        })
        
        # 保存数据
        if not self._save_data(job_data):
            return False
            
        return True

    def run(self) -> None:
        """运行爬虫主程序"""
        try:
            # 获取所有待处理URL
            pending_urls = self._get_pending_urls()
            total_count = len(pending_urls)
            if total_count == 0:
                logger.info("没有需要处理的新URL")
                return

            logger.info(f"共发现 {total_count} 个待处理URL")

            # 初始化浏览器
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=self.headless,
                    timeout=30000
                )
                context = browser.new_context(
                    user_agent=random.choice(self.user_agents),
                    viewport={"width": 1280, "height": 720},
                    java_script_enabled=True
                )
                page = context.new_page()

                # 处理每个URL
                success_count = 0
                for i, record in enumerate(pending_urls, 1):
                    try:
                        # 显示进度信息
                        progress = i / total_count * 100
                        logger.info(f"正在处理第({i}/{total_count})条URL，进度：{progress:.1f}%")
                        
                        # 再次检查是否已处理（防止并发问题）
                        existing_success = self.log_collection.count_documents({
                            "job_url": record["job_url"],
                            "status": "success"
                        }) > 0
                        
                        existing_in_target = self.target_collection.count_documents({
                            "source_url": record["job_url"]
                        }) > 0
                        
                        if existing_success or existing_in_target:
                            logger.info(f"URL已处理过或目标集合中已存在，跳过: {record['job_url']}")
                            continue
                            
                        if self.process_single_page(page, record):
                            success_count += 1
                            self._save_log(record, True)
                        else:
                            self._save_log(record, False)
                            
                        # 随机延迟
                        time.sleep(self.get_random_delay(2.0, 5.0))
                        
                    except Exception as e:
                        logger.error(f"处理过程中出错: {e}")
                        self._save_log(record, False)
                        time.sleep(5)  # 出错后延长等待

                # 最终报告
                logger.info(
                    f"处理完成! 成功: {success_count}, 失败: {total_count-success_count}, "
                    f"成功率: {success_count/total_count*100:.1f}%"
                )

                # 关闭浏览器
                try:
                    page.close()
                    context.close()
                    browser.close()
                except:
                    pass

        except Exception as e:
            logger.error(f"爬虫运行异常: {e}")
        finally:
            if hasattr(self, 'client') and self.client:
                self.client.close()
            logger.info("资源清理完成")

if __name__ == "__main__":
    try:
        crawler = JobDetailCrawler(headless=False)
        crawler.run()
    except KeyboardInterrupt:
        logger.info("用户中断执行")
    except Exception as e:
        logger.error(f"程序崩溃: {e}")
    finally:
        logger.info("程序结束")
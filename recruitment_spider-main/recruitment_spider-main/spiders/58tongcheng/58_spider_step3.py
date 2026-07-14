import re
import time
import random
import logging
from datetime import datetime
from pymongo import MongoClient
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Page

# 配置日志（仅控制台输出）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

class AreaLinkCrawler:
    def __init__(self, headless=False):
        self.headless = headless
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        
        # MongoDB连接配置
        self.mongo_host = "210.14.140.50"
        self.mongo_port = 10387
        self.mongo_username = "mooc_da"
        self.mongo_password = "6WLg29gu3014i"
        self.source_db_name = "MOOC123_DA"
        
        # 初始化MongoDB连接
        self.client = self._get_mongo_client()
        self.db = self.client[self.source_db_name]
        
        # 日志集合列表
        self.log_collections = [
            "58_202504_step1_log_part1",
            "58_202504_step1_log_part2",
            "58_202504_step1_log_part3",
            "58_202504_step1_log_part4"
        ]
        
        # URL源集合列表
        self.url_collections = [
            "58_step1_urls_part1",
            "58_step1_urls_part2",
            "58_step1_urls_part3",
            "58_step1_urls_part4"
        ]
        
        # 目标集合
        self.main_target_collection = "58_step2_urls"
        self.part_target_collections = [
            "58_step2_urls_part1",
            "58_step2_urls_part2",
            "58_step2_urls_part3",
            "58_step2_urls_part4"
        ]
        
        # 初始化时创建唯一索引
        self._create_unique_indexes()
    
    def _create_unique_indexes(self):
        """创建唯一索引"""
        try:
            # 为主目标集合创建唯一索引
            self.db[self.main_target_collection].create_index(
                [("city_code", 1), ("job_path", 1), ("area_name", 1)],
                unique=True,
                name="unique_city_job_area"
            )
            
            # 为每个分片目标集合创建同样的唯一索引
            for col_name in self.part_target_collections:
                self.db[col_name].create_index(
                    [("city_code", 1), ("job_path", 1), ("area_name", 1)],
                    unique=True,
                    name="unique_city_job_area"
                )
            
            logging.info("成功创建唯一索引")
        except Exception as e:
            logging.error(f"创建唯一索引时出错: {e}")
    
    def _get_mongo_client(self):
        """创建MongoDB客户端连接"""
        try:
            username = quote_plus(self.mongo_username)
            password = quote_plus(self.mongo_password)
            
            uri = f"mongodb://{username}:{password}@{self.mongo_host}:{self.mongo_port}/{self.source_db_name}?authMechanism=SCRAM-SHA-256"
            
            client = MongoClient(
                uri,
                serverSelectionTimeoutMS=3000,
                socketTimeoutMS=30000,
                connectTimeoutMS=3000
            )
            
            client.admin.command('ping')
            logging.info("成功连接到MongoDB")
            return client
            
        except Exception as e:
            logging.error(f"连接MongoDB失败: {e}")
            raise
    
    def check_collections_count(self):
        """检查日志集合和URL集合的数据数目是否匹配"""
        try:
            all_matched = True
            for i in range(4):
                log_count = self.db[self.log_collections[i]].count_documents({})
                url_count = self.db[self.url_collections[i]].count_documents({})
                
                if log_count < url_count:
                    logging.error(f"集合 {self.log_collections[i]} 数据数目({log_count}) 少于 {self.url_collections[i]} 的数据数目({url_count})")
                    all_matched = False
                else:
                    logging.info(f"集合 {self.log_collections[i]}({log_count}) 和 {self.url_collections[i]}({url_count}) 数据数目检查通过")
            
            if not all_matched:
                logging.error("集合数据数目检查不通过，程序终止")
                return False
            return True
        except Exception as e:
            logging.error(f"检查集合数据数目时出错: {e}")
            return False
    
    def clean_illegal_characters(self, text):
        """清理字符串中的非法字符"""
        if not isinstance(text, str):
            return text
        return re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text).strip()
    
    def get_random_delay(self, min=1, max=3):
        """生成随机延迟"""
        return random.uniform(min, max)
    
    def _handle_slider_captcha(self, page: Page):
        """处理滑动验证码"""
        try:
            logging.info("尝试处理滑动验证码...")
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
                    logging.info("已点击重试按钮")
            except:
                pass
            
            return True
        except Exception as e:
            logging.error(f"处理滑动验证码时出错: {e}")
            return False

    def _check_and_handle_verification(self, page: Page, target_url: str) -> bool:
        """检查并处理验证码"""
        try:
            if "callback.58.com/antibot/verifycode" in page.url:
                logging.warning("检测到验证码页面，尝试处理...")
                
                try:
                    verify_button = page.get_by_role("button", name="点击按钮进行验证")
                    if verify_button.is_visible():
                        verify_button.click(timeout=3000)
                        logging.info("已点击验证按钮")
                        
                        try:
                            page.wait_for_url(target_url, timeout=3000)
                            logging.info("验证成功，已返回原页面")
                            return True
                        except PlaywrightTimeoutError:
                            logging.warning("验证后未能返回原页面，检查是否有滑动验证码")
                            
                            if page.locator(".geetest_slider_button").is_visible():
                                self._handle_slider_captcha(page)
                                try:
                                    page.wait_for_url(target_url, timeout=3000)
                                    return True
                                except:
                                    pass
                            
                            logging.warning("验证后未能返回目标页面")
                            return False
                except Exception as e:
                    logging.error(f"点击验证按钮失败: {e}")
                    return False
            
            captcha_elements = [
                page.locator(".geetest_slider_button"),
                page.locator("text=请点击此处重试"),
                page.locator("text=验证码"),
                page.locator("text=请完成验证")
            ]
            
            for element in captcha_elements:
                if element.is_visible(timeout=2000):
                    logging.warning("检测到验证码元素，尝试处理...")
                    return self._handle_slider_captcha(page)
            
            return True
            
        except Exception as e:
            logging.error(f"检查验证码时发生错误: {e}")
            return False
    
    def _navigate_with_verification_check(self, page: Page, url: str) -> bool:
        """导航到指定URL并检查验证码"""
        try:
            page.goto(url, timeout=5000)
            time.sleep(self.get_random_delay(1, 3))
            
            if not self._check_and_handle_verification(page, url):
                logging.warning(f"验证码处理失败，无法访问: {url}")
                return False
            
            return True
        except Exception as e:
            logging.error(f"导航到URL {url} 失败: {e}")
            return False
    
    def extract_area_links(self, page: Page, base_data: dict):
        """从页面中提取区域筛选链接"""
        try:
            url = base_data["url"]
            logging.info(f"开始提取区域链接: {url}")
            
            user_agent = random.choice(self.user_agents)
            page.set_extra_http_headers({"User-Agent": user_agent})
            
            if not self._navigate_with_verification_check(page, url):
                return []
            
            try:
                page.wait_for_selector('div.filter_item.filter_area', timeout=5000)
            except:
                logging.warning("未找到区域筛选器，可能页面结构已变化")
                return []
            
            for _ in range(3):
                page.mouse.wheel(0, random.randint(30, 80))
                time.sleep(random.uniform(0.5, 1.5))
            
            area_links = []
            area_elements = page.query_selector_all('div.filter_item.filter_area a')
            
            for element in area_elements:
                try:
                    href = element.get_attribute('href')
                    text = element.text_content().strip()
                    if href and text:
                        area_data = {
                            "base_url": url,
                            "url": self.clean_illegal_characters(href),
                            "city": base_data.get("city", ""),
                            "city_code": base_data.get("city_code", ""),
                            "job_category": base_data.get("job_category", ""),
                            "job_path": base_data.get("job_path", ""),
                            "area_name": self.clean_illegal_characters(text),
                            "status": "pending",  # 添加状态字段
                            "created_at": datetime.now()
                        }
                        area_links.append(area_data)
                except Exception as e:
                    logging.warning(f"提取区域链接时出错: {e}")
                    continue
            
            logging.info(f"从页面中提取到{len(area_links)}个区域链接")
            return area_links
        
        except Exception as e:
            logging.error(f"提取区域链接时发生错误: {e}")
            return []
    
    def get_urls_with_jobs(self):
        """从MongoDB获取所有job_count不为零的URL"""
        try:
            urls_with_jobs = []
            
            for collection_name in self.log_collections:
                logging.info(f"正在从集合 {collection_name} 读取数据...")
                collection = self.db[collection_name]
                
                query = {
                    "success": True,
                    "job_count": {"$gt": 0}
                }
                
                urls = list(collection.find(
                    query,
                    {
                        "url": 1, 
                        "_id": 1, 
                        "job_count": 1,
                        "city": 1,
                        "city_code": 1,
                        "job_category": 1,
                        "job_path": 1
                    }
                ))
                
                urls_with_jobs.extend(urls)
            
            logging.info(f"总共找到{len(urls_with_jobs)}个有职位的URL")
            return urls_with_jobs
        except Exception as e:
            logging.error(f"查询URL时出错: {e}")
            return []
    
    def remove_duplicates(self, data):
        """去除重复数据，基于url字段"""
        if not data:
            return []
        
        seen_urls = set()
        unique_data = []
        
        for item in data:
            if item['url'] not in seen_urls:
                seen_urls.add(item['url'])
                unique_data.append(item)
        
        logging.info(f"去重前数据量: {len(data)}, 去重后数据量: {len(unique_data)}")
        return unique_data
    
    def save_to_mongodb(self, data, collection_name):
        """将数据保存到指定的MongoDB集合"""
        try:
            if not data:
                return
            
            collection = self.db[collection_name]
            
            # 使用insert_many的ordered=False参数，即使有重复键错误也会继续插入非重复文档
            try:
                result = collection.insert_many(data, ordered=False)
                logging.info(f"成功插入{len(result.inserted_ids)}条数据到集合{collection_name}")
            except Exception as e:
                if hasattr(e, 'details') and 'nInserted' in e.details:
                    logging.info(f"成功插入{e.details['nInserted']}条数据到集合{collection_name}，跳过{len(data)-e.details['nInserted']}条重复数据")
                else:
                    raise e
        except Exception as e:
            logging.error(f"保存到MongoDB集合{collection_name}时出错: {e}")
    
    def distribute_to_part_collections(self, all_data):
        """将数据平均分配到4个子集合中"""
        if not all_data:
            return
        
        # 计算每个子集合应该包含的数据量
        total = len(all_data)
        part_size = total // 4
        
        # 将数据分成4部分
        parts = [
            all_data[:part_size],
            all_data[part_size:2*part_size],
            all_data[2*part_size:3*part_size],
            all_data[3*part_size:]
        ]
        
        # 确保最后一部分包含所有剩余数据
        parts[-1] = all_data[3*part_size:]
        
        # 保存到各个子集合
        for i, part_data in enumerate(parts):
            if part_data:
                self.save_to_mongodb(part_data, self.part_target_collections[i])
    
    def process_urls(self, urls_with_jobs):
        """处理所有有职位的URL"""
        if not urls_with_jobs:
            return []
        
        all_area_links = []
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=self.headless,
                slow_mo=50,
            )
            
            context = browser.new_context(
                user_agent=random.choice(self.user_agents),
                viewport={"width": 1280, "height": 720},
            )
            
            page = context.new_page()
            
            try:
                for i, doc in enumerate(urls_with_jobs):
                    logging.info(f"开始处理第{i+1}/{len(urls_with_jobs)}个URL (职位数: {doc['job_count']}): {doc['url']}")
                    
                    try:
                        area_links = self.extract_area_links(page, doc)
                        
                        if area_links:
                            all_area_links.extend(area_links)
                        
                        time.sleep(self.get_random_delay(2, 5))
                    
                    except Exception as e:
                        logging.error(f"处理URL {doc['url']} 时出错: {e}")
                        continue
                
                return all_area_links
                
            except Exception as e:
                logging.error(f"处理URL时出错: {e}")
                return []
            finally:
                if 'page' in locals():
                    page.close()
                browser.close()
    
    def run(self):
        """运行爬虫"""
        # 首先检查集合数据数目是否匹配
        if not self.check_collections_count():
            return
        
        # 获取所有有职位的URL
        urls_with_jobs = self.get_urls_with_jobs()
        
        # 处理所有URL
        all_data = self.process_urls(urls_with_jobs)
        
        if not all_data:
            logging.warning("没有提取到任何有效数据")
            return
        
        # 只进行一次去重
        unique_data = self.remove_duplicates(all_data)
        
        if unique_data:
            # 先保存到主集合
            self.save_to_mongodb(unique_data, self.main_target_collection)
            
            # 再分配到子集合
            self.distribute_to_part_collections(unique_data)
            
            logging.info(f"处理完成，共保存{len(unique_data)}条唯一数据")
        else:
            logging.warning("去重后没有剩余数据")

if __name__ == "__main__":
    crawler = AreaLinkCrawler(headless=True)
    crawler.run()
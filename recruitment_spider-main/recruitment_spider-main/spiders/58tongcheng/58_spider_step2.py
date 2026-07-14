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

class URLValidator:
    def __init__(self, headless=True):
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
        
        # 集合名称
        self.source_collection_name = "58_step1_urls_part1"
        self.log_collection_name = "58_step1_urls_202504_log_part1"
        
        # 初始化MongoDB连接
        self.client = None
        self.db = None
        self.source_collection = None
        self.log_collection = None
    
    def connect_mongodb(self):
        """连接MongoDB数据库"""
        try:
            self.client = MongoClient(
                host=self.mongo_host,
                port=self.mongo_port,
                username=self.mongo_username,
                password=self.mongo_password,
                authSource=self.source_db_name
            )
            self.db = self.client[self.source_db_name]
            self.source_collection = self.db[self.source_collection_name]
            self.log_collection = self.db[self.log_collection_name]
            logging.info("成功连接到MongoDB数据库")
            return True
        except Exception as e:
            logging.error(f"连接MongoDB失败: {str(e)}")
            return False
    
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
    
    def count_job_elements(self, page: Page) -> int:
        """计算页面上的职位元素数量"""
        try:
            job_elements = page.query_selector_all('li.job_item')
            return len(job_elements)
        except Exception as e:
            logging.error(f"计算职位元素数量时出错: {e}")
            return 0
    
    def validate_url(self, page: Page, url_data: dict) -> dict:
        """验证单个URL是否有数据"""
        url = url_data.get('url', '')
        city = url_data.get('city', '')
        city_code = url_data.get('city_code', '')
        job_category = url_data.get('job_category', '')
        job_path = url_data.get('job_path', '')
        
        logging.info(f"开始验证URL: {url}")
        
        try:
            user_agent = random.choice(self.user_agents)
            page.set_extra_http_headers({"User-Agent": user_agent})
            
            if not self._navigate_with_verification_check(page, url):
                return {
                    "city": city,
                    "city_code": city_code,
                    "job_category": job_category,
                    "job_path": job_path,
                    "url": url,
                    "success": False,
                    "job_count": 0,
                    "crawl_time": datetime.now(),
                    "error": "验证码处理失败或无法访问页面"
                }
            
            # 滚动页面以加载更多内容
            for _ in range(3):
                page.mouse.wheel(0, random.randint(30, 80))
                time.sleep(random.uniform(0.5, 1.5))
            
            job_count = self.count_job_elements(page)
            success = job_count > 0
            
            return {
                "city": city,
                "city_code": city_code,
                "job_category": job_category,
                "job_path": job_path,
                "url": url,
                "success": success,
                "job_count": job_count,
                "crawl_time": datetime.now(),
                "error": "" if success else "未找到职位信息"
            }
            
        except Exception as e:
            logging.error(f"验证URL {url} 时出错: {e}")
            return {
                "city": city,
                "city_code": city_code,
                "job_category": job_category,
                "job_path": job_path,
                "url": url,
                "success": False,
                "job_count": 0,
                "crawl_time": datetime.now(),
                "error": str(e)
            }
    
    def get_unprocessed_urls(self):
        """获取未处理的URL列表"""
        try:
            # 获取已处理的URL列表
            processed_urls = {doc['url'] for doc in self.log_collection.find({}, {'url': 1})}
            
            # 查询未处理的URL
            query = {"url": {"$nin": list(processed_urls)}}
            urls = list(self.source_collection.find(query))
            
            logging.info(f"找到 {len(urls)} 个待验证的URL")
            return urls
        except Exception as e:
            logging.error(f"获取未处理URL列表时出错: {e}")
            return []
    
    def save_validation_result(self, result):
        """保存验证结果到日志集合"""
        try:
            self.log_collection.insert_one(result)
            logging.info(f"已保存验证结果: {result['url']} - 成功: {result['success']} - 职位数: {result['job_count']}")
        except Exception as e:
            logging.error(f"保存验证结果时出错: {e}")
    
    def run(self):
        """运行验证程序"""
        if not self.connect_mongodb():
            return
        
        url_list = self.get_unprocessed_urls()
        if not url_list:
            logging.info("没有需要验证的URL")
            return
        
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
                for i, url_data in enumerate(url_list):
                    logging.info(f"处理进度: {i+1}/{len(url_list)}")
                    
                    result = self.validate_url(page, url_data)
                    self.save_validation_result(result)
                    
                    # 随机延迟，避免请求过于频繁
                    time.sleep(self.get_random_delay(2, 5))
                
                logging.info(f"验证完成，共处理 {len(url_list)} 个URL")
                
            except Exception as e:
                logging.error(f"验证过程中出错: {e}")
            finally:
                page.close()
                context.close()
                browser.close()
                self.client.close()

if __name__ == "__main__":
    validator = URLValidator(headless=False)
    validator.run()
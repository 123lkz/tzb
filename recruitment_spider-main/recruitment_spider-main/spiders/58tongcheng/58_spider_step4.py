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

class JobCrawler:
    def __init__(self, headless=False):
        self.headless = headless
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        
        # 翻页配置
        self.enable_pagination = True
        self.max_pages = 3
        self.page_size_threshold = 70
        
        # MongoDB连接配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.source_collection_name = "58_step2_urls_part4"
        self.log_collection_name = "58_step2_urls_202507_log_part4"
        self.target_collection_name = "58_job_raw_07_part4"
        
        # 初始化MongoDB连接
        self.client = self._get_mongo_client()
        self.db = self.client.get_database()
        self.source_collection = self.db[self.source_collection_name]
        self.log_collection = self.db[self.log_collection_name]
        self.target_collection = self.db[self.target_collection_name]
    
    def _get_mongo_client(self):
        """创建MongoDB客户端连接"""
        try:
            client = MongoClient(
                self.mongo_uri,
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
                            if page.locator(".geetest_slider_button").is_visible():
                                self._handle_slider_captcha(page)
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
            return self._check_and_handle_verification(page, url)
        except Exception as e:
            logging.error(f"导航到URL {url} 失败: {e}")
            return False
    
    def extract_job_info_from_element(self, job_element):
        """从单个职位元素中提取信息"""
        try:
            job_data = {
                "title": job_element.query_selector('span.cate').text_content().strip() if job_element.query_selector('span.cate') else "",
                "salary": job_element.query_selector('p.job_salary').text_content().replace('元/月', '').strip() if job_element.query_selector('p.job_salary') else "",
                "location": job_element.query_selector('span.address').text_content().strip() if job_element.query_selector('span.address') else "",
                "company": job_element.query_selector('div.comp_name a').text_content().strip() if job_element.query_selector('div.comp_name a') else "",
                "company_url": job_element.query_selector('div.comp_name a').get_attribute('href') if job_element.query_selector('div.comp_name a') else "",
                "job_url": job_element.query_selector('a').get_attribute('href') if job_element.query_selector('a') else "",
                "job_type": "全职",
                "education": job_element.query_selector('span.xueli').text_content().strip() if job_element.query_selector('span.xueli') else "",
                "experience": job_element.query_selector('span.jingyan').text_content().strip() if job_element.query_selector('span.jingyan') else "",
                "benefits": [benefit.text_content().strip() for benefit in job_element.query_selector_all('div.job_wel span')],
                "recommend_reason": job_element.query_selector('span.tui_jian_txt').text_content().strip() if job_element.query_selector('span.tui_jian_txt') else "",
                "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "58同城",
                "uploader": "cencipifu"
            }
            
            for key, value in job_data.items():
                if isinstance(value, str):
                    job_data[key] = self.clean_illegal_characters(value)
                elif isinstance(value, list):
                    job_data[key] = [self.clean_illegal_characters(v) for v in value]
            
            return job_data
        except Exception as e:
            logging.error(f"提取职位信息时出错: {e}")
            return None
    
    def _try_click_next_page(self, page: Page):
        """尝试点击下一页按钮"""
        try:
            next_button = page.locator(".next")
            if next_button.is_visible(timeout=2000):
                next_button.click()
                time.sleep(self.get_random_delay(2, 4))
                return True
            return False
        except Exception as e:
            logging.warning(f"尝试点击下一页按钮失败: {e}")
            return False
    
    def scrape_job_list(self, page, url):
        """从给定的URL爬取职位列表，仅在当前页有70个职位时才尝试翻页"""
        time.sleep(self.get_random_delay())
        logging.info(f"开始爬取URL: {url}")
        
        try:
            user_agent = random.choice(self.user_agents)
            page.set_extra_http_headers({"User-Agent": user_agent})
            
            if not self._navigate_with_verification_check(page, url):
                return []
            
            job_data_list = []
            current_page = 1
            
            while current_page <= self.max_pages:
                try:
                    page.wait_for_selector('li.job_item', state="attached", timeout=5000)
                    
                    # 模拟滚动
                    for _ in range(3):
                        page.mouse.wheel(0, random.randint(30, 80))
                        time.sleep(random.uniform(0.5, 1.5))
                    
                    job_elements = page.query_selector_all('li.job_item')
                    page_job_count = len(job_elements)
                    
                    logging.info(f"第{current_page}页找到{page_job_count}个职位")
                    
                    # 提取当前页所有职位信息
                    for job_element in job_elements:
                        try:
                            job_data = self.extract_job_info_from_element(job_element)
                            if job_data:
                                job_data_list.append(job_data)
                        except Exception as e:
                            logging.warning(f"提取职位信息时出错: {e}")
                            continue
                    
                    # 检查是否需要翻页
                    if (self.enable_pagination and 
                        page_job_count == self.page_size_threshold and 
                        current_page < self.max_pages):
                        
                        logging.info(f"当前页有{page_job_count}个职位，尝试翻页...")
                        if self._try_click_next_page(page):
                            current_page += 1
                            continue
                    
                    break  # 不满足翻页条件则终止循环
                    
                except Exception as e:
                    logging.error(f"处理第{current_page}页时出错: {e}")
                    break
            
            logging.info(f"共找到{len(job_data_list)}个职位(共{current_page}页)")
            return job_data_list
        
        except Exception as e:
            logging.error(f"爬取职位列表时出错: {e}")
            return []

    def _get_urls_from_mongo(self):
        """从MongoDB获取待爬取的URL列表"""
        try:
            processed_urls = {doc['url'] for doc in self.log_collection.find({}, {'url': 1})}
            query = {"url": {"$nin": list(processed_urls)}}
            
            urls = list(self.source_collection.find(
                query,
                {
                    "url": 1, 
                    "city": 1,
                    "city_code": 1,
                    "job_category": 1,
                    "job_path": 1,
                    "area_name": 1
                }
            ))
            
            logging.info(f"从MongoDB中读取了{len(urls)}个待处理的URL")
            return urls
        except Exception as e:
            logging.error(f"从MongoDB读取URL时出错: {e}")
            return []
    
    def _save_to_log_collection(self, record, success, job_count=0):
        """将处理结果保存到日志集合（按照指定格式）"""
        try:
            log_data = {
                "url": record.get("url", ""),
                "city": record.get("city", ""),
                "city_code": record.get("city_code", ""),
                "job_category": record.get("job_category", ""),
                "job_path": record.get("job_path", ""),
                "area_name": record.get("area_name", "无"),
                "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "job_count": job_count,
                "success": success
            }
            
            # 使用insert_one自动生成新_id
            self.log_collection.insert_one(log_data)
            
        except Exception as e:
            logging.error(f"保存处理结果到日志集合时出错: {e}")
    
    def _save_job_data(self, job_data_list):
        """将职位数据保存到目标集合"""
        try:
            if job_data_list:
                result = self.target_collection.insert_many(job_data_list)
                logging.info(f"成功插入{len(result.inserted_ids)}条数据到目标集合")
        except Exception as e:
            logging.error(f"保存职位数据到目标集合时出错: {e}")
    
    def run(self):
        """运行爬虫"""
        url_docs = self._get_urls_from_mongo()
        if not url_docs:
            logging.error("没有获取到待处理的URL列表，程序终止")
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
                for i, doc in enumerate(url_docs):
                    url = doc['url']
                    logging.info(f"处理第{i+1}/{len(url_docs)}个URL: {url}")
                    
                    try:
                        job_data_list = self.scrape_job_list(page, url)
                        
                        if job_data_list:
                            self._save_job_data(job_data_list)
                            self._save_to_log_collection(doc, True, len(job_data_list))
                        else:
                            self._save_to_log_collection(doc, False, 0)
                    
                    except Exception as e:
                        logging.error(f"处理URL {url} 时出错: {e}")
                        self._save_to_log_collection(doc, False, 0)
                        continue
                
                logging.info(f"爬取完成，共处理{len(url_docs)}个URL")
                
            except Exception as e:
                logging.error(f"爬虫运行出错: {e}")
            finally:
                if 'page' in locals():
                    page.close()
                browser.close()
                self.client.close()

if __name__ == "__main__":
    crawler = JobCrawler(headless=False)
    crawler.enable_pagination = True
    crawler.max_pages = 3
    crawler.page_size_threshold = 70
    crawler.run()
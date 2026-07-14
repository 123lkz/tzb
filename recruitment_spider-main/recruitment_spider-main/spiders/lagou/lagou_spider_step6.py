#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
拉勾网爬虫 - 第六步
功能：根据step5生成的职位详情页URL，获取职位详情数据

主要步骤：
1. 从MongoDB加载step5生成的职位详情页URL
2. 使用Selenium模拟浏览器访问职位详情页
3. 解析职位详情数据
4. 保存到MongoDB

数据存储：
- 输入集合：lagou_step3_urls_part1
- 输出集合：lagou_job_detail_part1
- 日志集合：lagou_step3_urls_202504_log_part1
"""

import json
import logging
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from tqdm import tqdm
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from captcha_recognizer.recognizer import Recognizer

# 将项目根目录添加到Python路径中
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent  # 从当前文件向上找三层到项目根目录
sys.path.append(str(project_root))

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "lagou_spider_step6")
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class LagouSpiderStep6:
    """拉勾网爬虫 - 第六步"""
    
    def __init__(self, headless: bool = False):
        """初始化爬虫"""
        # 加载环境变量
        load_dotenv()
        
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.mongo_client = None
        self.db = None
        self.collection = None
        self.progress_collection = None
        
        # 输入输出集合名称
        self.input_collection = 'lagou_step3_urls_part2'
        self.output_collection = 'lagou_job_detail_part2'
        self.log_collection = 'lagou_step3_urls_202504_log_part2'
        
        # 基础数据文件路径
        self.cookie_path = Path("recruitment_spider/data/lagou/lagou_cookie.json")
        logger.info(f"基础数据文件路径: {self.cookie_path.absolute()}")
        
        # 加载cookie配置
        self.cookies = self.load_cookies()
        
        # Selenium配置
        self.headless = headless
        self.driver = None
        self.wait = None
        
        # 已处理URL缓存
        self.processed_urls = {}
        
        # 初始化MongoDB连接
        self._init_mongodb()
        self._load_processed_urls()
        
        logger.info(f"初始化完成")
    
    def load_cookies(self) -> Dict:
        """加载cookie配置"""
        try:
            if not self.cookie_path.exists():
                logger.error(f"Cookie文件不存在: {self.cookie_path}")
                return {}
            
            with open(self.cookie_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            logger.info(f"成功加载 {len(cookies)} 个账号的cookie配置")
            return cookies
        except Exception as e:
            logger.error(f"加载cookie配置失败: {str(e)}")
            return {}
    
    def _init_mongodb(self) -> None:
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            self.collection = self.db[self.output_collection]
            self.progress_collection = self.db[self.log_collection]            
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise

    def _load_processed_urls(self) -> None:
        """从MongoDB加载已处理的URL到内存中"""
        try:
            cursor = self.progress_collection.find({}, {
                "positionUrl": 1,
                "status": 1
            })
            
            for doc in cursor:
                self.processed_urls[doc['positionUrl']] = 1
            
            logger.info(f"已加载 {len(self.processed_urls)} 个已处理的URL")
        except Exception as e:
            logger.error(f"加载已处理URL失败: {str(e)}")

    def init_selenium(self):
        """初始化Selenium"""
        try:
            # 创建Chrome选项
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # 设置窗口大小为普通用户常用的尺寸
            chrome_options.add_argument('--window-size=1024,760')
            chrome_options.add_argument('--start-maximized')
            
            # 设置中文语言环境
            chrome_options.add_argument('--lang=zh-CN')
            
            # 添加一些常见的用户代理字符串
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            ]
            chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
            
            # 禁用不必要的功能
            chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
            chrome_options.add_argument('--disable-dev-shm-usage')  # 禁用/dev/shm使用
            chrome_options.add_argument('--no-sandbox')  # 禁用沙箱
            chrome_options.add_argument('--disable-web-security')  # 禁用网页安全性检查
            chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')  # 禁用站点隔离
            chrome_options.add_argument('--disable-site-isolation-trials')  # 禁用站点隔离试验
            chrome_options.add_argument('--disable-webgl')  # 禁用WebGL
            chrome_options.add_argument('--disable-notifications')  # 禁用通知
            chrome_options.add_argument('--disable-extensions')  # 禁用扩展
            chrome_options.add_argument('--disable-popup-blocking')  # 禁用弹窗拦截
            chrome_options.add_argument('--disable-infobars')  # 禁用信息栏
            chrome_options.add_argument('--disable-logging')  # 禁用日志
            chrome_options.add_argument('--log-level=3')  # 设置日志级别为ERROR
            chrome_options.add_argument('--silent')  # 静默模式
            chrome_options.add_argument('--disable-webrtc')  # 禁用WebRTC
            
            # 创建WebDriver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            
            # 设置页面加载超时
            self.driver.set_page_load_timeout(30)
            self.driver.set_script_timeout(30)
            
            # 注入JavaScript代码来绕过检测
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
                Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en'] });
            """)
            
            logger.info("Selenium初始化成功")
            
            # 执行登录
            if not self.login():
                logger.error("登录失败")
                raise Exception("登录失败")
            
        except Exception as e:
            logger.error(f"Selenium初始化失败: {e}")
            raise

    def login(self) -> bool:
        """使用账号密码登录"""
        try:
            # 随机选择一个账号
            account = random.choice(list(self.cookies.keys()))
            password = self.cookies[account]
            logger.info(f"已随机选择账号 {account} 进行登录")
            
            # 访问登录页面
            self.driver.get("https://passport.lagou.com/login/login.html")
            
            # 检查页面是否加载完成
            max_retries = 3
            for attempt in range(max_retries):
                if "登录" in self.driver.page_source:
                    break
                time.sleep(1)
                if attempt == max_retries - 1:
                    logger.error("登录页面加载失败")
                    return False
            
            # 切换到密码登录
            try:
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '密码登录')]")
                if elements:
                    elements[0].click()
                    time.sleep(1)
            except Exception as e:
                logger.warning(f"切换到密码登录失败: {e}")
            
            # 输入账号
            try:
                username_input = self.driver.find_element(By.NAME, "account")
                username_input.clear()
                username_input.send_keys(account)
                time.sleep(1)
            except Exception as e:
                logger.error(f"输入账号失败: {e}")
                return False
            
            # 输入密码
            try:
                password_input = self.driver.find_element(By.NAME, "password")
                password_input.clear()
                password_input.send_keys(password)
                time.sleep(1)
            except Exception as e:
                logger.error(f"输入密码失败: {e}")
                return False
            
            # 勾选协议
            try:
                agreement_checkbox = self.driver.find_element(By.CSS_SELECTOR, ".sc-furwcr.bVYGWy")
                agreement_checkbox.click()
                time.sleep(0.5)
            except Exception as e:
                logger.warning(f"勾选协议失败: {e}")
            
            # 点击登录按钮
            try:
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button.ant-btn.ant-btn-primary")
                login_button.click()
            except Exception as e:
                logger.error(f"点击登录按钮失败: {e}")
                return False
            
            # 等待登录完成
            time.sleep(2)
            if not self.retry_with_captcha():
                logger.error("验证码处理失败")
                return False                        
            
            # 检查登录状态
            if self.verify_login():
                logger.info("登录成功")
                return True
            else:
                logger.error("登录失败")
                return False
                
        except Exception as e:
            logger.error(f"登录过程出错: {e}")
            return False

    def verify_login(self) -> bool:
        """验证登录状态"""
        try:
            # 检查是否存在登录按钮或其他未登录标识
            login_button = self.driver.find_elements(By.CSS_SELECTOR, '.login, .btn-login, [data-lg-tj-id="1810"]')
            user_avatar = self.driver.find_elements(By.CSS_SELECTOR, '.user-avatar, .avatar, .user-head-img')
            unick = self.driver.find_elements(By.CSS_SELECTOR, '.unick, .user-name, .user-info')
            
            # 检查当前URL是否在登录页面
            is_login_page = 'login' in self.driver.current_url
            
            # 综合判断登录状态
            is_logged_in = (
                not login_button and
                (user_avatar or unick) and
                not is_login_page
            )
            
            if is_logged_in:
                logger.info("登录状态验证成功")
            else:
                logger.warning(f"登录状态验证失败，当前URL: {self.driver.current_url}")
            
            return is_logged_in
            
        except Exception as e:
            logger.error(f"验证登录状态失败: {e}")
            return False

    def handle_captcha(self) -> bool:
        """处理验证码"""
        try:
            # 等待验证码元素出现
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "geetest_captcha"))
            )
            # 检查验证码类型
            retry_count = 0
            max_retry = 999
            while retry_count < max_retry:
                if "geetest_slider" in self.driver.page_source:
                    return self.handle_slider_captcha()
                else:
                    logger.warning("不是滑块认证，尝试点击左上角(50,50)并重新点击登录按钮")
                    webdriver.ActionChains(self.driver).move_by_offset(50, 50).click().perform()
                    time.sleep(0.5)
                    # 点击登录按钮
                    try:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, "button.ant-btn.ant-btn-primary")
                        login_button.click()
                        time.sleep(1)
                    except Exception as e:
                        logger.error(f"点击登录按钮失败: {e}")
                    retry_count += 1
            logger.error("未知的验证码类型，重试多次后仍未出现滑块认证")
            return False
                
        except Exception as e:
            logger.error(f"验证码处理失败: {e}")
            return False

    def handle_slider_captcha(self) -> bool:
        """处理滑块验证码"""
        max_retries = 10
        for attempt in range(max_retries):
            try:
                # 等待验证码完全加载
                time.sleep(2)
                
                # 创建保存目录
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_dir = os.path.join("captcha_images", 'lagou')
                os.makedirs(save_dir, exist_ok=True)
                
                # 优化：只对可见的.geetest_window截图
                window_elements = self.driver.find_elements(By.CLASS_NAME, "geetest_window")
                window_elem = None
                for elem in window_elements:
                    size = elem.size
                    if size['width'] > 0 and size['height'] > 0 and elem.is_displayed():
                        window_elem = elem
                        break
                if not window_elem:
                    logger.error("未找到可见的.geetest_window区域，所有高度都为0")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    return False
                
                logger.info(f"选中的.geetest_window尺寸: width={window_elem.size['width']}, height={window_elem.size['height']}")
                window_png = window_elem.screenshot_as_png
                with open(os.path.join(save_dir, "window.png"), "wb") as f:
                    f.write(window_png)
                
                # 1. 调用识别器识别window.png缺口坐标
                recognizer = Recognizer()
                box, confidence = recognizer.identify_gap(source=os.path.join(save_dir, 'window.png'), verbose=False)
                if not box or not isinstance(box, (list, tuple)) or len(box) < 1:
                    logger.error(f'识别缺口失败，box结果异常: {box}，将删除本次截图并重试')
                    # 删除本次截图
                    try:
                        window_path = os.path.join(save_dir, "window.png")
                        if os.path.exists(window_path):
                            os.remove(window_path)
                            logger.info(f"已删除识别失败的验证码截图: {window_path}")
                    except Exception as e:
                        logger.warning(f"删除验证码截图失败: {e}")
                    
                    # 点击刷新按钮
                    try:
                        refresh_button = None
                        refresh_selectors = [
                            (By.CSS_SELECTOR, "[class^='geetest_refresh']"),
                            (By.CSS_SELECTOR, "button[class*='geetest_refresh']"),
                            (By.CSS_SELECTOR, "button[aria-label='刷新验证']")
                        ]
                        
                        for by, selector in refresh_selectors:
                            elements = self.driver.find_elements(by, selector)
                            for elem in elements:
                                if elem.is_displayed() and elem.size['width'] > 0:
                                    refresh_button = elem
                                    break
                            if refresh_button:
                                break
                        
                        if refresh_button:
                            refresh_button.click()
                            logger.info("成功点击刷新验证按钮")
                            time.sleep(1)
                        else:
                            logger.error("未找到刷新验证按钮")
                    except Exception as e:
                        logger.error(f"点击登录按钮失败: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    return False
                
                logger.info(f'识别到缺口坐标: {box}, 可信度: {confidence}')
                gap_x = box[0]

                # 2. 获取滑块按钮元素和初始位置
                try:
                    slider_elem = None
                    selectors = [
                        (By.CSS_SELECTOR, "[class^='geetest_btn']"),
                        (By.CSS_SELECTOR, ".geetest_slider_button"),
                        (By.CSS_SELECTOR, "div[class*='geetest_btn']")
                    ]
                    
                    for by, selector in selectors:
                        elements = self.driver.find_elements(by, selector)
                        for elem in elements:
                            if elem.is_displayed() and elem.size['width'] > 0 and elem.size['height'] > 0:
                                slider_elem = elem
                                break
                        if slider_elem:
                            break
                    
                    if not slider_elem:
                        logger.error("未找到可用的滑块按钮")
                        return False
                        
                    logger.info(f"成功找到滑块按钮，大小: {slider_elem.size}")
                except Exception as e:
                    logger.error(f"查找滑块按钮失败: {e}")
                    return False

                # 3. 计算需要移动的距离
                window_location = window_elem.location
                move_distance = gap_x - (slider_elem.location['x'] - window_location['x'])
                logger.info(f'滑块初始x: {slider_elem.location['x']}, window原点x: {window_location['x']}, 需要移动距离: {move_distance}')

                # 4. 滑动
                action_chains = webdriver.ActionChains(self.driver)
                action_chains.move_to_element(slider_elem).perform()
                time.sleep(0.5)
                action_chains.click_and_hold(slider_elem).perform()
                time.sleep(0.5)
                # 模拟人类滑动轨迹
                track = self.get_track(move_distance-13)
                for x in track:
                    action_chains.move_by_offset(xoffset=x, yoffset=0).perform()
                    # 减小时间间隔，使滑动更快
                    time.sleep(random.uniform(0.01, 0.05))
                action_chains.release().perform()
                
                # 等待页面跳转完成
                try:
                    current_url = self.driver.current_url
                    WebDriverWait(self.driver, 30).until(
                        lambda driver: driver.current_url != current_url or
                        not driver.find_elements(By.CLASS_NAME, "geetest_window")
                    )
                    logger.info("验证码验证完成，页面已跳转")
                    # 删除验证码截图
                    try:
                        window_path = os.path.join(save_dir, "window.png")
                        if os.path.exists(window_path):
                            os.remove(window_path)
                            logger.info(f"已删除验证码截图: {window_path}")
                    except Exception as e:
                        logger.warning(f"删除验证码截图失败: {e}")
                    
                    return self.check_captcha_result()
                except TimeoutException:
                    logger.error("等待页面跳转超时")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    return False
                
            except Exception as e:
                logger.error(f"处理滑块验证码失败: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return False
        
        return False

    def get_track(self, distance: int) -> List[int]:
        """生成滑动轨迹"""
        # 减少轨迹点数，直接计算几个关键点
        track = []
        # 初始加速
        track.append(int(distance * 0.3))
        # 匀速
        track.append(int(distance * 0.4))
        # 减速
        track.append(int(distance * 0.3))
        return track

    def check_captcha_result(self) -> bool:
        """检查验证码处理结果"""
        try:
            # 等待页面加载完成
            time.sleep(2)
            
            # 检查是否还在登录页面
            if 'login' in self.driver.current_url:
                logger.error("验证码处理后仍在登录页面")
                return False
            
            # 检查是否有错误提示
            error_messages = self.driver.find_elements(By.CSS_SELECTOR, '.error-message, .ant-message-error')
            if error_messages:
                for msg in error_messages:
                    if msg.is_displayed():
                        logger.error(f"验证码处理后出现错误提示: {msg.text}")
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"检查验证码处理结果失败: {e}")
            return False

    def retry_with_captcha(self) -> bool:
        """处理验证码并重试"""
        try:
            # 等待验证码出现
            time.sleep(2)
            
            # 检查是否需要处理验证码
            if "geetest_captcha" in self.driver.page_source:
                logger.info("检测到验证码，开始处理")
                if not self.handle_captcha():
                    logger.error("验证码处理失败")
                    return False
                
                # 验证码处理后检查登录状态
                if self.verify_login():
                    logger.info("验证码处理后登录成功")
                    return True
                else:
                    logger.error("验证码处理后登录失败")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"验证码重试过程出错: {e}")
            return False

    def _get_job_detail(self, position_url: str) -> Optional[Dict]:
        """获取职位详情数据
        
        Args:
            position_url: 职位详情页URL
            
        Returns:
            职位详情数据
        """
        max_retries = 3  # 最大重试次数
        retry_delay = 5  # 重试间隔（秒）
        
        for retry in range(max_retries):
            try:
                # 访问职位详情页
                logger.info(f"第 {retry + 1} 次尝试访问职位详情页: {position_url}")
                self.driver.get(position_url)
                # 等待页面加载完成
                time.sleep(2)
                
                # 检查URL是否被重定向
                current_url = self.driver.current_url
                if current_url != position_url:
                    logger.error(f"URL被重定向，可能被反爬系统检测: {position_url} -> {current_url}")
                    if retry < max_retries - 1:
                        logger.info(f"等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        continue
                    sys.exit(1)
                
                # 模拟用户行为
                self._simulate_user_behavior()
                
                # 等待并获取包含职位数据的script标签
                try:
                    script_element = self.wait.until(
                        EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
                    )
                    json_data = script_element.get_attribute('textContent')
                    if not json_data:
                        logger.error(f"未找到职位数据: {position_url}")
                        if retry < max_retries - 1:
                            logger.info(f"等待 {retry_delay} 秒后重试...")
                            time.sleep(retry_delay)
                            continue
                        return None
                    
                    # 解析JSON数据
                    data = json.loads(json_data)
                    
                    # 提取职位详情数据
                    job_data = data.get('props', {}).get('pageProps', {}).get('jobDetailInfo', {})
                    if job_data.get('isPageError',False):
                        # 说明职业已经下架
                        logger.error(f"职位数据下架: {position_url}")
                        return None
                    if not job_data:
                        logger.error(f"职位数据格式异常: {position_url}")
                        if retry < max_retries - 1:
                            logger.info(f"等待 {retry_delay} 秒后重试...")
                            time.sleep(retry_delay)
                            continue
                        return None
                    
                    # 构建职位详情数据
                    job_detail = job_data.get('job')                    
                    
                    logger.info(f"成功解析职位详情数据: {position_url}")
                    return job_detail
                    
                except TimeoutException:
                    logger.error(f"等待职位数据超时: {position_url}")
                    if retry < max_retries - 1:
                        logger.info(f"等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        continue
                    return None
                except json.JSONDecodeError:
                    logger.error(f"解析职位数据JSON失败: {position_url}")
                    if retry < max_retries - 1:
                        logger.info(f"等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        continue
                    return None
                except Exception as e:
                    logger.error(f"处理职位数据失败: {position_url}, 错误: {str(e)}")
                    if retry < max_retries - 1:
                        logger.info(f"等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        continue
                    return None
                
            except Exception as e:
                logger.error(f"获取职位详情数据失败: {position_url}, 错误: {str(e)}")
                if retry < max_retries - 1:
                    logger.info(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    continue
                return None        
        return None

    def _simulate_user_behavior(self) -> None:
        """模拟用户行为"""
        try:
            # 获取页面高度
            page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            logger.info(f"页面高度: {page_height}")
            
            # 随机滚动几次
            scroll_times = random.randint(1, 3)
            for i in range(scroll_times):
                # 随机滚动位置
                scroll_position = random.randint(300, page_height - 200)
                self.driver.execute_script(f"window.scrollTo(0, {scroll_position})")
                time.sleep(random.uniform(1, 1.5))
                
        except Exception as e:
            logger.warning(f"模拟用户行为失败: {e}")

    def _save_job_detail(self, job_detail: Dict) -> None:
        """保存职位详情数据到MongoDB
        
        Args:
            job_detail: 职位详情数据
        """
        try:
            if not job_detail:
                return
                
            # 添加爬取时间
            job_detail['crawl_time'] = datetime.now()
            
            # 保存数据
            self.collection.insert_one(job_detail)
            logger.info(f"职位详情数据保存成功")
            
        except BulkWriteError as bwe:
            logger.error(f"批量写入出错: {str(bwe.details)}")
        except Exception as e:
            logger.error(f"保存职位详情数据失败: {str(e)}")

    def _save_url_log(self, position_url: str, status: str) -> None:
        """保存URL处理日志
        
        Args:
            position_url: 处理的URL
            status: 处理状态
        """
        try:
            log_data = {
                'positionUrl': position_url,
                'status': status,
                'create_time': datetime.now()
            }
            
            self.progress_collection.insert_one(log_data)
            
            # 更新内存中的缓存
            self.processed_urls[position_url] = 1
        except Exception as e:
            logger.error(f"保存URL处理日志失败: {str(e)}")

    def close(self) -> None:
        """关闭所有连接"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"关闭浏览器失败: {str(e)}")
                
        if self.mongo_client:
            try:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")
            except Exception as e:
                logger.error(f"关闭MongoDB连接失败: {str(e)}")

    def run(self) -> None:
        """运行爬虫"""
        try:
            # 初始化浏览器
            self.init_selenium()
            
            # 获取职位详情页URL列表
            urls = list(self.db[self.input_collection].find({}, {'_id': 0}))
            total_urls = len(urls)
            logger.info(f"获取到 {total_urls} 个职位详情页URL")
            
            # 创建进度条
            pbar = tqdm(total=total_urls, 
                       desc="爬取进度", 
                       unit="URL",
                       ncols=120,
                       bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
                       position=0,
                       leave=True)
            
            # 处理每个URL
            url_counter = 0
            for url_data in urls:
                try:
                    position_url = url_data.get('positionUrl')
                    if not position_url:
                        logger.error(f"URL数据缺少positionUrl字段: {url_data}")
                        pbar.update(1)
                        continue
                        
                    # 检查是否已处理
                    if position_url in self.processed_urls:
                        logger.info(f"跳过已处理的URL: {position_url}")
                        pbar.update(1)
                        continue
                    
                    # 更新进度条描述
                    pbar.set_description(f"正在处理: {position_url.split('/')[-1]}")
                    
                    # 每处理10个URL重启浏览器
                    url_counter += 1
                    if url_counter > 0 and url_counter % 10 == 0:
                        logger.info("已处理10个URL，准备重启浏览器...")
                        self.driver.quit()
                        self.init_selenium()
                        logger.info("浏览器重启完成")
                    
                    # 获取职位详情数据
                    job_detail = self._get_job_detail(position_url)
                    if job_detail:
                        # 保存职位详情数据
                        self._save_job_detail(job_detail)
                        self._save_url_log(position_url, 'success')
                    else:
                        self._save_url_log(position_url, 'error')
                    
                    # 更新进度条
                    pbar.update(1)
                    
                except Exception as e:
                    logger.error(f"处理URL失败: {position_url}, 错误: {str(e)}")
                    self._save_url_log(position_url, 'error')
                    # 发生错误时重启浏览器
                    self.driver.quit()
                    self.init_selenium()
                    pbar.update(1)
                    continue
                
                # 随机等待一段时间
                time.sleep(random.uniform(1, 3))
            
            # 关闭进度条
            pbar.close()
            logger.info("所有URL处理完成")
            
        except Exception as e:
            logger.error(f"运行出错: {str(e)}")
            raise
        finally:
            self.close()

def main():
    """主函数"""
    try:                
        # 创建爬虫实例，显式指定headless=False
        spider = LagouSpiderStep6(headless=False)
        # 运行爬虫
        spider.run()
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main() 
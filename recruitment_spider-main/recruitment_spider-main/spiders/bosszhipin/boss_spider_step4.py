import json
import logging
import os
import re
import sys
import time
import argparse
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import asyncio
import urllib.parse
from dotenv import load_dotenv
import aiohttp

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, UpdateOne
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

# 将项目根目录加入到工作路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
sys.path.append(project_root)

from recruitment_spider.spiders.base_spider import BaseSpider

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    # 配置日志，第一个参数是日志器名称，第二个参数是爬虫名称
    logger = get_logger(__name__, "boss_spider")
except ImportError:
    # 配置基本日志，以防日志管理模块未安装
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

# 设置调试模式
debug_mode = os.environ.get('DEBUG_MODE', '0') == '1'
if debug_mode:
    logger.setLevel(logging.DEBUG)
    logger.debug("BOSS直聘爬虫调试模式已启用")


class BossSpider(BaseSpider):
    """BOSS直聘爬虫，继承自BaseSpider"""
    name = 'boss_spider'
    
    def __init__(self, headless: bool = True, browser_count: int = 1, tabs_per_browser: int = 1, city: str = "全国", 
                 block_resources: bool = True, resource_filter_level: str = "medium", *args, **kwargs):
        super(BossSpider, self).__init__(
            headless=headless,
            browser_count=browser_count,
            tabs_per_browser=tabs_per_browser,
            city=city,
            block_resources=block_resources,
            resource_filter_level=resource_filter_level,
            *args, **kwargs
        )
        
        # 加载环境变量
        load_dotenv()
        
        # BOSS直聘特有配置
        # self.city_code = CITY_MAP.get(city, '100010000')  # 默认全国
        self.base_url = "https://www.zhipin.com"
        
        # MongoDB配置从环境变量读取
        self.mongo_uri = "mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test"
        self.mongo_db = "da_test"
        self.collection_name = "boss_job_raw_part1" #数据存储集合
        self.url_collection_name = f"boss_step2_urls_202504_log_part1"  # 已经爬取URL记录集合
        self.boss_urls_202504_part = "boss_step2_urls_part1"  # 需要爬取URL集合名称
        self.boss_urls = None  # 初始化为None，在init_db中设置
        self.mongo_client = None
        self.db = None
        
        # URL缓存字典
        self.crawled_urls = {}
        
        if not all([self.mongo_uri, self.mongo_db, self.collection_name]):
            raise ValueError("MongoDB配置信息不完整，请检查环境变量")
        # 上传者信息
        self.uploader = "单永旭"
                       
    
    async def init_browser(self):
        try:
            # 调用父类的初始化方法
            await super().init_browser()
            logger.info("浏览器初始化成功")            
            # 检查是否成功创建页面
            if not self.pages or len(self.pages) == 0:
                raise Exception("没有成功创建任何浏览器页面")
            return
            
        except Exception as e:                        
            # 确保关闭已创建的资源
            if hasattr(self, 'browsers') and self.browsers:
                for browser in self.browsers:
                    try:
                        await browser.close()
                    except:
                        pass
                        
            if hasattr(self, 'playwright') and self.playwright:
                try:
                    await self.playwright.stop()
                except:
                    pass
            
            # 重置资源列表
            self.playwright = None
            self.browsers = []
            self.contexts = []
            self.pages = []            
            logger.error("浏览器初始化失败，已达到最大重试次数")
            raise    
    
    async def run(self):
        """运行爬虫的主方法"""
        try:
            # 初始化数据库
            await self.init_db()
            logger.info("数据库初始化成功")
            
            # 初始化浏览器
            await self.init_browser()
            
            # 检查页面是否成功创建
            if not self.pages or len(self.pages) == 0:
                logger.error("没有可用的浏览器页面，请检查浏览器初始化是否成功")
                return
                
            logger.info(f"成功创建 {len(self.pages)} 个浏览器页面")
            
            # 访问登录页面，等待用户扫码登录
            login_url = "https://www.zhipin.com/web/user/?ka=header-login"
            logger.info(f"请访问 {login_url} 进行扫码登录")
            await self.pages[0].goto(login_url, wait_until='networkidle')
            
            # 点击验证码登录/注册的div，切换到扫码登录界面
            await self.pages[0].click('.switch-tip')
            
            # 等待用户登录成功
            try:
                # 等待最多5分钟，检查是否登录成功
                await asyncio.wait_for(
                    self.wait_for_login_success(self.pages[0]),
                    timeout=300
                )
                logger.info("登录成功，继续执行后续操作")
            except asyncio.TimeoutError:
                logger.error("登录超时，请重新运行程序")
                return
            except Exception as e:
                logger.error(f"登录过程发生错误: {str(e)}")
                return
            # 初始化计数器
            completed_jobs = 0
            skipped_jobs = 0
            
            # 使用分批处理获取URL
            batch_size = 1000  # 每批处理的数据量
            skip = 0  # 初始化skip值
            
            # 获取总数据量
            total_jobs = await self.db[self.boss_urls_202504_part].count_documents({})
            logger.info(f"总共需要处理 {total_jobs} 个岗位类型")
            
            while True:
                # 使用skip参数获取下一批数据
                cursor = self.db[self.boss_urls_202504_part].find().skip(skip).limit(batch_size)
                batch = await cursor.to_list(length=batch_size)
                
                if not batch:
                    break
                    
                for url in batch:
                    # 检查是否已经爬取过
                    if await self.is_url_crawled(url):
                        logger.info(f"URL已爬取过，跳过: {url['url']}")
                        skipped_jobs += 1
                        continue
                        
                    # 重新组装url:https://www.zhipin.com/wapi/zpgeek/search/joblist.json?page=1&pageSize=30&scene=1&city=101120100&industry=101105
                    page_index = (completed_jobs + skipped_jobs) % len(self.pages)
                    await self.process_job_type(url, page_index)
                    
                    # 更新完成数量
                    completed_jobs += 1
                    progress = ((completed_jobs + skipped_jobs) / total_jobs) * 100
                    logger.info(f"进度: {completed_jobs + skipped_jobs}/{total_jobs} ({progress:.2f}%) - 已完成: {completed_jobs}, 已跳过: {skipped_jobs}")
                
                # 更新skip值，准备获取下一批数据
                skip += batch_size
            
            logger.info(f"所有岗位类型处理完成 - 总共: {total_jobs}, 已完成: {completed_jobs}, 已跳过: {skipped_jobs}")
            
        except Exception as e:
            logger.error(f"爬虫运行出错: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            # 关闭浏览器和数据库连接
            await self.close_browser()
    
    async def process_job_type(self, url: dict, page_index: int = 0):
        """处理特定职位类型"""
        try:
            # 检查页面索引是否有效
            if page_index >= len(self.pages) or not self.pages[page_index]:
                logger.error(f"无效的页面索引: {page_index}, 当前页面数量: {len(self.pages)}")
                return
                
            page = self.pages[page_index]
            
            # 检查页面是否已关闭
            if page.is_closed():
                logger.error(f"页面已关闭，无法处理岗位类型: {url['industry_name']}, {url['job_type_name']}")
                return                        
                
            logger.info(f"处理行业: {url['industry_name']}, 代码: {url['industry_code']}, 岗位名称：{url['job_type_name']}, 代码: {url['job_type_code']}")
            
            # 获取职位列表
            job_list_data = await self.get_job_list(url, page)
            if job_list_data.get('code','') == 0:
                # 将数据存入mongodb
                await self.save_job_list_data(job_list_data)                
                # 构建基础字段
                base_fields = {                
                    'page': 1,  # 当前页码
                    'uploader': '单永旭',
                    'total_count': job_list_data['zpData'].get('totalCount', 0),
                    'has_more': job_list_data['zpData'].get('hasMore', False),
                    'filter_string': job_list_data['zpData'].get('filterString', ''),
                    'lid': job_list_data['zpData'].get('lid', '')
                }
                # 标记URL为已爬取
                await self.mark_url_crawled(url, base_fields, success=True)
                logger.info(f"{url['url']}成功爬取职位列表，共{job_list_data['zpData'].get('totalCount', 0)}个职位")                
            elif job_list_data.get('message') != 'Success':
                    logger.error(f"获取职位列表失败,IP被封禁,程序退出: {job_list_data.get('message')}")                    
                    # 程序退出
                    sys.exit(1)
            else:
                # 标记URL为爬取失败
                # await self.mark_url_crawled(url, base_fields, success=False)
                logger.warning(f"{url['url']}IP可能被封禁，本次请求失败")
            
        except Exception as e:
            logger.error(f"{url['url']}IP可能被封禁，本次请求失败,获取或处理职位列表失败: {str(e)}")
            # 标记URL为爬取失败
            # await self.mark_url_crawled(url['url'], base_fields, success=False)            
            import traceback
            logger.error(traceback.format_exc())
        
    
    async def handle_verify_code(self, page: Page) -> bool:
        """处理验证码"""
        try:
            # 检查页面是否存在验证码，verify-slider?callbackUrl=是否在url中
            if "verify" in page.url or "验证" in (await page.title()):
                logger.info("检测到验证码，开始处理")
                # 先点击“点击按钮进行验证”
                tip_btn = await page.query_selector('.geetest_radar_tip')
                if tip_btn:
                    await tip_btn.click()
                    await page.wait_for_timeout(500)  # 等待弹出验证码
                # 等待5秒，确保验证码弹出
                await page.wait_for_timeout(5000)
                verify_button = await page.wait_for_selector('.geetest_radar_btn', timeout=5000)
                if not verify_button:
                    logger.error("未找到验证按钮")
                    return False
                
                # 先检查是否是易盾验证码
                try:
                    yidun_button = await page.wait_for_selector('.yidun_intelli-control', timeout=5000)
                    if yidun_button:
                        logger.info("检测到易盾验证码，点击验证按钮")
                        await yidun_button.click()
                        # 等待验证完成（等待页面跳转）
                        try:
                            await page.wait_for_url("**/job_detail/**", timeout=30000)
                            logger.info("易盾验证完成，页面已跳转")
                            return True
                        except TimeoutError:
                            logger.error("易盾验证超时")
                            return False
                except TimeoutError:
                    # 如果不是易盾验证码，继续原有的极验验证码处理逻辑
                    pass
                
                # 原有的极验验证码处理逻辑
                # 先点击“点击按钮进行验证”
                tip_btn = await page.query_selector('.geetest_radar_tip')
                if tip_btn:
                    await tip_btn.click()
                    await page.wait_for_timeout(500)  # 等待弹出验证码

                verify_button = await page.wait_for_selector('.geetest_radar_btn', timeout=5000)
                if not verify_button:
                    logger.error("未找到验证按钮")
                    return False
                
                # 开始监听网络请求
                challenge_urls = set()
                async def handle_request(request):
                    if request.resource_type == 'image' and 'challenge' in request.url:
                        challenge_urls.add(request.url)
                        logger.info(f"捕获到验证码图片请求: {request.url}")
                
                # 添加请求监听器
                page.on('request', handle_request)
                
                # 点击验证按钮
                await verify_button.click()
                logger.info("已点击验证按钮")
                
                # 等待一段时间，确保捕获到所有请求
                await page.wait_for_timeout(2000)
                
                # 移除请求监听器
                page.remove_listener('request', handle_request)
                
                if challenge_urls:
                    logger.info(f"成功捕获到 {len(challenge_urls)} 个验证码图片请求")
                    image_url = challenge_urls.pop()
                    # 下载验证码图片
                    async with aiohttp.ClientSession() as session:
                        async with session.get(image_url) as response:
                            if response.status == 200:
                                # 确保目录存在
                                save_dir = "recruitment_spider/data/bosszhipin/captcha_images"
                                os.makedirs(save_dir, exist_ok=True)
                                # 使用年_月_日_时_分_秒的格式命名
                                current_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                                image_path = f"{save_dir}/verify_code_{current_time}.png"
                                with open(image_path, "wb") as f:
                                    f.write(await response.read())
                                logger.info(f"验证码图片已保存到: {image_path}")
                                # return True
                                return image_path
                else:
                    logger.error("未捕获到验证码图片请求")
                    return False
            elif "403.html" in page.url:
                logger.error("检测到403错误，请检查是否需要登录")
                # 对当前页面截图保存                
                current_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                image_name = f"recruitment_spider/data/bosszhipin/captcha_images/403_{current_time}.png"    
                await page.screenshot(path=image_name)
                logger.info(f"403错误页面截图已保存到: {image_name}")                
                return False
            else:
                logger.info("未检测到验证码")
                return False
                
        except Exception as e:
            logger.error(f"处理验证码时发生错误: {str(e)}")
            return False
    
    async def handle_verify_image(self, image_path: str):
        """处理验证码图片"""
        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(ignore_https_errors=True)
            page = await context.new_page()
            
            try:
                # 访问登录页面
                await page.goto("https://bq1gpmr8.xiaomy.net/account/loginPage/")
                
                # 输入用户名和密码
                await page.fill("#username", "shanyongxu")
                await page.fill("#password", "syx123456")
                
                # 点击同意协议复选框
                await page.click("#user_agreement_div .layui-form-checkbox")
                
                # 点击登录按钮并等待导航完成
                async with page.expect_navigation(timeout=10000) as navigation_info:
                    await page.click("#login_btn")
                    await navigation_info.value
                
                # 检查是否登录成功
                try:
                    # 等待URL变化
                    await page.wait_for_url("**/blog/blogPage/**", timeout=10000)
                    logger.info("登录成功，当前页面：" + page.url)
                except Exception as e:
                    logger.error(f"登录失败: {str(e)}")
                    return None
                
                # 直接跳转到验证码识别页面
                await page.goto("https://bq1gpmr8.xiaomy.net/tool/verifyCodeIdentifyPage/?verify_idf_id=69")
                
                # 等待页面加载完成
                try:
                    await page.wait_for_selector(".upload_img_div", timeout=10000)
                    logger.info("验证码识别页面加载完成")
                except Exception as e:
                    logger.error(f"等待页面加载超时: {str(e)}")
                    return None
                
                # 监听网络请求
                response_data = None
                
                async def handle_response(response):
                    nonlocal response_data
                    if "/tool/verify_code_identify/" in response.url:
                        try:
                            response_data = await response.json()
                            logger.info("成功获取响应数据")
                        except Exception as e:
                            logger.error(f"解析响应数据失败: {str(e)}")
                
                page.on("response", handle_response)
                
                # 上传文件
                try:
                    await page.set_input_files("input[type='file']", image_path)
                    logger.info("文件上传成功")
                except Exception as e:
                    logger.error(f"文件上传失败: {str(e)}")
                    return None
                
                # 点击识别按钮
                try:
                    await page.click("#img_submit")
                    logger.info("点击识别按钮成功")
                except Exception as e:
                    logger.error(f"点击识别按钮失败: {str(e)}")
                    return None
                
                # 等待XHR请求完成
                async with page.expect_response("**/tool/verify_code_identify/**") as response_info:
                    response = await response_info.value
                    if response.ok:
                        response_data = await response.json()
                        logger.info(f"识别结果：{response_data}")
                    else:
                        logger.error(f"请求失败：{response.status}")
                        return None
                
                return response_data
                
            except Exception as e:
                logger.error(f"登录过程中出现错误: {str(e)}")
                return None
            finally:
                # 关闭浏览器
                await page.close()
                await context.close()
                await browser.close()

    async def click_verify_positions(self, page: Page, positions: List[tuple]):
        """点击验证码图片上的指定位置"""
        try:
            # 等待验证码图片加载完成
            await page.wait_for_selector('.geetest_item_img', timeout=5000)
            
            # 获取所有验证码图片元素
            image_elements = await page.query_selector_all('.geetest_item')
            if not image_elements:
                logger.error("未找到验证码图片元素")
                return False
            
            # 获取第一个图片元素的位置和大小信息
            first_box = await image_elements[0].bounding_box()
            if not first_box:
                logger.error("无法获取验证码图片的位置信息")
                return False
            
            # 使用图片的实际尺寸
            img_width = 344  # 图片实际宽度
            img_height = 384  # 图片实际高度
            
            logger.info(f"使用图片实际尺寸: 宽度={img_width}, 高度={img_height}")
            
            # 计算每个格子的实际大小
            item_width = first_box['width']
            item_height = first_box['height']
            
            # 计算网格的行列数（3x3网格）
            grid_size = 3
            
            # 点击每个坐标位置
            for x, y in positions:
                # 计算坐标所在的格子位置
                grid_x = x // (img_width // grid_size)  # 使用图片实际宽度
                grid_y = y // (img_height // grid_size)  # 使用图片实际高度
                
                logger.info(f"坐标({x}, {y})映射到格子位置: ({grid_x}, {grid_y})")
                
                # 计算在网格中的索引
                grid_index = grid_y * grid_size + grid_x
                
                if grid_index < len(image_elements):
                    # 获取对应格子的元素
                    target_element = image_elements[grid_index]
                    
                    # 获取格子的位置信息
                    box = await target_element.bounding_box()
                    if box:
                        # 计算格子内的相对点击位置
                        relative_x = x % (img_width // grid_size)
                        relative_y = y % (img_height // grid_size)
                        
                        # 计算实际的点击位置
                        click_x = box['x'] + (relative_x * box['width'] / (img_width // grid_size))
                        click_y = box['y'] + (relative_y * box['height'] / (img_height // grid_size))
                        
                        # 移动鼠标到指定位置并点击
                        await page.mouse.move(click_x, click_y)
                        await page.mouse.click(click_x, click_y)
                        # 添加随机延迟，模拟人工操作
                        await asyncio.sleep(random.uniform(0.5, 1.5))
                        logger.info(f"点击位置: ({click_x}, {click_y})")
            
            # 点击确认按钮
            verify_button = await page.query_selector('.geetest_commit')
            if verify_button:
                await verify_button.click()
                logger.info("已点击确认按钮")
                # 等待验证结果
                await asyncio.sleep(2)
                return True
            else:
                logger.error("未找到确认按钮")
                return False
                
        except Exception as e:
            logger.error(f"点击验证码位置时发生错误: {str(e)}")
            return False

    async def get_job_list(self, url: dict, page: Page) -> List[Dict]:
        """获取职位列表"""
        max_retries = 3  # 最大重试次数
        retry_delay = 5  # 重试间隔（秒）
        
        for retry in range(max_retries):
            try:
                # 确保页面是活跃的
                logger.info(f"第 {retry + 1} 次尝试，确保页面处于活跃状态...")                
                # 设置请求监听
                job_list_data = None
                async def handle_request(request):
                    nonlocal job_list_data
                    if request.resource_type in ["xhr", "fetch"] and "joblist.json" in request.url:
                        logger.info(f"监听到职位列表请求: {request.method} {request.url}")
                        try:
                            # 获取响应
                            response = await request.response()
                            if response:
                                status = response.status
                                logger.info(f"响应状态码: {status}")
                                if status == 200:
                                    try:
                                        response_body = await response.text()
                                        response_data = json.loads(response_body)
                                        if response_data.get('code') == 0 and response_data.get('message').lower() == 'success':
                                            logger.info("获取到有效的职位列表数据")
                                            job_list_data = response_data
                                        else:
                                            logger.warning(f"响应内容不符合预期: {response_body}")
                                    except:
                                        logger.warning("无法解析响应内容")
                                else:
                                    logger.warning(f"请求返回非200状态码: {status}")
                        except Exception as e:
                            logger.warning(f"获取请求详情失败: {str(e)}")
                    elif request.resource_type in ["xhr", "fetch"] and "getUserInfo.json" in request.url:
                        logger.info(f"监听到获取用户信息请求: {request.method} {request.url}")
                        try:
                            response = await request.response()
                            if response:
                                status = response.status                                
                                logger.info(f"用户信息响应状态码: {status}")
                                if status == 200:
                                    try:
                                        response_body = await response.text()
                                        response_data = json.loads(response_body)
                                        if response_data.get('code') == 0:
                                            user_info = response_data.get('zpData', {})
                                            logger.info(f"用户信息:  {user_info}")
                                        else:
                                            # 如果登录用户失效，记录log，退出程序
                                            logger.error(f"登录状态失效: code={response_data.get('code')}, message={response_data.get('message')}")                                        
                                            sys.exit(1)
                                    except Exception as e:
                                        logger.warning(f"解析用户信息响应失败: {str(e)}")
                                else:
                                    logger.warning(f"获取用户信息请求返回非200状态码: {status}")
                        except Exception as e:
                            logger.warning(f"获取用户信息请求详情失败: {str(e)}")
                                                        
                                
                # 开始监听请求
                page.on('request', handle_request)                
                # 访问URL
                logger.info(f"正在访问URL: {url['url']}")
                try:                    
                    await page.goto(url['url'], wait_until='load', timeout=30000)
                    # 随机等待一段时间，模拟人类思考
                    await asyncio.sleep(random.uniform(4, 8))
                    
                    # 这里需要处理验证码的问题
                    is_verify_code = await self.handle_verify_code(page)
                    if is_verify_code:
                        logger.info("检测到验证码，正在处理验证")
                        # 获取检测目标图片的验证码坐标
                        deta_response = await self.handle_verify_image(is_verify_code)
                        if deta_response and deta_response.get('code') == 200:
                            try:
                                # 解析坐标字符串为坐标列表
                                positions_str = deta_response['data']['res_str']
                                # 移除首尾的方括号，并按逗号分割
                                positions_str = positions_str.strip('[]')
                                positions = []
                                for pos in positions_str.split('), ('):
                                    # 清理坐标字符串并转换为元组
                                    pos = pos.strip('()')
                                    x, y = map(int, pos.split(', '))
                                    positions.append((x, y))
                                
                                logger.info(f"解析后的验证码坐标: {positions}")
                                # 点击验证码坐标
                                success = await self.click_verify_positions(page, positions)
                                if success:
                                    logger.info("验证码处理成功")
                                    # 等待验证完成
                                    await asyncio.sleep(2)
                                else:
                                    logger.error("验证码处理失败")
                                    return False
                            except Exception as e:
                                logger.error(f"处理验证码坐标时发生错误: {str(e)}")
                                return False
                        else:
                            logger.error("获取验证码坐标失败")
                            return False
                    
                    # 检查页面是否成功加载
                    page_title = await page.title()
                    logger.info(f"页面标题: {page_title}")
                    
                    # 模拟人类浏览行为
                    # 1. 随机滚动页面
                    await page.evaluate("""
                    (async function() {
                        const scrollStep = Math.floor(Math.random() * 100) + 50;  // 50-150的随机步长
                        const scrollInterval = Math.floor(Math.random() * 200) + 100;  // 100-300ms的随机间隔
                        const scrollDuration = Math.floor(Math.random() * 2000) + 1000;  // 1-3秒的随机持续时间
                        const scrollCount = Math.floor(scrollDuration / scrollInterval);
                        
                        for (let i = 0; i < scrollCount; i++) {
                            window.scrollBy(0, scrollStep);
                            await new Promise(resolve => setTimeout(resolve, scrollInterval));
                        }
                    })();
                    """)
                    
                    # 2. 随机移动鼠标
                    await page.mouse.move(
                        random.randint(100, 800),
                        random.randint(100, 600)
                    )
                    # 增加更复杂的多点平滑移动鼠标操作，模拟人类曲线移动
                    points = [
                        (random.randint(100, 800), random.randint(100, 600)),
                        (random.randint(100, 800), random.randint(100, 600)),
                        (random.randint(100, 800), random.randint(100, 600))
                    ]
                    # 假设初始点为(0,0)，Playwright没有直接API获取当前鼠标位置
                    current_x, current_y = 0, 0
                    for x, y in points:
                        steps = 10
                        for i in range(1, steps + 1):
                            intermediate_x = current_x + (x - current_x) * i / steps
                            intermediate_y = current_y + (y - current_y) * i / steps
                            await page.mouse.move(intermediate_x, intermediate_y)
                            await asyncio.sleep(random.uniform(0.02, 0.08))
                        current_x, current_y = x, y
                    
                    # 3. 随机等待一段时间
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                    
                    # 检查页面内容是否加载
                    content = await page.content()
                    if not content:
                        logger.warning("页面内容为空")
                        if retry < max_retries - 1:
                            logger.info(f"等待 {retry_delay} 秒后重试...")
                            await asyncio.sleep(retry_delay)
                            continue
                        return False
                    
                    logger.info("页面加载成功")
                    
                except Exception as e:
                    logger.error(f"页面加载失败: {str(e)}")
                    if retry < max_retries - 1:
                        logger.info(f"等待 {retry_delay} 秒后重试...")
                        await asyncio.sleep(retry_delay)
                        continue
                    return False
                finally:
                    # 停止监听请求                    
                    page.remove_listener('request', handle_request)
                
                # 返回获取到的职位列表数据
                if job_list_data:
                    return job_list_data
                else:
                    if retry < max_retries - 1:
                        logger.info(f"未获取到有效数据，等待 {retry_delay} 秒后重试...")
                        await asyncio.sleep(retry_delay)
                        continue
                    return False
                
            except Exception as e:
                logger.error(f"请求失败: {str(e)}")
                if retry < max_retries - 1:
                    logger.info(f"等待 {retry_delay} 秒后重试...")
                    await asyncio.sleep(retry_delay)
                    continue
                return False
        
        return False
                

    async def init_db(self):
        """初始化MongoDB连接"""
        try:
            # 创建MongoDB客户端连接
            self.mongo_client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            
            # 测试连接
            await self.db.command("ping")
            logger.info("MongoDB连接成功")
            
            # 创建索引
            collection = self.db[self.collection_name]
            await collection.create_index([("encryptJobId", ASCENDING)], unique=True)
            
            # 创建URL集合的索引
            url_collection = self.db[self.url_collection_name]
            # 删除旧的索引
            try:
                await url_collection.drop_indexes()
            except:
                pass
            # 创建新的索引，使用URL作为唯一标识
            await url_collection.create_index([("url", ASCENDING)], unique=True)
            await url_collection.create_index([("crawl_time", ASCENDING)])
            
            # 初始化boss_urls集合
            self.boss_urls = self.db[self.boss_urls_202504_part]
            
            # 加载已爬取的URL到缓存
            await self.load_crawled_urls()
            
            logger.info("MongoDB索引创建成功")
            
        except Exception as e:
            logger.error(f"MongoDB连接失败: {str(e)}")
            raise

    async def load_crawled_urls(self):
        """
        从数据库加载所有已爬取的URL到内存中
        """
        try:
            url_collection = self.db[self.url_collection_name]
            cursor = url_collection.find(
                {},
                {"_id": 0, "crawl_time": 0, "job_count": 0,'success':0,}
            )
            
            self.crawled_urls.clear()
            async for doc in cursor:
                self.crawled_urls[f'{doc["city_code"]}-{doc["job_type_code"]}-{doc["industry_code"]}'] = 1
            
            logger.info(f"已加载 {len(self.crawled_urls)} 个已爬取的URL到缓存")
        except Exception as e:
            logger.error(f"加载已爬取URL失败: {str(e)}")
            self.crawled_urls = {}

    async def is_url_crawled(self, url: dict) -> bool:
        """检查URL是否已经爬取过"""
        return f"{url.get('city_code','')}-{url.get('job_type_code','')}-{url.get('industry_code','')}" in self.crawled_urls

    async def mark_url_crawled(self, url: dict, base_fields: dict, success: bool = True):
        """标记URL为已爬取"""
        try:            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')            
            url_collection = self.db[self.url_collection_name]
            document = {
                "url": url['url'],
                "crawl_time": current_time,
                "success": success,
                "industry_code": url.get('industry_code',''),
                "industry_name": url.get('industry_name',''),
                "job_type_code": url.get('job_type_code',''),
                "job_type_name": url.get('job_type_name',''),
                "city_code": url.get('city_code',''),
                "city_name": url.get('city_name',''),
                **base_fields
            }
            await url_collection.update_one(
                {"url": url['url']},
                {"$set": document},
                upsert=True
            )
        except Exception as e:
            logger.error(f"标记URL状态失败: {str(e)}")
    

    async def close_spider(self):
        """关闭爬虫时的清理操作"""
        try:
            if self.mongo_client:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")
        except Exception as e:
            logger.error(f"关闭MongoDB连接失败: {str(e)}")

    async def wait_for_login_success(self, page):
        """等待登录成功的标志出现"""
        while True:
            try:
                if "login" in page.url:
                    await asyncio.sleep(5)
                else:
                    return True
            except:
                return True

    async def save_job_list_data(self, job_list_data: dict):
        """保存职位列表数据到MongoDB
        
        Args:
            job_list_data: 职位列表数据，包含code、message、zpData等字段
        """
        try:
            if not job_list_data or not job_list_data.get('zpData', {}).get('jobList'):
                logger.warning("没有职位数据需要保存")
                return
                
            # 获取职位列表
            job_list = job_list_data['zpData']['jobList']
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 准备批量插入的数据
            bulk_operations = []
            for job in job_list:
                # 构建基础字段
                base_fields = {
                    'create_time': current_time,
                    'page': 1,  # 当前页码
                    'uploader': '单永旭',
                    # 'total_count': job_list_data['zpData'].get('totalCount', 0),
                    # 'has_more': job_list_data['zpData'].get('hasMore', False),
                    # 'filter_string': job_list_data['zpData'].get('filterString', ''),
                    # 'lid': job_list_data['zpData'].get('lid', '')
                }
                
                # 合并职位数据和基础字段
                job_data = {**job, **base_fields}
                
                # 使用encryptJobId作为唯一标识
                bulk_operations.append(
                    UpdateOne(
                        {'encryptJobId': job['encryptJobId']},
                        {'$set': job_data},
                        upsert=True
                    )
                )
            
            if bulk_operations:
                # 执行批量更新
                result = await self.db[self.collection_name].bulk_write(bulk_operations)
                logger.info(f"成功保存 {len(bulk_operations)} 条职位数据，"
                          f"插入: {result.upserted_count}, "
                          f"更新: {result.modified_count}")
            else:
                logger.warning("没有职位数据需要保存")
                
        except Exception as e:
            logger.error(f"保存职位列表数据失败: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

# 解析命令行参数
def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='BOSS直聘爬虫')
    parser.add_argument('--headless', action='store_true', default=False,
                        help='是否使用无头模式运行浏览器（默认：否）')
    parser.add_argument('--browser-count', type=int, default=1,
                        help='浏览器实例数量（默认：1）')
    parser.add_argument('--tabs-per-browser', type=int, default=1,
                        help='每个浏览器的标签页数量（默认：1）')
    parser.add_argument('--city', type=str, default='全国',
                        help='搜索城市（默认：全国）')
    parser.add_argument('--debug', action='store_true',
                        help='启用调试模式')
    return parser.parse_args()

# 主函数
async def main():
    """主函数"""
    try:
        # 使用环境变量或默认值
        headless = os.environ.get('HEADLESS', 'false').lower() == 'true'
        browser_count = int(os.environ.get('BROWSER_COUNT', '1'))
        tabs_per_browser = int(os.environ.get('TABS_PER_BROWSER', '1'))
        city = os.environ.get('CITY', '全国')
        
        # 设置调试模式
        debug_mode = os.environ.get('DEBUG_MODE', '0') == '1'
        if debug_mode:
            logger.setLevel(logging.DEBUG)
            logger.debug("调试模式已启用")
        
        logger.info(f"启动参数: 浏览器数量={browser_count}, 每个浏览器标签页数量={tabs_per_browser}, "
                   f"无头模式={headless}, 城市={city}")
        
        # 创建爬虫实例
        spider = BossSpider(
            headless=headless,
            browser_count=browser_count,
            tabs_per_browser=tabs_per_browser,
            city=city,
            resource_filter_level="low"
        )
        
        # 运行爬虫
        await spider.run()
        
    except Exception as e:
        logger.error(f"爬虫运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    

if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main()) 
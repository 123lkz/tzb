import logging
import random
import re
import json
import asyncio, time
from playwright.async_api import Page, TimeoutError as PWTimeout
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from playwright.async_api import Page
from pymongo import MongoClient

from recruitment_spider.spiders.base_spider import BaseSpider
from recruitment_spider.utils.log_manager import get_logger

# 设置日志
logger = get_logger(__name__, "liepin_spider")
# 猎聘常见的安全验证选择器（可自行补充）
SECURITY_SELECTORS = [
    '.geetest_panel', '.geetest_box', '.geetest_radar_tip',
    '.nc-container', '.nc-lang-cnt',
    'text="安全验证"', 'text="请完成安全验证"', 'text="滑动验证"'
]


async def simulate_user_behavior(page: Page) -> None:
    """
    进入列表页后模拟真实用户的随机操作，降低反爬概率：
      • 随机移动鼠标 2-4 次
      • 随机小幅滚动 3-5 次（偶尔回到顶部）
      • 随机停顿
      • 再做 3-5 次平滑大滚动
      • 鼠标悬停在导航元素上
    """
    try:
        # ---------- 鼠标随机移动 ----------
        for _ in range(random.randint(2, 4)):
            await page.mouse.move(
                random.randint(100, 800),
                random.randint(100, 600)
            )
            await asyncio.sleep(random.uniform(0.1, 0.3))

        # ---------- 小幅随机滚动 ----------
        for _ in range(random.randint(3, 5)):
            dist = random.randint(100, 300)
            await page.evaluate(f'window.scrollBy(0, {dist})')
            await asyncio.sleep(random.uniform(0.5, 0.7))

        # ---------- 偶尔回到顶部 ----------
        if random.random() < 0.3:
            await page.evaluate('window.scrollTo(0, 0)')
            await asyncio.sleep(random.uniform(0.1, 1))

        # ---------- 随机暂停 ----------
        await asyncio.sleep(random.uniform(0.5, 1.0))

        # ---------- 多段平滑滚动 ----------
        page_height = await page.evaluate('() => document.documentElement.scrollHeight')
        for _ in range(random.randint(3, 5)):
            top = random.randint(100, max(100, page_height - 100))
            await page.evaluate(f'''
                window.scrollTo({{
                    top: {top},
                    behavior: 'smooth'
                }});
            ''')
            await asyncio.sleep(random.uniform(1, 1.2))

        # ---------- 鼠标悬停 ----------
        nav_items = await page.query_selector_all('.header-quick-menu-box')
        if nav_items:
            await random.choice(nav_items).hover()
            await asyncio.sleep(random.uniform(1, 1.3))

    except Exception as e:
        logger.warning(f"模拟用户行为时出错: {e}")
    # 最后再随机停一下
    await asyncio.sleep(random.uniform(1.5, 2))
async def handle_security_popup(page: Page, logger, wait_timeout: int = 120_000) -> None:
    """
    若检测到猎聘安全验证弹窗，则提醒用户手动处理并阻塞直到验证码消失或超时
    """
    for sel in SECURITY_SELECTORS:
        if await page.query_selector(sel):
            logger.warning("⚠️  检测到猎聘安全验证弹窗，需要人工滑动验证。")
            # 可选：保存截图方便核对
            #shot = f"captcha_{int(time.time())}.png"
            #await page.screenshot(path=shot, full_page=True)
            #logger.warning(f"已保存验证截图：{shot}")

            # 等用户处理；input 会阻塞事件循环 → 放到线程里
            await asyncio.to_thread(input, "👉  在打开的浏览器中完成验证后，按 <Enter> 继续 …… ")

            # 再次检查弹窗是否已关闭
            try:
                await page.wait_for_function(
                    """() => !document.querySelector(
                        '.geetest_panel,.geetest_box,.geetest_radar_tip, \
                        .nc-container,.nc-lang-cnt')""",
                    timeout=wait_timeout
                )
                logger.info("✅  安全验证已通过，继续爬取。")
            except PWTimeout:
                raise RuntimeError("等待用户验证超时，放弃当前页面。")
            break

class LiepinSpider(BaseSpider):
    """猎聘网爬虫，继承自BaseSpider，支持断点续爬并记录进度到MongoDB"""
    name = 'liepin_spider'

    def __init__(
        self,
        headless: bool = False,
        browser_count: int = 1,
        tabs_per_browser: int = 1,
        city: str = "全国",
        block_resources: bool = True,
        resource_filter_level: str = "medium",
        *args,
        **kwargs
    ):
        super().__init__(
            headless=headless,
            browser_count=browser_count,
            tabs_per_browser=tabs_per_browser,
            city=city,
            block_resources=block_resources,
            resource_filter_level=resource_filter_level,
            *args,
            **kwargs
        )
        self.cookie_raw = (
            "__uuid=1740119551046.14; __gc_id=1700ca40fe3e4469b02c91e294d98dc8; "
            "need_bind_tel=false; _ga=GA1.1.159827211.1740126958; _clck=14kec9q%7C2%7Cftp%7C0%7C1878; "
            "new_user=false; c_flag=33916466dbef7155af1ea3f9541cae47; imId=4939a3ed0739e18aaeee0209628fef64; "
            "imClientId=4939a3ed0739e18a6446a6d1ef9dc5d9; _uetvid=a12d0650f01d11efb7eaeffe16205256; "
            "HMACCOUNT=154ED5DBBDF21669; XSRF-TOKEN=PBLCWQPzR5uyjITdMHm7ww; "
            "Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1744792347,1745388496,1745508673; "
            "Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1745595941"
        )
        # 页面与文件路径
        self.base_url = "https://www.liepin.com"
        self.province_type_code_path = Path(
            "recruitment_spider/data/liepin/province_type_code.json"
        )

        # 爬虫节流配置
        self.min_delay = random.uniform(2, 4)
        self.max_delay = random.uniform(4, 6)

        # 上传者信息
        self.uploader = "郭沛翰"

        # MongoDB 配置
        self.mongo_uri = (
            "mongodb://voc:34hDGwge98hER4lsdv2@210.14.140.50:10387/voc_data"
        )
        self.mongo_db = "voc_data"
        self.urls_collection_name = "liepin_urls_part4"
        self.progress_collection_name = "liepin_urls_202504_log_part4"
        self.data_collection_name = "liepin_job_raw_part4"
        self.crawled: Dict[str, bool] = {}

        # 初始化 MongoDB
        self._init_mongodb()
        # 加载已爬进度
        self._load_progress()


    def _init_mongodb(self):
        client = MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        self.urls_collection = db[self.urls_collection_name]
        self.progress_collection = db[self.progress_collection_name]
        self.data_collection = db[self.data_collection_name]
        logger.info("MongoDB 连接成功")

    def _load_progress(self):
        for doc in self.progress_collection.find({}, {"url": 1}):
            self.crawled[doc["url"]] = True
        logger.info(f"已加载 {len(self.crawled)} 条进度记录")

    def is_crawled(self, url: str) -> bool:
        return self.crawled.get(url, False)

    async def init_db(self):
        return

    # ====================== LiepinSpider 里覆写的 init_browser ======================
    async def init_browser(self):
        """
        1. 先执行 BaseSpider 的 init_browser() —— 创建 browser / context / page
        2. 给所有 context 同步三套域的登陆 Cookie（.liepin.com - www.liepin.com - wow.liepin.com）
        3. 默认把 XSRF-TOKEN 和 Referer 写进请求头
        4. 做一次首跳检测：若仍被 302 到 wow 登录页，说明 Cookie 已失效
        """
        # ---------------- ① 基础浏览器资源 ----------------
        await super().init_browser()  # ← 这行别删，父类里会产生 self.contexts / self.pages

        # ---------------- ② 需要注入的原始 Cookie ----------------
        cookie_raw = """
   __uuid=1740119551046.14; __gc_id=1700ca40fe3e4469b02c91e294d98dc8; need_bind_tel=false; _ga=GA1.1.159827211.1740126958; _clck=14kec9q%7C2%7Cftp%7C0%7C1878; new_user=false; c_flag=33916466dbef7155af1ea3f9541cae47; imId=4939a3ed0739e18aaeee0209628fef64; imId_0=4939a3ed0739e18aaeee0209628fef64; imClientId=4939a3ed0739e18a6446a6d1ef9dc5d9; imClientId_0=4939a3ed0739e18a6446a6d1ef9dc5d9; _uetvid=a12d0650f01d11efb7eaeffe16205256; _uetmsclkid=_uet2c5a17e1e51516ba8674701e80b03408; __tlog=1745508670534.27%7C00000000%7C00000000%7C00000000%7C00000000; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1744792347,1745388496,1745508673; HMACCOUNT=154ED5DBBDF21669; XSRF-TOKEN=PBLCWQPzR5uyjITdMHm7ww; _ga_54YTJKWN86=GS1.1.1745674168.39.1.1745674168.0.0.0; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1745674170; acw_tc=1a0c65d317457323429552228e010c0d5d27973d2569eec27525b86617c2e6; fe_se=-1745732352472; UniqueKey=0e6f24364538435a6bc56763ae71c6f2; liepin_login_valid=0; lt_auth=vukJOCZQylr55CGKjmZZsvkc3Nv8UTjM8S4OhxhWh4W7WPDn4P%2FqQg6Dq7cE%2BCoIq09yf60zMLf6MO%2F9y3BM40Ib%2BFGnn5yuv%2F6%2Fz3wCUeFiHuyflMXuqsjQQ5wtrXo6ykpgn2siwUnO; access_system=C; user_roles=0; user_photo=5f8fa3a6f6d1ab58476f322808u.png; user_name=%E9%83%AD%E6%B2%9B; inited_user=8952b102575b7217dc289aa0a0a4d581; __session_seq=23; __tlg_event_seq=69; imApp_0=1; fe_im_socketSequence_new_0=1_1_1; fe_im_connectJson_0=%7B%220_0e6f24364538435a6bc56763ae71c6f2%22%3A%7B%22socketConnect%22%3A%223%22%2C%22connectDomain%22%3A%22liepin.com%22%7D%7D; fe_im_opened_pages=
    """.strip()

        def build_cookie_objs(domain: str):
            cookies = []
            for kv in cookie_raw.split(";"):
                if "=" not in kv:
                    continue
                name, value = kv.strip().split("=", 1)
                cookies.append({
                    "name": name,
                    "value": value,
                    "domain": domain,
                    "path": "/",
                    "expires": -1  # 会话 cookie
                })
            return cookies

        # 三份域：根域  +  www  +  wow
        domains = [".liepin.com", "www.liepin.com", "wow.liepin.com"]
        all_cookies = sum([build_cookie_objs(d) for d in domains], [])

        # 把 XSRF-TOKEN 挑出来备用
        xsrf_val = next((c["value"] for c in all_cookies if c["name"] == "XSRF-TOKEN"), "")

        # ---------------- ③ 注入 cookie & 额外请求头 + 绑定监听器 ----------------
        # >>> 修改开始
        for ctx in self.contexts:
            await ctx.add_cookies(all_cookies)
            await ctx.set_extra_http_headers({
                "Referer": "https://www.liepin.com/",
                "XSRF-TOKEN": xsrf_val,
                "X-Requested-With": "XMLHttpRequest"
            })
            ctx.on(
                "response",
                lambda resp, ctx=ctx: asyncio.create_task(
                    self._response_cookie_watcher(resp)
                )
            )

        logger.info("🍪  已向所有 BrowserContext 注入 Cookie，并绑定自动刷新监听器")


        # ---------------- ④ 首跳检测：确认职位页是否还会被 302 ----------------
        try:
            test_page = self.pages[0]  # BaseSpider 至少创建了一个 page
            resp = await test_page.goto(
                "https://www.liepin.com/zhaopin/?city=010&dq=010",  # 任意职位搜索页
                wait_until="domcontentloaded"
            )
            final_url = resp.url if resp else test_page.url

            if "wow.liepin.com/t101" in final_url:
                logger.warning("⚠️  Cookie 仍被风控拦截 —— 访问职位页被 302 到登录/校验页")
            else:
                # 页面里是否还有 “登录 / 注册” 文案
                login_node = await test_page.query_selector('a:has-text("登录")')
                if login_node:
                    logger.warning("⚠️  职位页加载成功，但检测到未登录文案，Cookie 可能已失效")
                else:
                    logger.info("✅  Cookie 检测通过：职位页保持登录状态")
        except Exception as e:
            logger.error(f"首跳检测失败: {e}")

    # ===============================================================================
    async def run(self):
        try:
            await self.init_db()
            logger.info("数据库初始化成功")
            await self.init_browser()
            if not self.pages:
                logger.error("浏览器页面未初始化")
                return

            # 如果 URL 集合为空，自动生成并插入
            existing = await asyncio.to_thread(self.urls_collection.count_documents, {})
            if existing == 0:
                urls = self.build_search_urls()
                await asyncio.to_thread(
                    self.urls_collection.insert_many,
                    [{'url': u} for u in urls]
                )
                logger.info(f"插入 {len(urls)} 条待爬 URL 到集合")

            # 加载已爬进度
            crawled_docs = await asyncio.to_thread(
                lambda: list(self.progress_collection.find({}, {'url': 1}))
            )
            self.crawled = {doc['url']: True for doc in crawled_docs}

            # 构建待爬列表
            all_docs = await asyncio.to_thread(
                lambda: list(self.urls_collection.find({}, {'url': 1}))
            )
            pending = [d['url'] for d in all_docs if not self.crawled.get(d['url'], False)]
            total = len(pending)
            logger.info(f"待爬 URL 总数（未完成）：{total}")
            completed = 0

            for url in pending:
                try:
                    # -------- 1. 抓取 --------
                    jobs, blocked = await self.get_job_list(url, self.pages[0])
                    # 过滤 None / 无效条目
                    real_jobs = [j for j in jobs if j]
                    job_count = len(real_jobs)

                    # 规则：只要不是 blocked 就算 success
                    success = not blocked

                except Exception as e:
                    logger.error(f"[抓取异常] {url} -> {e}")
                    jobs, job_count, success = [], 0, False

                # -------- 2. 保存岗位数据 --------
                if real_jobs:
                    processed = [self.process_job_data(job) for job in real_jobs]
                    await asyncio.to_thread(self.data_collection.insert_many, processed)

                # -------- 3. 写入进度集合 --------
                from urllib.parse import urlparse, parse_qs
                qs = parse_qs(urlparse(url).query)
                city_code = (qs.get("city") or qs.get("dqs") or [""])[0]
                industry_code = (qs.get("industryType") or qs.get("industry") or [""])[0]

                await asyncio.to_thread(
                    self.progress_collection.insert_one,
                    {
                        "url": url,
                        "crawl_time": datetime.now(),
                        "job_count": job_count-2,
                        "city_code": city_code,
                        "industry_code": industry_code,
                        "success": success
                    }
                )

                # -------- 4. 进度日志与状态更新 --------
                self.crawled[url] = True
                completed += 1
                logger.info(f"已完成 {completed}/{total} —— 本页 {job_count-2} 条, success={success}")
                # ---------- 新增保险：若被风控则强制休眠 40 分钟 ----------
                if blocked:
                    logger.warning("⚠️  连续出现 Whitelabel/flag=0，暂停 40 分钟后重试 …")
                    await asyncio.sleep(40 * 60)  # 40 min = 2400 s
                    continue  # 跳到下一轮 while
                # 每处理 40 个 URL，强制休眠 5 分钟
                if completed % 40 == 0 and completed < total:
                    logger.info("🌙  已抓取 50 个 URL，休息 5 分钟避免触发反爬 ...")
                    await asyncio.sleep(40)  # 300 秒 = 5 分钟

        except Exception as e:
            logger.error(f"爬虫运行出错: {e}")
        finally:
            await self.close_browser()

    async def get_job_list(self, url: str, page: Page) -> tuple[list[Dict], bool]:
        """
        返回 (jobs, blocked)
        ─────────────────────
        jobs      : 抓取到的岗位列表（可能为空）
        blocked   : 是否被风控（flag=0 / 302 wow 登录页 / 连续超时…）
        """
        max_retries, retry = 4, 0
        while retry < max_retries:
            try:
                resp = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await handle_security_popup(page, logger)

                # 302 重定向到 wow 登录页 → 视为风控
                if resp and "wow.liepin.com/t101" in resp.url:
                    logger.warning(f"[风控] 302 to wow login ({retry+1}/{max_retries})")
                    raise RuntimeError("redirected")

                html = await page.content()
                if '"flag":0' in html or "Whitelabel Error Page" in html:
                    logger.warning(f"[风控] flag=0 白页 ({retry+1}/{max_retries})")
                    raise RuntimeError("flag0")

                # ---------- 页面真的没有职位 ----------
                try:
                    await page.wait_for_selector(".ant-empty-description", timeout=2_000)
                    txt = await page.eval_on_selector(
                        ".ant-empty-description", "el=>el.textContent.trim()")
                    if "没有合适的职位" in txt:
                        logger.info(f"[空页面] {url}")
                        return [], False               # ☆ 0 条职位 ≠ 风控
                except PWTimeout:
                    pass

                # ---------- 正常抓取 ----------
                await simulate_user_behavior(page)
                await page.wait_for_selector(".job-list-box", timeout=10000)

                jobs = []
                for card in await page.query_selector_all(".job-card-pc-container"):
                    if await card.query_selector(".ad-flag-box"):
                        continue
                    info = await self._extract_job_info(card)
                    if info:
                        jobs.append(info)
                return jobs, False                   # ☆ blocked=False

            except Exception as e:
                retry += 1
                logger.error(f"[重试] {url} -> {e}  ({retry}/{max_retries})")
                await asyncio.sleep(min(300, 2 ** retry + random.uniform(2, 5)))

        # 连续失败算风控
        logger.error(f"[放弃] 连续 {max_retries} 次失败: {url}")
        return [], True
    async def _extract_job_info(self, job_card) -> Dict:
        # 提取核心字段，包括 refreshTime
        try:
            link = await job_card.query_selector(
                'a[data-nick="job-detail-job-info"]'
            )
            if not link:
                return None
            href = await link.get_attribute("href")
            job_url = href if href.startswith("http") else f"{self.base_url}{href}"
            job_id = None
            for pat in [r"lptjob/(\d+)", r"job/(\d+)\.shtml", r"a/(\d+)\.shtml"]:
                m = re.search(pat, job_url)
                if m:
                    job_id = m.group(1)
                    break

            title_elem = await job_card.query_selector(
                ".job-title-box .ellipsis-1"
            )
            title = (await title_elem.get_attribute("title")) if title_elem else ""
            title = title[2:] if title.startswith("招聘") else title
            title = re.sub(r"\([A-Z0-9]+\)$", "", title).strip()

            salary_elem = await job_card.query_selector(".job-salary")
            salary = (await salary_elem.text_content()) if salary_elem else "面议"

            location_elem = await job_card.query_selector(
                ".job-dq-box .ellipsis-1"
            )
            location = (await location_elem.text_content()).strip("【】") if location_elem else ""

            labels = await job_card.query_selector_all(".labels-tag")
            txts, tags = [], []
            for lb in labels:
                txt = (await lb.text_content()).strip()
                txts.append(txt)
                if not any(k in txt for k in ["年","本科","大专","硕士","博士","经验","学历"]):
                    tags.append(txt)
            experience = next((x for x in txts if "年" in x), "经验不限")
            education = next(
                (x for x in txts if any(e in x for e in ["本科","硕士","博士"])),
                "学历不限"
            )

            comp_link = await job_card.query_selector(
                'a[data-nick="job-detail-company-info"]'
            )
            comp_href = (await comp_link.get_attribute("href")) if comp_link else ""
            company_url = comp_href if comp_href.startswith("http") else f"{self.base_url}{comp_href}"
            cn_elem = await job_card.query_selector(".company-name")
            company_name = (await cn_elem.text_content()) if cn_elem else ""
            comp_tags = []
            ct_box = await job_card.query_selector(".company-tags-box")
            if ct_box:
                for sp in await ct_box.query_selector_all('span'):
                    comp_tags.append((await sp.text_content()).strip())
            industry = comp_tags[0] if len(comp_tags) > 0 else ""
            stage = comp_tags[1] if len(comp_tags) > 1 else ""
            size = comp_tags[2] if len(comp_tags) > 2 else ""

            rec_name_elem = await job_card.query_selector(".recruiter-name")
            rec_name = (await rec_name_elem.text_content()) if rec_name_elem else ""
            rec_title_elem = await job_card.query_selector(".recruiter-title")
            rec_title = (await rec_title_elem.text_content()) if rec_title_elem else ""
            hr_active = "高回复率"
            rec_box = await job_card.query_selector(".recruiter-info-box")
            if rec_box and 'recruiter-offline' in (await rec_box.get_attribute('class')):
                hr_active = '离线'



            return {
                'job_id': job_id,
                'title': title,
                'salary': salary,
                'location': location,
                'experience': experience,
                'education': education,
                'company_name': company_name,
                'company_url': company_url,
                'company_industry': industry,
                'company_development_stage': stage,
                'company_size': size,
                'job_tags': tags,
                'recruiter_name': rec_name,
                'recruiter_title': rec_title,
                'hr_active': hr_active,
                'job_url': job_url,
                'source': 'liepin',
                'refreshTime': ''
            }
        except Exception as e:
            logger.error(f"提取职位信息出错: {e}")
            return None

    async def _response_cookie_watcher(self, resp):
        """
        捕获 liepin.com 响应里的 Set-Cookie。
        若发现 XSRF-TOKEN / lt_auth / UniqueKey 有更新：
            1) 同步到所有 BrowserContext
            2) 顺便刷新默认请求头里的 XSRF-TOKEN
        """
        try:
            # 1. 只处理 liepin 站内请求
            if "liepin.com" not in resp.url:
                return

            # 2. 拿原始 Set-Cookie 字符串（Playwright ≥1.40 headers 是 Mapping[str, str]）
            sc_str = resp.headers.get("set-cookie")  # 可能为 None / "" / 单条 / 多条
            if not sc_str:
                return
            sc_list = sc_str.split(", ")  # 多条用逗号+空格分隔

            # 3. 解析我们关心的几个键
            watched = ("XSRF-TOKEN", "lt_auth", "UniqueKey")
            new_cookies, header_patch = [], {}

            for item in sc_list:
                for key in watched:
                    if item.startswith(f"{key}="):
                        value = item.split(";", 1)[0].split("=", 1)[1]
                        new_cookies.append({
                            "name": key,
                            "value": value,
                            "domain": ".liepin.com",
                            "path": "/",
                            "expires": -1
                        })
                        if key == "XSRF-TOKEN":
                            header_patch["XSRF-TOKEN"] = value
                        break  # 命中一个 key 就跳出内层 for

            if not new_cookies:
                return  # 本次响应没有更新任何目标字段

            # 4. 同步到所有 Context，并刷新 Header
            for ctx in self.contexts:
                await ctx.add_cookies(new_cookies)
                if header_patch:
                    await ctx.set_extra_http_headers({
                        **header_patch,
                        "Referer": "https://www.liepin.com/",
                        "X-Requested-With": "XMLHttpRequest"
                    })

            logger.info(f"🔄 Cookie auto-refresh: {[c['name'] for c in new_cookies]}")

        except Exception as e:
            logger.warning(f"Cookie watcher error: {e}")

    # ------------------------------------------------------------------
    def process_job_data(self, job_data: Dict) -> Dict:
        data = {
            'job_id': job_data.get('job_id',''),
            'source': 'liepin',
            'title': job_data.get('title',''),
            'salary': job_data.get('salary','面议'),
            'experience': job_data.get('experience','经验不限'),
            'education': job_data.get('education','学历不限'),
            'company': job_data.get('company_name',''),
            'company_type': '',
            'company_size': job_data.get('company_size',''),
            'company_industry': job_data.get('company_industry',''),
            'company_development_stage': job_data.get('company_development_stage',''),
            'company_url': job_data.get('company_url',''),
            'hr_name': job_data.get('recruiter_name',''),
            'hr_position': job_data.get('recruiter_title',''),
            'hr_active': job_data.get('hr_active','高回复率'),
            'job_type': '全职',
            'job_tags': job_data.get('job_tags',[]),
            'job_url': job_data.get('job_url',''),
            'publish_time': job_data.get('refreshTime',''),
            'update_time':'',
            'uploader': self.uploader,
            'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        loc = job_data.get('location','')
        city, district = loc.split('-',1) if '-' in loc else (loc,'')
        data['city'] = city
        data['district'] = district

        sal = job_data.get('salary','面议')
        if '面议' not in sal:
            try:
                unit = '元/月'; mn = mx = 0
                if '元/天' in sal:
                    unit = '元/天'; nums = re.findall(r'(\d+)', sal); mn = mx = int(nums[0])
                elif '万' in sal:
                    nums = re.findall(r'(\d+(?:\.\d+)?)', sal)
                    if len(nums) >= 2:
                        mn, mx = [float(x)*10000 for x in nums[:2]]
                elif 'k' in sal.lower():
                    nums = re.findall(r'(\d+(?:\.\d+)?)', sal)
                    if len(nums) >= 2:
                        mn, mx = [float(x)*1000 for x in nums[:2]]
                else:
                    nums = re.findall(r'(\d+)', sal)
                    if len(nums) >= 2:
                        mn, mx = [int(x) for x in nums[:2]]
                data['salary_min'] = mn; data['salary_max'] = mx; data['salary_unit'] = unit
            except:
                data.update({'salary_min':0,'salary_max':0,'salary_unit':'元/月'})
        else:
            data.update({'salary_min':0,'salary_max':0,'salary_unit':'元/月'})
        return data

if __name__ == "__main__":
    spider = LiepinSpider()
    asyncio.run(spider.run())
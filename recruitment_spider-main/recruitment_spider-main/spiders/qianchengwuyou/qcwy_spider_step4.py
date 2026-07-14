# -*- coding:utf-8 -*-
# cookies 获取方式 登录前程无忧登录页并进行注册https://login.51job.com/login.php?lang=c&isjump=1&url=https%3A%2F%2Fwe.51job.com%2Fpc%2Fsearch%3FjobArea%3D010000%26amp%3Bkeyword%3D%25E7%2589%25A9%25E4%25B8%259A%26amp%3BsearchType%3D2%26amp%3BkeywordType%3Dguess_exp_tag6%26amp%3Bnoclear%3D1
# 注册成功后跳转至https://www.51job.com/ ，找到对应页面响应标头中的set-cookie并复制到cookies列表里，
# get_ratio(total_urls_count)中修改为自己的part，以及133-135行代码中对应的part
import json
import time
from DrissionPage import ChromiumPage
from DrissionPage._configs.chromium_options import ChromiumOptions
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin, Style
from datetime import datetime
from DrissionPage._pages.chromium_page import ChromiumPage
from DrissionPage.errors import ElementNotFoundError
from DrissionPage.common import Actions
from pymongo import MongoClient
from pymongo import UpdateOne
import random
from hunmanMouse import humanMouse
from DrissionPage._pages.session_page import SessionPage

cookies = [
    "51job=cuid%3D138251799%26%7C%26cusername%3D6245UHfZ0dqIjzJEfQrEpP3dPj14ZGJBspzLU2iGqtA%253D%26%7C%26cpassword%3D%26%7C%26cname%3D%26%7C%26cemail%3DR%252FA9l2SMe9jesWRA%252BY4iQ4MnsQezEQiwZCTYRuBfx20%253D%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.0a5kNHU84.ss%26%7C%26cconfirmkey%3D19qk7LzdSG4BU%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D%26%7C%26cnamekey%3D19afZtfWJFcmA%26%7C%26to%3D4ffca5144bcdfae6795ce9990879cc4868258e65%26%7C%26; expires=Fri, 15-May-2026 06:49:50 GMT; Max-Age=31536000; path=/; domain=.51job.com; HttpOnly",
    "51job=cuid%3D260598000%26%7C%26cusername%3DkIIcFrrh0cn0rn2z3mTGYj93oMEyKHNZGNH5TQgnHZ8%253D%26%7C%26cpassword%3D%26%7C%26cname%3DNGvqESSCSQEE%252FmYLtXbzFg%253D%253D%26%7C%26cemail%3DWasfzX2MZ1sNoj%252FvkXRfXenN1ysYbDKEv0y5ERkcOqc%253D%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.0V7MTEDqQlGI%26%7C%26cconfirmkey%3DjecA8np.nX4s.%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D1%26%7C%26cnamekey%3Dje8aNNox2HQM.%26%7C%26to%3Dfeaa01156b950d6aa81a4e746625b7f868258ec4%26%7C%26; expires=Fri, 15-May-2026 06:50:57 GMT; Max-Age=31536000; path=/; domain=.51job.com; HttpOnly",
    "51job=cuid%3D260596912%26%7C%26cusername%3Do16WLuwvO3vkca%252FJLJyueFSkEYbLxSesCX09MoFdemg%253D%26%7C%26cpassword%3D%26%7C%26cname%3D00IcySvKlfAzsOiuuYk0og%253D%253D%26%7C%26cemail%3D%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.04w.OZvKA5Pw%26%7C%26cconfirmkey%3D%25241%2524AhBhZcRO%2524EHF3JCbffTisMxbwuZUfH0%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D1%26%7C%26cnamekey%3D%25241%2524kYv79h%252Fb%2524n1TOc5iacens5WYMVfA.G.%26%7C%26to%3Da68db4fc13214ce871aa8863e1f98f6b68258f03%26%7C%26; expires=Fri, 15-May-2026 06:52:13 GMT; Max-Age=31536000; path=/; domain=.51job.com; HttpOnly",
    "51job=cuid%3D260599192%26%7C%26cusername%3DOt9OBIea0x%252BG%252FoTN32q8zf2oFSnjEQXLWpQUF6obtHM%253D%26%7C%26cpassword%3D%26%7C%26cname%3D3PC3o7f%252BHJXYh4EbTqPRWQ%253D%253D%26%7C%26cemail%3DlU7M5B2DXepgzfzT3a7HVg%253D%253D%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.0n6l8YiHOxAY%26%7C%26cconfirmkey%3DbnOkRb4TWzqMo%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3DbnJHVJPL4Lj3c%26%7C%26to%3D8e61006786ad70b25c19a4f6fefcf19c68258f68%26%7C%26; expires=Fri, 15-May-2026 06:53:46 GMT; Max-Age=31536000; path=/; domain=.51job.com; HttpOnly",
    "51job=cuid%3D260599807%26%7C%26cusername%3D6d5Ob1fMxmuArqUOHpRxg6MDHQjx95Z%252BxtaAySh11jM%253D%26%7C%26cpassword%3D%26%7C%26cname%3D8vtZ%252BWhal%252BWGzMi6nNZiPQ%253D%253D%26%7C%26cemail%3DzbLaLk1tcUzRTWKy3VYHwO2nZFepc6SKiJpSCnGfJoo%253D%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0FLXaUe1VUH6%26%7C%26cconfirmkey%3D30JdKqOBo6VYI%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D1%26%7C%26cnamekey%3D30vgfhfBX2G%252FM%26%7C%26to%3De10d26ed0bdee1951de9074203be3cf168258fad%26%7C%26; expires=Fri, 15-May-2026 06:54:46 GMT; Max-Age=31536000; path=/; domain=.51job.com; HttpOnly",
]
mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"

mongo_db = "MOOC123_DA"
sleepTime = 12 # 运行休眠时间5秒 比较稳定能运行 2秒也可以


def check_text(text):  # 检查是否有405页面
    return "很抱歉，由于您访问" in text


def check405(url):  # 查看网页是否被封
    page400 = SessionPage()
    # 获取内置的 session 对象
    session = page400.session
    # 发送 HEAD 请求
    response = session.head(url)

    print(f"HEAD 请求状态码: {response.status_code}")
    if response.status_code == 405:
        return True
    else:
        return False


def slide_verify(page, use_id=True):
    """
    进行滑动验证
    :param page: ChromiumPage 对象
    :param use_id: 是否使用 id 定位滑块元素，默认为 True
    :return: 验证成功返回 True，验证失败或出现异常返回 False
    """
    try:
        while True:
            # 使用 class 定位
            slider = page.ele('css:span.nc_iconfont.btn_slide', timeout=4)
            ac = Actions(page)

            # 模拟随机初始移动
            for _ in range(random.randint(10, 20)):
                ac.move(random.randint(-20, 20), random.randint(-10, 10))

            # 移动到滑块元素
            ac.move_to(slider)
            # 按下滑块，稍作停留
            ac.hold()
            time.sleep(random.uniform(0.1, 0.3))

            # 使用 humanMouse 类生成基础随机轨迹
            hm = humanMouse()
            base_track = hm.getRandomTrackSpacingArray(水平移动=160, 垂直移动=5, 分割=20)

            # 记录当前位置
            current_x = 0
            target_x = 300  # 目标总位移

            # 处理轨迹点，添加终点抖动和速度变化
            for i, (dx, dy) in enumerate(base_track):
                # 计算当前应移动的距离（随时间变化速度）
                progress = min(current_x / target_x, 1.0)

                # 前期加速，后期减速
                speed_factor = 0.8 + 0.4 * progress  # 速度因子 0.8-1.2
                adjusted_dx = dx * speed_factor
                adjusted_dy = dy * speed_factor

                # 移动
                ac.move(adjusted_dx, adjusted_dy)
                current_x += adjusted_dx

                # 接近终点时添加抖动
                if progress > 0.8:
                    # 80% 进度后添加随机小范围回退和前进
                    if random.random() > 0.7:
                        shake_dx = random.uniform(-5, 5)
                        ac.move(shake_dx, 0)
                        current_x += shake_dx
                        time.sleep(random.uniform(0.03, 0.08))

                # 随机暂停
                if random.random() > 0.7:
                    time.sleep(random.uniform(0.02, 0.06))

            # 确保最终到达目标位置
            final_adjust = target_x - current_x
            if abs(final_adjust) > 1:
                ac.move(final_adjust, 0)

            # 在终点停留一小段时间
            time.sleep(random.uniform(0.3, 0.5))

            # 释放滑块，模拟人类放松的动作（先轻微回退）
            if random.random() > 0.5:
                ac.move(-2, 0)
            ac.release()

            time.sleep(3)  # 等待页面响应
    except ElementNotFoundError:
        print("未找到滑块，认为验证成功")
        return True
    except Exception as e:
        print(f"进行验证时出现{str(e)}")
        return False


def generate_51job_url(job_area, job_id):
    """
    生成51job职位URL
    :param job_area: 地区字符串，格式如"北京·朝阳区"
    :param job_id: 职位ID字符串
    :return: 完整的职位URL
    """

    def convert_area(job_area):
        """处理地区转换的内部函数"""
        if '·' in job_area:
            city, district = job_area.split('·', 1)
        else:
            city, district = job_area, ''

        city_part = ''.join(lazy_pinyin(city)).lower()
        district_part = ''.join([
            lazy_pinyin(c, style=Style.FIRST_LETTER)[0].lower()
            for c in district if c.strip()
        ])
        return f"{city_part}-{district_part}" if district_part else city_part

    # 执行转换
    region = convert_area(job_area.strip())
    return f"https://jobs.51job.com/{region}/{job_id}.html"


def extract_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取 href 后面的 URL
    a_tag = soup.find('a')
    url = a_tag.get('href') if a_tag else None

    # 提取 title 属性的值
    title = a_tag.get('title') if a_tag else None

    # 提取三个 span 标签的内容
    spans = soup.find_all('span', class_='dc')
    industry = spans[0].text if spans else None
    company_type = spans[1].text if len(spans) > 1 else None
    company_size = spans[2].text if len(spans) > 2 else None

    return url, title, industry, company_type, company_size


# 新增函数，用于获取两者之比
def get_ratio(total_urls_count):
    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    collection_log = db['qcwy_step2_urls_202505_log_part1']
    pipeline = [
        {"$match": {"is_final_status": True}},
        {"$group": {"_id": "$url"}},
        {"$count": "unique_count"}
    ]
    result = list(collection_log.aggregate(pipeline))
    success_urls_count = result[0]['unique_count'] if result else 0
    if total_urls_count == 0:
        ratio = 0
    else:
        ratio = success_urls_count / total_urls_count

    print(
        f"success_urls_count: {success_urls_count}, total_urls_count: {total_urls_count}, 爬取进度: {int(ratio*100)}%")  # 打印全局进度
    return ratio


# ... 原有的导入语句 ...

def spider():
    default_account=True
    # 记录打开浏览器的时间
    start_time = datetime.now()

    # 定义alive_clist和sleep_clist，以及用于跟踪cookie进入sleep_clist的时间的字典
    alive_clist = cookies.copy()  # 复制原有的cookies列表
    sleep_clist = []
    sleep_cookie_time = {}
    # # IP代理
    # proxy = 'tunpool-gkem4.qg.net:13775'
    # 连接 MongoDB
    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    collection_job = db['qcwy_step2_job_raw_part1']  # 改为对应的集合名part1,part2,part3,part4
    collection_log = db['qcwy_step2_urls_202505_log_part1']  # 改为对应的集合名part1,part2,part3,part4
    collection_urls = db['qcwy_step2_urls_part1']  # 假设urls集合存储待爬取URL    #改为对应的集合名part1,part2,part3,part4,参照数据库改名
    total_urls_count = collection_urls.count_documents({})
    # 浏览器配置
    options = ChromiumOptions()
    options.no_imgs()  # 禁用图片加载
    options.set_argument('--disable-javascript')  # 禁用 JavaScript
    options.set_argument('--disable-plugins')  # 禁用插件
    # IP代理
    # options.set_proxy(proxy)
    options.set_user_agent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36')
    options.set_argument('--window-size=1920,1080')  # 设置窗口大小
    # # 无痕
    options.incognito(True)
    #浏览器切换
    # options.set_browser_path(r"E:\Twinkstar Browser\twinkstar.exe")
    # 设置浏览器路径（可选）
    # 创建ChromiumPage对象（保持不变）

    browser = ChromiumPage(options)
    page = browser.latest_tab
    page.set.cookies.clear()
    current_cookie = random.choice(alive_clist)
    page.set.cookies(current_cookie)

    # 定义定位器（保持不变）
    locatorB = 't:button@@class=btn-next'
    locator1 = 't:div@@class=joblist-item-job sensors_exposure'
    locator2 = 't:div@@class=bl'
    locator_none = 't:div@@class=j_nolist'
    locator_405 = 't:div@@class=message'
    success_urls = set()
    try:
        BATCH_SIZE = 1000  # 每批读取的文档数量
        skip = 0

        while True:
            # 分页查询，每次读取BATCH_SIZE条记录
            cursor = collection_log.find(
                {"is_final_status": {"$in": [True, "True"]}},
                {"url": 1}
            ).skip(skip).limit(BATCH_SIZE)

            batch = list(cursor)
            if not batch:
                break

            # 将当前批次的URL添加到集合中
            for doc in batch:
                success_urls.add(doc['url'])

            skip += BATCH_SIZE
            print(f"已读取 {skip} 条成功记录...")

        print(f"共读取 {len(success_urls)} 条已成功爬取的URL")
    except Exception as e:
        log_entry = {
            'url': None,
            'page': 0,
            'job_counts': 0,
            'crawl_time': datetime.now(),
            'status': False,
            'error': f"读取成功URL时出错: {str(e)}",
            'is_final_status': False
        }
        collection_log.insert_one(log_entry)

    # 定义时间阈值（保持不变）
    threshold_date = datetime(2025, 1, 1)

    def insert_with_retry(items):
        MAX_RETRIES = 3
        RETRY_DELAY = 5  # 重试间隔（秒）
        retries = 0
        while retries < MAX_RETRIES:
            try:
                if items:
                    # 构建批量操作列表，假设使用 job_id 作为唯一标识，可按需修改
                    operations = [
                        UpdateOne(
                            {'job_id': item['job_id']},
                            {'$set': item},
                            upsert=True
                        ) for item in items
                    ]
                    # 执行批量操作
                    collection_job.bulk_write(operations)
                    print(f"此页爬取到 {len(items)} 条数据，已使用批量 upsert 操作处理。")
                return True
            except Exception as e:
                print(f"插入数据时出错: {e}，重试第 {retries + 1} 次...")
                retries += 1
                time.sleep(RETRY_DELAY)
        print("达到最大重试次数，插入失败。")
        return False

    url_counter = 0  # 新增：URL 计数器
    # 从MongoDB urls集合读取待爬取URL
    try:
        url_docs = collection_urls.find()  # 假设集合中每个文档包含'url'字段
        for doc in url_docs:
            url = doc['url']
            if url in success_urls:
                # print(f"URL: {url} 已成功爬取，跳过。")
                continue
            validation_count = 0
            page.get(url)
            # 休眠
            time.sleep(sleepTime)

            last_crawl_time = datetime.now()
            page_count = 1
            last_successful_job_count = 0
            while True:
                # 解析职位元素（保持不变）
                get_ratio(total_urls_count)
                elements1 = page.eles(locator1)
                elements2 = page.eles(locator2)
                joblen = len(elements1)
                # 创建一个Actions对象
                ac = Actions(page)
                # 增加鼠标移动操作
                x_move = random.randint(-50, 250)
                y_move = random.randint(-250, 50)
                ac.move(x_move, y_move)
                # 模拟鼠标滚轮向下滚动随机滚动距离
                ac.scroll(delta_y=random.randint(200, 500))
                time.sleep(0.5)
                ac.scroll(delta_y=random.randint(1000, 1300))

                if joblen == 0:
                    no_job_element = page.ele(locator_none)

                    if no_job_element and no_job_element.text == "哦哦！没有职位不要怕，你那么年轻那么好看，再重搜一次呗~":
                        no_job_element.hover()  # 模拟鼠标悬停
                        time.sleep(1)
                        print(f"URL: {url}, 页数: {page_count} - 此页面访问成功但未爬到数据，跳过。")
                        log_entry = {
                            'url': url,
                            'page': page_count,
                            'job_counts': 0,
                            'crawl_time': datetime.now(),
                            'status': True,
                            'error': "此页面访问成功但未爬到数据",
                            'is_final_status': True,
                        }
                        collection_log.insert_one(log_entry)
                        break
                    else:

                        print(f"URL: {url}, 页数: {page_count} - 此页面访问失败且未爬到数据，尝试进行滑块验证。")
                        validation_count += 1
                        time.sleep(2)
                        if validation_count == 3:
                            msg405 = page.ele(locator_405)

                            if msg405 and "很抱歉，由于您访问" in msg405.text:
                                print("账户被封禁")
                                # 将当前cookie从alive_clist移到sleep_clist
                                alive_clist.remove(current_cookie)
                                sleep_clist.append(current_cookie)
                                sleep_cookie_time[current_cookie] = datetime.now()

                                if alive_clist:
                                    print("切换新用户")
                                    # 从alive_clist随机选择一个新cookie
                                    current_cookie = random.choice(alive_clist)
                                    # 重启浏览器并注入新cookie
                                    browser.quit()
                                    browser = ChromiumPage(options)
                                    page = browser.latest_tab
                                    page.set.cookies.clear()
                                    page.set.cookies(current_cookie)
                                    break

                                else:
                                    print("没有剩余用户，程序进行休眠")
                                    log_entry = {
                                        'url': None,
                                        'page': 0,
                                        'job_counts': 0,
                                        'crawl_time': datetime.now(),
                                        'status': False,
                                        'error': f"所用用户均被封禁，程序休眠",
                                        'is_final_status': False
                                    }
                                    collection_log.insert_one(log_entry)
                                    browser.quit()
                                    client.close()
                                    time.sleep(7 * 3600)
                                    return True

                            else:
                                print("没有滑块，也没有被封禁，拟重启浏览器并跳过此url")
                                # 关闭当前浏览器
                                browser.quit()
                                # 创建新的浏览器实例
                                browser = ChromiumPage(options)
                                page = browser.latest_tab
                                page.set.cookies.clear()
                                page.set.cookies(current_cookie)
                                break


                        if validation_count > 3:
                            print(f"IP被封禁一段时间，无法爬取 URL: {url}")
                            log_entry = {
                                'url': url,
                                'page': page_count,
                                'job_counts': 0,
                                'crawl_time': datetime.now(),
                                'status': False,
                                'error': "账户被封禁一段时间，无法爬取",
                                'is_final_status': False
                            }
                            collection_log.insert_one(log_entry)

                            # 将当前cookie从alive_clist移到sleep_clist
                            if current_cookie in alive_clist:
                                alive_clist.remove(current_cookie)
                            sleep_clist.append(current_cookie)
                            sleep_cookie_time[current_cookie] = datetime.now()

                            # 检查是否还有可用cookie
                            if alive_clist:
                                print("切换新用户")
                                # 从alive_clist随机选择一个新cookie
                                current_cookie = random.choice(alive_clist)
                                # 重启浏览器并注入新cookie
                                browser.quit()
                                browser = ChromiumPage(options)
                                page = browser.latest_tab
                                page.set.cookies.clear()
                                page.set.cookies(current_cookie)
                                break
                            # elif default_account:
                            #
                            #     print("没有剩余用户,但默认账户未使用，选择不注入cookie进行爬取")
                            #     log_entry = {
                            #         'url': None,
                            #         'page': 0,
                            #         'job_counts': 0,
                            #         'crawl_time': datetime.now(),
                            #         'status': False,
                            #         'error': f"默认账户使用中",
                            #         'is_final_status': False
                            #     }
                            #     collection_log.insert_one(log_entry)
                            #     browser.quit()
                            #     browser = ChromiumPage(options)
                            #     page = browser.latest_tab
                            #     page.set.cookies.clear()
                            #     default_account = False  # 默认账户已使用
                            #
                            #     break
                            else:
                                print("没有剩余用户，程序进行休眠")
                                log_entry = {
                                    'url': None,
                                    'page': 0,
                                    'job_counts': 0,
                                    'crawl_time': datetime.now(),
                                    'status': False,
                                    'error': f"所用用户均被封禁，程序休眠",
                                    'is_final_status': False
                                }
                                collection_log.insert_one(log_entry)
                                browser.quit()
                                client.close()
                                time.sleep(7 * 3600)


                                return True

                        verify_result = slide_verify(page)
                        if verify_result:
                            print(f"滑块验证成功，继续爬取 URL: {url}")
                            continue
                        else:
                            print(f"滑块验证失败 URL: {url}, 翻页次数: {page_count} - 此页面访问失败且未爬到数据，跳过。")

                            log_entry = {
                                'url': url,
                                'page': page_count,
                                'job_counts': 0,
                                'crawl_time': datetime.now(),
                                'status': False,
                                'error': "滑块验证失败，此页面访问失败且未爬到数据",
                                'is_final_status': False
                            }
                            collection_log.insert_one(log_entry)
                            break

                items = []
                for ele1, ele2 in zip(elements1, elements2):
                    item = {}

                    # 提取职位信息
                    info1 = ele1.attrs
                    sensors_data_str = info1.get('sensorsdata')
                    if sensors_data_str:
                        try:
                            sensors_data = json.loads(sensors_data_str)
                            item['job_id'] = sensors_data.get('jobId')
                            item['job_title'] = sensors_data.get('jobTitle')
                            item['job_type'] = sensors_data.get('jobType')
                            item['job_salary'] = sensors_data.get('jobSalary')
                            item['job_area'] = sensors_data.get('jobArea')

                            # 分割 job_area
                            if '·' in item['job_area']:
                                item['city'], item['district'] = item['job_area'].split('·', 1)
                            else:
                                item['city'] = item['job_area']
                                item['district'] = ''

                            item['education'] = sensors_data.get('jobDegree')
                            item['experience'] = sensors_data.get('jobYear')
                            item['publish_time'] = sensors_data.get('jobTime')

                            # 检查 publish_time 是否在 2025 年 3 月 1 日之后
                            try:
                                publish_date = datetime.strptime(item['publish_time'], '%Y-%m-%d  %H:%M:%S')
                                if publish_date < threshold_date:
                                    continue
                            except ValueError:
                                continue

                            # 生成职位 URL
                            item['job_url'] = generate_51job_url(item['job_area'], item['job_id'])

                        except json.JSONDecodeError:
                            continue

                    # 提取公司信息
                    # 获取元素的 innerHTML
                    html_content = ele2.html
                    # 使用正则表达式或其他方式从 HTML 中提取文本
                    # 这里简单示例，直接去除标签，保留文本
                    start_index = html_content.find('>') + 1
                    end_index = html_content.rfind('<')
                    text = html_content[start_index:end_index].strip() if start_index != 0 and end_index != -1 else ""

                    # 提取信息
                    item['company_url'], item['company_title'], item['industry'], item['company_type'], item[
                        'company_size'] = extract_info(text)

                    # 记录爬取结束时间
                    item['crawl_time'] = datetime.now()
                    last_crawl_time = item['crawl_time']
                    item['uploader'] = "胡靖凯"
                    item['source'] = "qcwy"
                    items.append(item)

                job_counts = len(items)
                # 如果当前页没有符合条件的数据，跳出循环
                if not items:
                    print(f"URL: {url}, 翻页次数: {page_count} - 当前页没有符合条件的数据，跳出循环")
                    log_entry = {
                        'url': url,
                        'page': page_count,
                        'job_counts': job_counts,
                        'crawl_time': last_crawl_time,
                        'status': True,
                        'is_final_status': True,
                    }
                    collection_log.insert_one(log_entry)

                    break

                if not insert_with_retry(items):
                    log_entry = {
                        'url': url,
                        'page': page_count,
                        'job_counts': job_counts,
                        'crawl_time': datetime.now(),
                        'status': False,
                        'error': "达到最大重试次数，插入数据到 MongoDB 失败",
                        'is_final_status': False
                    }
                    collection_log.insert_one(log_entry)

                    break
                # 在成功处理每页数据后更新
                else:
                    print(f"URL: {url}, 页数: {page_count} - 此页爬取到 {job_counts} 条数据。")

                    log_entry = {
                        'url': url,
                        'page': page_count,
                        'job_counts': job_counts,
                        'crawl_time': last_crawl_time,
                        'status': True,
                        'is_final_status': False,
                    }
                    collection_log.insert_one(log_entry)

                # 查找元素
                next_button = page.ele(locatorB)
                page.scroll.to_bottom()
                if next_button:
                    print(f"URL: {url}, 页数: {page_count} - 找到下一页按钮。")

                    # 检查按钮是否被禁用
                    if next_button.attr('disabled'):
                        next_button.hover()  # 鼠标操作悬停
                        time.sleep(1)
                        print(f"URL: {url}, 页数: {page_count} - 按钮被禁用，跳出该 URL 访问。")
                        log_entry = {
                            'url': url,
                            'page': page_count,
                            'job_counts': job_counts,
                            'crawl_time': last_crawl_time,
                            'status': True,
                            'is_final_status': True,
                        }
                        collection_log.insert_one(log_entry)

                        break
                    else:
                        try:
                            # 点击按钮翻页
                            next_button.hover()  # 鼠标操作悬停
                            time.sleep(0.5)
                            next_button.click()
                            page_count += 1  # 翻页次数加 1
                            # 每次翻页后等待X秒
                            time.sleep(sleepTime)
                        except Exception:
                            log_entry = {
                                'url': url,
                                'page': page_count,
                                'job_counts': job_counts,
                                'crawl_time': datetime.now(),
                                'status': False,
                                'error': "点击下一页按钮时出错",
                                'is_final_status': False
                            }
                            collection_log.insert_one(log_entry)
                            break
                else:
                    break

            url_counter += 1  # 新增：URL 计数器加 1
            if url_counter % 5 == 0:  # 每 20 个 URL 进行判断
                print("，重启浏览器并更换用户...")
                # 关闭当前浏览器
                browser.quit()
                # 创建新的浏览器实例
                browser = ChromiumPage(options)
                page = browser.latest_tab
                page.set.cookies.clear()
                current_cookie = random.choice(alive_clist)
                page.set.cookies(current_cookie)

            # cookie计时和恢复的逻辑
            current_time = datetime.now()
            cookies_to_remove = []
            for cookie, entry_time in sleep_cookie_time.items():
                if (current_time - entry_time).total_seconds() >= 6 * 3600:
                    sleep_clist.remove(cookie)
                    alive_clist.append(cookie)
                    cookies_to_remove.append(cookie)

            for cookie in cookies_to_remove:
                del sleep_cookie_time[cookie]

    except Exception as e:
        log_entry = {
            'url': None,
            'page': 0,
            'job_counts': 0,
            'crawl_time': datetime.now(),
            'status': False,
            'error': f"处理URL集合时出错: {str(e)}",
            'is_final_status': False
        }
        collection_log.insert_one(log_entry)

    # 关闭浏览器和MongoDB连接
    browser.quit()
    client.close()
    return True

# ... 主程序部分保持不变 ...


# 主程序
MAX_RETRY_ATTEMPTS = 200
RETRY_INTERVAL = 30  # 重试间隔（秒）

for attempt in range(MAX_RETRY_ATTEMPTS):
    try:
        # 如果spider()返回True，表示需要重试
        if spider():
            print("正在重启程序")
            time.sleep(120)
            continue

    except Exception as e:
        if "[WinError 10054]" in str(e):
            print(f"遇到网络错误 [WinError 10054]，等待 {RETRY_INTERVAL} 秒后重试...")
            time.sleep(RETRY_INTERVAL)
            continue
        print(f"发生错误: {e}，等待 {RETRY_INTERVAL} 秒后重试...")
        time.sleep(RETRY_INTERVAL)
else:
    print("达到最大重试次数，程序终止,检查log是否已爬完。")
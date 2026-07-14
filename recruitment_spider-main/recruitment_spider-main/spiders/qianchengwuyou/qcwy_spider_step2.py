import time
from datetime import datetime
from DrissionPage import ChromiumPage
from DrissionPage._configs.chromium_options import ChromiumOptions
from pymongo import MongoClient, UpdateOne
import random
from DrissionPage.errors import ElementNotFoundError
from DrissionPage.common import Actions
import csv
import random
import os

# 在代码开头定义表名常量
QCWY_VERIFY_LOGS_TABLE = "qcwy_step1_urls_part2"
QCWY_STEP1_VERIFY_LOGS_TABLE = "qcwy_step1_verify_logs_part2"


def slide_verify(page, use_id=True):
    """
    进行滑动验证
    :param page: ChromiumPage 对象
    :param use_id: 是否使用 id 定位滑块元素，默认为 True
    :return: 验证成功返回 True，验证失败或出现异常返回 False
    """
    try:
        while True:
            if use_id:
                slider = page.ele('css:span#nc_1_n1z', timeout=1)
            else:
                # 使用 class 定位
                slider = page.ele('css:span.nc_iconfont.btn_slide', timeout=1)

            if not slider:
                print("未找到滑块，认为验证成功")
                return True

            page.clear_cache()  # 清除缓存
            ac = Actions(page)

            # 模拟人类随机移动
            for _ in range(random.randint(10, 20)):
                ac.move(random.randint(-20, 20), random.randint(-10, 10))

            # 移动到滑块元素
            ac.move_to(slider)

            # 按下并滑动滑块
            ac.hold().move(300)

            time.sleep(4)  # 等待页面响应
    except ElementNotFoundError:
        print("未找到滑块，认为验证成功")
        return True
    except Exception as e:
        print(f"进行验证时出现{str(e)}")
        return False


def load_status(num):
    if num is None:
        return False
    return num.text in {'50', '51'}


def check_no_job_element(no_job_element):
    """
    检查是否出现无职位提示元素
    :param no_job_element: 页面元素对象
    :return: 存在提示返回True，否则返回False
    """
    if no_job_element:
        expected_text = "哦哦！没有职位不要怕，你那么年轻那么好看，再重搜一次呗~"
        return no_job_element.text == expected_text
    return False


class QCWY_URL_Verifier:
    def __init__(self):
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.db_name = "MOOC123_DA"

        self.client = None
        self.db = None
        # 浏览器配置
        options = ChromiumOptions()
        options.no_imgs()  # 禁用图片加载
        options.set_argument('--disable-javascript')  # 禁用 JavaScript
        options.set_argument('--disable-plugins')  # 禁用插件
        options.set_argument('--window-size=1920,1080')  # 设置窗口大小

        # 浏览器实例
        self.page = ChromiumPage(options)
        # 浏览器实例
        self.page = ChromiumPage()

        # 定位器配置
        self.locator1 = "t:div@@class=joblist-item-job sensors_exposure"
        self.locator_num50 = "t:li@@class=number@@tx():50"
        self.locator_num51 = "t:li@@class=number@@tx():51"
        self.locator_none = "t:div@@class=j_nolist"

        # 滑动验证计数器
        self.verify_attempts = {}

    def connect_mongo(self):
        """连接MongoDB数据库"""
        max_retries = 3
        retry_delay = 5  # 秒

        for attempt in range(max_retries):
            try:
                self.client = MongoClient(self.mongo_uri)
                self.db = self.client[self.db_name]
                # 测试连接
                self.db.command('ping')
                print("MongoDB连接成功")
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"MongoDB连接失败，已达到最大重试次数: {str(e)}")
                    raise e
                print(f"MongoDB连接失败，{retry_delay}秒后重试...")
                # 关闭之前的连接（如果存在）
                if self.client:
                    try:
                        self.client.close()
                    except:
                        pass
                time.sleep(retry_delay)

    def init_collections(self):
        """初始化集合（如果不存在则创建）"""
        if QCWY_VERIFY_LOGS_TABLE not in self.db.list_collection_names():
            print(f"{QCWY_VERIFY_LOGS_TABLE}表不存在")

        if QCWY_STEP1_VERIFY_LOGS_TABLE not in self.db.list_collection_names():
            self.db.create_collection(QCWY_STEP1_VERIFY_LOGS_TABLE)

    def get_unverified_urls(self):
        """获取待验证的URL（断点续爬）"""
        # 获取 qcwy_step1_verify_logs_part1 中 claw——status 为 "success" 的 url 集合
        success_urls = set(self.db[QCWY_STEP1_VERIFY_LOGS_TABLE].find({"claw——status": "success"}, {"url": 1}).distinct("url"))
        all_urls = set(self.db[QCWY_VERIFY_LOGS_TABLE].find({}, {"url": 1}).distinct("url"))
        return [{"url": url} for url in all_urls - success_urls]

    def check_elements(self):
        """检测页面关键元素"""
        elements = {
            'num50': self.page.ele(self.locator_num50, timeout=1),
            'num51': self.page.ele(self.locator_num51, timeout=1),
            'no_job': self.page.ele(self.locator_none, timeout=1),
        }
        return elements

    def handle_verification(self, url):
        """处理滑动验证流程"""
        attempt_count = self.verify_attempts.get(url, 0) + 1
        self.verify_attempts[url] = attempt_count

        if attempt_count > 3:
            # 触发休眠重启机制
            print(f"URL: {url} 验证失败超过5次，休眠20分钟...")
            self.page.quit()
            time.sleep(2400)
            self.page = ChromiumPage()  # 重启浏览器
            self.verify_attempts.pop(url, None)
            return False

        # 执行滑动验证
        verify_result = slide_verify(self.page)
        log_data = {
            "url": url,
            "status": "retry",
            "verify_attempt": attempt_count,
            "timestamp": datetime.now(),
            "error": "触发滑动验证" if verify_result else "滑动验证失败"
        }
        print("触发滑动验证" if verify_result else "滑动验证失败")

        return verify_result

    def verify_single_url(self, url):
        """验证单个URL的核心逻辑"""
        try:
            self.page.get(url)
            time.sleep(4)  # 可调大
            # 创建一个Actions对象
            ac = Actions(self.page)

            # 模拟鼠标滚轮向下滚动200个单位
            ac.scroll(delta_y = 400 + random.randint(200, 300))
            element1 = self.page.eles(self.locator1, timeout=1)
            elements = self.check_elements()
            validation_flag = False
            flag5x = False
            joblen = len(element1)
            # 第一层判断
            if joblen != 0:
                validation_flag = True
                if elements['num50'] and elements['num50'].text == '50':
                    flag5x = True
                elif elements['num51'] and elements['num51'].text == '51':  # 必须这么判断否则 抛出错误 影响后续程序进行
                    flag5x = True
                else:
                    flag5x = False
            else:
                # 第二层判断
                if check_no_job_element(elements['no_job']):
                    validation_flag = True
                    flag5x = False
                else:
                    if not self.handle_verification(url):
                        return False
                    return self.verify_single_url(url)  # 递归重试

            # 记录最终结果
            log_entry = {
                "url": url,
                "verification——status": flag5x,
                "timestamp": datetime.now(),
                "claw——status": "success" if validation_flag else "fail",
                "verify_attempt": self.verify_attempts.get(url, 0)
            }
            self.db[QCWY_STEP1_VERIFY_LOGS_TABLE].insert_one(log_entry)
            print("符合条件" if flag5x else "不符合条件")

            # 更新主URL集合状态
            # self.db[INDUSTRY_KEYWORD_URLS_TABLE].update_one(#QCWY_VERIFY_LOGS_TABLE
            #     {"url": url},
            #     {"$set": {"valid": validation_flag}}
            # )

            return True

        except Exception as e:
            error_log = {
                "url": url,
                "status": "error",
                "timestamp": datetime.now(),
                "error": str(e),
                "verify_attempt": self.verify_attempts.get(url, 0)
            }
            print("error")
            return False

    def run(self):
        """主运行流程"""
        self.connect_mongo()
        self.init_collections()

        # 初始化时，删除 qcwy_step1_verify_logs_part 中 claw——status 不为 "success" 的数据
        self.db[QCWY_STEP1_VERIFY_LOGS_TABLE].delete_many({"claw——status": {"$ne": "success"}})

        urls = self.get_unverified_urls()
        print(f"待验证URL数量: {len(urls)}")

        for idx, url_doc in enumerate(urls, 1):
            url = url_doc['url']
            print(f"正在处理({idx}/{len(urls)}): {url}")

            success = self.verify_single_url(url)
            status = "成功" if success else "失败"
            print(f"处理结果: {status}\n{'=' * 50}")
        # 对 qcwy_step1_verify_logs_part2 表进行去重操作
        pipeline = [
            {"$group": {"_id": "$url", "dups": {"$push": "$_id"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}}
        ]
        duplicates = list(self.db[QCWY_STEP1_VERIFY_LOGS_TABLE].aggregate(pipeline))
        for duplicate in duplicates:
            dups = duplicate["dups"]
            dups.pop(0)  # 保留第一个文档
            self.db[QCWY_STEP1_VERIFY_LOGS_TABLE].delete_many({"_id": {"$in": dups}})

        # 验证两张表的对应的 url 是否一致
        url_set1 = set(self.db[QCWY_VERIFY_LOGS_TABLE].find({}, {"url": 1, "_id": 0}).distinct("url"))
        url_set2 = set(self.db[QCWY_STEP1_VERIFY_LOGS_TABLE].find({}, {"url": 1, "_id": 0}).distinct("url"))
        if url_set1 == url_set2:
            count1 = self.db[QCWY_VERIFY_LOGS_TABLE].count_documents({})
            count2 = self.db[QCWY_STEP1_VERIFY_LOGS_TABLE].count_documents({})
            print(f"qcwy_step1_urls_part2 表的数据数量: {count1}")
            print(f"qcwy_step1_verify_logs_part2 表的数据数量: {count2}")
        else:
            print("两张表的 url 不一致")

        self.page.quit()
        self.client.close()


if __name__ == "__main__":
    verifier = QCWY_URL_Verifier()
    verifier.run()
    print("验证任务已完成")
# -*- coding: gbk -*-
from random import random
import requests
import re
import execjs
import jsonpath
import csv
import time
import random
from datetime import datetime
import pandas as pd

# 读取 JavaScript 加密文件
with open('../scripts/qianchengwuyou/QCWY.js', encoding='utf-8') as f:#../scripts/qianchengwuyou/QCWY.js
    js_code = f.read()
_cell = execjs.compile(js_code)

# 请求头配置
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "close",
    "From-Domain": "51job_web",
    "Pragma": "no-cache",
    "Referer": "https://we.51job.com/pc/search?keyword=%E4%BC%9A%E8%AE%A1&searchType=2&sortType=0&metro=",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "account-id;": "",
    "partner;": "",
    "property": "%7B%22partner%22%3A%22%22%2C%22webId%22%3A2%2C%22fromdomain%22%3A%2251job_web%22%2C%22frompageUrl%22%3A%22https%3A%2F%2Fwe.51job.com%2F%22%2C%22pageUrl%22%3A%22https%3A%2F%2Fwe.51job.com%2Fpc%2Fsearch%3Fkeyword%3D%25E4%25BC%259A%25E8%25AE%25A1%26searchType%3D2%26sortType%3D0%26metro%3D%22%2C%22identityType%22%3A%22%22%2C%22userType%22%3A%22%22%2C%22isLogin%22%3A%22%E5%90%A6%22%2C%22accountid%22%3A%22%22%7D",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    # "sign": "5509d264647dea0724a4b5d5362e3eaa5f9f290abd31c4971e433b39456be526",
    "user-token;": "",
    "uuid": "f7a111f2e61e9571dd1fb368a1fb93d0"
}

# CSV文件字段定义
CSV_FIELDS = [
    'unique_id', 'benefits', 'company_name', 'company_size', 'company_type',
    'crawl_time', 'education', 'experience', 'headcount', 'company_industry',
    'jobdescription', 'job_url', 'location', 'publish_time', 'job_salary',
    'skills', 'source', 'title'
]


def get_data(jobArea, industry, page):
    """获取指定条件的职位数据"""
    cookies = {
        "guid": "f7a111f2e61e9571dd1fb368a1fb93d0",
        "nsearch": "jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D",
        "search": "jobarea%7E%60%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%BB%E1%BC%C6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21",
        "acw_tc": "ac11000117226604806963490e0097689b55d5f2907bb0c58b4f2c143e48c7",
        "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%22f7a111f2e61e9571dd1fb368a1fb93d0%22%2C%22first_id%22%3A%2219112b76a8e83-05dbb07efb4b5c4-26001951-921600-19112b76a8f13a6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxMTJiNzZhOGU4My0wNWRiYjA3ZWZiNGI1YzQtMjYwMDE5NTEtOTIxNjAwLTE5MTEyYjc2YThmMTNhNiIsIiRpZGVudGl0eV9sb2dpbl9pZCI6ImY3YTExMWYyZTYxZTk1NzFkZDFmYjM2OGExZmI5M2QwIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22f7a111f2e61e9571dd1fb368a1fb93d0%22%7D%2C%22%24device_id%22%3A%2219112b76a8e83-05dbb07efb4b5c4-26001951-921600-19112b76a8f13a6%22%7D",
        # "acw_sc__v2": "66adb6821951992b774d83ab120d19f5c6d00ac3",
        "JSESSIONID": "8F2AA22A27794E4177D7EF03BCD02100",
        "ssxmod_itna": "QqUxR7i=e=wxl4iqYKYZ7D9Ax0Yx0EwfTq3ol4GNfeYDZDiqAPGhDC48tjqRATr5ieWpAuGdKeESi5F31IYxGCWgjvPDHxY=DUZYoeDx1q0rD74irDDxD3DbfdDSDWKD9D0RSBc6yKGWDmR8DWPDYxDrLaKDRxi7DDHQkx07DQvk1DDz1nO5TxGicY2GYUPwnrECqGYPWjKD9OoDsp0j1jKmn8k5ShYLUKA3px0keq0O9ryz1roDUBKsyPANbA+xbDrN314dqixYTo2r8m6eKii4KQGKT6Deqm0DTx+KjVw9HAs5DDPoF743YD==",
        "ssxmod_itna2": "QqUxR7i=e=wxl4iqYKYZ7D9Ax0Yx0EwfTq3oeA6n=PD/KmSDFgxY5w8o=ikHGFmWkKPqDPIT40xueFl7uIDEimA2sWEfeMjCWKQ1K=0Cuz=LWUzNNQxiXeEjjk8BNdHktuXiT/US1QpqO8QesVi0ikx+hHpG+DpBzm2Asxry1AxFtVmmbWrwbP/uzsReFn7e4uGahNOG=j+hWR0fxOxF4w8GmUYhi1+dQ2+a+KPwjtEm4jKLkWlY+echdCSiCeY5fulYOWiahYQPTPUPnu0AyQbRQ8lK=POcWLN9lTNZW2/=yg5HCZTxhBI+OPghPvQAEBPB1K8WUYct+iI5p0tP2zeK6eI3IqXiIZm5bxAN3Ii3eB6PmnPGWAZD4YSeG0YhBwsQun0A51AkUPoZNEpwx9RsKt/Zwh/=FbvxfRmzECBUsirlEKw4fszapDNoI28A6L+hViP0ja3ea0RK=+5qlRLUhNaRDS4ntyb4HKFHBEhWDG2bi4KGNKiAmijRKyDjGcbhv2hg2CTPkgIe9q5jxc95PDr+bDji5khCH9vqtCD5ibyy6KkxR4oD08DijtYD",
        "tfstk": "f7B-TZMtGr4ohzPhFgNDKbVEPQrDJTIPZaSsKeYoOZQAfNdINQ1hJBLA8UAkFpYdkM_T4H4PK05VSGMlE7JnpLJedP4gIRqP4pJIg6NZW4RXxHeHAYOWe8o_eP4gI-jfMAgLS6jXfAdvYEtWVeM7DKtyVptSd3ZvlHKZO4_BdoIXuhuSdH9BhntkjjUjeenW7vCCazndyzqIKvXvcy812kM64txJlFI5eDiQY3dJ5gTYSpnIWIse99oEpCs5_w-1P4ap8tIfF1__obY56HIG9gwShLXPV1OCCylCWLQp1TOxAYpVqEpvcOZn_EXvrw6JGlD9tK6M1L10gzAHehQCUanKdNscjTRVpP3X8_xwhHBUfXLpOgRcIOK7lVY9xbZYDXleNn0qNlnK0OdAtnLg0ZlETIK2DFqYDXleNn-vSoRZTXRv0"
    }
    params = {
        "api_key": "51job",
        "timestamp": "1722660517",
        "keyword": "",
        "searchType": "2",
        "function": "",
        "industry": industry,
        "jobArea": jobArea,
        "jobArea2": "",
        "landmark": "",
        "metro": "",
        "salary": "",
        "workYear": "",
        "degree": "",
        "companyType": "",
        "companySize": "",
        "jobType": "",
        "issueDate": "",
        "sortType": "0",
        "pageNum": page,
        "requestId": "d107ae451130f2248175f8009071b07e",
        "pageSize": "20",
        "source": "1",
        "accountId": "",
        "pageCode": "sou|sou|soulb"
    }
    #代理-快代理测试
    import requests

    # 隧道域名:端口号
    tunnel = "m246.kdltps.com:15818"

    # 用户名密码方式
    username = "t14020051919793"
    password = "13f5c1s9"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }







    url = "https://we.51job.com/api/job/search-pc"
    # try:
    #     # 第一次请求获取加密参数
    #     response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies)
    #     arg1 = re.findall("var arg1='(.*?)';", response.text)[0]
    #     acw_sc__v2 = _cell.call("get_arg1", arg1)
    #
    #     # 更新cookies后再次请求
    #     cookies['acw_sc__v2'] = acw_sc__v2
    #     res2 = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies)
    #
    #     # 解析数据
    #     items = jsonpath.jsonpath(res2.json(), '$..items')
    #     if not items:
    #         return []
    #
    #     return [process_item(data) for data in items[0]]
    #
    # except Exception as e:
    #     print(f"请求失败: {str(e)}")
    #     return []
    for attempt in range(3):  # 最大重试次数
        try:
            # 第一次请求获取加密参数
            response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies)
            response.raise_for_status()  # 检查请求是否成功
            arg1 = re.findall("var arg1='(.*?)';", response.text)[0]
            acw_sc__v2 = _cell.call("get_arg1", arg1)

            # 更新cookies后再次请求
            cookies['acw_sc__v2'] = acw_sc__v2
            res2 = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies)
            res2.raise_for_status()  # 检查请求是否成功

            # 解析数据
            items = jsonpath.jsonpath(res2.json(), '$..items')
            if not items:
                return []
            return [process_item(data) for data in items[0]]

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {str(e)}，重试第 {attempt + 1} 次")
            time.sleep(5)  # 等待5秒后重试，您可以根据需求调整等待时间
            if attempt == 2:  # 如果达到最大重试次数，打印日志或处理最终失败
                print(f"是否收集的请求最终失败，jobArea={jobArea}, industry={industry}, page={page}")
                return []

def process_item(data):
    """处理单条职位数据"""
    return {
        "unique_id": data.get('jobId', 'N/A'),
        "benefits": "nan",
        "company_name": data.get('companyName', 'N/A'),
        "company_size": data.get('companySizeString', 'N/A'),
        "company_type": data.get('companyTypeString', 'N/A'),
        "crawl_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "education": data.get('degreeString', 'N/A'),
        "experience": data.get('workYearString', 'N/A'),
        "headcount": "nan",
        "company_industry": data.get('companyIndustryType1Str', 'N/A'),
        "jobdescription": data.get('jobDescribe', 'N/A'),
        "job_url": data.get('jobHref', 'N/A'),
        "location": data.get('jobAreaString', 'N/A'),
        "publish_time": data.get('confirmDateString', 'N/A'),
        "job_salary": data.get('provideSalaryString', 'N/A'),
        "skills": "nan",
        "source": 'qianchengwuyou',
        "title": data.get('jobName', 'N/A'),
    }


def main():
    """主程序"""
    # 初始化CSV文件
    with open('jobs.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()

        # 使用pandas读取CSV文件的第二列
        job_area_data = pd.read_csv('../data/qianchengwuyou/qianchengwuyou_job_area_data.csv', encoding='utf-8', dtype={'后6位数字': str})#'../data/qianchengwuyou/qianchengwuyou_job_area_data.csv'
        job_areas = job_area_data['后6位数字'].tolist()  # 直接获取“后6位数字”列数据

        # # 遍历所有组合
        # for industry in (f"{i:02d}" for i in range(1, 64)):
        #     for jobArea in job_areas:
        #         for page in range(1, 2):
        #             # 获取数据并写入文件
        #             items = get_data(jobArea, industry, page)
        #             if items:
        #                 writer.writerows(items)
        #                 print(f"已写入 {len(items)} 条数据：地区={jobArea}, 行业={industry}, 页码={page}")
        #
        #             # 随机延迟（3-5秒）
        #             delay = random.uniform(3, 5)
        #             print(f"等待 {delay:.2f} 秒...")
        #             time.sleep(delay)
        # 遍历所有组合
        for jobArea in job_areas:  # 先遍历 jobArea
            for industry in (f"{i:02d}" for i in range(1, 64)):  # 然后遍历 industry
                for page in range(1, 2):
                    # 获取数据并写入文件
                    items = get_data(jobArea, industry, page)
                    if items:
                        writer.writerows(items)
                        print(f"已写入 {len(items)} 条数据：地区={jobArea}, 行业={industry}, 页码={page}")

                    # 随机延迟（3-5秒）
                    delay = random.uniform(3, 4)
                    print(f"等待 {delay:.2f} 秒...")
                    time.sleep(delay)
if __name__ == "__main__":
    main()
# 已写入 20 条数据：地区=010000, 行业=01, 页码=1
# 等待 4.75 秒...
# 已写入 20 条数据：地区=010000, 行业=02, 页码=1
# 等待 3.54 秒...
# 已写入 20 条数据：地区=010000, 行业=03, 页码=1
# 等待 3.36 秒...
# 已写入 20 条数据：地区=010000, 行业=04, 页码=1
# 等待 4.25 秒...
# 已写入 20 条数据：地区=010000, 行业=05, 页码=1
# 等待 3.90 秒...
# 已写入 20 条数据：地区=010000, 行业=06, 页码=1
# 等待 4.59 秒...
# 已写入 20 条数据：地区=010000, 行业=07, 页码=1
# 等待 4.68 秒...
# 已写入 20 条数据：地区=010000, 行业=08, 页码=1
# 等待 3.43 秒...
# 已写入 20 条数据：地区=010000, 行业=09, 页码=1
# 等待 4.86 秒...
# 等待 3.06 秒...
# 请求失败: list index out of range
# 等待 3.72 秒...
# 请求失败: list index out of range
# 等待 3.50 秒...



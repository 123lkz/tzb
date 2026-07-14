# -*- coding: utf-8 -*-
import csv
import requests
import time
import random
import pandas as pd  # 引入 pandas 库
from datetime import datetime  # 用于时间比较

cookies = {
    '_ga': 'GA1.2.86406105.1740364190',
    '_gid': 'GA1.2.1146682772.1740364190',
    'mantis8961': 'ccf1c9f133ef4d7799be1762accae0ee@8961',
}

headers = {
    'Accept': 'application/json, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/133.0.0.0 Safari/537.36',
}

json_data = {
    'page': 1,
    'page_size': 50,
    'profession_id': [0],
    'exam_id': [2],  # 1国考2省考3事业单位4军队文职5银行招聘
    'words': '',
    'exclude_words': '',
}

# 设置 **截止日期**
cutoff_date = datetime.strptime("2024-10-01", "%Y-%m-%d")

# 打开 CSV 文件并写入标题行
with open('公务员职位信息.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.DictWriter(file, fieldnames=["title", "publish_time", "公告名称", "考试名称", "location", "company_name",
                                              "专业要求", "招聘人数", "education", "jobdescription", "面试比例", "job_url","source"])
    writer.writeheader()

    # 遍历 area_id（2 到 34）
    for area in range(2, 35):
        json_data['area_id'] = [area]  # 设置当前 area_id
        page = 1  # 初始化页码
        stop_crawling = False  # **新增变量：是否停止爬取该地区**

        while not stop_crawling:  # **循环遍历所有页**
            json_data['page'] = page  # 设置当前页数
            print(f"正在爬取 area_id = {area}, 第 {page} 页...")

            # 发送请求
            response = requests.post('https://ajax.eoffcn.com/api/radar/position/list', cookies=cookies,
                                     headers=headers, json=json_data)

            if response.status_code != 200:  # **检查请求是否成功**
                print(f"请求失败，状态码：{response.status_code}")
                break

            response_json = response.json()

            # 获取职位列表
            job_list = response_json.get('data', {}).get('list', [])

            if not job_list:  # **如果没有数据，说明到达最后一页，跳出循环**
                print(f"area_id = {area} 全部数据爬取完毕！")
                break

            # 遍历职位列表
            for job in job_list:
                pub_time = job['pubTime']  # 获取发布日期（格式如 "2024-09-30"）
                pub_date = datetime.strptime(pub_time, "%Y-%m-%d")  # 转换为 datetime 类型

                # **如果发布日期 < 2024-10-01，停止当前地区爬取**
                if pub_date < cutoff_date:
                    print(f"检测到 {area} 地区的职位发布日期 {pub_time} < 2024-10-01，停止爬取此地区")
                    stop_crawling = True  # 标记停止
                    break  # **跳出职位遍历**

                # 继续保存数据
                job_data = {
                    "title": job['name'],
                    "publish_time": pub_time,
                    "公告名称": job['announcementName'],
                    "考试名称": job['examName'],
                    "location": job['districtName'],
                    "company_name": job['workUnitName'],
                    "专业要求": job['professional'],
                    "招聘人数": job['recruitsNum'],
                    "education": job['educational'],
                    "jobdescription": job['brief'],
                    "面试比例": job['percent'],
                    "job_url": job['site'],
                    "source":'zhonggong',
                }

                writer.writerow(job_data)  # **直接写入 CSV**

            # **当前页爬取完成，准备请求下一页**
            if stop_crawling:
                break  # **停止该地区爬取**
            page += 1

            # **随机 sleep，防止被封**
            time.sleep(random.uniform(1, 3))  # 随机暂停 1~3 秒

print("数据已成功写入 CSV 文件！")
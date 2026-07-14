#from .base_spider import BaseSpider

#class Spider58(BaseSpider):
#    name = '58'
#    allowed_domains = ['58.com']
#    start_urls = ['https://www.58.com'] 
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 请求头信息
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "xz.58.com",
    "Referer": "https://xz.58.com/quanzhizhaopin/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "Cookie": "f=n; commontopbar_new_city_info=471%7C%E5%BE%90%E5%B7%9E%7Cxz; userid360_xml=7538C9E683EBF6AE38FC961C9BE7C522; time_create=1742630801243; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; f=n; commontopbar_new_city_info=471%7C%E5%BE%90%E5%B7%9E%7Cxz; id58=ChBPl2e0S8JOz1ekHWVcAg==; 58tj_uuid=3d12dfc5-37ef-40fe-8e81-4ded54855dc1; als=0; wmda_uuid=2f8457ccb29d8e9ef1aea24a7131bf0e; wmda_new_uuid=1; xxzlclientid=b377a645-caeb-4347-90a1-1739869165452; xxzlxxid=pfmxSyjRlnDcFcb7TPNxEYJBn0jQzdKL/sX8nkbGNsxEi7yQtLglcuB4yZbcJQ+NWeI9; __utma=253535702.1798001534.1739885442.1739885442.1739885442.1; __utmz=253535702.1739885442.1.1.utmcsr=cn.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/job.shtml; myfeet_tooltip=end; wmda_visited_projects=%3B1731916484865%3B10104579731767%3B2286118353409; 58uname=h6z72vaku; passportAccount=atype=0&bstate=0; 58home=xz; fzq_h=59ba443cd401c6a17236ed9b1258b893_1740044673758_03c7ad02a80f42678d47e5319d096bcf_42540765144255954245029899102060523709; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1740071649; ppStore_fingerprint=3E9AFCB3760118660E572374DC58570C9816598E29B72B91%EF%BC%BF1740071657950; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; Hm_lvt_b4a22b2e0b326c2da73c447b956d6746=1739949928,1739953725,1739965088,1740112476; Hm_lpvt_b4a22b2e0b326c2da73c447b956d6746=1740112476; HMACCOUNT=0D589B1455536F38; ipcity=bj%7C%u5317%u4EAC; f=n; commontopbar_new_city_info=471%7C%E5%BE%90%E5%B7%9E%7Cxz; sessionid=abd593ef-3c1c-4192-b50f-25b80aa371c9; city=bj; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1740038801,1740069775,1740112501; JSESSIONID=D0F5F46A04E8823F27B3FC6407B87736; wmda_report_times=1; new_uv=12; utm_source=; spm=; init_refer=https%253A%252F%252Fxz.58.com%252Fquanzhizhaopin%252Fpn9%252F%253Fpid%253D791651588015882242%2526PGTID%253D0d3002a2-001d-7e79-5cf6-9ef47ffce4be%2526ClickID%253D3; new_session=0; qz_gdt=; wmda_session_id_1731916484865=1740118275082-b0c7c9e0-9d0a-09a6-856141bc-; fzq_js_zhaopin_list_pc=9363e913fcee17e625618c00e853d33f_1740118275245_9; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1740118275; PPU=UID=110211973657667&UN=h6z72vaku&TT=95027a41c7e89d22c8cf7a732f8d76a7&PBODY=ISBO0cbplbkdBkIEYSL_wOeVAGilWbLgzH2JzNmLg0FcJnS8VIHe92tE2wqjDh78qtWWfrFKqvSkxc4Tcu4DzXrtoaYnGNUL8_aP9olbO86z5wHdOlW7VSqxR-js9GJ4jLQ5volcog-vtzLNifLAwNWuIEInJkyTSdxJ6R1-eeI&VER=1&CUID=f-i3Tdmeu94o4U2czs8ipg; xxzlbbid=pfmbM3wxMDI5MnwxLjEwLjB8MTc0MDExODI3NjM1NDMzODU5MHx5UVluZEdacmNzNHM4RjJhdmdacmZKWVBob09xc0RkZDByR3d4cUc4VkN3PXwxZDJlZDBiZTA5OGY4YzA4MGNiMmY0NWFiMjJmMjJhMl8xNzQwMTE4Mjc1NjAyX2ZhMzM4ZmFjMjFmZjQ2ZmI5NWI1MDEwZGU4YTExNmFiXzE5Mjg3NzYwNzh8NGQxYzIxZWNmMWZlZTZjZDIzZDM4YWM0YmQ3MjlkMzVfMTc0MDExODI3NjE0Ml8yNTY="  # 请替换为实际cookie
}

# 存储数据的列表
job_data = []

# 获取职位类别链接
def get_job_links():
    job_links = []
    response = requests.get("https://xz.58.com/quanzhizhaopin/", headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        filter_items = soup.find('div', id='filterJob').find_all('li')
        for item in filter_items:
            a_tag = item.find('a')
            if a_tag and 'href' in a_tag.attrs:
                job_links.append(a_tag['href'])  # 获取职位链接
    return job_links

# 根据职位链接爬取数据，支持翻页，最多爬取10页
def scrape_jobs_from_category(job_link):
    # 解析出fullPath和其他必要的参数
    full_path = job_link.split('fullPath=')[-1]
    base_data_url = f"https://xz.58.com/{job_link.split('/')[3]}/?fullPath={full_path}&PGTID=0d202408-0000-174f-6ff7-28c65e44b587&ClickID=2"  # 示例PGTID和ClickID，需根据实际情况调整

    page = 1
    while page <= 10:  # 限制最多爬取10页
        # 构造翻页URL
        url = f"{base_data_url}&pn={page}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"正在爬取：{url}")
            soup = BeautifulSoup(response.text, 'html.parser')
            job_items = soup.find_all('li', class_='job_item clearfix')

            # 如果没有找到职位信息，则停止翻页
            if not job_items:
                print("没有更多职位信息，停止翻页。")
                break

            for job in job_items:
                # 获取职位链接
                job_link = job.find('a')  # 找到职位名称中的链接
                job_url = job_link['href'] if job_link else '无'  # 检查链接是否存在
                
                # 获取地点
                address = job.find('span', class_='address')
                address_text = address.get_text(strip=True) if address else '无'  # 检查地址是否存在

                # 获取名称
                name = job.find('span', class_='name')
                name_text = name.get_text(strip=True) if name else '无'  # 检查名称是否存在
                
                # 获取工资
                salary = job.find('p', class_='job_salary')
                salary_text = salary.get_text(strip=True) if salary else '无'  # 检查工资是否存在
                
                # 获取标签
                tags_div = job.find('div', class_='job_wel clearfix')
                tags_list = []
                if tags_div:
                    tags = tags_div.find_all('span')
                    tags_list = [tag.get_text(strip=True) for tag in tags]

                # 获取公司名称
                company = job.find('div', class_='comp_name').find('a')
                company_text = company.get_text(strip=True) if company else '无'  # 检查公司是否存在

                # 获取要求中的三个小项：工作类别、学历、经验
                job_category = '无'
                education = '无'
                experience = '无'
                
                # 提取工作类别
                cate = job.find('span', class_='cate')
                if cate:
                    job_category = cate.get_text(strip=True)

                # 提取学历
                xueli = job.find('span', class_='xueli')
                if xueli:
                    education = xueli.get_text(strip=True)

                # 提取经验
                jingyan = job.find('span', class_='jingyan')
                if jingyan:
                    experience = jingyan.get_text(strip=True)

                # 将数据添加到列表
                job_data.append({
                    '链接': job_url,
                    '地点': address_text,
                    '名称': name_text,
                    '工资': salary_text,
                    '标签': ', '.join(tags_list),
                    '公司': company_text,
                    '工作类别': job_category,
                    '学历': education,
                    '经验': experience,
                })

            # 翻页
            page += 1
        else:
            print(f"请求失败，状态码：{response.status_code}")
            break

# 主程序
job_links = get_job_links()  # 获取所有职位类别链接

for job_link in job_links:
    scrape_jobs_from_category(job_link)  # 爬取每个职位类别的数据

# 输出爬取到的数据
#print(job_data)

# 将数据转换为DataFrame
df = pd.DataFrame(job_data)

# 保存到Excel文件
df.to_excel('job_data.xlsx', index=False)

print("数据已成功保存到 job_data.xlsx")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
猎聘网城市信息获取工具
功能：通过API获取猎聘网各省区下的城市信息，并保存到JSON文件

主要步骤：
1. 从province_type_code.json读取省区代码
2. 对每个省区调用API获取城市信息
3. 将获取到的城市信息保存到新的JSON文件

数据存储：
- 输入文件：data/liepin/province_type_code.json
- 输出文件：data/liepin/city_info.json
"""

import json
import logging
import requests
import time
from pathlib import Path
from typing import Dict, List

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CityInfoFetcher:
    """猎聘网城市信息获取工具"""
    
    def __init__(self):
        # API配置
        self.city_api_url = "https://api-c.liepin.com/api/com.liepin.searchfront4c.pc-search-job-cond-init"
        
        # 文件路径
        self.project_root = Path(__file__).parent.parent.parent
        self.province_file = self.project_root / "data" / "liepin" / "province_type_code.json"
        self.city_file = self.project_root / "data" / "liepin" / "city_info.json"
        
        # 确保输出目录存在
        self.city_file.parent.mkdir(parents=True, exist_ok=True)
    
    def get_city_info(self, province_code: str) -> List[dict]:
        """通过API获取省区下的城市信息"""
        try:
            # 构建请求头
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
                "Origin": "https://www.liepin.com",
                "Referer": "https://www.liepin.com/",
                "Sec-Ch-Ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "X-Client-Type": "web",
                "X-Fscp-Bi-Stat": '{"location": "https://www.liepin.com/zhaopin/?city=250140&dq=250140&pubTime=&currentPage=0&pageSize=40&key=Java&suggestTag=&workYearCode=&compId=&compName=&compTag=&industry=&salaryCode=&jobKind=&compScale=&compKind=&compStage=&eduLevel=&otherCity=&sfrom=search_job_pc&ckId=4dlkoxxfztinvl6ix3e1r250iykclq79&skId=ycyfaykmaqchp9xgiqtnorly7qkpewua&fkId=4dlkoxxfztinvl6ix3e1r250iykclq79&scene=condition&suggestId="}',
                "X-Fscp-Fe-Version": "",
                "X-Fscp-Std-Info": '{"client_id": "40108"}',
                "X-Fscp-Trace-Id": "a0b343ee-dab0-48d4-9509-3a3c6d6c000e",
                "X-Fscp-Version": "1.1",
                "X-Requested-With": "XMLHttpRequest",
                "X-Xsrf-Token": "ArB1SMFrRZO18mxbOOdPOQ",
                "Cookie": "inited_user=f61147a6170aa5a5b3047399f04fc796; XSRF-TOKEN=ArB1SMFrRZO18mxbOOdPOQ; __gc_id=3dad4c755de14778bdf9438f7a067a0e; __uuid=1748395987113.72; hpo_role-sec_project=sec_project_liepin; hpo_sec_tenant=0; _ga=GA1.1.1769692972.1748395992; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1748395992; HMACCOUNT=55B60FA1F020E7A1; __tlog=1748395987145.41%7C00000000%7C00000000%7Cs_o_009%7Cgg_pc_02; _gcl_aw=GCL.1748483373.CjwKCAjw6NrBBhB6EiwAvnT_roLM0VcKWUt5ACvPaE2QtHZWcf2237wml4pHCJmkbzRaPlHkmAUgHBoC02EQAvD_BwE; _gcl_gs=2.1.k1$i1748483371$u167471928; _gcl_au=1.1.1989709726.1748483373.1286268244.1748483379.1748483378; user_roles=0; user_photo=5f8fa3bc8dbe6273dcf85e5e08u.png; user_name=%E8%83%A1%E5%B0%8F; need_bind_tel=false; new_user=false; c_flag=93be4d678ef7b2021a988848acb2751f; imId=a1103676d495eaa09b95c8b3fab76db8; imId_0=a1103676d495eaa09b95c8b3fab76db8; imClientId=a1103676d495eaa0a4ca3863b012351a; imClientId_0=a1103676d495eaa0a4ca3863b012351a; imApp_0=1; inited_user=f61147a6170aa5a5b3047399f04fc796; fe_im_socketSequence_new_0=5_5_5; fe_im_connectJson_0=%7B%220_ac322420791966d141344312b1f2ca2b%22%3A%7B%22socketConnect%22%3A%222%22%2C%22connectDomain%22%3A%22liepin.com%22%7D%7D; fe_im_opened_pages=; city_site=bj; acw_tc=1a0c651417489148347217854e0051f7544295937d20d88eddf3528a5dec70; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1748915328; _ga_54YTJKWN86=GS2.1.s1748912533$o10$g1$t1748915796$j60$l0$h0; __session_seq=306; __tlg_event_seq=1372"
            }
            
            # 构建请求数据
            data = f"selectedDqCode={province_code}"
            
            # 发送请求
            logger.info(f"正在请求省区 {province_code} 的城市信息...")
            logger.info(f"请求URL: {self.city_api_url}")
            logger.info(f"请求数据: {data}")
            
            response = requests.post(
                self.city_api_url, 
                data=data,  # 使用form-urlencoded格式
                headers=headers,
                verify=False,  # 忽略SSL证书验证
                timeout=30  # 设置超时时间
            )
            
            # 记录响应信息
            logger.info(f"响应状态码: {response.status_code}")
            logger.info(f"响应头: {dict(response.headers)}")
            
            response.raise_for_status()  # 检查响应状态
            
            # 解析响应
            result = response.json()
            logger.info(f"响应内容: {result}")
            
            if 'data' in result:
                cities = result['data'].get('dqs', [])
                logger.info(f"成功获取省区 {province_code} 下的 {len(cities)} 个城市信息")
                return cities
            else:
                logger.error(f"获取城市信息失败: {result.get('msg', '未知错误')}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"错误响应内容: {e.response.text}")
            return []
        except Exception as e:
            logger.error(f"获取城市信息时出错: {str(e)}")
            return []
    
    def load_province_codes(self) -> Dict[str, List[str]]:
        """加载省区代码"""
        try:
            with open(self.province_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"成功加载 {len(data)} 个省区代码")
            return data
        except Exception as e:
            logger.error(f"加载省区代码失败: {str(e)}")
            return {}
    
    def save_city_info(self, city_info: Dict[str, List[dict]]):
        """保存城市信息到JSON文件"""
        try:
            with open(self.city_file, 'w', encoding='utf-8') as f:
                json.dump(city_info, f, ensure_ascii=False, indent=2)
            logger.info(f"成功保存城市信息到 {self.city_file}")
        except Exception as e:
            logger.error(f"保存城市信息失败: {str(e)}")
    
    def run(self):
        """运行获取城市信息的主流程"""
        try:
            # 加载省区代码
            province_data = self.load_province_codes()
            if not province_data:
                return
            
            # 获取每个省区的城市信息
            city_info = {}
            for province_code, cities in province_data.items():
                # 获取城市信息
                city_list = self.get_city_info(province_code)
                
                # 创建城市代码到名称的映射
                city_map = {city['code']: city['name'] for city in city_list}
                
                # 保存城市信息
                city_info[province_code] = [
                    {
                        'code': city_code,
                        'name': city_map.get(city_code, city_code)
                    }
                    for city_code in cities
                ]
                
                # 添加延迟，避免请求过快
                time.sleep(3)
            
            # 保存所有城市信息
            self.save_city_info(city_info)
            
        except Exception as e:
            logger.error(f"运行出错: {str(e)}")
            raise

def main():
    """主函数"""
    try:
        # 创建获取器实例
        fetcher = CityInfoFetcher()
        # 运行获取流程
        fetcher.run()
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main() 
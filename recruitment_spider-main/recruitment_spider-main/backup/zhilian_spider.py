import json
import time
import random
import pandas as pd
from pathlib import Path
from typing import Dict, List
from urllib.parse import urlencode
from scrapy import Request
import os

from recruitment_spider.spiders.base_spider import BaseSpider
from recruitment_spider.auth.zhilian.auth_helper import ZhilianAuthHelper

class ZhilianSpider(BaseSpider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    
    def __init__(self, *args, **kwargs):
        super(ZhilianSpider, self).__init__(*args, **kwargs)
        self.api_url = 'https://fe-api.zhaopin.com/c/i/search/positions'
        self.auth_helper = ZhilianAuthHelper()
        self.job_keys = set()  # 用于职位去重
        
        # 添加 User-Agent 列表
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36'
        ]
        
        # 设置数据文件路径
        self.data_dir = Path(__file__).parent.parent / 'data'
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True)
        
        # 加载基础数据
        self.base_data = self._load_base_data()
        self.categories = self.get_filtered_categories()
        self.processed_combinations = 0
        self.combination_count = 0
        
        # 计算理论上的总组合数
        self.need_category_keys = [
            'companyType',
            # 'salaryType',
            # 'companySize',
            # 'educationType',
            # 'jobStatus',
            # 'jobType'
        ]
        self.total_combinations = 1
        for key in self.need_category_keys:
            if key in self.categories:
                self.total_combinations *= len(self.categories[key])
        self.logger.info(f"理论总组合数: {self.total_combinations}")
    
    def get_headers(self):
        """生成请求头"""
        request_params = self.auth_helper._generate_request_params()
        return {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://sou.zhaopin.com',
            'Pragma': 'no-cache',
            'Referer': 'https://sou.zhaopin.com/',
            'User-Agent': random.choice(self.user_agents),
            'x-zp-client-id': request_params['x-zp-client-id'],
            'x-zp-page-request-id': request_params['x-zp-page-request-id']
        }
    
    def _load_base_data(self):
        """从本地文件加载base_data数据"""
        try:
            base_data_path = self.data_dir / 'zhilian' / 'base_data.json'
            if not base_data_path.exists():
                # 如果data/zhilian目录下没有，尝试从zhilianpachong目录复制
                zhilianpachong_path = Path(__file__).parent.parent / 'zhilianpachong' / 'base_data.json'
                if zhilianpachong_path.exists():
                    import shutil
                    os.makedirs(base_data_path.parent, exist_ok=True)  # 确保目录存在
                    shutil.copy(str(zhilianpachong_path), str(base_data_path))
                    self.logger.info(f"已从 {zhilianpachong_path} 复制基础数据文件到 {base_data_path}")
                else:
                    self.logger.error(f"基础数据文件不存在: {zhilianpachong_path}")
                    return {}
            
            with open(base_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except FileNotFoundError:
            self.logger.warning(f"未找到base_data.json文件: {base_data_path}")
            return {}
        except json.JSONDecodeError:
            self.logger.warning(f"base_data.json文件格式错误: {base_data_path}")
            return {}
    
    def get_filtered_categories(self):
        """获取过滤后的分类组合"""
        if not self.base_data:
            return {}
            
        data = self.base_data.get('data', {})
        categories = {}
        
        # 处理所有主要分类
        category_keys = {
            'companyType': '公司类型',
            'salaryType': '薪资范围',
            'educationType': '教育程度',
            'workExpType': '工作经验',
            'jobStatus': '工作性质',
            'companySize': '公司规模'
        }
        
        # 处理基础分类
        for key, display_name in category_keys.items():
            if key in data:
                items = [
                    {'code': item['code'], 'name': item['name']}
                    for item in data[key]
                    if item.get('code')  # 排除没有code的项
                ]
                if items:
                    categories[key] = items
                    self.logger.info(f"{display_name}分类数量: {len(items)}")
        
        # 处理职位类型（三级分类）
        if 'jobType' in data:
            job_types = self.get_nested_items(data['jobType'])
            if job_types:
                job_types.sort(key=lambda x: x['full_name'])
                categories['jobType'] = job_types
                self.logger.info(f"职位类型分类数量: {len(job_types)}")
        
        return categories
    
    def get_nested_items(self, items: List, parent_name: str = "", parent_codes: List[str] = None) -> List[Dict]:
        """递归获取所有层级的分类项"""
        result = []
        parent_codes = parent_codes or []
        
        for item in items:
            if item.get('name') == '不限' or not item.get('code'):
                continue
                
            current_name = f"{parent_name}-{item['name']}" if parent_name else item['name']
            current_codes = parent_codes + [item['code']]
            
            if item.get('sublist'):
                result.extend(self.get_nested_items(item['sublist'], current_name, current_codes))
            else:
                result.append({
                    'code': ','.join(current_codes),
                    'name': item['name'],
                    'full_name': current_name,
                    'parent_code': item.get('parentCode')
                })
        
        return result
    
    def get_city_districts(self, items: List) -> List[Dict]:
        """获取城市和行政区数据"""
        result = []
        
        for province in items:
            province_code = province.get('code')
            province_name = province.get('name')
            
            # 处理直辖市和特殊城市
            if not province.get('sublist'):
                if province_code:
                    result.append({
                        'province_code': province_code,
                        'province_name': province_name,
                        'city_code': province_code,
                        'city_name': province_name,
                        'full_name': province_name,
                        'district_code': None,
                        'district_name': None
                    })
                continue
            
            # 处理普通省份下的城市
            for city in province['sublist']:
                if not city.get('code'):
                    continue
                    
                if not city.get('sublist'):
                    result.append({
                        'province_code': province_code,
                        'province_name': province_name,
                        'city_code': city['code'],
                        'city_name': city['name'],
                        'full_name': f"{province_name}-{city['name']}",
                        'district_code': None,
                        'district_name': None
                    })
                    continue
                
                # 处理城市下的行政区
                has_valid_district = False
                for district in city['sublist']:
                    if district.get('code'):
                        has_valid_district = True
                        result.append({
                            'province_code': province_code,
                            'province_name': province_name,
                            'city_code': city['code'],
                            'city_name': city['name'],
                            'full_name': f"{province_name}-{city['name']}-{district['name']}",
                            'district_code': district['code'],
                            'district_name': district['name']
                        })
                
                if not has_valid_district:
                    result.append({
                        'province_code': province_code,
                        'province_name': province_name,
                        'city_code': city['code'],
                        'city_name': city['name'],
                        'full_name': f"{province_name}-{city['name']}",
                        'district_code': None,
                        'district_name': None
                    })
        
        return result
    
    def start_requests(self):
        """开始请求"""
        try:
            # 获取认证信息
            cookies_str, url_params = self.auth_helper.get_auth_info()
            if not cookies_str or not url_params:
                self.logger.error("获取认证信息失败")
                return
            
            # 生成所有分类组合
            def generate_combinations(current_dict: Dict, category_index: int = 0):
                if category_index >= len(self.need_category_keys):
                    self.combination_count += 1
                    combo_info = ", ".join([
                        f"{k.replace('Type', '')}: {v['name']}"
                        for k, v in current_dict.items()
                    ])
                    
                    # 每100个组合显示一次进度
                    if self.combination_count % 100 == 0:
                        self.logger.info(f"已生成 {self.combination_count}/{self.total_combinations} 个组合")
                    
                    self.logger.info(f"正在爬取: {combo_info}")
                    
                    payload = {
                        "S_SOU_WORK_CITY": "489",  # 固定使用全国
                        "order": 4,
                        "pageSize": 20,
                        "pageIndex": 1,
                        "eventScenario": "pcSearchedSouSearch",
                        "anonymous": 1
                    }
                    
                    # 添加分类参数
                    param_mapping = {
                        'companyType': 'S_SOU_COMPANY_TYPE',
                        # 'salaryType': 'S_SOU_SALARY',
                        # 'companySize': 'S_SOU_COMPANY_SCALE',
                        # 'educationType': 'S_SOU_EDUCATION_LOWESTLEVEL',
                        # 'jobStatus': 'S_SOU_POSITION_TYPE',
                        # 'jobType': 'S_SOU_JD_JOB_LEVEL3'
                    }
                    
                    for key, value in current_dict.items():
                        if key in param_mapping:
                            if key == 'jobType':
                                codes = value['code'].split(',')
                                payload[param_mapping[key]] = codes[-1]
                                continue
                            payload[param_mapping[key]] = value['code']
                    
                    headers = self.get_headers()
                    headers['Cookie'] = cookies_str
                    
                    return {
                        'request': Request(
                            url=self.api_url,
                            method='POST',
                            headers=headers,
                            body=json.dumps(payload),
                            callback=self.parse_job_list,
                            meta={
                                'page': 1,
                                'payload': payload,
                                'params': url_params,
                                'cookies_str': cookies_str,
                                'combo_info': current_dict
                            },
                            dont_filter=True
                        ),
                        'delay': random.uniform(3, 7)
                    }
                
                result = []
                current_category = self.need_category_keys[category_index]
                if current_category not in self.categories:
                    return result
                    
                for item in self.categories[current_category]:
                    new_dict = current_dict.copy()
                    new_dict[current_category] = item
                    combo_result = generate_combinations(new_dict, category_index + 1)
                    if combo_result:
                        result.append(combo_result)
                
                return result
            
            # 展平组合结果并生成请求
            def flatten_combinations(combinations):
                if isinstance(combinations, dict):
                    return [combinations]
                
                result = []
                for item in combinations:
                    if isinstance(item, dict):
                        result.append(item)
                    else:
                        result.extend(flatten_combinations(item))
                return result
            
            # 生成所有组合
            all_combinations = generate_combinations({})
            flattened_combinations = flatten_combinations(all_combinations)
            
            # 按顺序发送请求
            for combo in flattened_combinations:
                request = combo['request']
                # 打印完整URL和参数
                self.logger.info(f"请求URL: {request.url}")
                self.logger.info(f"请求参数: {request.body.decode('utf-8')}")
                time.sleep(combo['delay'])
                yield request
                
        except Exception as e:
            self.logger.error(f"生成请求失败: {str(e)}")
    
    def parse_job_list(self, response):
        """解析职位列表"""
        try:
            data = json.loads(response.text)
            
            # 处理认证失效的情况
            if data.get('code') != 200:
                if 'unauthorized' in str(data).lower():
                    self.logger.info("认证已失效，重新获取认证信息...")
                    cookies_str, url_params = self.auth_helper.get_auth_info()
                    if cookies_str and url_params:
                        payload = response.meta['payload']
                        headers = self.get_headers()
                        headers['Cookie'] = cookies_str
                        
                        yield Request(
                            url=self.api_url,
                            method='POST',
                            headers=headers,
                            body=json.dumps(payload),
                            callback=self.parse_job_list,
                            meta={
                                'page': response.meta['page'],
                                'payload': payload,
                                'params': url_params,
                                'cookies_str': cookies_str,
                                'combo_info': response.meta.get('combo_info')
                            },
                            dont_filter=True
                        )
                    return
                
                self.logger.error(f'API返回错误: {data}')
                return
            
            job_list = data.get('data', {}).get('list', [])
            self.logger.info(f'当前页({response.meta["page"]})找到{len(job_list)}个职位')
            
            for job in job_list:
                job_item = self._parse_job_item(job)
                if job_item:
                    job_key = f"{job_item['公司名称']}_{job_item['职位名称']}_{job_item['工作地点']}"
                    if job_key not in self.job_keys:
                        self.job_keys.add(job_key)
                        yield job_item
            
            # 处理下一页
            current_page = response.meta['page']
            total = data.get('data', {}).get('total', 0)
            if current_page * 20 < min(total, 600):  # 限制最多爬取30页
                payload = response.meta['payload'].copy()
                payload['pageIndex'] = current_page + 1
                
                headers = self.get_headers()
                headers['Cookie'] = response.meta['cookies_str']
                
                time.sleep(random.uniform(3, 7))
                
                yield Request(
                    url=self.api_url,
                    method='POST',
                    headers=headers,
                    body=json.dumps(payload),
                    callback=self.parse_job_list,
                    meta={
                        'page': current_page + 1,
                        'payload': payload,
                        'params': response.meta['params'],
                        'cookies_str': response.meta['cookies_str'],
                        'combo_info': response.meta.get('combo_info')
                    },
                    dont_filter=True
                )
                
        except json.JSONDecodeError:
            self.logger.error(f'JSON解析错误: {response.text[:200]}...')
        except Exception as e:
            self.logger.error(f'解析错误: {str(e)}')
    
    def _parse_job_item(self, job):
        """解析单个职位信息"""
        try:
            # 创建职位唯一标识
            job_id = job.get('jobId', '')
            company_id = job.get('companyId', '')
            unique_id = f"{job_id}_{company_id}"
            
            # 处理工作地点
            city = job.get('workCity', '')
            district = job.get('cityDistrict', '')
            street = job.get('streetName', '')
            location = f"{city} {district} {street}".strip()
            
            # 处理福利标签
            welfare = ', '.join(job.get('welfareTagList', []))
            
            # 处理技能标签
            skills = ', '.join([tag.get('name', '') for tag in job.get('jobSkillTags', [])])
            
            return {
                'unique_id': unique_id,
                '职位名称': job.get('name', ''),
                '公司名称': job.get('companyName', ''),
                '工作地点': location,
                '薪资': job.get('salary60', ''),
                '工作经验': job.get('workingExp', ''),
                '学历要求': job.get('education', ''),
                '公司规模': job.get('companySize', ''),
                '公司性质': job.get('property', ''),
                '职位链接': job.get('positionURL', ''),
                '发布时间': job.get('firstPublishTime', ''),
                '职位描述': job.get('jobSummary', ''),
                '所需人数': job.get('recruitNumber', ''),
                '福利待遇': welfare,
                '技能要求': skills,
                '行业': job.get('industryName', '')
            }
        except Exception as e:
            self.logger.error(f'职位解析错误: {str(e)}')
            return None

    def generate_request(self, current_dict, cookies_str, url_params):
        """生成请求"""
        combo_info = ", ".join([
            f"{k.replace('Type', '')}: {v['name']}"
            for k, v in current_dict.items()
        ])
        
        payload = {
            "S_SOU_WORK_CITY": "489",  # 固定使用全国
            "order": 4,
            "pageSize": 20,
            "pageIndex": 1,
            "eventScenario": "pcSearchedSouSearch",
            "anonymous": 1
        }
        
        # 添加分类参数
        param_mapping = {
            'companyType': 'S_SOU_COMPANY_TYPE',
            'salaryType': 'S_SOU_SALARY',
            'jobStatus': 'S_SOU_POSITION_TYPE',
            'jobType': 'S_SOU_JD_JOB_LEVEL3'
        }
        
        for key, value in current_dict.items():
            if key in param_mapping:
                if key == 'jobType':
                    codes = value['code'].split(',')
                    payload[param_mapping[key]] = codes[-1]
                    continue
                payload[param_mapping[key]] = value['code']
        
        # 打印完整的请求信息
        self.logger.info(f"组合信息: {combo_info}")
        self.logger.info(f"请求参数: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        
        headers = self.get_headers()
        headers['Cookie'] = cookies_str
        
        return Request(
            url=self.api_url,
            method='POST',
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse_job_list,
            meta={
                'page': 1,
                'payload': payload,
                'params': url_params,
                'cookies_str': cookies_str,
                'combo_info': current_dict
            },
            dont_filter=True
        ) 
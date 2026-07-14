#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
猎聘网爬虫 - 第三步
功能：将step2生成的URL平均分配到4个部分，为并行爬取做准备

主要步骤：
1. 从MongoDB加载step2生成的URL数据
2. 计算每个部分的大小（总数除以4，向上取整）
3. 清空原有的4个part集合
4. 将URL数据平均分配到4个part集合中
5. 为每个part集合创建必要的索引

数据存储：
- 输入集合：liepin_step1_urls_202504_log_part1
- 输出集合：
  * liepin_step2_urls_part1
  * liepin_step2_urls_part2
  * liepin_step2_urls_part3
  * liepin_step2_urls_part4
- 索引配置：
  * (industry_parent_code, industry_child_code, job_industry, job_category, job_type_name) - 唯一复合索引
  * status - 状态索引
  * create_time - 创建时间索引
  * part - 部分索引

数据分配策略：
1. 计算基础大小：total_urls // 4
2. 处理余数：如果total_urls % 4 != 0，则基础大小+1
3. 按顺序分配，确保每个部分大小相近
4. 最后一个部分可能略小（如果总数不能被4整除）

注意事项：
1. 分配前会清空所有part集合，确保数据一致性
2. 每个part集合都创建相同的索引结构
3. 记录每个part的URL数量，方便后续处理
4. 保持原有的URL数据结构不变，只增加part标记
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from pymongo import MongoClient
from tqdm import tqdm
import sys
import os

province_info = [
  {"code": "100", "name": "甘肃"},
  {"code": "110", "name": "广西"},
  {"code": "120", "name": "贵州"},
  {"code": "130", "name": "海南"},
  {"code": "140", "name": "河北"},
  {"code": "150", "name": "河南"},
  {"code": "160", "name": "黑龙江"},
  {"code": "170", "name": "湖北"},
  {"code": "180", "name": "湖南"},
  {"code": "190", "name": "吉林"},
  {"code": "200", "name": "江西"},
  {"code": "210", "name": "辽宁"},
  {"code": "220", "name": "内蒙古"},
  {"code": "230", "name": "宁夏"},
  {"code": "240", "name": "青海"},
  {"code": "250", "name": "山东"},
  {"code": "260", "name": "山西"},
  {"code": "270", "name": "陕西"},
  {"code": "280", "name": "四川"},
  {"code": "290", "name": "西藏"},
  {"code": "300", "name": "新疆"},
  {"code": "310", "name": "云南"},
  {"code": "320", "name": "香港"},
  {"code": "330", "name": "澳门"},
  {"code": "340", "name": "台湾"},
  {"code": "090", "name": "福建"},
  {"code": "070", "name": "浙江"},
  {"code": "050", "name": "广东"},
  {"code": "030", "name": "天津"},
  {"code": "010", "name": "北京"},
  {"code": "080", "name": "安徽"},
  {"code": "060", "name": "江苏"},
  {"code": "040", "name": "重庆"},
  {"code": "020", "name": "上海"}
]


# 将项目根目录添加到Python路径中
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent  # 从当前文件向上找三层到项目根目录
sys.path.append(str(project_root))

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "liepin_spider_step3")
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class LiepinSpiderStep3:
    """猎聘网爬虫 - 第三步"""
    
    def __init__(self):
        # MongoDB配置
        self.mongo_uri = "mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test"
        self.mongo_db = "da_test"
        self.mongo_client = None
        self.db = None
        
        # 加载城市信息
        self.city_info = self.load_city_info()
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        logger.info(f"初始化完成，加载了 {len(self.city_info)} 个省区的城市信息")
    
    def load_city_info(self) -> Dict[str, List[dict]]:
        """从city_info.json加载城市信息"""
        try:
            # 构建文件路径
            file_path = Path(__file__).parent.parent.parent / "data" / "liepin" / "city_info.json"
            
            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"成功加载 {len(data)} 个省区的城市信息")
            return data
            
        except Exception as e:
            logger.error(f"加载城市信息失败: {str(e)}")
            return {}
    
    def get_city_name(self, province_code: str, city_code: str) -> str:
        """根据省区代码和城市代码获取城市名称"""
        try:
            # 从已加载的城市信息中查找
            cities = self.city_info.get(province_code, [])
            for city in cities:
                if city['code'] == city_code:
                    return city['name']
            return city_code  # 如果找不到，返回代码
        except Exception as e:
            logger.error(f"获取城市名称失败: {str(e)}")
            return city_code

    def get_province_name(self, province_code: str) -> str:
        """根据省份代码获取省份名称"""
        try:
            for province in province_info:
                if province['code'] == province_code:
                    return province['name']
            return province_code  # 如果找不到，返回代码
        except Exception as e:
            logger.error(f"获取省份名称失败: {str(e)}")
            return province_code

    def _init_mongodb(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise

    def close(self):
        """关闭MongoDB连接"""
        if self.mongo_client:
            try:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")
            except Exception as e:
                logger.error(f"关闭MongoDB连接失败: {str(e)}")

    def get_url_key(self, doc):
        """生成URL的唯一键，用于比较"""
        return (
            doc.get('industry_parent_code', ''),
            doc.get('industry_child_code', ''),
            doc.get('job_type_name', '')
        )
    
    def analyze_collection_group(self, url_collection, log_collection):
        """分析单个集合组的数据差异"""
        logger.info(f"分析集合组: {url_collection} vs {log_collection}")
        
        # 获取url_part数据
        url_docs = list(self.db[url_collection].find({}))
        url_keys = {self.get_url_key(doc): doc for doc in url_docs}
        
        # 获取log_part数据
        log_docs = list(self.db[log_collection].find({}))
        log_keys = {self.get_url_key(doc): doc for doc in log_docs}
        
        logger.info(f"URL集合数量: {len(url_docs)}")
        logger.info(f"LOG集合数量: {len(log_docs)}")
        
        # 找出只在log_part中存在的数据
        only_in_log = []
        for key, doc in log_keys.items():
            if key not in url_keys:
                only_in_log.append(doc)
        
        # 找出只在url_part中存在的数据
        only_in_url = []
        for key, doc in url_keys.items():
            if key not in log_keys:
                only_in_url.append(doc)
        
        # 找出共同存在的数据
        common_keys = set(url_keys.keys()) & set(log_keys.keys())
        
        logger.info(f"只在LOG中存在的数据数量: {len(only_in_log)}")
        logger.info(f"只在URL中存在的数据数量: {len(only_in_url)}")
        logger.info(f"共同存在的数据数量: {len(common_keys)}")
        
        return {
            'url_collection': url_collection,
            'log_collection': log_collection,
            'url_count': len(url_docs),
            'log_count': len(log_docs),
            'only_in_log': only_in_log,
            'only_in_url': only_in_url,
            'common_count': len(common_keys)
        }
    
    def validate_collections(self):
        """验证所有集合组的数据一致性"""
        logger.info("开始验证集合数据一致性...")
        
        collection_groups = [
            {
                'url_part': 'liepin_step1_urls_part1',
                'log_part': 'liepin_step1_urls_202504_log_part1'
            },
            {
                'url_part': 'liepin_step1_urls_part2', 
                'log_part': 'liepin_step1_urls_202504_log_part2'
            },
            {
                'url_part': 'liepin_step1_urls_part3',
                'log_part': 'liepin_step1_urls_202504_log_part3'
            },
            {
                'url_part': 'liepin_step1_urls_part4',
                'log_part': 'liepin_step1_urls_202504_log_part4'
            }
        ]
        
        all_valid = True
        results = []
        
        for group in collection_groups:
            result = self.analyze_collection_group(
                group['url_part'], 
                group['log_part']
            )
            results.append(result)
            
            # 检查是否有不一致的数据
            if result['only_in_log'] or result['only_in_url']:
                all_valid = False
                logger.error(f"集合组 {group['url_part']} vs {group['log_part']} 数据不一致！")
                logger.error(f"  只在LOG中的数据: {len(result['only_in_log'])}")
                logger.error(f"  只在URL中的数据: {len(result['only_in_url'])}")
            else:
                logger.info(f"集合组 {group['url_part']} vs {group['log_part']} 数据一致 ✓")
        
        # 汇总统计
        total_url_count = sum(r['url_count'] for r in results)
        total_log_count = sum(r['log_count'] for r in results)
        total_only_in_log = sum(len(r['only_in_log']) for r in results)
        total_only_in_url = sum(len(r['only_in_url']) for r in results)
        total_common = sum(r['common_count'] for r in results)
        
        logger.info(f"汇总统计:")
        logger.info(f"  总URL数据量: {total_url_count}")
        logger.info(f"  总LOG数据量: {total_log_count}")
        logger.info(f"  总只在LOG中的数据量: {total_only_in_log}")
        logger.info(f"  总只在URL中的数据量: {total_only_in_url}")
        logger.info(f"  总共同数据量: {total_common}")
        
        if all_valid:
            logger.info("所有集合组数据验证通过！")
        else:
            logger.error("存在数据不一致的集合组，请先清理数据！")
        
        return all_valid

    def run(self):
        """运行爬虫"""
        try:
            # 首先验证所有集合组的数据一致性
            if not self.validate_collections():
                logger.error("数据验证失败，程序退出！请先清理不一致的数据。")
                return
            
            logger.info("数据验证通过，开始生成URL...")
            
            # 生成所有URL组合
            all_urls = []
            for part_num in range(1,5):
                part_urls = list(self.db[f'liepin_step1_urls_202504_log_part{part_num}'].find({'status':'success'}, {'_id': 0,'status':0}))
                
                for step1 in part_urls:
                    # 遍历所有省区
                    seen_combinations = set()  # 用于去重的集合，基于关键参数
                    for province_code, cities in self.city_info.items():
                        # 构建去重的关键参数组合
                        key_combination = (
                            step1.get('job_type_name'),
                            step1.get('industry_parent_code'),
                            step1.get('industry_child_code'),
                            province_code
                        )
                        
                        # 检查关键参数组合是否已存在，避免重复
                        if key_combination not in seen_combinations:
                            seen_combinations.add(key_combination)  # 添加到已见集合
                            
                            # 构建URL
                            url = f"https://www.liepin.com/zhaopin/?city={province_code}&dq={province_code}&currentPage=0&pageSize=40&key={step1.get('job_type_name')}&industry={step1.get('industry_parent_code')}${step1.get('industry_child_code')}"
                            
                            # 添加到URL列表
                            all_urls.append({
                                'url': url,
                                'industry_parent_code': step1.get('industry_parent_code'),
                                'industry_parent_name': step1.get('industry_parent_name'),
                                'industry_child_code': step1.get('industry_child_code'),
                                'industry_child_name': step1.get('industry_child_name'),
                                'job_industry': step1.get('job_industry'),
                                'job_category': step1.get('job_category'),
                                'job_type_name': step1.get('job_type_name'),
                                'province_code': province_code,
                                'province_name': self.get_province_name(province_code),
                                'create_time': datetime.now()
                            })
            
            # 清空原有集合
            self.db['liepin_step2_urls'].drop()
            for part_num in range(1,5):
                self.db[f'liepin_step2_urls_part{part_num}'].drop()
            logger.info("已清空原有集合")
            
            # 保存所有URL到总集合
            if all_urls:
                self.db['liepin_step2_urls'].insert_many(all_urls)
                logger.info(f"总集合生成了 {len(all_urls)} 个URL")
                
                # 为总集合创建索引
                self.db['liepin_step2_urls'].create_index([
                    ('industry_parent_code', 1),
                    ('industry_child_code', 1),
                    ('job_industry', 1),
                    ('job_category', 1),
                    ('job_type_name', 1),
                    ('province_code', 1)
                ], unique=True)
                self.db['liepin_step2_urls'].create_index([('status', 1)])
                self.db['liepin_step2_urls'].create_index([('create_time', 1)])
                self.db['liepin_step2_urls'].create_index([('province_code', 1)])
            
            # 计算每个part的大小
            total_urls = len(all_urls)
            base_size = total_urls // 4
            remainder = total_urls % 4
            
            # 分配URL到4个part集合
            start_idx = 0
            for part_num in range(1,5):
                # 计算当前part的大小
                current_size = base_size + (1 if remainder > 0 else 0)
                remainder -= 1
                
                # 获取当前part的URL
                part_urls = all_urls[start_idx:start_idx + current_size]
                start_idx += current_size
                
                # 保存到对应的part集合
                if part_urls:
                    collection_name = f'liepin_step2_urls_part{part_num}'
                    self.db[collection_name].insert_many(part_urls)
                    logger.info(f"Part{part_num} 生成了 {len(part_urls)} 个URL")
                    
                    # 为part集合创建索引
                    self.db[collection_name].create_index([
                        ('industry_parent_code', 1),
                        ('industry_child_code', 1),
                        ('job_industry', 1),
                        ('job_category', 1),
                        ('job_type_name', 1),
                        ('province_code', 1)
                    ], unique=True)
                    self.db[collection_name].create_index([('status', 1)])
                    self.db[collection_name].create_index([('create_time', 1)])
                    self.db[collection_name].create_index([('province_code', 1)])
            
            logger.info(f"总共生成 {total_urls} 个step2 URL")
            
        except Exception as e:
            logger.error(f"运行出错: {str(e)}")
            raise
        finally:
            self.close()

def main():
    """主函数"""
    try:
        # 创建爬虫实例
        spider = LiepinSpiderStep3()
        # 运行爬虫
        spider.run()
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()

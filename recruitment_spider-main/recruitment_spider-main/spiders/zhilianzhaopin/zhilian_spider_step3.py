#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智联招聘爬虫 - 第三步
功能：将step2生成的URL平均分配到4个部分，为并行爬取做准备

主要步骤：
1. 从MongoDB加载step2生成的URL数据
2. 计算每个部分的大小（总数除以4，向上取整）
3. 清空原有的4个part集合
4. 将URL数据平均分配到4个part集合中
5. 为每个part集合创建必要的索引

数据存储：
- 输入集合：zhilian_step2_urls
- 输出集合：
  * zhilian_step2_urls_part1
  * zhilian_step2_urls_part2
  * zhilian_step2_urls_part3
  * zhilian_step2_urls_part4
- 索引配置：
  * (industry_code, job_type_code, city_code) - 唯一复合索引
  * status - 状态索引
  * create_time - 创建时间索引
  * job_type_code - 岗位代码索引
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

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "zhilian_spider")
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class ZhilianSpiderStep3:
    """智联招聘爬虫 - Requests版本"""
    
    def __init__(self):
        # API配置
        self.base_url = "https://fe-api.zhaopin.com"
        self.search_api = "/c/i/search/positions"
        
        # 基础数据文件路径
        self.base_data_path = Path("recruitment_spider/data/zhilian/base_data.json")
        
        # 加载基础数据
        self.job_type_codes = self.load_job_type_codes()
        self.city_codes = self.load_city_codes()
        self.industry_codes = self.load_industry_codes()
        
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.mongo_client = None
        self.db = None
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        logger.info(f"初始化完成: {len(self.job_type_codes)} 个岗位类型, {len(self.city_codes)} 个城市, {len(self.industry_codes)} 个行业")
    
    def load_base_data(self) -> dict:
        """加载基础数据文件"""
        try:
            if not self.base_data_path.exists():
                logger.error(f"基础数据文件不存在: {self.base_data_path}")
                return {}
                
            with open(self.base_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载基础数据失败: {str(e)}")
            return {}

    def load_city_codes(self) -> List[dict]:
        """从base_data.json加载城市代码"""
        try:
            data = self.load_base_data()
            cities = data.get('data', {}).get('allCity', [])
            city_codes = []
            
            for city in cities:
                code = city.get('code')
                name = city.get('name')
                if code and name:
                    city_codes.append({
                        'code': code,
                        'name': name
                    })
            
            logger.info(f"成功加载 {len(city_codes)} 个城市")
            return city_codes
            
        except Exception as e:
            logger.error(f"加载城市代码失败: {str(e)}")
            return []

    def load_industry_codes(self) -> List[dict]:
        """从base_data.json加载行业代码"""
        try:
            data = self.load_base_data()
            industries = data.get('data', {}).get('industry', [])
            industry_codes = []
            
            def extract_last_level(industry_list):
                for item in industry_list:
                    sublist = item.get('sublist', [])
                    if not sublist:
                        code = item.get('code')
                        name = item.get('name')
                        if code and name:
                            industry_codes.append({
                                'code': code,
                                'name': name
                            })
                    else:
                        extract_last_level(sublist)
            
            extract_last_level(industries)
            logger.info(f"成功加载 {len(industry_codes)} 个行业")
            return industry_codes
            
        except Exception as e:
            logger.error(f"加载行业代码失败: {str(e)}")
            return []

    def load_job_type_codes(self) -> List[dict]:
        """从base_data.json加载岗位代码"""
        try:
            data = self.load_base_data()
            job_types = data.get('data', {}).get('jobType', [])
            combined_codes = []
            
            for level1 in job_types:
                level1_code = level1.get('code')
                if not level1_code:
                    continue
                    
                for level2 in level1.get('sublist', []):
                    level2_code = level2.get('code')
                    if not level2_code:
                        continue
                        
                    level3_list = level2.get('sublist', [])
                    if not level3_list:
                        combined_codes.append({
                            'code': level2_code,
                            'name': level2.get('name', '')
                        })
                        continue
                    
                    for level3 in level3_list:
                        level3_code = level3.get('code')
                        if level3_code:
                            combined_codes.append({
                                'code': level3_code,
                                'name': level3.get('name', '')
                            })
            
            logger.info(f"成功加载 {len(combined_codes)} 个岗位代码")
            return combined_codes
        
        except Exception as e:
            logger.error(f"加载岗位代码失败: {str(e)}")
            return []
    
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

    def run(self):
        """运行爬虫"""
        try:
            # 比较每个url的part和log数量是否相同，只有都相同才说明划分成功
            all_parts_valid = True
            for i in range(1,5):
                # 获取part集合数据
                part_data = list(self.db[f'zhilian_step1_urls_part{i}'].find(
                    {},
                    {'industry_code': 1, 'job_type_code': 1, '_id': 0}
                ))
                # 获取log集合数据
                log_data = list(self.db[f'zhilian_step1_urls_202504_log_part{i}'].find(
                    {},
                    {'industry_code': 1, 'job_type_code': 1, '_id': 0}
                ))
                
                part_count = len(part_data)
                log_count = len(log_data)
                
                if part_count != log_count:
                    logger.error(f"Part{i} 数量不一致，URL part数量={part_count}, URL log数量={log_count}")
                    return
                                    
                logger.info(f"Part{i} 数量一致，URL数量={part_count}")
                
                # 验证字段组合是否完全匹配
                part_combinations = {(item['industry_code'], item['job_type_code']) for item in part_data}
                log_combinations = {(item['industry_code'], item['job_type_code']) for item in log_data}
                
                # 检查是否有不匹配的组合
                if part_combinations != log_combinations:
                    # 找出不匹配的组合
                    part_only = part_combinations - log_combinations
                    log_only = log_combinations - part_combinations
                    
                    if part_only:
                        logger.error(f"Part{i} part集合中存在但log集合中不存在的组合: {part_only}")
                    if log_only:
                        logger.error(f"Part{i} log集合中存在但part集合中不存在的组合: {log_only}")
                    return
                else:
                    logger.info(f"Part{i} industry_code和job_type_code组合验证通过")
            
            # 清空原有的step2 URL集合
            self.db['zhilian_step2_urls'].delete_many({})
            # 为每个人part生成step2的URL
            total_step2_urls = 0
            for part_num in range(1,5):
                self.all_urls = []
                part_urls = list(self.db[f'zhilian_step1_urls_202504_log_part{part_num}'].find({'status':'success'}, {'_id': 0,'status':0}))
                for city in self.city_codes:
                    for step1 in part_urls:
                        url = f"{self.base_url}{self.search_api}"
                        # 构建url
                        self.all_urls.append({
                            'url':url,
                            'industry_code':step1.get('industry_code'),
                            'industry_name':step1.get('industry_name'),
                            'city_code':city.get('code'),
                            'city_name':city.get('name'),
                            'job_type_code':step1.get('job_type_code'),
                            'job_type_name':step1.get('job_type_name'),
                            'create_time':datetime.now(),
                            'part':part_num
                        })
                # 批量保存到mongodb
                if self.all_urls:
                    self.db['zhilian_step2_urls'].insert_many(self.all_urls)
                    total_step2_urls+=len(self.all_urls)
                    logger.info(f"Part{part_num} 已生成 {len(self.all_urls)} 个step2 URL")
            # 创建索引
            self.db['zhilian_step2_urls'].create_index([
                ('industry_code',1),
                ('job_type_code',1),
                ('city_code',1)
            ],unique=True)
            self.db['zhilian_step2_urls'].create_index([('create_time',1)])
            self.db['zhilian_step2_urls'].create_index([('part',1)])
            logger.info(f"总共生成 {total_step2_urls} 个step2 URL组合，已保存到MongoDB")
            # 将zhilian_step2_urls中的数据平均分配到4个part集合中
            all_step2_urls = list(self.db['zhilian_step2_urls'].find({}, {'_id': 0,'part':0}))
            part_size = len(all_step2_urls) // 4
            if len(all_step2_urls) % 4 != 0:
                part_size += 1
                
            # 清空原有的part集合
            for i in range(1, 5):
                self.db[f'zhilian_step2_urls_part{i}'].delete_many({})
            
            # 将数据分成4个部分并保存
            for i in range(4):
                start_idx = i * part_size
                end_idx = min((i + 1) * part_size, len(all_step2_urls))
                part_urls = all_step2_urls[start_idx:end_idx]
                
                if part_urls:
                    self.db[f'zhilian_step2_urls_part{i+1}'].insert_many(part_urls)
                    # 创建索引
                    self.db[f'zhilian_step2_urls_part{i+1}'].create_index([
                        ('industry_code', 1),                    
                        ('job_type_code', 1),
                        ('city_code', 1)
                    ], unique=True)
                    self.db[f'zhilian_step2_urls_part{i+1}'].create_index([('status', 1)])
                    self.db[f'zhilian_step2_urls_part{i+1}'].create_index([('create_time', 1)])
                    self.db[f'zhilian_step2_urls_part{i+1}'].create_index([('job_type_code', 1)])
                    self.db[f'zhilian_step2_urls_part{i+1}'].create_index([('part', 1)])
                    
                logger.info(f"Step2 Part{i+1} 已保存 {len(part_urls)} 个URL组合")
            
        except Exception as e:
            logger.error(f"爬虫运行出错: {str(e)}")
            raise
        finally:
            self.close()

def main():
    """主函数"""
    try:
        # 创建爬虫实例
        spider = ZhilianSpiderStep3()
        
        # 运行爬虫
        spider.run()
        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()

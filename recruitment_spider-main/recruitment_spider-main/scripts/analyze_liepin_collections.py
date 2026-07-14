#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
分析猎聘网不同part集合的数据差异
功能：
1. 分析每组集合中url_part和log_part的数据差异
2. 找出只在log_part中存在的数据
3. 找出只在url_part中存在的数据
4. 以url_part为基准，删除log_part中url_part没有的数据
"""

import os
import sys
from datetime import datetime
from pymongo import MongoClient
from collections import defaultdict

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

class LiepinCollectionAnalyzer:
    def __init__(self):
        # MongoDB配置
        self.mongo_uri = "mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test"
        self.mongo_db = "da_test"
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        
        # 定义集合组
        self.collection_groups = [
            {
                'url_part': 'liepin_step2_urls_part1',
                'log_part': 'liepin_step2_urls_202504_log_part1'
            },
            {
                'url_part': 'liepin_step2_urls_part2', 
                'log_part': 'liepin_step2_urls_202504_log_part2'
            },
            {
                'url_part': 'liepin_step2_urls_part3',
                'log_part': 'liepin_step2_urls_202504_log_part3'
            },
            {
                'url_part': 'liepin_step2_urls_part4',
                'log_part': 'liepin_step2_urls_202504_log_part4'
            }
        ]
    
    def get_url_key(self, doc):
        """生成URL的唯一键，用于比较"""
        return (
            doc.get('industry_parent_code', ''),
            doc.get('industry_child_code', ''),
            doc.get('job_type_name', ''),
            doc.get('province_code', '')
        )
    
    def analyze_collection_group(self, url_collection, log_collection):
        """分析单个集合组的数据差异"""
        print(f"\n{'='*60}")
        print(f"分析集合组: {url_collection} vs {log_collection}")
        print(f"{'='*60}")
        
        # 获取url_part数据
        url_docs = list(self.db[url_collection].find({}))
        url_keys = {self.get_url_key(doc): doc for doc in url_docs}
        
        # 获取log_part数据
        log_docs = list(self.db[log_collection].find({}))
        log_keys = {self.get_url_key(doc): doc for doc in log_docs}
        
        print(f"URL集合数量: {len(url_docs)}")
        print(f"LOG集合数量: {len(log_docs)}")
        
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
        
        print(f"只在LOG中存在的数据数量: {len(only_in_log)}")
        print(f"只在URL中存在的数据数量: {len(only_in_url)}")
        print(f"共同存在的数据数量: {len(common_keys)}")
        
        # 显示只在log_part中的数据详情
        if only_in_log:
            print(f"\n只在LOG中存在的数据:")
            for i, doc in enumerate(only_in_log[:5]):  # 只显示前5个
                print(f"  {i+1}. URL: {doc.get('url', 'N/A')}")
                print(f"     岗位: {doc.get('job_type_name', 'N/A')}")
                print(f"     行业: {doc.get('industry_parent_name', 'N/A')} -> {doc.get('industry_child_name', 'N/A')}")
                print(f"     状态: {doc.get('status', 'N/A')}")
            if len(only_in_log) > 5:
                print(f"  ... 还有 {len(only_in_log) - 5} 条数据")
        
        # 显示只在url_part中的数据详情
        if only_in_url:
            print(f"\n只在URL中存在的数据:")
            for i, doc in enumerate(only_in_url[:5]):  # 只显示前5个
                print(f"  {i+1}. URL: {doc.get('url', 'N/A')}")
                print(f"     岗位: {doc.get('job_type_name', 'N/A')}")
                print(f"     行业: {doc.get('industry_parent_name', 'N/A')} -> {doc.get('industry_child_name', 'N/A')}")
                print(f"     状态: {doc.get('status', 'N/A')}")
            if len(only_in_url) > 5:
                print(f"  ... 还有 {len(only_in_url) - 5} 条数据")
        
        return {
            'url_collection': url_collection,
            'log_collection': log_collection,
            'url_count': len(url_docs),
            'log_count': len(log_docs),
            'only_in_log': only_in_log,
            'only_in_url': only_in_url,
            'common_count': len(common_keys)
        }
    
    def clean_log_collections(self, dry_run=True):
        """清理log_part中url_part没有的数据"""
        print(f"\n{'='*60}")
        print(f"清理LOG集合中的重复数据 (dry_run={dry_run})")
        print(f"{'='*60}")
        
        total_deleted = 0
        
        for group in self.collection_groups:
            url_collection = group['url_part']
            log_collection = group['log_part']
            
            print(f"\n处理集合组: {url_collection} vs {log_collection}")
            
            # 获取url_part的唯一键
            url_docs = list(self.db[url_collection].find({}))
            url_keys = {self.get_url_key(doc) for doc in url_docs}
            
            # 获取log_part中需要删除的数据
            log_docs = list(self.db[log_collection].find({}))
            to_delete = []
            
            for doc in log_docs:
                key = self.get_url_key(doc)
                if key not in url_keys:
                    to_delete.append(doc['_id'])
            
            print(f"  需要删除的LOG数据数量: {len(to_delete)}")
            
            if not dry_run and to_delete:
                # 执行删除
                result = self.db[log_collection].delete_many({'_id': {'$in': to_delete}})
                deleted_count = result.deleted_count
                total_deleted += deleted_count
                print(f"  实际删除数量: {deleted_count}")
            elif to_delete:
                print(f"  模拟删除数量: {len(to_delete)}")
        
        if not dry_run:
            print(f"\n总计删除数量: {total_deleted}")
        else:
            print(f"\n模拟删除完成，如需实际删除请设置 dry_run=False")
    
    def run_analysis(self):
        """运行完整分析"""
        print("开始分析猎聘网集合数据差异...")
        
        results = []
        for group in self.collection_groups:
            result = self.analyze_collection_group(
                group['url_part'], 
                group['log_part']
            )
            results.append(result)
        
        # 汇总统计
        print(f"\n{'='*60}")
        print("汇总统计")
        print(f"{'='*60}")
        
        total_url_count = sum(r['url_count'] for r in results)
        total_log_count = sum(r['log_count'] for r in results)
        total_only_in_log = sum(len(r['only_in_log']) for r in results)
        total_only_in_url = sum(len(r['only_in_url']) for r in results)
        total_common = sum(r['common_count'] for r in results)
        
        print(f"总URL数据量: {total_url_count}")
        print(f"总LOG数据量: {total_log_count}")
        print(f"总只在LOG中的数据量: {total_only_in_log}")
        print(f"总只在URL中的数据量: {total_only_in_url}")
        print(f"总共同数据量: {total_common}")
        
        return results
    
    def close(self):
        """关闭数据库连接"""
        if hasattr(self, 'client'):
            self.client.close()

def main():
    analyzer = LiepinCollectionAnalyzer()
    try:
        # 运行分析
        results = analyzer.run_analysis()
        
        # 询问是否要清理数据
        print(f"\n{'='*60}")
        print("是否要清理LOG集合中的重复数据？")
        print("1. 先模拟运行 (dry_run=True)")
        print("2. 直接清理 (dry_run=False)")
        print("3. 退出")
        
        choice = input("请选择 (1/2/3): ").strip()
        
        if choice == '1':
            analyzer.clean_log_collections(dry_run=True)
        elif choice == '2':
            confirm = input("确认要删除数据吗？(y/N): ").strip().lower()
            if confirm == 'y':
                analyzer.clean_log_collections(dry_run=False)
            else:
                print("取消删除操作")
        else:
            print("退出程序")
            
    except Exception as e:
        print(f"分析过程中发生错误: {str(e)}")
    finally:
        analyzer.close()

if __name__ == "__main__":
    main() 
from pymongo import MongoClient
from typing import List, Dict
import pandas as pd
from datetime import datetime

def get_missing_records(log_collection: str, url_collection: str, client: MongoClient) -> List[Dict]:
    """
    比较两个集合，找出在log中存在但在url中不存在的记录
    使用job_type_code和industry_code作为匹配条件
    """
    db = client['MOOC123_DA']
    log_coll = db[log_collection]
    url_coll = db[url_collection]
    
    # 获取log集合中的所有记录
    log_records = list(log_coll.find({}, {
        'url': 1,
        'job_type_code': 1,
        'industry_code': 1,
        '_id': 0
    }))
    
    # 获取url集合中的所有记录
    url_records = list(url_coll.find({}, {
        'url': 1,
        'job_type_code': 1,
        'industry_code': 1,
        '_id': 0
    }))
    
    # 创建url集合的复合键集合
    url_keys = set()
    for record in url_records:
        if 'job_type_code' in record and 'industry_code' in record:
            key = (record['job_type_code'], record['industry_code'])
            url_keys.add(key)
    
    # 找出在log中存在但在url中不存在的记录
    missing_records = []
    for record in log_records:
        if 'job_type_code' in record and 'industry_code' in record:
            key = (record['job_type_code'], record['industry_code'])
            if key not in url_keys:
                # 获取完整记录
                full_record = log_coll.find_one({
                    'job_type_code': record['job_type_code'],
                    'industry_code': record['industry_code']
                })
                if full_record:
                    missing_records.append(full_record)
    
    return missing_records

def delete_missing_records(log_collection: str, missing_records: List[Dict], client: MongoClient) -> int:
    """
    从log集合中删除缺失记录
    """
    db = client['MOOC123_DA']
    log_coll = db[log_collection]
    
    deleted_count = 0
    for record in missing_records:
        if 'job_type_code' in record and 'industry_code' in record:
            result = log_coll.delete_one({
                'job_type_code': record['job_type_code'],
                'industry_code': record['industry_code']
            })
            if result.deleted_count > 0:
                deleted_count += 1
    
    return deleted_count

def main():
    # MongoDB连接配置
    mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
    client = MongoClient(mongo_uri)
    
    # 定义要比较的集合对
    collection_pairs = [
        ('boss_step1_urls_202504_log_part1', 'boss_step1_urls_part1'),
        ('boss_step1_urls_202504_log_part2', 'boss_step1_urls_part2'),
        ('boss_step1_urls_202504_log_part3', 'boss_step1_urls_part3'),
        ('boss_step1_urls_202504_log_part4', 'boss_step1_urls_part4')
    ]
    
    # 创建结果DataFrame
    results = []
    
    # 比较每对集合
    for log_coll, url_coll in collection_pairs:
        print(f"\n比较 {log_coll} 和 {url_coll}...")
        missing_records = get_missing_records(log_coll, url_coll, client)
        
        # 统计信息
        total_log = client['MOOC123_DA'][log_coll].count_documents({})
        total_url = client['MOOC123_DA'][url_coll].count_documents({})
        missing_count = len(missing_records)
        
        # 删除缺失记录
        deleted_count = delete_missing_records(log_coll, missing_records, client)
        
        results.append({
            'log_collection': log_coll,
            'url_collection': url_coll,
            'total_log_records': total_log,
            'total_url_records': total_url,
            'missing_records': missing_count,
            'deleted_records': deleted_count
        })
        
        print(f"Log集合记录数: {total_log}")
        print(f"URL集合记录数: {total_url}")
        print(f"缺失记录数: {missing_count}")
        print(f"已删除记录数: {deleted_count}")
    
    # 保存总体统计信息
    summary_df = pd.DataFrame(results)
    summary_df.to_csv('deletion_summary.csv', index=False, encoding='utf-8')
    print("\n删除操作统计信息已保存到: deletion_summary.csv")

if __name__ == '__main__':
    main() 
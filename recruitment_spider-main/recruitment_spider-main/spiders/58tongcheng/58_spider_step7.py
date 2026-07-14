# 第一次运行或重新运行会清空数据，断点续传需在文件最后修改代码
from pymongo import MongoClient
from tqdm import tqdm
import os
import json
import signal
import sys
from bson.objectid import ObjectId

def signal_handler(sig, frame):
    print("\n检测到CTRL+C中断，正在保存检查点...")
    save_checkpoint(current_collection_idx, seen_combinations, seen_ids, checkpoint_file)
    print(f"检查点已保存，下次可使用resume=True继续运行")
    client.close()
    sys.exit(0)

def save_checkpoint(collection_idx, combinations, ids, checkpoint_file):
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        f.write(f"{collection_idx}\n")
        f.write(json.dumps(list(combinations), ensure_ascii=False) + '\n')
        f.write(json.dumps(list(ids), ensure_ascii=False) + '\n')

def deduplicate_and_save_jobs(resume=False):
    global current_collection_idx, seen_combinations, seen_ids, checkpoint_file, client
    
    # 连接MongoDB
    client = MongoClient('mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA')
    db = client['MOOC123_DA']
    
    # 源集合列表
    source_collections = [
        '58_job_detail_part1',
        '58_job_detail_part2',
        '58_job_detail_part3',
        '58_job_detail_part4'
    ]
    
    # 目标集合
    target_collection = '58_job_detail'
    
    # 断点记录文件
    checkpoint_file = 'job_deduplication_checkpoint.txt'
    
    # 注册CTRL+C信号处理
    signal.signal(signal.SIGINT, signal_handler)
    
    # 如果不需要续传或没有检查点文件，则初始化
    if not resume or not os.path.exists(checkpoint_file):
        print("检查点文件不存在或不完整，将从第一个集合开始处理")
        current_collection_idx = 0
        seen_combinations = set()
        seen_ids = set()
        
        # 初始化检查点文件
        save_checkpoint(current_collection_idx, seen_combinations, seen_ids, checkpoint_file)
    else:
        # 从检查点恢复
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) < 3:  # 检查文件是否完整
                    raise ValueError("检查点文件不完整")
                
                current_collection_idx = int(lines[0].strip())
                seen_combinations = set(json.loads(lines[1].strip()))
                seen_ids = set(json.loads(lines[2].strip()))
            
            print(f"从检查点恢复: 集合 {source_collections[current_collection_idx]}")
        except Exception as e:
            print(f"读取检查点失败: {e}，将从第一个集合开始处理")
            current_collection_idx = 0
            seen_combinations = set()
            seen_ids = set()
            save_checkpoint(current_collection_idx, seen_combinations, seen_ids, checkpoint_file)
    
    try:
        # 从当前集合索引开始处理
        for idx in range(current_collection_idx, len(source_collections)):
            collection_name = source_collections[idx]
            print(f"正在处理集合: {collection_name}")
            
            # 更新检查点中的集合索引
            save_checkpoint(idx, seen_combinations, seen_ids, checkpoint_file)
            
            # 获取当前集合中的所有文档
            collection = db[collection_name]
            total_docs = collection.count_documents({})
            
            # 使用进度条显示处理进度
            for doc in tqdm(collection.find({}), total=total_docs):
                try:
                    doc_id = str(doc['_id'])
                    
                    # 如果这个ID已经处理过，则跳过
                    if doc_id in seen_ids:
                        continue
                    
                    # 提取关键字段
                    job_name = doc.get('job_name', '')
                    
                    # 处理company_info可能是字典或字符串的情况
                    company_info = doc.get('company_info', {})
                    if isinstance(company_info, dict):
                        company_name = company_info.get('company_name', '')
                    else:
                        company_name = str(company_info)
                    
                    detail_address = doc.get('detail_address', '')
                    
                    # 创建唯一标识组合
                    combination = f"{job_name}_{company_name}_{detail_address}"
                    
                    # 如果这个组合还没出现过，则尝试插入到目标集合
                    if combination not in seen_combinations:
                        try:
                            db[target_collection].insert_one(doc)
                            seen_combinations.add(combination)
                        except Exception as e:
                            if "duplicate key error" in str(e):
                                # 如果是重复ID错误，视为已处理
                                pass
                            else:
                                raise e
                    
                    # 记录已处理的ID
                    seen_ids.add(doc_id)
                    
                    # 定期更新检查点（每处理100条记录）
                    if len(seen_ids) % 100 == 0:
                        save_checkpoint(idx, seen_combinations, seen_ids, checkpoint_file)
                        
                except Exception as e:
                    print(f"处理文档时出错: {e}")
                    continue
        
        print(f"去重完成! 共处理 {len(seen_ids)} 条记录。")
        
        # 处理完成后删除检查点文件
        if os.path.exists(checkpoint_file):
            os.remove(checkpoint_file)
            
    except Exception as e:
        print(f"程序中断: {e}")
        print("已保存检查点，可以使用resume=True参数继续运行")
    finally:
        client.close()

if __name__ == '__main__':
    # 第一次运行或重新开始
    # deduplicate_and_save_jobs(resume=False)
    
    # 从上次中断处继续
    deduplicate_and_save_jobs(resume=True)
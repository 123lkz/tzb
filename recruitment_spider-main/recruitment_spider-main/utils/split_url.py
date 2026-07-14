from pymongo import MongoClient
import math

# 数据库连接配置 [[5]]
uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
client = MongoClient(uri)
db = client['MOOC123_DA']

# 原始集合
source_col = db['boss_step1_urls']

# 计算分页参数 [[6]][[9]]
total = source_col.count_documents({})
page_size = math.ceil(total / 4)  # 向上取整确保覆盖所有数据

# 分页查询与插入 [[7]]
for i in range(4):
    part_name = f"boss_step1_urls_part{i+1}"
    target_col = db[part_name]
    
    # 分页查询（按_id排序保证稳定性）
    skip = i * page_size
    cursor = source_col.find().sort("_id", 1).skip(skip).limit(page_size)
    docs = list(cursor)
    
    # 批量插入新集合 [[7]]
    if docs:
        target_col.insert_many(docs)
        print(f"Inserted {len(docs)} docs into {part_name}")
    else:
        print(f"No data for {part_name}")

# 验证数据量 [[6]]
for i in range(4):
    part_name = f"boss_step1_urls_part{i+1}"
    count = db[part_name].count_documents({})
    print(f"{part_name} has {count} documents")
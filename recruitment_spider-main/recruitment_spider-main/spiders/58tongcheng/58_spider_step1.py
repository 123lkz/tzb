import json
import pymongo
from pymongo import MongoClient
from math import ceil

class URLGenerator:
    def __init__(self):
        # MongoDB连接配置
        self.mongo_host = "210.14.140.50"
        self.mongo_port = 10387
        self.mongo_username = "mooc_da"
        self.mongo_password = "6WLg29gu3014i"
        self.source_db_name = "MOOC123_DA"
        self.main_collection_name = "58_step1_urls"
        self.part_collections = [
            "58_step1_urls_part1",
            "58_step1_urls_part2",
            "58_step1_urls_part3",
            "58_step1_urls_part4"
        ]
        
        # 初始化MongoDB连接
        self.client = None
        self.db = None
        self.main_collection = None
        self.part_collections_obj = []

    def connect_mongodb(self):
        """连接MongoDB数据库并初始化所有集合对象并创建唯一索引"""
        try:
            self.client = MongoClient(
                host=self.mongo_host,
                port=self.mongo_port,
                username=self.mongo_username,
                password=self.mongo_password,
                authSource=self.source_db_name
            )
            self.db = self.client[self.source_db_name]
            self.main_collection = self.db[self.main_collection_name]
            self.part_collections_obj = [self.db[col] for col in self.part_collections]
            
            # 为主集合创建唯一索引（组合city_code和job_path）
            self.main_collection.create_index(
                [("city_code", pymongo.ASCENDING), ("job_path", pymongo.ASCENDING)],
                unique=True,
                name="unique_city_job"
            )
            
            # 为每个分片集合创建同样的唯一索引
            for col in self.part_collections_obj:
                col.create_index(
                    [("city_code", pymongo.ASCENDING), ("job_path", pymongo.ASCENDING)],
                    unique=True,
                    name="unique_city_job"
                )
            
            print("成功连接到MongoDB数据库并初始化集合和唯一索引")
            return True
        except Exception as e:
            print(f"连接MongoDB失败: {str(e)}")
            return False

    def load_city_data(self, file_path):
        """加载城市数据JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                city_data = json.load(f)
            return city_data
        except Exception as e:
            print(f"加载城市数据失败: {str(e)}")
            return None

    def load_job_data(self, file_path):
        """加载职业数据JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                job_data = json.load(f)
            return job_data
        except Exception as e:
            print(f"加载职业数据失败: {str(e)}")
            return None

    def generate_urls(self, city_data, job_data):
        """生成所有可能的URL组合并进行唯一性检查"""
        urls = []
        seen_urls = set()  # 用于URL去重
        
        for city, city_code in city_data.items():
            for job, path in job_data.items():
                url = f"https://{city_code}.58.com/{path}"
                
                # 检查URL是否已存在，保证唯一性
                if url not in seen_urls:
                    seen_urls.add(url)
                    doc = {
                        "city": city,
                        "city_code": city_code,
                        "job_category": job,
                        "job_path": path,
                        "url": url,
                        "status": "pending"
                    }
                    urls.append(doc)
        
        print(f"生成 {len(urls)} 条唯一URL（已自动去重）")
        return urls

    def split_and_save_data(self, urls):
        """将已去重的数据分成4份并保存到不同集合"""
        if not self.part_collections_obj:
            print("分片集合未初始化")
            return False

        try:
            # 计算每份数据的大小
            total = len(urls)
            part_size = ceil(total / 4)
            
            # 清空原有分片集合
            for col in self.part_collections_obj:
                col.delete_many({})
            
            # 分割并保存数据（无需再次去重）
            for i in range(4):
                start = i * part_size
                end = start + part_size if i < 3 else total  # 最后一部分包含剩余数据
                part_data = urls[start:end]
                
                if part_data:
                    try:
                        self.part_collections_obj[i].insert_many(part_data, ordered=False)
                        print(f"成功保存 {len(part_data)} 条数据到 {self.part_collections[i]}")
                    except pymongo.errors.BulkWriteError as e:
                        # 即使有重复键错误，也会插入非重复文档
                        print(f"插入部分数据时遇到重复键，已跳过重复项: {str(e.details['writeErrors'][0]['errmsg'])}")
                        print(f"实际成功插入 {e.details['nInserted']} 条数据到 {self.part_collections[i]}")
            
            return True
        except Exception as e:
            print(f"分割保存数据失败: {str(e)}")
            return False

    def process(self, city_json_path, job_json_path):
        """处理整个流程"""
        # 连接MongoDB
        if not self.connect_mongodb():
            return False
        
        # 加载数据
        city_data = self.load_city_data(city_json_path)
        if not city_data:
            return False
        
        job_data = self.load_job_data(job_json_path)
        if not job_data:
            return False
        
        # 生成URL（已包含去重逻辑）
        urls = self.generate_urls(city_data, job_data)
        if not urls:
            print("没有生成任何URL")
            return False
        
        # 保存到主集合（数据已去重）
        try:
            self.main_collection.delete_many({})  # 清空原有数据
            self.main_collection.insert_many(urls, ordered=False)
            print(f"成功保存 {len(urls)} 条唯一数据到主集合 {self.main_collection_name}")
        except pymongo.errors.BulkWriteError as e:
            print(f"保存到主集合时遇到重复键，已跳过重复项: {str(e.details['writeErrors'][0]['errmsg'])}")
            print(f"实际成功插入 {e.details['nInserted']} 条数据到主集合")
        except Exception as e:
            print(f"保存到主集合失败: {str(e)}")
            return False
        
        # 分割并保存到分片集合（数据已去重）
        if not self.split_and_save_data(urls):
            return False
        
        return True

if __name__ == "__main__":
    city_json_path = "city.json"
    job_json_path = "job.json"
    
    generator = URLGenerator()
    if generator.process(city_json_path, job_json_path):
        print("URL生成和分片保存成功完成")
    else:
        print("处理过程中出现错误")
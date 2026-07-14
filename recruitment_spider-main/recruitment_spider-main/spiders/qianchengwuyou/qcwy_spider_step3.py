import csv
from pymongo import MongoClient
from datetime import datetime
import urllib.parse
import pandas as pd
from pymongo import UpdateOne
from urllib.parse import urlparse, parse_qs
import time

class URLDataProcessor:
    def __init__(self, mongo_uri, mongo_db, collection_name, industry_csv, city_csv, batch_size=1000):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name
        self.industry_csv = industry_csv
        self.city_csv = city_csv
        self.batch_size = batch_size
        self.client = None
        self.collection = None
        self.industry_mapping = {}
        self.city_mapping = {}

    def parse_url_industry_keyword_jobarea(self, url):
        """从URL中提取industry、keyword、jobArea信息"""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        result = {}

        # 提取industry信息
        if 'industry' in query_params:
            result['industry_code'] = query_params['industry'][0]

        # 提取keyword信息并解码
        if 'keyword' in query_params:
            encoded_keyword = query_params['keyword'][0]
            result['keyword'] = urllib.parse.unquote(encoded_keyword)

        # 提取jobArea信息
        if 'jobArea' in query_params:
            result['jobArea_code'] = query_params['jobArea'][0]

        return result

    def load_industry_mapping(self):
        """从CSV文件加载行业代码映射"""
        try:
            df = pd.read_csv(self.industry_csv)
            # 检查CSV文件结构
            print(f"行业映射CSV列名: {df.columns.tolist()}")
            # 根据实际结构调整列名
            code_col = '行业code' if '行业code' in df.columns else 'code'
            industry_col = '行业' if '行业' in df.columns else df.columns[0]

            # 构建映射字典，确保code为字符串
            mapping = {}
            for _, row in df.iterrows():
                code = str(row[code_col]).zfill(2)  # 将代码转换为字符串并补齐到2位
                industry = row[industry_col]
                mapping[code] = industry

            print(f"成功加载 {len(mapping)} 条行业映射")
            self.industry_mapping = mapping
        except Exception as e:
            print(f"加载行业映射失败: {e}")

    def load_city_mapping(self):
        """从CSV文件加载城市代码映射"""
        try:
            df = pd.read_csv(self.city_csv)
            # 检查CSV文件结构
            print(f"城市映射CSV列名: {df.columns.tolist()}")
            # 根据实际结构调整列名
            city_col = '城市' if '城市' in df.columns else df.columns[0]
            code_col = 'code' if 'code' in df.columns else df.columns[1]

            # 构建映射字典，同时存储标准和非标准格式
            mapping = {}
            for _, row in df.iterrows():
                city = row[city_col]
                code = str(row[code_col])

                # 存储原始代码
                mapping[code] = city

                # 处理前导零的情况
                if len(code) == 5:  # 如果城市代码为5位
                    # 存储去掉前导零的版本
                    if code.startswith('0'):
                        mapping[code[1:]] = city
                    # 存储添加前导零的版本
                    else:
                        mapping['0' + code] = city

                # 处理不足6位的代码
                if len(code) < 6:
                    # 补齐到6位
                    padded_code = code.zfill(6)
                    mapping[padded_code] = city

            print(f"成功加载 {len(mapping)} 条城市映射")
            # 示例：打印一些映射信息
            sample_codes = ['10000', '010000', '90600', '090600']
            for code in sample_codes:
                print(f"城市代码 {code} 映射到: {mapping.get(code, '未找到')}")

            self.city_mapping = mapping
        except Exception as e:
            print(f"加载城市映射失败: {e}")

    def process_batch(self, urls_batch):
        """处理一批URL并生成更新操作"""
        bulk_operations = []

        for doc in urls_batch:
            url = doc.get('url', '')
            doc_id = doc.get('_id')

            if not url:
                continue

            # 解析URL信息
            parsed_data = self.parse_url_industry_keyword_jobarea(url)
            update_data = {}

            # 更新industry信息
            if 'industry_code' in parsed_data:
                industry_code = parsed_data['industry_code']
                industry_name = self.industry_mapping.get(industry_code, f"未知行业({industry_code})")
                update_data['industry'] = industry_name

            # 更新keyword信息
            if 'keyword' in parsed_data:
                update_data['keyword'] = parsed_data['keyword']

            # 更新jobArea信息
            if 'jobArea_code' in parsed_data:
                jobArea_code = parsed_data['jobArea_code']
                city_name = self.city_mapping.get(jobArea_code, None)

                # 尝试不同的格式匹配
                if city_name is None:
                    # 尝试去掉前导零
                    if jobArea_code.startswith('0'):
                        city_name = self.city_mapping.get(jobArea_code.lstrip('0'), None)
                    # 尝试添加前导零
                    else:
                        city_name = self.city_mapping.get('0' + jobArea_code, None)
                    # 尝试6位格式
                    if city_name is None:
                        city_name = self.city_mapping.get(jobArea_code.zfill(6), None)

                # 如果仍然未找到，使用原始代码
                if city_name is None:
                    city_name = f"未知城市({jobArea_code})"
                    # 记录未找到的代码，方便调试
                    print(f"未找到城市代码: {jobArea_code}")

                update_data['jobArea'] = city_name

            # 生成更新操作
            if update_data:
                bulk_operations.append(
                    UpdateOne({'_id': doc_id}, {'$set': update_data})
                )

        return bulk_operations

    def run(self):
        start_time = time.time()
        try:
            # 连接MongoDB
            print("正在连接MongoDB...")
            self.client = MongoClient(self.mongo_uri)
            db = self.client[self.mongo_db]
            self.collection = db[self.collection_name]

            # 加载映射数据
            print("正在加载映射数据...")
            self.load_industry_mapping()
            self.load_city_mapping()

            if not self.industry_mapping or not self.city_mapping:
                print("映射数据加载失败，请检查CSV文件")
                return

            # 获取总文档数
            total_docs = self.collection.count_documents({})
            print(f"总共需要处理 {total_docs} 条文档")

            # 遍历文档
            cursor = self.collection.find({}, {'_id': 1, 'url': 1})
            batch = []
            total_processed = 0
            total_updated = 0

            for doc in cursor:
                batch.append(doc)

                if len(batch) >= self.batch_size:
                    # 处理当前批次
                    bulk_ops = self.process_batch(batch)

                    if bulk_ops:
                        # 执行批量更新
                        result = self.collection.bulk_write(bulk_ops)
                        modified_count = result.modified_count
                        total_updated += modified_count
                    else:
                        modified_count = 0

                    total_processed += len(batch)
                    elapsed_time = time.time() - start_time
                    percent_complete = (total_processed / total_docs) * 100

                    # 显示详细进度
                    print(f"进度: {total_processed}/{total_docs} ({percent_complete:.2f}%), "
                          f"已更新: {total_updated}, "
                          f"当前批次更新: {modified_count}, "
                          f"耗时: {elapsed_time:.2f}秒, "
                          f"预计剩余时间: {(elapsed_time / total_processed) * (total_docs - total_processed):.2f}秒")

                    # 清空批次
                    batch = []

            # 处理最后一批
            if batch:
                bulk_ops = self.process_batch(batch)
                if bulk_ops:
                    result = self.collection.bulk_write(bulk_ops)
                    total_updated += result.modified_count
                    total_processed += len(batch)

                    # 显示最终进度
                    final_elapsed_time = time.time() - start_time
                    print(f"最终进度: {total_processed}/{total_docs} (100%), "
                          f"总共更新: {total_updated}, "
                          f"处理时间: {final_elapsed_time:.2f}秒")

            print("处理完成。")

        except Exception as e:
            print(f"处理过程中出现错误: {e}")

        finally:
            if self.client:
                self.client.close()
                print("MongoDB连接已关闭")

class QcwySpiderStep3:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        # 源集合列表
        self.source_collections = [
            "qcwy_step1_verify_logs_part1",
            "qcwy_step1_verify_logs_part2",
            "qcwy_step1_verify_logs_part3",
            "qcwy_step1_verify_logs_part4"
        ]
        # 合并后的集合
        self.merged_collection_name = "qcwy_step2_urls"
        # 分割后的目标集合列表
        self.target_collections = [
            "qcwy_step2_urls_part1",
            "qcwy_step2_urls_part2",
            "qcwy_step2_urls_part3",
            "qcwy_step2_urls_part4"
        ]

    def connect_mongo(self):
        mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        db_name = "MOOC123_DA"
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                client = MongoClient(mongo_uri)
                db = client[db_name]
                db.command('ping')
                print("MongoDB连接成功")
                return client, db
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"MongoDB连接失败，已达到最大重试次数: {str(e)}")
                    raise e
                print(f"MongoDB连接失败，{retry_delay}秒后重试...")
                import time
                time.sleep(retry_delay)

    def read_city_codes(self):
        city_codes = []
        with open(self.csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                city_codes.append(row['code'])
        return city_codes

    def validate_url_counts(self, db, city_codes, success_count, failed_count, total_inserted):
        """
        新表中url数量一致性校验：
        - 验证扩展URL数量 = 验证成功的URL数量 × 城市代码数量
        - 验证直接URL数量 = 验证失败的URL数量
        - 检查总数是否符合预期
        """
        print("" + " = " * 50)
        print("开始进行URL数量一致性校验...")
        print("=" *  50)

        # 计算预期数量
        city_code_count = len(city_codes)
        expected_expanded_urls = success_count * city_code_count
        expected_direct_urls = failed_count
        expected_total = expected_expanded_urls + expected_direct_urls

        # 从新表中统计实际数量
        new_collection = db[self.merged_collection_name]
        actual_total = new_collection.count_documents({})

        # 打印校验结果
        print(f"城市代码数量: {city_code_count}")
        print(f"验证成功的URL数量: {success_count}")
        print(f"验证失败的URL数量: {failed_count}")
        print("预期数量计算: ")
        print(f"  扩展URL数量 = {success_count} × {city_code_count} = {expected_expanded_urls}")
        print(f"  直接URL数量 = {failed_count}")
        print(f"  总预期数量 = {expected_expanded_urls} + {expected_direct_urls} = {expected_total}")

        print(f"实际插入数量: {total_inserted} ")
        print(f"新表实际总数量: {actual_total}")

        # 校验结果
        validation_passed = True

        if total_inserted != expected_total:
            print(f"❌ 插入数量校验失败: 实际插入({total_inserted}) != 预期总数({expected_total})")
            validation_passed = False
        else:
            print(f"✅ 插入数量校验通过: {total_inserted}")

        if actual_total != expected_total:
            print(f"❌ 新表总数校验失败: 实际总数({actual_total}) != 预期总数({expected_total})")
            validation_passed = False
        else:
            print(f"✅ 新表总数校验通过: {actual_total}")

        # 详细分析
        if not validation_passed:
            print("详细分析: ")
        difference = actual_total - expected_total
        if difference > 0:
            print(f"  新表中多了 {difference} 条URL记录")
        elif difference < 0:
            print(f"  新表中少了 {abs(difference)} 条URL记录")

        # 检查可能的重复记录
        duplicate_pipeline = [
            {"$group": {"_id": "$url", "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}},
            {"$group": {"_id": None, "total_duplicates": {"$sum": {"$subtract": ["$count", 1]}}}}
        ]
        duplicate_result = list(new_collection.aggregate(duplicate_pipeline))
        if duplicate_result:
            duplicate_count = duplicate_result[0]['total_duplicates']
            print(f"  检测到 {duplicate_count} 条重复URL记录")

        print("=" * 50)
        return validation_passed

    def merge_collections(self, db):
        """合并多个源集合的数据到一个新集合"""
        print("开始合并多个源集合的数据...")

        # 创建或清空合并后的集合
        if self.merged_collection_name in db.list_collection_names():
            db[self.merged_collection_name].delete_many({})

        merged_collection = db[self.merged_collection_name]
        total_docs = 0

        # 从每个源集合读取数据并合并
        for source_collection_name in self.source_collections:
            source_collection = db[source_collection_name]
            # 检查源集合是否存在
            if source_collection_name not in db.list_collection_names():
                print(f"警告: 集合 {source_collection_name} 不存在，跳过")
                continue

            # 检查是否存在 status 为 error 的数据
            error_docs = source_collection.find_one({"status": "error"})
            if error_docs:
                # 提示用户确认是否删除
                result = source_collection.delete_many({"status": "error"})
                print(f"已从 {source_collection_name} 中删除 {result.deleted_count} 条爬取失败的URL数据。")

            # 统计该集合中的文档数量
            count = source_collection.count_documents({"claw_status": {"$exists": True}})
            print(f"从集合 {source_collection_name} 读取 {count} 条文档")
            total_docs += count

            # 将数据添加到合并后的集合
            cursor = source_collection.find({"claw_status": {"$exists": True}}, {"url": 1, "verification_status": 1})
            docs = list(cursor)
            if docs:
                merged_collection.insert_many(docs)

        print(f"已完成合并操作，共合并 {total_docs} 条记录到 {self.merged_collection_name}")
        return True, total_docs

    def split_collection(self, db, total_docs):
        """将合并后的集合平均分割为四个部分"""
        print("开始将合并后的集合分割为四个部分...")

        # 获取合并后的集合
        merged_collection = db[self.merged_collection_name]

        # 计算每个分割部分应包含的文档数量
        docs_per_part = total_docs // len(self.target_collections)
        remainder = total_docs % len(self.target_collections)

        # 清空或创建目标集合
        for target_collection_name in self.target_collections:
            if target_collection_name in db.list_collection_names():
                db[target_collection_name].delete_many({})

        # 获取所有文档的ID列表（用于分割）
        all_ids = [doc['_id'] for doc in merged_collection.find({}, {"_id": 1})]

        # 分割并插入到目标集合
        start_idx = 0
        for i, target_collection_name in enumerate(self.target_collections):
            target_collection = db[target_collection_name]

            # 计算当前部分的文档数量（处理余数）
            current_part_size = docs_per_part + (1 if i < remainder else 0)

            # 获取当前部分的文档ID
            part_ids = all_ids[start_idx: start_idx + current_part_size]

            # 从合并集合中获取文档并插入到目标集合
            docs_to_insert = []
            for doc_id in part_ids:
                doc = merged_collection.find_one({"_id": doc_id})
                if doc:
                    docs_to_insert.append(doc)

            if docs_to_insert:
                target_collection.insert_many(docs_to_insert)
                print(f"已将 {len(docs_to_insert)} 条记录插入到 {target_collection_name}")

            start_idx += current_part_size

        print("已完成分割操作")
        return True

    def process_urls(self, db, city_codes):
        # 合并多个集合
        merge_success, total_docs = self.merge_collections(db)
        if not merge_success:
            return "⚠️ 合并集合失败，请检查数据"

        merged_collection = db[self.merged_collection_name]

        # 统计验证成功和失败的数量
        success_count = merged_collection.count_documents({"verification_status": True})
        failed_count = merged_collection.count_documents({"verification_status": {"$ne": True}})

        # 收集要插入的文档
        docs_to_insert = []
        docs = merged_collection.find({}, {"url": 1, "verification_status": 1})

        for doc in docs:
            base_url = doc['url']
            verification_status = doc.get("verification_status", False)

            if verification_status:
                # 验证成功，为每个城市代码生成URL
                for code in city_codes:
                    new_url = f"{base_url}&jobArea={code}"
                    new_doc = {
                        "url": new_url,
                        "timestamp": datetime.now()
                    }
                    docs_to_insert.append(new_doc)
            else:
                # 验证失败，直接插入原URL
                new_doc = {
                    "url": base_url,
                    "timestamp": datetime.now()
                }
                docs_to_insert.append(new_doc)

        # 清空合并后的集合（准备重新插入处理后的URL）
        merged_collection.delete_many({})

        # 批量插入
        total_inserted = 0
        if docs_to_insert:
            # 分批插入以避免超出MongoDB的大小限制
            batch_size = 1000
            for i in range(0, len(docs_to_insert), batch_size):
                batch = docs_to_insert[i:i + batch_size]
                result = merged_collection.insert_many(batch)
                total_inserted += len(result.inserted_ids)
            print(f"已完成批量插入操作，共插入 {total_inserted} 条记录")

        # 去重操作
        print("开始去重操作...")
        pipeline = [
            {"$group": {"_id": "$url", "dups": {"$push": "$_id"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}},
            {"$project": {"dups": {"$slice": ["$dups", 1, {"$subtract": ["$count", 1]}]}}}
        ]

        deleted_count = 0
        for doc in merged_collection.aggregate(pipeline):
            for dup_id in doc['dups']:
                merged_collection.delete_one({"_id": dup_id})
                deleted_count += 1

        if deleted_count > 0:
            print(f"已完成去重操作，删除了 {deleted_count} 条重复记录")
        else:
            print("去重操作完成，未发现重复记录")

        # 执行URL数量一致性校验
        validation_passed = self.validate_url_counts(db, city_codes, success_count, failed_count, total_inserted)

        if validation_passed:
            # 为qcwy_step2_urls补充信息
            industry_csv = "industryCode.csv"
            city_csv = "qianchengwuyou_job_area_data.csv"
            processor = URLDataProcessor(
                mongo_uri="mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA",
                mongo_db="MOOC123_DA",
                collection_name=self.merged_collection_name,
                industry_csv=industry_csv,
                city_csv=city_csv
            )
            processor.run()

            # 分割集合
            split_success = self.split_collection(db, merged_collection.count_documents({}))
            if split_success:
                return "✅ 已完成urls的生成、合并、分割和校验，所有操作均通过，请进行下一步"
            else:
                return "⚠️ 已完成urls的生成和校验，但分割操作失败，请检查数据"
        else:
            return "⚠️ 已完成urls的生成，但数量一致性校验未通过，请检查数据"

    def run(self):
        client, db = self.connect_mongo()
        city_codes = self.read_city_codes()
        result = self.process_urls(db, city_codes)
        client.close()
        print(result)
        print("程序退出")


if __name__ == "__main__":
    csv_file_path = "qianchengwuyou_job_area_data.csv"
    spider = QcwySpiderStep3(csv_file_path)
    spider.run()
import csv
from urllib.parse import quote, urlparse, parse_qs
from pymongo import MongoClient, UpdateOne
import hashlib
from typing import List, Dict, Tuple, Set, Optional
import pandas as pd
import time


class URLGenerator:
    """生成和校验URL的类"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.url_map = {}  # 存储 (industry, keyword) 到 URL 的映射

    def generate_urls(self, industries: List[str], keywords: List[str]) -> Dict[Tuple[str, str], str]:
        """生成所有行业和关键词组合的URL"""
        for industry in industries:
            for keyword in keywords:
                encoded_keyword = quote(keyword, safe='')
                url = self.base_url.format(industry=industry, keyword=encoded_keyword)

                if self._is_valid_url(url):
                    self.url_map[(industry, keyword)] = url
                else:
                    print(f"无效 URL: {url}")

        return self.url_map

    def _is_valid_url(self, url: str) -> bool:
        """校验URL格式是否有效"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False


class MongoDBHandler:
    """处理MongoDB操作的类"""

    def __init__(self, mongo_uri: str, db_name: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def clear_collection(self, collection_name: str) -> None:
        """清空指定集合中的所有文档"""
        collection = self.db[collection_name]
        if collection.count_documents({}) > 0:
            collection.delete_many({})
            print(f"已清空集合: {collection_name}")

    def insert_documents(self, collection_name: str, documents: List[Dict]) -> None:
        """向指定集合插入多个文档"""
        collection = self.db[collection_name]
        if documents:
            collection.insert_many(documents)
            print(f"已存储 {len(documents)} 个文档到 {collection_name}")

    def close_connection(self) -> None:
        """关闭MongoDB连接"""
        self.client.close()


class URLManager:
    """管理URL处理流程的类"""

    def __init__(self, generator: URLGenerator, db_handler: MongoDBHandler):
        self.generator = generator
        self.db_handler = db_handler

    def process_and_store_urls(self, industries: List[str], keywords: List[str], collections: Dict[str, str]) -> None:
        """处理并存储URL到MongoDB"""
        # 清空所有集合
        for col_name in collections.values():
            self.db_handler.clear_collection(col_name)

        # 生成URL
        url_map = self.generator.generate_urls(industries, keywords)
        valid_urls = list(url_map.values())
        total_count = len(valid_urls)

        # 存储所有URL
        all_docs = [{"industry": k[0], "keyword": k[1], "url": v} for k, v in url_map.items()]
        self.db_handler.insert_documents(collections["all"], all_docs)

        # 校验生成情况
        self._validate_generation(url_map, industries, keywords)

    def split_urls_into_parts(self, collections: Dict[str, str]) -> None:
        """将主集合中的URL分割到多个子集合中"""
        all_collection = self.db_handler.db[collections["all"]]

        # 获取所有URL
        all_urls = list(all_collection.find({}, {"_id": 0, "industry": 1, "keyword": 1, "url": 1}))
        total_count = len(all_urls)

        if total_count == 0:
            print("主集合中没有URL可分割")
            return

        # 分批存储
        part_size = total_count // 4
        parts = {
            "part1": all_urls[:part_size],
            "part2": all_urls[part_size:2 * part_size],
            "part3": all_urls[2 * part_size:3 * part_size],
            "part4": all_urls[3 * part_size:]
        }

        for part_name, docs in parts.items():
            self.db_handler.insert_documents(collections[part_name], docs)
            print(f"已将 {len(docs)} 个URL存储到 {collections[part_name]}")

    def _validate_generation(self, url_map: Dict[Tuple[str, str], str], industries: List[str],
                             keywords: List[str]) -> None:
        """校验所有(industry, keyword)对是否都生成了有效URL"""
        missing_pairs = []
        for industry in industries:
            for keyword in keywords:
                if (industry, keyword) not in url_map:
                    missing_pairs.append((industry, keyword))

        if missing_pairs:
            print(f"警告: 有 {len(missing_pairs)} 对 (industry, keyword) 没有生成有效 URL")
            for pair in missing_pairs[:10]:
                print(f"缺失: industry={pair[0]}, keyword={pair[1]}")
            if len(missing_pairs) > 10:
                print(f"... 以及其他 {len(missing_pairs) - 10} 对")
        else:
            print("所有 (industry, keyword) 对都生成了有效 URL")


class URLDataProcessor:
    """处理URL数据并更新MongoDB文档的类"""

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
            result['keyword'] = quote(encoded_keyword, safe='')

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
            # 根据实际CSV结构调整列名
            code_col = '行业code' if '行业code' in df.columns else 'code'
            industry_col = '行业' if '行业' in df.columns else df.columns[0]

            # 构建映射字典，确保code为字符串类型
            mapping = {}
            for _, row in df.iterrows():
                code = str(row[code_col]).zfill(2)  # 将代码转换为字符串并补齐到2位
                industry = row[industry_col]
                mapping[code] = industry

            print(f"成功加载 {len(mapping)} 个行业映射")
            self.industry_mapping = mapping
        except Exception as e:
            print(f"加载行业映射失败: {e}")

    def load_city_mapping(self):
        """从CSV文件加载城市代码映射"""
        try:
            df = pd.read_csv(self.city_csv)
            # 检查CSV文件结构
            print(f"城市映射CSV列名: {df.columns.tolist()}")
            # 根据实际CSV结构调整列名
            city_col = '城市' if '城市' in df.columns else df.columns[0]
            code_col = 'code' if 'code' in df.columns else df.columns[1]

            # 构建映射字典，同时存储标准格式和变体格式
            mapping = {}
            for _, row in df.iterrows():
                city = row[city_col]
                code = str(row[code_col])

                # 存储原始代码
                mapping[code] = city

                # 处理前导零的变体
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

            print(f"成功加载 {len(mapping)} 个城市映射")
            # 示例: 打印一些映射结果
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

                # 尝试多种变体格式匹配
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
                    # 记录未找到的代码，便于调试
                    print(f"未找到城市代码: {jobArea_code}")

                update_data['jobArea'] = city_name

            # 生成更新操作
            if update_data:
                bulk_operations.append(
                    UpdateOne({'_id': doc_id}, {'$set': update_data})
                )

        return bulk_operations

    def run(self):
        """执行数据处理和更新操作"""
        start_time = time.time()
        try:
            # 连接MongoDB
            print(f"正在连接MongoDB，准备处理集合 {self.collection_name}...")
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
            print(f"总共需要处理 {total_docs} 个文档")

            # 分批处理
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
                          f"总耗时: {final_elapsed_time:.2f}秒")

            print(f"集合 {self.collection_name} 处理完成。")

        except Exception as e:
            print(f"处理过程中出现错误: {e}")

        finally:
            if self.client:
                self.client.close()
                print("MongoDB连接已关闭")


def read_keywords(file_path: str) -> List[str]:
    """从CSV文件读取关键词"""
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过标题行
        return [row[0] for row in reader]


def generate_industries() -> List[str]:
    """生成行业代码列表（01 - 64）"""
    return [f"{i:02d}" for i in range(1, 65)]


def main():
    """主函数，程序入口点"""
    # 配置信息
    MONGO_URI = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
    MONGO_DB = "MOOC123_DA"
    COLLECTIONS = {
        "all": "qcwy_step1_urls",
        "part1": "qcwy_step1_urls_part1",
        "part2": "qcwy_step1_urls_part2",
        "part3": "qcwy_step1_urls_part3",
        "part4": "qcwy_step1_urls_part4"
    }
    BASE_URL = "https://we.51job.com/pc/search?industry={industry}&searchType=2&sortType=1&metro=&keyword={keyword}"
    KEYWORDS_FILE = 'keyword(1).csv'
    INDUSTRY_CSV = "industryCode.csv"
    CITY_CSV = "qianchengwuyou_job_area_data.csv"

    # 读取数据
    print("正在读取关键词和生成行业代码...")
    keywords = read_keywords(KEYWORDS_FILE)
    industries = generate_industries()

    # 初始化组件
    print("正在初始化URL生成器和数据库处理器...")
    url_generator = URLGenerator(BASE_URL)
    db_handler = MongoDBHandler(MONGO_URI, MONGO_DB)
    url_manager = URLManager(url_generator, db_handler)

    # 处理并存储URL到主集合
    print("开始生成URL并存储到主集合...")
    url_manager.process_and_store_urls(industries, keywords, COLLECTIONS)

    # 处理主集合中的URL数据
    print("开始处理主集合中的URL数据...")
    data_processor = URLDataProcessor(MONGO_URI, MONGO_DB, COLLECTIONS["all"], INDUSTRY_CSV, CITY_CSV)
    data_processor.run()

    # 将主集合分割到多个子集合
    print("开始将主集合分割到多个子集合...")
    url_manager.split_urls_into_parts(COLLECTIONS)

    # 关闭数据库连接
    db_handler.close_connection()
    print("所有操作完成，已关闭数据库连接。")


if __name__ == "__main__":
    main()
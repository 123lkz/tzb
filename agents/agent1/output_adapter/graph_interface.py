"""GraphInterface — 图谱接口适配器

职责：将 Agent1Output 写入 MongoDB agent1_output 集合，
并提供给后续模块（Agent2/图谱搭建）消费的查询接口。
"""
from datetime import datetime
from loguru import logger

from agents.agent1.config import MONGODB_URI, MONGODB_DB, AGENT1_OUTPUT_COLLECTION
from agents.agent1.output_adapter.schemas import Agent1Output


class GraphInterface:
    """图谱接口适配器 —— 管理 agent1_output 集合的读写"""

    def __init__(self, uri: str = MONGODB_URI, db_name: str = MONGODB_DB):
        self.uri = uri
        self.db_name = db_name
        self._client = None
        self._collection = None
        logger.info(f"GraphInterface: db={db_name}, collection={AGENT1_OUTPUT_COLLECTION}")

    @property
    def _db(self):
        """懒加载 MongoDB 连接"""
        if self._client is None:
            import pymongo
            self._client = pymongo.MongoClient(self.uri)
            db = self._client[self.db_name]
            self._collection = db[AGENT1_OUTPUT_COLLECTION]
            self._collection.create_index("output_id", unique=True)
            self._collection.create_index("status")
            self._collection.create_index([("output_type", 1), ("status", 1)])
            self._collection.create_index("created_at")
        return self._collection

    def save(self, output: Agent1Output) -> bool:
        """保存单条输出到 MongoDB"""
        try:
            data = output.model_dump()
            data["_schema_version"] = "1.0"
            self._db.replace_one(
                {"output_id": output.output_id},
                data,
                upsert=True,
            )
            return True
        except Exception as e:
            logger.error(f"保存 Agent1Output 失败: {e}")
            return False

    def save_batch(self, outputs: list[Agent1Output]) -> int:
        """批量保存输出记录

        Returns:
            成功保存的数量
        """
        success = 0
        for output in outputs:
            if self.save(output):
                success += 1
        logger.info(f"批量保存完成: {success}/{len(outputs)} 条成功")
        return success

    def get_pending(self, output_type: str = None, limit: int = 100) -> list[dict]:
        """查询待处理（pending）的输出记录

        Args:
            output_type: 可选，按类型筛选 "new_position" / "skill_change"
            limit: 最大返回条数

        Returns:
            未处理的 Agent1Output 记录列表
        """
        query = {"status": "pending"}
        if output_type:
            query["output_type"] = output_type

        results = list(
            self._db.find(query, {"_id": 0}).sort("created_at", 1).limit(limit)
        )
        return results

    def get_verified(self, output_type: str = None, limit: int = 100) -> list[dict]:
        """查询已验证通过（verified）的输出记录"""
        query = {"status": "verified"}
        if output_type:
            query["output_type"] = output_type
        results = list(
            self._db.find(query, {"_id": 0}).sort("created_at", 1).limit(limit)
        )
        return results

    def update_status(self, output_id: str, status: str,
                      verified_by: str = None,
                      verification_report_id: str = None) -> bool:
        """更新输出记录的状态

        Args:
            output_id: 输出记录 ID
            status: 新状态 (verified / rejected / merged)
            verified_by: 验证者标识（可选）
            verification_report_id: 验证报告 ID（可选）
        """
        try:
            update = {"$set": {"status": status, "updated_at": datetime.now().isoformat()}}
            if verified_by:
                update["$set"]["verified_by"] = verified_by
            if verification_report_id:
                update["$set"]["verification_report_id"] = verification_report_id
            self._db.update_one({"output_id": output_id}, update)
            return True
        except Exception as e:
            logger.error(f"更新输出状态失败: {e}")
            return False

    def count_by_status(self, output_type: str = None) -> dict:
        """按状态统计输出记录数"""
        match = {}
        if output_type:
            match["output_type"] = output_type
        pipeline = [
            {"$match": match},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
        ]
        results = list(self._db.aggregate(pipeline))
        counts = {r["_id"]: r["count"] for r in results}
        return counts

    def close(self):
        """关闭 MongoDB 连接"""
        if self._client:
            self._client.close()
            self._client = None
            logger.info("GraphInterface 资源已释放")

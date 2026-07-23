"""Dedup module - clean job deduplication"""
import pymongo, re
from collections import defaultdict
from difflib import SequenceMatcher
from loguru import logger
from agents.agent2.config import MONGODB_URI, MONGODB_DB, JOBS_CLEAN_COLLECTION, JOBS_DEDUPLICATED_COLLECTION

U = lambda s: s.encode().decode("unicode_escape")

def similar(a, b, threshold=0.85):
    if not a or not b: return False
    a, b = a.strip().lower(), b.strip().lower()
    if a == b: return True
    return SequenceMatcher(None, a, b).ratio() >= threshold

def norm_company(name):
    if not name: return ""
    n = name.strip().lower()
    for suf in [U(r"\u6709\u9650\u516c\u53f8"), U(r"\u80a1\u4efd\u6709\u9650\u516c\u53f8"),
                U(r"\u96c6\u56e2"), U(r"\u79d1\u6280"), "inc.", "ltd"]:
        n = re.sub(re.escape(suf) + r"$", "", n)
    return n.strip()

class DedupResult:
    def __init__(self):
        self.kept = []; self.removed = []; self.stats = {}

class ExactDeduper:
    def dedup(self, records):
        result = DedupResult()
        seen = {}
        for r in records:
            key = (r.get("title","").strip().lower(),
                   r.get("company","").strip().lower(),
                   r.get("city","").strip().lower())
            if key in seen:
                nd = len(r.get("description","") or "")
                od = len(seen[key].get("description","") or "")
                if nd > od * 1.5 or (r.get("pub_date","") > seen[key].get("pub_date","")):
                    result.removed.append(seen[key]); seen[key] = r
                else:
                    result.removed.append(r)
            else:
                seen[key] = r
        result.kept = list(seen.values())
        result.stats = {"before":len(records),"after":len(result.kept),"removed":len(records)-len(result.kept)}
        return result

class CrossPlatformDeduper:
    def dedup(self, records):
        groups = defaultdict(list)
        for r in records:
            groups[(r.get("title","").strip().lower(),
                    norm_company(r.get("company","")),
                    r.get("city","").strip().lower())].append(r)
        result = DedupResult()
        for key, group in groups.items():
            if len(group) == 1:
                result.kept.append(group[0])
            else:
                best = max(group, key=lambda r: len(r.get("description","") or "") + len(r.get("skills",[]) or []))
                sources = list(set(r.get("source","") for r in group if r.get("source")))
                if sources: best["source"] = "+".join(sources)
                all_sk = []
                for r in group:
                    for s in (r.get("skills",[]) or []):
                        if s not in all_sk: all_sk.append(s)
                if all_sk: best["skills"] = all_sk
                result.kept.append(best)
                for r in group:
                    if r is not best: result.removed.append(r)
        result.stats = {"before":len(records),"after":len(result.kept),"removed":len(records)-len(result.kept)}
        return result


class ContentDeduper:
    def dedup(self, records):
        groups = {}
        used = set()
        result = DedupResult()
        for i, a in enumerate(records):
            if i in used:
                continue
            cluster = [i]
            used.add(i)
            at = a.get("title","").strip().lower()
            ad = (a.get("description","") or "")[:200].lower()
            for j, b in enumerate(records):
                if j in used or i == j:
                    continue
                bt = b.get("title","").strip().lower()
                bd = (b.get("description","") or "")[:200].lower()
                if similar(at, bt, 0.8) and similar(ad, bd, 0.7):
                    cluster.append(j)
                    used.add(j)
            if len(cluster) > 1:
                items = [records[k] for k in cluster]
                best = max(items, key=lambda r: len(r.get("description","") or "") + len(r.get("skills",[]) or []))
                for item in items:
                    if item is best:
                        result.kept.append(item)
                    else:
                        result.removed.append(item)
            else:
                result.kept.append(records[cluster[0]])
        result.stats = {"before":len(records),"after":len(result.kept),"removed":len(records)-len(result.kept)}
        return result

class DedupOrchestrator:
    def __init__(self, uri=MONGODB_URI, db_name=MONGODB_DB):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.src = self.db[JOBS_CLEAN_COLLECTION]
        self.tgt = self.db[JOBS_DEDUPLICATED_COLLECTION]

    def run(self, batch_size=0):
        records = list(self.src.find().limit(batch_size) if batch_size else self.src.find())
        logger.info(f"Dedup: loaded {len(records)} from {JOBS_CLEAN_COLLECTION}")
        s1 = ExactDeduper().dedup(records)
        logger.info(f"Exact dedup: {s1.stats['before']} -> {s1.stats['after']} (removed {s1.stats['removed']})")
        s2 = CrossPlatformDeduper().dedup(s1.kept)
        s3 = ContentDeduper().dedup(s2.kept)
        logger.info(f"Cross-platform dedup: {s2.stats['before']} -> {s2.stats['after']} (removed {s2.stats['removed']})")
        self.tgt.delete_many({})
        if s3.kept:
            for r in s3.kept: r.pop("_id", None)
            self.tgt.insert_many(s3.kept)
        total = len(records) - len(s3.kept)
        result = {"source":len(records),"exact_removed":s1.stats["removed"],"cross_removed":s2.stats["removed"],"content_removed":s3.stats["removed"],"total_removed":total,"deduplicated":len(s3.kept)}
        logger.info(f"Dedup done: {result}")
        return result

    def close(self): self.client.close()

__all__ = ["DedupOrchestrator", "ExactDeduper", "CrossPlatformDeduper"]

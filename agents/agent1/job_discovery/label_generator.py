"""LabelGenerator -- LLM assisted labeling"""
import json, re, time
from loguru import logger
from agents.agent1.job_discovery.schemas import NewPositionSuggestion, ClusterInfo

class LabelGenerator:
    def __init__(self, llm_client=None):
        self.llm = llm_client

    def generate(self, cluster, cluster_records=None):
        if self.llm is not None:
            time.sleep(2)
            return self._generate_with_llm(cluster, cluster_records)
        return self._generate_statistical(cluster, cluster_records)

    def generate_batch(self, clusters, all_records):
        suggestions = []
        for cluster in clusters:
            cr = None
            if all_records and cluster.sample_indices:
                cr = [all_records[i] for i in cluster.sample_indices if i < len(all_records)]
            suggestions.append(self.generate(cluster, cr))
        return suggestions

    def _generate_with_llm(self, cluster, cluster_records=None):
        tt = chr(10).join(f"- {t}" for t in cluster.titles_sample[:5])
        dt = chr(10).join(f"- {d[:300]}" for d in cluster.text_sample[:3])
        p = f"""你是一个招聘数据分析专家。以下是一组已聚类的招聘岗位样本，请分析这些岗位的共同特征并输出：

1. 建议的岗位名称
2. 该岗位的自然语言描述
3. 该岗位的核心职责(3-5项)
4. 该岗位的必需技能(3-5项)
5. 该岗位的加分技能(0-3项)
6. 该岗位的典型行业应用场景(1-3项)
7. 你的置信度(0-1)

样本岗位名称:
{tt}

样本JD片段:
{dt}

请以JSON格式输出:
{{"suggested_name":"xxx","description":"xxx","core_responsibilities":[...],"required_skills":[...],"optional_skills":[...],"typical_applications":[...],"confidence":0.xx}}"""
        try:
            result = self.llm.chat_with_json([{"role":"user","content":p}], temperature=0.3)
        except:
            return self._generate_statistical(cluster, cluster_records)
        if isinstance(result, dict) and "suggested_name" in result:
            return NewPositionSuggestion(
                suggested_name=result.get("suggested_name",""),
                description=result.get("description",""),
                cluster_size=cluster.size, novelty_score=0.0,
                evidence_samples=cluster.text_sample, related_skills=[],
                suggested_required_skills=result.get("required_skills",[]),
                suggested_optional_skills=result.get("optional_skills",[]),
                core_responsibilities=result.get("core_responsibilities",[]),
                typical_applications=result.get("typical_applications",[]),
                typical_salary_range={},
                confidence=float(result.get("confidence",0.7)),
                provenance={"generation_method":"llm"})
        return self._generate_statistical(cluster, cluster_records)

    def _generate_statistical(self, cluster, cluster_records=None):
        t = cluster.titles_sample
        name = self._extract_common_name(t) if t else f"emerging_{cluster.cluster_id}"
        sk = self._extract_skills_from_records(cluster_records) if cluster_records else []
        return NewPositionSuggestion(
            suggested_name=name,
            description=f"基于{len(t)}条招聘记录发现",
            cluster_size=cluster.size, novelty_score=0.0,
            evidence_samples=cluster.text_sample,
            related_skills=sk,
            suggested_required_skills=sk[:3],
            suggested_optional_skills=sk[3:5],
            typical_salary_range={}, confidence=0.5,
            provenance={"generation_method":"statistical"})

    def _extract_common_name(self, titles):
        from collections import Counter
        c = [re.sub(r"[(\)()（）]","",t).strip() for t in titles]
        return Counter(c).most_common(1)[0][0] if c else (titles[0] if titles else "unknown")

    def _extract_skills_from_records(self, records):
        sk, seen = [], set()
        for r in records:
            s = r.get("skills",[])
            for x in (s if isinstance(s,list) else [s]):
                x = x.strip()
                if x and x not in seen: seen.add(x); sk.append(x)
        return sk[:10]
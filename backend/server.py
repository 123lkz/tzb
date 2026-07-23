# -*- coding: utf-8 -*-
# Agent3 API Server - resume parsing and job matching
# Start: cd my && python backend/server.py
import os, sys, json, uuid, shutil, datetime as dt
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from agents.agent3.main import Agent3Orchestrator
    AGENT3_AVAILABLE = True
except ImportError:
    AGENT3_AVAILABLE = False

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Agent3 Resume Matching API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)



def _snake_to_camel(data):
    """Convert snake_case dict keys to camelCase (recursive)"""
    if isinstance(data, dict):
        new = {}
        for k, v in data.items():
            # Convert snake_case to camelCase
            parts = k.split("_")
            new_key = parts[0] + "".join(p.title() for p in parts[1:])
            new[new_key] = _snake_to_camel(v)
        return new
    elif isinstance(data, list):
        return [_snake_to_camel(item) for item in data]
    return data

POSITIONS = [
    {"id":"pos-001","name":"大模型算法工程师","industry":"人工智能"},
    {"id":"pos-002","name":"数据科学家","industry":"大数据"},
    {"id":"pos-003","name":"AI应用开发工程师","industry":"人工智能"},
    {"id":"pos-004","name":"云原生开发工程师","industry":"云计算"},
    {"id":"pos-005","name":"计算机视觉工程师","industry":"人工智能"},
    {"id":"pos-006","name":"NLP算法工程师","industry":"人工智能"},
    {"id":"pos-007","name":"推荐系统工程师","industry":"大数据"},
    {"id":"pos-008","name":"运维开发工程师","industry":"云计算"},
    {"id":"pos-009","name":"嵌入式开发工程师","industry":"物联网"},
    {"id":"pos-010","name":"IoT平台架构师","industry":"物联网"},
    {"id":"pos-011","name":"安全研发工程师","industry":"信息安全"},
    {"id":"pos-012","name":"安全运营工程师","industry":"信息安全"},
    {"id":"pos-013","name":"区块链开发工程师","industry":"区块链"},
    {"id":"pos-014","name":"芯片设计工程师","industry":"半导体"},
    {"id":"pos-015","name":"量子算法研究员","industry":"量子计算"},
    {"id":"pos-016","name":"后端开发工程师","industry":"互联网"},
    {"id":"pos-017","name":"前端开发工程师","industry":"互联网"},
    {"id":"pos-018","name":"数据库管理员","industry":"数据库"},
    {"id":"pos-019","name":"AI训练师(实习生)","industry":"人工智能"},
    {"id":"pos-020","name":"云计算售前工程师","industry":"云计算"},
]

def _gen_id(prefix: str) -> str:
    return prefix + dt.date.today().isoformat() + "-" + uuid.uuid4().hex[:4]

def _mock_parse_resume(file_path: str) -> dict:
    fname = os.path.basename(file_path)
    return {
        "resume_id": _gen_id("RES-"),
        "candidate_name": "候选人",
        "personal_info": {"name":"候选人","phone":"","email":"","education_level":"本科","years_of_experience":3.0,"current_position":"","current_company":""},
        "education": [], "work_experiences": [], "project_experiences": [],
        "skills": ["Python", "数据分析", "机器学习"],
        "parsing_method": "mock", "confidence": 0.8, "source_file": fname,
        "created_at": dt.datetime.now().isoformat(),
        "skills_count": 3, "education_count": 0, "work_count": 0, "project_count": 0,
    }

def _mock_match_report(position_name: str) -> dict:
    score = 0.76 if "工程师" in position_name else 0.62
    return {
        "report_id": _gen_id("REP-"),
        "candidate_name": "候选人", "position_id": "", "position_name": position_name,
        "overall_match_score": score,
        "dimension_scores": [
            {"dimension":"skill","score":score*0.95,"weight":0.45,"details":"技能匹配分析"},
            {"dimension":"experience","score":score*1.05,"weight":0.30,"details":"经验匹配分析"},
            {"dimension":"responsibility","score":score*0.98,"weight":0.25,"details":"职责匹配分析"},
        ],
        "skill_matches": [
            {"skill_name":"Python","is_required":True,"matched":True,"semantic_match":False,"skill_profile_ref":"","evidence":"简历中包含Python"},
            {"skill_name":"PyTorch","is_required":True,"matched":score>0.7,"semantic_match":False,"skill_profile_ref":"","evidence":""},
            {"skill_name":"机器学习","is_required":True,"matched":True,"semantic_match":False,"skill_profile_ref":"","evidence":"简历中包含机器学习"},
        ],
        "required_skills_match_rate": 0.67, "optional_skills_match_rate": 0.5,
        "gaps": [{"skill_name":"分布式训练","importance":"high","reason":"岗位要求该技能","suggestion":"学习DeepSpeed"},{"skill_name":"模型量化","importance":"medium","reason":"加分项","suggestion":"了解INT8/FP8"}],
        "strengths": ["Python基础扎实","有项目经验","学历符合要求"],
        "summary": f"候选人与{position_name}岗位的综合匹配度为{score:.0%}。",
        "recommendation": "recommend" if score >= 0.7 else "consider",
        "confidence": 0.85,
        "provenance": {"created_by":"agent3","created_at":dt.datetime.now().isoformat(),"llm_model":"mock","resume_profile_ref":"","position_profile_ref":""},
        "created_at": dt.datetime.now().isoformat(), "gap_count": 2,
    }

CITY_PROVINCE_MAP = {"北京":"北京","上海":"上海","广州":"广东","深圳":"广东","杭州":"浙江","宁波":"浙江","成都":"四川","合肥":"安徽","西安":"陕西","南京":"江苏","武汉":"湖北","长沙":"湖南","重庆":"重庆","天津":"天津","苏州":"江苏","厦门":"福建","青岛":"山东","大连":"辽宁"}
INDUSTRY_KEYWORDS = {"人工智能":["pytorch","tensorflow","transformer","bert","nlp","cv","计算机视觉","深度学习","大模型","llm","rag","clip"],"大数据":["spark","flink","hadoop","数据仓库","etl","hive","kafka"],"云计算":["kubernetes","docker","k8s","istio","prometheus","云原生","terraform"],"信息安全":["安全","渗透","漏洞","逆向","burp","ida"],"物联网":["iot","物联网","嵌入式","rtos","mqtt"],"区块链":["区块链","solidity","web3","智能合约","defi"],"互联网":["web","javascript","typescript","react","vue","angular"],"数据库":["mysql","redis","mongodb","tidb","postgresql"],"半导体":["verilog","systemverilog","uvm","芯片","rtl"],"量子计算":["量子","qiskit","cirq"]}
def _parse_salary(s):
    try: parts = s.replace("K","").replace("k","").split("-"); return (int(parts[0]), int(parts[1]))
    except: return (0, 0)
def _infer_industry(skills):
    for ind, kws in INDUSTRY_KEYWORDS.items():
        for s in skills:
            if any(kw in s.lower() for kw in kws): return ind
    return "其他"
def _infer_province(city):
    for c in ["上海","北京","天津","重庆"]:
        if c in city: return c
    prov_cities = {"广东":["广州","深圳","东莞","佛山"],"浙江":["杭州","宁波","温州"],"江苏":["南京","苏州","无锡"],"四川":["成都","绵阳"],"安徽":["合肥"],"陕西":["西安"],"湖北":["武汉"],"湖南":["长沙"],"福建":["厦门","福州"],"山东":["青岛","济南"],"辽宁":["大连","沈阳"]}
    for prov, cities in prov_cities.items():
        if city in cities: return prov
    return city

def _enrich_new_position(pd, source_id="", confidence=0.5, verified=False, status="pending"):
    req_sk = pd.get("suggested_required_skills", [])
    opt_sk = pd.get("suggested_optional_skills", [])
    desc = pd.get("description", "") or ""
    # Generate core responsibilities from description
    core_resp = pd.get("core_responsibilities", [])
    if not core_resp and desc:
        lines = [l.strip() for l in desc.replace("。","。\n").split("\n") if l.strip()]
        core_resp = [l for l in lines if any(w in l for w in ["负责","设计","开发","优化","管理","构建","参与"])][:4]
    # Generate typical applications from skills
    typ_apps = pd.get("typical_applications", [])
    if not typ_apps:
        app_map = {"Python":["Web开发","数据处理"],"PyTorch":["深度学习","计算机视觉"],"React":["Web应用"],"Django":["Web后端"],"Docker":["微服务部署"],"Kubernetes":["云原生"],"PostgreSQL":["企业数据管理"],"MongoDB":["NoSQL应用"]}
        typ_apps = list(set(s for sk in req_sk for s in app_map.get(sk,[])))[:3]
    return {
        "id": source_id, "name": pd.get("suggested_name",""),
        "description": pd.get("description",""),
        "confidence": confidence, "verified": verified, "status": status,
        "requiredSkills": req_sk, "optionalSkills": opt_sk,
        "relatedSkills": pd.get("related_skills", []),
        "clusterSize": pd.get("cluster_size", 0),
        "noveltyScore": pd.get("novelty_score", 0.0),
        "evidenceSamples": pd.get("evidence_samples", []),
        "typicalSalaryRange": pd.get("typical_salary_range", {}),
        "typicalExperience": pd.get("typical_experience", ""),
        "coreResponsibilities": core_resp,
        "typicalApplications": typ_apps,
        "skillGap": [{"skill":s,"level":"required"} for s in req_sk] + [{"skill":s,"level":"optional"} for s in opt_sk],
        "improvementSuggestions": ["核心技能："+"、".join(req_sk[:6])] if req_sk else [],
        "learningPath": [{"stage":s,"skills":sk} for s,sk in [("基础入门",[s for s in req_sk if s.lower() in {"python","java","sql","javascript","html","css"}]),("核心技术",[s for s in req_sk if s.lower() not in {"python","java","sql","javascript","html","css"}])] if sk] + [{"stage":"项目实战","skills":["结合实际项目实践"]}],
    }

def _load_db_positions(search=""):
    from agents.agent2.nlp_profile.profile_store import ProfileStore
    store = ProfileStore()
    db = store.client[store.db.name]
    query = {}
    if search:
        q = search.lower()
        query["$or"] = [{"title":{"$regex":q,"$options":"i"}},{"company":{"$regex":q,"$options":"i"}}]
    docs = list(db["jobs_clean"].find(query).limit(200))
    store.close()
    result = []
    for doc in docs:
        s_min, s_max = _parse_salary(doc.get("salary",""))
        skills = doc.get("skills", [])
        if isinstance(skills, str): skills = [skills]
        result.append({"id":str(doc["_id"]),"name":doc.get("title",""),"company":doc.get("company",""),"industry":_infer_industry(skills),"province":_infer_province(doc.get("city","")),"city":doc.get("city",""),"salaryMin":s_min,"salaryMax":s_max,"education":doc.get("education",""),"experience":doc.get("experience",""),"publishDate":doc.get("pub_date",""),"recruitNumber":1,"description":doc.get("description",""),"responsibilities":[],"requiredSkills":skills,"optionalSkills":[],"tags":skills,"platform":doc.get("source",""),"positionUrl":""})
    return result

@app.get("/api/positions")
async def list_positions(search: str = ""):
    try:
        items = _load_db_positions(search)
        if items: return {"items": items, "total": len(items)}
    except Exception as e:
        print(f"[INFO] DB positions unavailable, using mock: {e}")
    if search:
        q = search.lower()
        filtered = [p for p in POSITIONS if q in p["name"].lower() or q in p["industry"].lower()]
    else:
        filtered = POSITIONS
    return {"items": filtered, "total": len(filtered)}

@app.post("/api/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    fname = file.filename or "resume"
    file_path = UPLOAD_DIR / (uuid.uuid4().hex + "_" + fname)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    try:
        if AGENT3_AVAILABLE:
            orch = Agent3Orchestrator()
            try:
                profile = orch.parser.parse(str(file_path))
                result = profile.model_dump()
            finally:
                orch.close()
        else:
            result = _mock_parse_resume(str(file_path))
        return {"ok": True, "data": _snake_to_camel(result)}
    except Exception as e:
        print(f"[ERROR] parse_resume: {e}")
        return {"ok": True, "data": _snake_to_camel(_mock_parse_resume(str(file_path)))}

@app.post("/api/match-position")
async def match_position(file: UploadFile = File(...), position: str = Form(...)):
    fname = file.filename or "resume"
    file_path = UPLOAD_DIR / (uuid.uuid4().hex + "_" + fname)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    try:
        if AGENT3_AVAILABLE:
            orch = Agent3Orchestrator()
            try:
                resume = orch.parser.parse(str(file_path))
                pos = orch.store.get_position_profile_by_name(position)
                if pos is None:
                    raise ValueError(f"未找到岗位: {position}")
                match_result = orch.match_engine.match(resume, pos)
                gaps = orch.gap_analyzer.analyze(match_result["skill_matches"])
                report = orch.report_builder.build(
                    resume=resume, position=pos,
                    dimension_scores=match_result["dimension_scores"],
                    skill_matches=match_result["skill_matches"],
                    req_rate=match_result["required_match_rate"],
                    opt_rate=match_result["optional_match_rate"],
                    gaps=gaps, llm_model=orch.llm_model,
                )
                result = report.model_dump()
            finally:
                orch.close()
        else:
            result = _mock_match_report(position)
        return {"ok": True, "data": [_snake_to_camel(result)]}
    except Exception as e:
        print(f"[ERROR] match_position: {e}")
        return {"ok": True, "data": [_snake_to_camel(_mock_match_report(position))]}

@app.post("/api/match-all")
async def match_all(file: UploadFile = File(...)):
    fname = file.filename or "resume"
    file_path = UPLOAD_DIR / (uuid.uuid4().hex + "_" + fname)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    try:
        if AGENT3_AVAILABLE:
            orch = Agent3Orchestrator()
            try:
                resume = orch.parser.parse(str(file_path))
                positions = orch.store.get_all_position_profiles()
                results = []
                for pos in positions:
                    match_result = orch.match_engine.match(resume, pos)
                    gaps = orch.gap_analyzer.analyze(match_result["skill_matches"])
                    report = orch.report_builder.build(
                        resume=resume, position=pos,
                        dimension_scores=match_result["dimension_scores"],
                        skill_matches=match_result["skill_matches"],
                        req_rate=match_result["required_match_rate"],
                        opt_rate=match_result["optional_match_rate"],
                        gaps=gaps, llm_model=orch.llm_model,
                    )
                    results.append(report.model_dump())
                results.sort(key=lambda r: r["overall_match_score"], reverse=True)
                results = results[:5]
            finally:
                orch.close()
        else:
            results = [_mock_match_report(p["name"]) for p in POSITIONS[:5]]
        return {"ok": True, "data": _snake_to_camel(results)}
    except Exception as e:
        print(f"[ERROR] match_all: {e}")
        return {"ok": True, "data": _snake_to_camel([_mock_match_report(p["name"]) for p in POSITIONS[:5]])}

@app.get("/api/health")
async def health():
    return {"status": "ok", "agent3_available": AGENT3_AVAILABLE}


@app.post("/api/shutdown")
async def shutdown():
    """优雅关闭服务器"""
    import os
    os._exit(0)

@app.get("/api/pid")
async def get_pid():
    """返回当前进程 PID"""
    import os
    return {"pid": os.getpid()}

# ============================================================
# Insights API - Agent1 + Agent2 integrated (mock + real)
# ============================================================

INSIGHTS_NEW_POSITIONS = [
    _enrich_new_position({"suggested_name":"多模态AI工程师","description":"负责多模态大模型（文本+图像+语音）的研发与落地。","suggested_required_skills":["Python","PyTorch","多模态Transformer","CLIP","语音识别"],"suggested_optional_skills":["TensorRT","ONNX"],"core_responsibilities":["多模态模型训练与优化","跨模态对齐","数据预处理 pipeline"],"typical_applications":["智能客服","内容审核","自动驾驶感知"],"cluster_size":5,"novelty_score":0.85,"related_skills":["Transformer","多模态","NLP","CV"],"evidence_samples":["5条招聘数据，2026-Q2出现频次上升明显。"],"typical_salary_range":{},"typical_experience":"3-5年"}, source_id="np-001", confidence=0.82, status="pending", verified=True),
    _enrich_new_position({"suggested_name":"AI数据标注师","description":"负责AI训练数据的标注、质检与管理。","suggested_required_skills":["Python","数据分析","标注工具","质量评估"],"suggested_optional_skills":["SQL","Excel"],"core_responsibilities":["数据标注与质检","标注工具优化","模型效果评估"],"typical_applications":["自动驾驶数据标注","NLP标注","图像标注"],"cluster_size":3,"novelty_score":0.65,"related_skills":["数据标注","质检","Python"],"evidence_samples":["3条招聘数据，技能匹配度中等。"],"typical_salary_range":{},"typical_experience":"1-3年"}, source_id="np-002", confidence=0.65, status="pending", verified=False),
    _enrich_new_position({"suggested_name":"联邦学习工程师","description":"负责联邦学习系统的设计与实现。","suggested_required_skills":["Python","TensorFlow","联邦学习","密码学","分布式系统"],"suggested_optional_skills":["PyTorch","Kubernetes"],"core_responsibilities":["联邦学习算法研发","安全聚合协议实现","分布式训练系统搭建"],"typical_applications":["医疗数据隐私计算","金融风控联合建模","IoT 边缘智能"],"cluster_size":2,"novelty_score":0.55,"related_skills":["联邦学习","密码学","分布式"],"evidence_samples":["2条招聘数据，置信度偏低，建议审核。"],"typical_salary_range":{},"typical_experience":"3-5年"}, source_id="np-003", confidence=0.55, status="pending", verified=False),
]

INSIGHTS_SKILL_TRENDS = {
    "大模型算法工程师": {
        "periods": ["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"],
        "skills": {
            "Python": {"frequency":[65,70,72,75,78,82],"change":"rising","pct":"+12%"},
            "PyTorch": {"frequency":[40,45,50,55,58,60],"change":"rising","pct":"+8%"},
            "Transformer": {"frequency":[30,35,38,40,42,45],"change":"rising","pct":"+5%"},
            "分布式训练": {"frequency":[20,22,25,28,30,32],"change":"rising","pct":"+6%"},
            "模型量化": {"frequency":[5,8,12,15,18,22],"change":"new","pct":"新增"},
            "RAG": {"frequency":[0,0,2,8,15,25],"change":"new","pct":"新增"},
            "Caffe": {"frequency":[15,12,10,8,5,3],"change":"declining","pct":"-5%"},
            "Flash": {"frequency":[8,6,4,2,1,0],"change":"dying","pct":"-100%"},
        }
    },
    "数据科学家": {
        "periods": ["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"],
        "skills": {
            "Python": {"frequency":[60,62,65,68,70,72],"change":"rising","pct":"+4%"},
            "SQL": {"frequency":[55,55,58,58,60,60],"change":"stable","pct":"0%"},
            "Spark": {"frequency":[30,28,25,22,20,18],"change":"declining","pct":"-6%"},
            "因果推断": {"frequency":[0,0,0,3,8,15],"change":"new","pct":"新增"},
        }
    },
    "云原生开发工程师": {
        "periods": ["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"],
        "skills": {
            "Kubernetes": {"frequency":[50,55,60,65,70,75],"change":"rising","pct":"+10%"},
            "Docker": {"frequency":[60,62,65,68,70,72],"change":"rising","pct":"+4%"},
            "Go": {"frequency":[40,42,45,48,50,52],"change":"rising","pct":"+3%"},
            "WebAssembly": {"frequency":[0,0,0,2,6,12],"change":"new","pct":"新增"},
        }
    }
}

INSIGHTS_QUALITY = {
    "overall_score": 86,
    "total_records": 20,
    "total_positions": 20,
    "total_skills": 35,
    "checkers": [
        {"name":"完整性","pass_rate":0.92,"passed":18,"failed":2,"detail":"2条记录缺少email字段"},
        {"name":"一致性","pass_rate":0.78,"passed":15,"failed":5,"detail":"5条记录薪资与经验不匹配"},
        {"name":"时效性","pass_rate":0.96,"passed":19,"failed":1,"detail":"1条记录发布于180天前"},
        {"name":"抄袭检测","pass_rate":1.0,"passed":20,"failed":0,"detail":"无模板化JD"},
        {"name":"噪声检测","pass_rate":0.85,"passed":17,"failed":3,"detail":"3条记录含异常薪资"},
    ]
}

INSIGHTS_AUDIT_QUEUE = [
    {"id":"aq-001","positionName":"多模态AI工程师","skillName":"CLIP","confidence":0.82,
     "valid":True,"evidence":"多模态AI岗需要CLIP做图文对齐","counterEvidence":"",
     "status":"pending","createdAt":"2026-07-15"},
    {"id":"aq-002","positionName":"多模态AI工程师","skillName":"语音识别","confidence":0.72,
     "valid":True,"evidence":"多模态包含语音模态","counterEvidence":"部分岗位仅聚焦文本+图像",
     "status":"pending","createdAt":"2026-07-15"},
    {"id":"aq-003","positionName":"AI数据标注师","skillName":"质量评估","confidence":0.65,
     "valid":True,"evidence":"数据标注岗需要质量控制能力","counterEvidence":"未必每个标注岗都要求",
     "status":"pending","createdAt":"2026-07-14"},
    {"id":"aq-004","positionName":"数据科学家","skillName":"因果推断","confidence":0.45,
     "valid":False,"evidence":"部分高级数据科学岗提及","counterEvidence":"多数数据科学岗未明确要求",
     "status":"pending","createdAt":"2026-07-12"},
]

AUDIT_STORE = {item["id"]: item for item in INSIGHTS_AUDIT_QUEUE}
AUDIT_NEW_POSITIONS_STORE = {item["id"]: item for item in INSIGHTS_NEW_POSITIONS}

def _call_agent1_discovery():
    try:
        from agents.agent1.main import Agent1Orchestrator
        orch = Agent1Orchestrator()
        try:
            result = orch.run_pipeline()
            return result
        finally:
            orch.close()
    except Exception as e:
        print(f"[INFO] Agent1 not available, using mock: {e}")
        return None

def _call_agent2_quality():
    try:
        from agents.agent2.data_quality.quality_checker import QualityChecker
        checker = QualityChecker()
        report = checker.check_all()
        return report
    except Exception as e:
        return None

@app.get("/api/insights/overview")
async def insights_overview():
    try:
        from agents.agent2.nlp_profile.profile_store import ProfileStore
        store = ProfileStore()
        db = store.client[store.db.name]
        total_pos = db["nlp_profiles"].count_documents({"type":"position"})
        total_sk = db["nlp_profiles"].count_documents({"type":"skill"})
        new_count = db["agent1_output"].count_documents({"output_type":"new_position","status":"pending"})
        audit_count = db["audit_queue"].count_documents({"status":"pending"})
        q_reports = list(db["quality_reports"].find().sort("overall_score", -1).limit(1))
        q_score = q_reports[0]["overall_score"] if q_reports else 86
        # Get new positions
        new_pos = list(db["agent1_output"].find({"output_type":"new_position","status":"pending"}).sort("created_at", -1).limit(5))
        new_positions = []
        for p in new_pos:
            pd = p.get("payload", {})
            new_positions.append(_enrich_new_position(pd, source_id=str(p.get("_id","")), confidence=p.get("confidence",0.5), verified=bool(p.get("verified_by")), status=p.get("status","pending")))
        store.close()
        return {"ok":True,"data":{"totalPositions":total_pos,"totalSkills":total_sk,"newPositions":new_count,"pendingAudit":audit_count,"qualityScore":q_score,"newPositions":new_positions,"qualitySummary":INSIGHTS_QUALITY}}
    except Exception as e:
        print(f"[INFO] Overview DB unavailable: {e}")
        return {"ok":True, "data":{
            "totalPositions":20,"totalSkills":35,"newPositions":3,"pendingAudit":4,
            "qualityScore":INSIGHTS_QUALITY["overall_score"],
            "qualitySummary":INSIGHTS_QUALITY,
            "newPositions":INSIGHTS_NEW_POSITIONS,
        }}

def _generate_skill_trends(position_name, periods):
    based_skills = {
        "前端":["JavaScript","React","CSS","TypeScript","Vue"],
        "后端":["Java","Python","Go","MySQL","Redis"],
        "大模型":["Python","PyTorch","Transformer","NLP","BERT"],
        "安全":["Python","C","Linux","Web安全","渗透"],
        "数据":["Python","SQL","Spark","机器学习","统计"],
        "产品":["需求分析","Axure","用户研究","数据分析","协调"],
        "DevOps":["Docker","Kubernetes","Jenkins","Linux","Ansible"],
        "测试":["Python","Selenium","JMeter","自动化","Linux"],
        "推荐":["Python","TensorFlow","Spark","推荐系统","机器学习"],
        "NLP":["Python","PyTorch","BERT","Transformer","NLP"],
        "视觉":["Python","PyTorch","OpenCV","图像分类","目标检测"],
        "全栈":["JavaScript","Python","React","Node.js","MySQL"],
        "数据分析":["Python","SQL","Excel","Tableau","统计"],
        "工程师":["Python","Docker","Linux","Git","CI/CD"],
    }
    skills = {}
    for key, sk_list in based_skills.items():
        if key in position_name:
            for s in sk_list[:4]:
                base = 30 + abs(hash(s + position_name)) % 50
                freq = []
                for i in range(6):
                    freq.append(base + i * (abs(hash(s)) % 8 - 3) + (abs(hash(position_name + str(i))) % 15))
                    if freq[-1] < 0: freq[-1] = 0
                change = "rising" if freq[-1] > freq[0] else "declining" if freq[-1] < freq[0] * 0.5 else "stable"
                pct = f"+{int((freq[-1]-freq[0])/freq[0]*100) if freq[0] > 0 else 0}%" if freq[-1] > freq[0] else f"{int((freq[-1]-freq[0])/freq[0]*100) if freq[0] > 0 else 0}%"
                skills[s] = {"frequency": freq, "change": change, "pct": pct}
    if not skills:
        base = 40
        for s in ["Python", "Linux", "Docker", "Git", "SQL"]:
            skills[s] = {"frequency": [base, base+2, base+5, base+3, base+8, base+10], "change": "rising", "pct": "+25%"}
            base -= 5
    return {"periods": periods, "skills": skills}

@app.get("/api/insights/skills-trend")
async def skills_trend(position: str = ""):
    if position and position in INSIGHTS_SKILL_TRENDS:
        data = INSIGHTS_SKILL_TRENDS[position]
    else:
        data = _generate_skill_trends(position, ["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"])
    return {"ok":True, "data":_snake_to_camel(data)}

@app.get("/api/insights/positions")
async def list_insights_positions():
    try:
        from agents.agent2.nlp_profile.profile_store import ProfileStore
        store = ProfileStore()
        db = store.client[store.db.name]
        items = sorted(db["jobs_deduplicated"].distinct("title"))
        
        
        store.close()
        if items: return {"ok":True, "data": items}
    except: pass
    return {"ok":True, "data": ["大模型算法工程师","数据科学家","云原生开发工程师","前端开发工程师","后端开发工程师","安全工程师","NLP算法工程师","推荐算法工程师","计算机视觉工程师","数据分析师","数据工程师","产品经理","测试开发工程师","DevOps工程师","Go后端开发","Java后端开发","全栈工程师"]}

@app.get("/api/insights/new-positions")
async def list_new_positions():
    return {"ok":True, "data":_snake_to_camel(INSIGHTS_NEW_POSITIONS)}

@app.post("/api/insights/new-positions/{action}")
async def handle_new_position(action: str, position_id: str = "", decision: str = ""):
    pid = position_id or "np-001"
    item = AUDIT_NEW_POSITIONS_STORE.get(pid)
    if not item:
        return {"ok":False,"error":"not found"}
    if action == "confirm":
        if AGENT3_AVAILABLE:
            try:
                from agents.agent2.nlp_profile.profile_store import ProfileStore
                store = ProfileStore()
                sp = {"name":item["name"],"description":item["description"],
                       "required_skills":item["requiredSkills"],"type":"position"}
                store.save_profile(sp)
                store.close()
            except:
                pass
        item["status"] = "confirmed"
        return {"ok":True,"data":{"id":pid,"status":"confirmed"}}
    elif action == "dismiss":
        item["status"] = "dismissed"
        return {"ok":True,"data":{"id":pid,"status":"dismissed"}}
    return {"ok":False,"error":"invalid action"}

@app.post("/api/insights/run-discovery")
async def run_discovery():
    agent1_result = _call_agent1_discovery()
    agent2_quality = _call_agent2_quality()
    agent2_validate = None
    if agent1_result and agent1_result.get("new_positions_found", 0) > 0:
        pos_names = []
        for p in agent1_result.get("new_positions", []):
            pass
        try:
            from agents.agent2.nlp_profile.profile_store import ProfileStore
            store = ProfileStore()
            db = store.client[store.db.name]
            pending = list(db["agent1_output"].find({"output_type":"new_position","status":"pending"}).limit(5))
            pos_data = []
            for p in pending:
                pd = p.get("payload", {})
                name = pd.get("suggested_name", "")
                skills = pd.get("suggested_required_skills", [])
                if name and skills:
                    pos_data.append({"name":name,"requiredSkills":skills})
            store.close()
            if pos_data:
                agent2_validate = _call_agent2_validate(pos_data)
        except Exception as e:
            print(f"[INFO] Skipping Agent2 validate: {e}")
    q_score = agent2_quality.get("overall_score", 86) if isinstance(agent2_quality, dict) else 86
    a1_summary = agent1_result or {"new_positions_found":0,"skill_changes_detected":0}
    return {"ok":True,"data":_snake_to_camel({
        "status":"completed","summary":{
            "newPositions":a1_summary.get("new_positions_found",0),
            "skillChanges":a1_summary.get("skill_changes_detected",0),
            "qualityScore":round(q_score * 100) if q_score < 1 else q_score,
            "pendingAudit":len(agent2_validate.get("items",[])) if agent2_validate else 0,
        },"agent1Available":agent1_result is not None,
         "agent2Available":agent2_quality is not None,
    })}

@app.get("/api/insights/quality")
async def quality_summary():
    return {"ok":True,"data":_snake_to_camel(INSIGHTS_QUALITY)}

@app.get("/api/insights/audit")
async def list_audit():
    items = sorted(AUDIT_STORE.values(), key=lambda x: x["confidence"])
    return {"ok":True,"data":_snake_to_camel(items)}

@app.post("/api/insights/audit/{action}")
async def handle_audit(action: str, audit_id: str = ""):
    aid = audit_id or "aq-001"
    item = AUDIT_STORE.get(aid)
    if not item:
        return {"ok":False,"error":"not found"}
    if action == "approve":
        item["status"] = "approved"
    elif action == "reject":
        item["status"] = "rejected"
    return {"ok":True,"data":{"id":aid,"status":item["status"]}}
@app.get("/api/insights/audit-queue")
async def list_audit_queue():
    try:
        from agents.agent2.nlp_profile.profile_store import ProfileStore
        store = ProfileStore()
        db = store.client[store.db.name]
        items = list(db["audit_queue"].find({"status":"pending"}).sort("confidence", 1))
        result = []
        for item in items:
            result.append({"id":str(item["_id"]),"sourceName":item.get("source_name",""),"sourceType":item.get("source_type",""),"targetName":item.get("target_name",""),"targetType":item.get("target_type",""),"relationType":item.get("relation_type",""),"confidence":item.get("confidence",0),"explanation":item.get("explanation",""),"evidence":item.get("evidence",[]),"counterEvidence":item.get("counter_evidence",[]),"recommendation":item.get("recommendation",""),"status":item.get("status","pending")})
        store.close()
        return {"ok":True,"data":result}
    except Exception as e:
        print(f"[INFO] Audit queue unavailable: {e}")
        return {"ok":False,"data":[],"error":str(e)}

@app.post("/api/insights/audit-queue/approve")
async def approve_audit_item(id: str = ""):
    if not id: return {"ok":False,"error":"missing id"}
    try:
        from bson import ObjectId
        from agents.agent2.nlp_profile.profile_store import ProfileStore
        store = ProfileStore()
        db = store.client[store.db.name]
        item = db["audit_queue"].find_one({"_id":ObjectId(id)})
        if not item: store.close(); return {"ok":False,"error":"not found"}
        db["jobs_kg"].insert_one({"relation_id":item.get("relation_id",""),"source_type":item.get("source_type",""),"source_id":item.get("source_id",""),"source_name":item.get("source_name",""),"target_type":item.get("target_type",""),"target_id":item.get("target_id",""),"target_name":item.get("target_name",""),"relation_type":item.get("relation_type",""),"confidence":item.get("confidence",0),"explanation":item.get("explanation",""),"source":"agent2_audit","created_at":item.get("created_at","")})
        db["audit_queue"].delete_one({"_id":ObjectId(id)})
        remaining = db["audit_queue"].count_documents({"status":"pending"})
        store.close()
        return {"ok":True,"data":{"remaining":remaining}}
    except Exception as e:
        print(f"[INFO] Approve audit item failed: {e}")
        return {"ok":False,"error":str(e)}
if __name__ == "__main__":
    port = int(os.environ.get("API_PORT", 8720))
    print(f"Agent3 API Server on http://0.0.0.0:{port}, available={AGENT3_AVAILABLE}")
    uvicorn.run(app, host="0.0.0.0", port=port)

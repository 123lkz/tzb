import pymongo
c = pymongo.MongoClient('mongodb://localhost:27017')
d = c['recruitment']

print('=== 技能画像 ===')
for s in d['nlp_profiles'].find({'type':'skill'}):
    print(f'  [{s["skill_id"]}] {s["name"]}')
    print(f'    摘要: {s["summary"][:80]}...')
    print(f'    前置知识: {s.get("prerequisites",[])}')
    print(f'    相关技术: {s.get("related_technologies",[])}')
    print()

print('=== 岗位画像 ===')
for p in d['nlp_profiles'].find({'type':'position'}):
    print(f'  [{p["position_id"]}] {p["name"]}')
    print(f'    摘要: {p["summary"][:80]}...')
    print(f'    必需技能: {p.get("required_skills",[])}')
    print(f'    核心职责: {p.get("core_responsibilities",[])}')
    print()

print('=== 关系画像（前5条）===')
for r in d['relation_profiles'].find().limit(5):
    print(f'  {r["source_name"]} -> {r["target_name"]}')
    print(f'    valid={r["valid"]}  confidence={r["confidence"]}')
    print(f'    理由: {r["explanation"][:80]}...')
    print()

print('=== 审核队列 ===')
for a in d['audit_queue'].find().limit(3):
    print(f'  {a.get("source_name","?")} -> {a.get("target_name","?")} (status: {a.get("status","?")})')
    print()

c.close()
print('完成!')

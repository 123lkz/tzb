import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.agent2.nlp_profile.profile_store import ProfileStore

store = ProfileStore()
db = store.client[store.db.name]
col = db["agent1_output"]

print("=== 清理前 ===")
total = col.count_documents({})
print(f"agent1_output 总记录: {total}")

# Dedup new positions by suggested_name
groups = {}
for r in col.find({"output_type":"new_position"}):
    name = r.get("payload",{}).get("suggested_name","unknown")
    tid = str(r["_id"])
    created = r.get("created_at","")
    if name not in groups or created > groups[name][0]:
        groups[name] = [created, tid]

keep_ids = {v[1] for v in groups.values()}
deleted_count = 0
to_delete_ids = []
for r in col.find({"output_type":"new_position"},{"_id":1}):
    rid = str(r["_id"])
    if rid not in keep_ids:
        to_delete_ids.append(r["_id"])
        deleted_count += 1

batch = []
for rid in to_delete_ids:
    batch.append(rid)
    if len(batch) >= 50:
        col.delete_many({"_id":{"$in":batch}})
        batch = []
if batch:
    col.delete_many({"_id":{"$in":batch}})

print(f"新岗位: 唯一 {len(groups)} 个, 删除 {deleted_count} 条重复")

# Dedup skill changes
groups2 = {}
for r in col.find({"output_type":"skill_change"}):
    pos = r.get("payload",{}).get("position_name","")
    skill = r.get("payload",{}).get("skill_name","")
    ctype = r.get("payload",{}).get("change_type","")
    key = pos + "|" + skill + "|" + ctype
    tid = str(r["_id"])
    created = r.get("created_at","")
    if key not in groups2 or created > groups2[key][0]:
        groups2[key] = [created, tid]

keep_ids2 = {v[1] for v in groups2.values()}
del2 = 0
for r in col.find({"output_type":"skill_change"},{"_id":1}):
    if str(r["_id"]) not in keep_ids2:
        col.delete_one({"_id":r["_id"]})
        del2 += 1
print(f"技能变化: 唯一 {len(groups2)} 个, 删除 {del2} 条重复")

print(f"\n=== 清理后 ===")
print(f"agent1_output 总记录: {col.count_documents({})}")
store.close()

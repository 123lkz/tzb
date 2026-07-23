import sys, os
sys.path.insert(0, os.path.dirname(os.getcwd()))
from agents.agent2.nlp_profile.profile_store import ProfileStore
store = ProfileStore()
db = store.client[store.db.name]
print("=" * 60)
print("MongoDB \u6570\u636e\u53bb\u91cd\u6e05\u7406")
print("=" * 60)
RULES = {
    "agent1_output": {"key":["output_type","payload.suggested_name"],"desc":"Agent1\u5206\u6790\u7ed3\u679c"},
    "nlp_profiles": {"key":["name","type"],"desc":"\u5c97\u4f4d/\u6280\u80fd\u753b\u50cf"},
    "audit_queue": {"key":["source_name","target_name"],"desc":"\u5f85\u5ba1\u6838\u5173\u7cfb"},
    "relation_profiles": {"key":["source_name","target_name"],"desc":"\u5173\u7cfb\u753b\u50cf"},
    "quality_reports": {"key":["record_id"],"desc":"\u8d28\u91cf\u62a5\u544a"},
}
total_del = 0
for cname, rule in RULES.items():
    if cname not in db.list_collection_names(): continue
    col = db[cname]
    total = col.count_documents({})
    groups = {}
    for r in col.find({}):
        parts = []
        for f in rule["key"]:
            val = r
            for k in f.split("."):
                if isinstance(val, dict): val = val.get(k, "")
                else: val = ""; break
            parts.append(str(val))
        key = "|".join(parts)
        rid = r["_id"]
        created = r.get("created_at", "")
        if key not in groups or created > groups[key][0]:
            groups[key] = [created, rid]
    keep = set(str(v[1]) for v in groups.values())
    todel = [r["_id"] for r in col.find({},{"_id":1}) if str(r["_id"]) not in keep]
    if todel:
        for i in range(0, len(todel), 50):
            col.delete_many({"_id":{"$in":todel[i:i+50]}})
    td = len(todel)
    total_del += td
    m = "\\u2714 \\u65e0\\u91cd\\u590d" if td == 0 else "\\u2757 \\u6709\\u91cd\\u590d"
    print(f"  {cname} ({rule["desc"]}): {total} \u6761 -> \u552f\u4e00{len(groups)} -{td} {m}")
store.close()
print(f"\\n\\u5b8c\\u6210\\uff0c\\u5171\\u5220\\u9664 {total_del} \\u6761\\u91cd\\u590d")
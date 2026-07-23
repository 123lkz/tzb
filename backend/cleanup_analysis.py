import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.agent2.nlp_profile.profile_store import ProfileStore

def clean_audit_queue(db, keep=20):
    total = db['audit_queue'].count_documents({})
    if total <= keep:
        print(f'  audit_queue: {total} items, no cleanup needed')
        return 0
    kept = list(db['audit_queue'].find().sort('_id', -1).limit(keep))
    db['audit_queue'].drop()
    db['audit_queue'].insert_many(kept)
    removed = total - keep
    print(f'  audit_queue: removed {removed}, kept {keep} (was {total})')
    return removed

def clean_quality_reports(db, keep=1):
    total = db['quality_reports'].count_documents({})
    if total <= keep:
        print(f'  quality_reports: {total} items, no cleanup needed')
        return 0
    kept = list(db['quality_reports'].find().sort('overall_score', -1).sort('_id', -1).limit(keep))
    db['quality_reports'].drop()
    db['quality_reports'].insert_many(kept)
    removed = total - keep
    print(f'  quality_reports: removed {removed}, kept {keep} (was {total})')
    return removed

def main():
    print('=== Database Cleanup ===')
    store = ProfileStore()
    db = store.client[store.db.name]
    clean_audit_queue(db, keep=20)
    clean_quality_reports(db, keep=1)
    store.close()
    print('=== Done ===')

if __name__ == '__main__':
    main()

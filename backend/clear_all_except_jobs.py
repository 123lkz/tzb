import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.agent2.nlp_profile.profile_store import ProfileStore

KEEP_COLLECTIONS = {'jobs_clean'}

def main():
    store = ProfileStore()
    db = store.client[store.db.name]
    
    all_cols = set(db.list_collection_names())
    to_drop = sorted(all_cols - KEEP_COLLECTIONS)
    
    print('=' * 50)
    print('数据库清理预览')
    print('=' * 50)
    print(f'保留的集合: {", ".join(sorted(KEEP_COLLECTIONS))}')
    print()
    print(f'将被清空的集合 ({len(to_drop)} 个):')
    for c in to_drop:
        cnt = db[c].count_documents({})
        print(f'  - {c} ({cnt} 条)')
    
    print()
    confirm = input('确认删除以上所有集合的数据？(yes/no): ')
    if confirm.lower() != 'yes':
        print('已取消')
        store.close()
        return
    
    for c in to_drop:
        cnt = db[c].count_documents({})
        db[c].drop()
        print(f'  [x] {c}: 已删除 ({cnt} 条)')
    
    store.close()
    print()
    print('清理完成！')

if __name__ == '__main__':
    main()

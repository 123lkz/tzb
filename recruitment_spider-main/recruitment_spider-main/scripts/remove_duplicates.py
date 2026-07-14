import json
from typing import Dict, List, Any

def remove_duplicates(data: Dict[str, Any], seen_codes: set = None) -> Dict[str, Any]:
    """
    递归处理JSON数据，移除所有层级的重复职位信息
    """
    if seen_codes is None:
        seen_codes = set()
    if not isinstance(data, dict):
        return data
    
    # 处理position列表
    if 'zpData' in data and 'position' in data['zpData']:
        positions = data['zpData']['position']
        unique_positions = []
        for pos in positions:
            if pos['code'] not in seen_codes:
                seen_codes.add(pos['code'])
                # 递归处理子列表
                if 'subLevelModelList' in pos and pos['subLevelModelList']:
                    pos['subLevelModelList'] = remove_duplicates_from_list(pos['subLevelModelList'], seen_codes)
                unique_positions.append(pos)
        data['zpData']['position'] = unique_positions
    return data

def remove_duplicates_from_list(items: List[Dict[str, Any]], seen_codes: set) -> List[Dict[str, Any]]:
    """
    处理列表中的重复项，所有层级共享同一个seen_codes集合
    """
    unique_items = []
    for item in items:
        if item['code'] not in seen_codes:
            seen_codes.add(item['code'])
            # 递归处理子列表
            if 'subLevelModelList' in item and item['subLevelModelList']:
                item['subLevelModelList'] = remove_duplicates_from_list(item['subLevelModelList'], seen_codes)
            unique_items.append(item)
    return unique_items

def main():
    # 读取原始JSON文件
    input_file = 'job_type.json'
    output_file = 'job_type_unique.json'
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 处理重复数据
        cleaned_data = remove_duplicates(data)
        # 保存处理后的数据
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
        print(f"处理完成！结果已保存到 {output_file}")
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")

if __name__ == '__main__':
    main() 
import re
import json
import os

file_path = "KetQuaWeKaTxt/fpGData"
# Hàm xử lý file TXT kết quả từ Weka và chuyển đổi thành JSON
def parse_weka_output(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    rules = []
    rule_pattern = r'(.+): (\d+) ==> \[(.+)\]: (\d+)\s+<conf:\(([\d.]+)\)> lift:\(([\d.]+)\) lev:\(([\d.]+)\) conv:\(([\d.]+)\)'

    # Lặp qua các dòng và tìm luật kết hợp
    for line in lines:
        match = re.match(rule_pattern, line.strip())
        if match:
            condition = match.group(1).strip()
            condition_support = int(match.group(2).strip())
            result = match.group(3).strip()
            result_support = int(match.group(4).strip())
            confidence = float(match.group(5).strip())
            lift = float(match.group(6).strip())
            leverage = float(match.group(7).strip())
            conviction = float(match.group(8).strip())

            # Tạo cấu trúc JSON cho từng luật
            rule = {
                'condition': condition,
                'condition_support': condition_support,
                'result': result,
                'result_support': result_support,
                'confidence': confidence,
                'lift': lift,
                'leverage': leverage,
                'conviction': conviction
            }
            rules.append(rule)

    return rules


# Hàm lưu dữ liệu JSON vào project
def save_rules_to_json(rules, output_dir, output_file):
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)

    # Đường dẫn đầy đủ đến file JSON
    output_path = os.path.join(output_dir, output_file)

    # Lưu dữ liệu ra file JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(rules, f, indent=4, ensure_ascii=False)

    print(f"Dữ liệu đã được lưu vào {output_path}")


# Đường dẫn tới file kết quả Weka (TXT)
weka_file_path = "weka_output.txt"

# Đường dẫn thư mục project để lưu file JSON
output_directory = "data"

# Tên file JSON muốn lưu
output_filename = "association_rules.json"

# Bước 1: Phân tích file TXT và chuyển thành JSON
parsed_rules = parse_weka_output(file_path)

# Bước 2: Lưu kết quả JSON vào project
save_rules_to_json(parsed_rules, output_directory, output_filename)

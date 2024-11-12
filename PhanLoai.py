import os
import json


# Hàm phân tích file Weka và chuyển đổi dữ liệu thành JSON
def parse_weka_output(file_path):
    categories = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        start_collecting = False

        for line in lines:
            # Xác định điểm bắt đầu thu thập phân loại hàng
            if "Attributes:" in line:
                start_collecting = True
                continue

            # Thoát khỏi vòng lặp khi tới phần === Associator model ===
            if "=== Associator model" in line:
                break

            # Thêm phân loại hàng vào danh sách
            if start_collecting:
                category = line.strip()
                if category:  # Bỏ qua dòng trống
                    categories.append(category)

    return categories


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
weka_file_path = "KetQuaWeKaTxt/fpGData"

# Đường dẫn thư mục project để lưu file JSON
output_directory = "data"

# Tên file JSON muốn lưu
output_filename = "phanloai.json"

# Bước 1: Phân tích file TXT và chuyển thành JSON
parsed_rules = parse_weka_output(weka_file_path)

# Bước 2: Lưu kết quả JSON vào project
save_rules_to_json(parsed_rules, output_directory, output_filename)

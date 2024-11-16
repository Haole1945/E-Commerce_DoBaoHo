# import csv
# from pymongo import MongoClient

# def export_interactions_to_csv(csv_file_path):
#     # Kết nối tới MongoDB
#     client = MongoClient("mongodb://localhost:27017/ecommerce")
#     db = client["ecommerce"]  # Thay "your_database_name" bằng tên database của bạn
#     collection = db["interactions"]   # Tên collection, khớp với schema Interaction

#     # Lấy dữ liệu từ MongoDB
#     interactions = collection.find({}, {"user_id": 1, "product_id": 1, "action": 1, "_id": 0})

#     # Ghi dữ liệu vào CSV
#     with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         # Ghi tiêu đề cột
#         writer.writerow(["user_id", "product_id", "action"])
#         # Ghi dữ liệu
#         for interaction in interactions:
#             writer.writerow([interaction["user_id"], interaction["product_id"], interaction["action"]])

#     print(f"Dữ liệu đã được xuất thành công tới {csv_file_path}")

# if __name__ == "__main__":
#     csv_path = "D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/interactions_data.csv"  # Đường dẫn tới file CSV
#     export_interactions_to_csv(csv_path)

# import csv
# from pymongo import MongoClient

# def export_interactions_to_csv(csv_file_path):
#     # Kết nối tới MongoDB
#     client = MongoClient("mongodb://localhost:27017/ecommerce")
#     db = client["ecommerce"]  # Thay "your_database_name" bằng tên database của bạn
#     collection = db["interactions"]   # Tên collection, khớp với schema Interaction

#     # Lấy dữ liệu từ MongoDB
#     interactions = collection.find({}, {"user_id": 1, "product_id": 1, "action": 1, "_id": 0})

#     # Tạo từ điển để lưu trữ giá trị đã mã hóa
#     user_id_map = {}
#     product_id_map = {}
#     action_map = {}

#     # Mã hóa các giá trị
#     def encode_value(value, value_map):
#         """Mã hóa giá trị, nếu chưa mã hóa thì thêm vào từ điển và trả lại giá trị mã hóa."""
#         if value not in value_map:
#             value_map[value] = len(value_map) + 1  # Bắt đầu từ 1 để mã hóa
#         return value_map[value]

#     # Ghi dữ liệu vào CSV
#     with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         # Ghi tiêu đề cột
#         writer.writerow(["user_id", "product_id", "action"])

#         # Ghi dữ liệu
#         for interaction in interactions:
#             encoded_user_id = encode_value(interaction["user_id"], user_id_map)
#             encoded_product_id = encode_value(interaction["product_id"], product_id_map)
#             encoded_action = encode_value(interaction["action"], action_map)
            
#             writer.writerow([encoded_user_id, encoded_product_id, encoded_action])

#     # Lưu lại từ điển mã hóa vào một file để sử dụng lại sau
#     with open("D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/Encoded_map/user_id_map.csv", mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(["user_id", "encoded_user_id"])
#         for user, encoded_user in user_id_map.items():
#             writer.writerow([user, encoded_user])

#     with open("D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/Encoded_map/product_id_map.csv", mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(["product_id", "encoded_product_id"])
#         for product, encoded_product in product_id_map.items():
#             writer.writerow([product, encoded_product])

#     with open("D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/Encoded_map/action_map.csv", mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(["action", "encoded_action"])
#         for action, encoded_action in action_map.items():
#             writer.writerow([action, encoded_action])

#     print(f"Dữ liệu đã được xuất thành công tới {csv_file_path}")
#     print("Các từ điển mã hóa đã được lưu vào các file 'user_id_map.csv', 'product_id_map.csv', 'action_map.csv'")

# if __name__ == "__main__":
#     csv_path = "D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/interactions_data.csv"  # Đường dẫn tới file CSV
#     export_interactions_to_csv(csv_path)

import csv
from pymongo import MongoClient

def load_product_id_map(encoded_map_dir):
    """Hàm tải file mã hóa product_id từ thư mục đã chỉ định"""
    product_id_map = {}
    try:
        with open(f"{encoded_map_dir}/product_id_map.csv", mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Bỏ qua tiêu đề cột
            for row in reader:
                product_id_map[row[0]] = int(row[1])
    except FileNotFoundError:
        print(f"File {encoded_map_dir}/product_id_map.csv không tồn tại.")
    return product_id_map

def export_interactions_to_csv(csv_file_path, encoded_map_dir):
    # Kết nối tới MongoDB
    client = MongoClient("mongodb://localhost:27017/ecommerce")
    db = client["ecommerce"]  # Thay "your_database_name" bằng tên database của bạn
    collection = db["interactions"]   # Tên collection, khớp với schema Interaction

    # Lấy dữ liệu từ MongoDB
    interactions = collection.find({}, {"user_id": 1, "product_id": 1, "action": 1, "_id": 0})

    # Mã hóa các trường user_id, action
    user_id_map = {}
    action_map = {}

    user_counter = 0
    action_counter = 0

    # Mã hóa product_id từ file product_id_map.csv
    product_id_map = load_product_id_map(encoded_map_dir)

    # Mở file CSV để ghi
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Ghi tiêu đề cột
        writer.writerow(["user_id", "product_id", "action"])

        # Duyệt qua các tương tác để mã hóa và ghi vào CSV
        for interaction in interactions:
            # Mã hóa user_id
            user_id = interaction["user_id"]
            if user_id not in user_id_map:
                user_id_map[user_id] = user_counter
                user_counter += 1

            # Mã hóa action
            action = interaction["action"]
            if action not in action_map:
                action_map[action] = action_counter
                action_counter += 1

            # Mã hóa product_id (dựa trên product_id_map)
            product_id = interaction["product_id"]
            encoded_product_id = product_id_map.get(str(product_id), -1)  # Nếu không tìm thấy mã hóa thì gán -1

            # Ghi vào file CSV
            writer.writerow([user_id_map[user_id], encoded_product_id, action_map.get(action, -1)])

    # Lưu các bản đồ mã hóa vào các file CSV
    with open(f"{encoded_map_dir}/user_id_map.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "encoded_id"])
        for user_id, encoded_id in user_id_map.items():
            writer.writerow([user_id, encoded_id])

    with open(f"{encoded_map_dir}/action_map.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["action", "encoded_id"])
        for action, encoded_id in action_map.items():
            writer.writerow([action, encoded_id])

    print(f"Dữ liệu đã được xuất thành công tới {csv_file_path}")
    print(f"Các bản đồ mã hóa đã được lưu vào {encoded_map_dir}")

def run_export_interact():
    csv_path = "D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/interactions_data.csv"  # Đường dẫn tới file CSV
    encoded_map_dir = "D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/encoded_map"  # Đường dẫn tới thư mục lưu các bản đồ mã hóa
    export_interactions_to_csv(csv_path, encoded_map_dir)

if __name__ == "__main__":
    csv_path = "D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/interactions_data.csv"  # Đường dẫn tới file CSV
    encoded_map_dir = "D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/encoded_map"  # Đường dẫn tới thư mục lưu các bản đồ mã hóa
    export_interactions_to_csv(csv_path, encoded_map_dir)
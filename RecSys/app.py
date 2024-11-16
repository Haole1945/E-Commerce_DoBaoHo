# from flask import Flask, request, jsonify
# from models.recommend import combined_recommendation
# from Utils.delete_training_model import delete_csv_files
# from data.export_interactions import run_export_interact
# from data.export_product_data import run_export_product_data
# from Utils.user_id_mapper import get_encoded_id
# import pandas as pd
# from Utils.Create_dic_encoded import get_product_id_mapping
# from flask_cors import CORS
# from pymongo import MongoClient
# from bson.objectid import ObjectId

# # Khởi tạo Flask app
# app = Flask(__name__)
# CORS(app)

# client = MongoClient('mongodb://localhost:27017/ecommerce')
# db = client['ecommerce']
# products_collection = db['products']

# @app.route('/recommend', methods=['GET'])
# def recommend():
#     # Lấy user_id từ request
#     user_id = request.args.get('user_id')

#     try:
#         # Lấy encoded_id từ user_id
#         encoded_id = get_encoded_id(user_id)
#         encoded_id = int(encoded_id)
#         print(f"Encoded ID for {user_id} is {encoded_id}")
#     except ValueError as e:
#         print(e)

#     # Lấy các đề xuất từ KNN và Content-Based Filtering
#     recommendations = combined_recommendation(encoded_id, k=5)
    
#     # Lấy ánh xạ từ encoded_id -> product_id
#     encoded_to_product = get_product_id_mapping()

#     # Chuyển đổi danh sách encoded_id thành product_id
#     product_recommendations = [encoded_to_product[encoded_id] for encoded_id in recommendations]

#     products = list(products_collection.find({"_id": {"$in": [ObjectId(pid) for pid in product_recommendations]}}))
    
#     # Chuyển đổi ObjectId thành chuỗi
#     for product in products:
#         product['_id'] = str(product['_id'])

#     return jsonify(products)

# if __name__ == "__main__":
#     delete_csv_files()
#     run_export_product_data()
#     run_export_interact()
#     app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, request
from models.recommend import combined_recommendation
from Utils.delete_training_model import delete_csv_files
from data.export_interactions import run_export_interact
from data.export_product_data import run_export_product_data
from Utils.user_id_mapper import get_encoded_id
from Utils.Create_dic_encoded import get_product_id_mapping
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

# Khởi tạo Flask app
app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/ecommerce')
db = client['ecommerce']
products_collection = db['products']

@app.route('/recommend', methods=['GET'])
def recommend():
    # Lấy user_id từ request
    user_id = request.args.get('user_id')

    try:
        # Lấy encoded_id từ user_id
        encoded_id = get_encoded_id(user_id)
        encoded_id = int(encoded_id)
        print(f"Encoded ID for {user_id} is {encoded_id}")
    except ValueError as e:
        print(e)
        return {"error": "Invalid user_id"}, 400

    # Lấy các đề xuất từ KNN và Content-Based Filtering
    recommendations = combined_recommendation(encoded_id, k=5)
    
    # Lấy ánh xạ từ encoded_id -> product_id
    encoded_to_product = get_product_id_mapping()

    # Chuyển đổi danh sách encoded_id thành product_id
    product_recommendations = [encoded_to_product[encoded_id] for encoded_id in recommendations]

    # Truy vấn MongoDB
    products = list(products_collection.find({"_id": {"$in": [ObjectId(pid) for pid in product_recommendations]}}))
    
    # Sử dụng bson.json_util.dumps để tuần tự hóa
    return dumps(products), 200

if __name__ == "__main__":
    delete_csv_files()
    run_export_product_data()
    run_export_interact()
    app.run(debug=True, host='0.0.0.0', port=5000)

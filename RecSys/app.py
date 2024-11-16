from flask import Flask, request, jsonify
from models.recommend import combined_recommendation
from Utils.delete_training_model import delete_csv_files
from data.export_interactions import run_export_interact
from data.export_product_data import run_export_product_data
from Utils.user_id_mapper import get_encoded_id  

# Khởi tạo Flask app
app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommend():
    # Lấy user_id từ request
    user_id = request.args.get('user_id')

    try:
        encoded_id = get_encoded_id(user_id)
        encoded_id = int(encoded_id)
        print(f"Encoded ID for {user_id} is {encoded_id}")
    except ValueError as e:
        print(e)

    # Lấy các đề xuất từ KNN và Content-Based Filtering
    recommendations = combined_recommendation(encoded_id, k=5)
    return jsonify(recommendations)

if __name__ == "__main__":
    delete_csv_files()
    run_export_product_data()
    run_export_interact()
    app.run(debug=True, host='0.0.0.0', port=5000)

# import pandas as pd
# from sklearn.neighbors import NearestNeighbors
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfVectorizer

# # Đường dẫn tới dữ liệu
# PRODUCT_CSV_PATH = "D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/product_data.csv"
# INTERACTIONS_CSV_PATH = "D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/interactions_data.csv"


# def load_data():
#     """Tải dữ liệu từ CSV."""
#     product_data = pd.read_csv(PRODUCT_CSV_PATH)
#     interaction_data = pd.read_csv(INTERACTIONS_CSV_PATH)
#     return product_data, interaction_data


# def get_knn_recommendations(user_id, interaction_data, k=5):
#     """Đề xuất sản phẩm đã tương tác dựa trên KNN."""
#     user_interactions = interaction_data[interaction_data['user_id'] == user_id]
#     interacted_product_ids = user_interactions['product_id'].tolist()

#     if not interacted_product_ids:
#         return []  # Người dùng chưa tương tác sản phẩm nào

#     # Xếp hạng các hành động của người dùng theo độ ưu tiên
#     action_priority = {0: 1, 1: 2, 2: 4, 3: 3}  # view, add_to_cart, purchase, wish_list
#     user_interactions = user_interactions.copy()
#     user_interactions['priority'] = user_interactions['action'].map(action_priority)

#     # Sắp xếp theo độ ưu tiên
#     user_interactions = user_interactions.sort_values(by='priority', ascending=False)

#     # Kết hợp dữ liệu từ interaction_data và product_data theo cột product_id
#     product_features = pd.merge(
#         interaction_data[interaction_data['product_id'].isin(interacted_product_ids)],
#         product_data[['product_id', 'category', 'brand']],
#         on='product_id', 
#         how='left'
#     )

#     product_features = product_features[['product_id', 'action', 'category', 'brand']]
    
#     # Tạo ma trận one-hot encoding
#     product_features_dummies = pd.get_dummies(product_features, columns=['action', 'category', 'brand'], drop_first=True)

#     # Lưu danh sách các cột đặc trưng
#     feature_columns = product_features_dummies.columns.drop('product_id')

#     # Huấn luyện mô hình KNN
#     knn_model = NearestNeighbors(n_neighbors=k, metric='cosine')
#     knn_model.fit(product_features_dummies[feature_columns])  # Huấn luyện mô hình

#     indices = []
#     for _, row in product_features_dummies.iterrows():
#         # Đảm bảo dữ liệu đầu vào có cùng cột như dữ liệu huấn luyện
#         product_vector = row[feature_columns].values.reshape(1, -1)
#         _, neighbor_indices = knn_model.kneighbors(product_vector)
#         indices.extend(neighbor_indices.flatten())

#     # Lấy product_id từ chỉ số
#     recommended_products = interaction_data.iloc[indices]['product_id'].tolist()
#     return list(set(recommended_products) - set(interacted_product_ids))


# def get_content_based_recommendations(user_id, product_data, interaction_data, top_n=5):
#     """Đề xuất sản phẩm chưa tương tác dựa trên Content-Based Filtering."""
#     user_interactions = interaction_data[interaction_data['user_id'] == user_id]
#     interacted_product_ids = user_interactions['product_id'].tolist()

#     # Lọc sản phẩm chưa được tương tác
#     unseen_products = product_data[~product_data['product_id'].isin(interacted_product_ids)]
#     if unseen_products.empty:
#         return []  # Không có sản phẩm nào chưa được tương tác

#     # Tạo đặc trưng từ category và brand
#     unseen_products['category'] = unseen_products['category'].astype(str)
#     unseen_products['brand'] = unseen_products['brand'].astype(str)

#     # print("Unseen products:", unseen_products)
#     # print("Category column:", unseen_products['category'].unique())
#     # print("Brand column:", unseen_products['brand'].unique())

    
#     product_features = unseen_products[['category', 'brand']].apply(lambda x: ' '.join(x), axis=1)

#     # Chuyển thành ma trận tf-idf
#     tfidf_vectorizer = TfidfVectorizer(stop_words=None)
#     tfidf_matrix = tfidf_vectorizer.fit_transform(product_features)

#     print("TF-IDF Matrix Shape:", tfidf_matrix.shape)
#     print("TF-IDF Feature Names:", tfidf_vectorizer.get_feature_names_out())


#     # Tính toán độ tương đồng cosine giữa các sản phẩm
#     cosine_sim = cosine_similarity(tfidf_matrix)
    
#     # Lấy các sản phẩm tương đồng nhất
#     mean_similarities = cosine_sim.mean(axis=1)
#     top_indices = mean_similarities.argsort()[-top_n:][::-1]  # Chọn sản phẩm có độ tương đồng cao nhất
#     recommended_products = unseen_products.iloc[top_indices]['product_id'].tolist()

#     return recommended_products


# def combine_recommendations(knn_recommendations, content_based_recommendations):
#     """Kết hợp danh sách đề xuất từ KNN và Content-Based Filtering."""
#     return list(set(knn_recommendations + content_based_recommendations))


# if __name__ == "__main__":
#     # Load dữ liệu
#     product_data, interaction_data = load_data()

#     # Nhập user_id để kiểm tra
#     user_id = 0  # Thay thế bằng user_id thật khi sử dụng

#     # Kết hợp đề xuất từ KNN và Content-Based Filtering
#     knn_results = get_knn_recommendations(user_id, interaction_data)
#     cbf_results = get_content_based_recommendations(user_id, product_data, interaction_data)
#     final_recommendations = combine_recommendations(knn_results, cbf_results)

#     print(f"Đề xuất cuối cùng cho user {user_id}: {final_recommendations}")


import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Đọc dữ liệu từ các file CSV
interactions = pd.read_csv('D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/interactions_data.csv')
products = pd.read_csv('D:/HaoHaoHao/Hoc Hanh/HK7/Phát triển các hệ thống thông minh/Đồ án môn thông minh/E-Commerce_DoBaoHo/RecSys/data/product_data.csv')

# Mã hóa dữ liệu hành động (actions) với độ ưu tiên
action_priority = {0: 1, 1: 3, 2: 5, 3: 4}  # view: 1, add_to_cart: 3, purchase: 5, wish_list: 4

# Tạo ma trận tương tác của người dùng và sản phẩm
interactions['priority'] = interactions['action'].map(action_priority)
user_product_matrix = interactions.groupby(['user_id', 'product_id'])['priority'].max().unstack(fill_value=0)

# Phần đề xuất sản phẩm theo hành động người dùng (KNN dựa trên hành động)
def knn_based_recommendations(user_id, user_product_matrix, k=5):
    # Đảm bảo rằng user_product_matrix là một DataFrame
    if isinstance(user_product_matrix, pd.DataFrame):
        # Kiểm tra số lượng người dùng có đủ dữ liệu hay không
        if len(user_product_matrix) <= k:
            k = len(user_product_matrix) - 1  # Nếu có ít người dùng hơn k, giảm k xuống
        
        # Lấy dữ liệu của người dùng hiện tại
        user_data = user_product_matrix.loc[user_id]
        
        # Tính độ tương đồng cosine giữa người dùng với các người dùng khác
        model_knn = NearestNeighbors(n_neighbors=k+1, metric='cosine')  # Lấy k+1 để tính tương tự với bản thân người dùng
        model_knn.fit(user_product_matrix)
        distances, indices = model_knn.kneighbors([user_data])
        
        # Lấy ra các sản phẩm đã được tương tác từ những người dùng tương tự
        similar_users = user_product_matrix.index[indices.flatten()]
        recommended_products = []
        
        for similar_user in similar_users:
            products_interacted = user_product_matrix.loc[similar_user][user_product_matrix.loc[similar_user] > 0].index
            recommended_products.extend(products_interacted)
        
        # Loại bỏ sản phẩm đã được người dùng tương tác
        recommended_products = list(set(recommended_products) - set(user_data[user_data > 0].index))
        
        return recommended_products
    else:
        raise ValueError("user_product_matrix phải là một DataFrame của Pandas")

# Phần đề xuất sản phẩm theo độ tương đồng giữa các sản phẩm (Content-Based Filtering)
def content_based_recommendations(user_id, k=5):
    # Tạo ma trận tương đồng sản phẩm dựa trên category và brand
    product_features = products[['category', 'brand']]
    product_features = pd.get_dummies(product_features)
    
    # Tính độ tương đồng cosine giữa các sản phẩm
    similarity_matrix = cosine_similarity(product_features)
    
    # Lấy ra các sản phẩm mà người dùng đã tương tác
    interacted_products = user_product_matrix.loc[user_id][user_product_matrix.loc[user_id] > 0].index
    
    # Tính điểm tương đồng cho mỗi sản phẩm đã tương tác
    scores = np.zeros(len(products))
    for product_id in interacted_products:
        product_idx = products[products['product_id'] == product_id].index[0]
        scores += similarity_matrix[product_idx]
    
    # Đề xuất k sản phẩm có độ tương đồng cao nhất
    recommended_indices = np.argsort(scores)[::-1][:k]
    recommended_products = products.iloc[recommended_indices]['product_id'].values
    
    # Loại bỏ các sản phẩm đã được người dùng tương tác
    recommended_products = [product for product in recommended_products if product not in interacted_products]
    
    return recommended_products

# Hàm chính để đưa ra đề xuất thông minh kết hợp giữa KNN và Content-Based Filtering
def combined_recommendation(user_id, k=5):
    # knn_recommendations = knn_based_recommendations(user_id, k)
    # content_recommendations = content_based_recommendations(user_id, k)
    
    # # Kết hợp đề xuất (có thể làm trọng số hoặc chỉ đơn giản là gộp các đề xuất)
    # recommendations = list(set(knn_recommendations + content_recommendations))

    knn_recommendations = knn_based_recommendations(user_id, user_product_matrix, k)  # Truyền đúng user_product_matrix
    content_recommendations = content_based_recommendations(user_id, k)
    recommendations = list(set(knn_recommendations + content_recommendations))
    return recommendations
    
    # return recommendations
if __name__ == "__main__":
# Ví dụ sử dụng
    user_id = 0  # Thay thế với user_id cần đề xuất
    recommendations = combined_recommendation(user_id, k=5)
    print(f"Đề xuất cho người dùng {user_id}: {recommendations}")


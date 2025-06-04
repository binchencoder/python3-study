import numpy as np
# np.import_array()  # 显式导入NumPy的C-API

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
from collections import defaultdict
import random
import streamlit as st

# 设置页面标题和布局
st.set_page_config(page_title="智能推荐系统", page_icon="🤖", layout="wide")
st.title("🎯 个性化智能推荐系统")
st.markdown("""
该推荐系统结合了多种推荐技术：
- **实体搜索**：通过关键词查找相关项目
- **基于内容推荐**：根据项目相似度推荐
- **协同过滤**：基于用户行为的个性化推荐
- **混合推荐**：综合多种推荐策略
""")


# 生成模拟数据
@st.cache_data
def generate_sample_data():
    # 电影数据
    movies = {
        'movie_id': range(1, 101),
        'title': [f"电影{chr(65 + i // 10)}{i % 10 + 1}" for i in range(100)],
        'genre': [random.choice(['动作', '喜剧', '爱情', '科幻', '恐怖', '悬疑', '动画', '剧情']) for _ in range(100)],
        'director': [f"导演{chr(65 + i // 26)}{chr(65 + i % 26)}" for i in range(100)],
        'year': [random.randint(1990, 2023) for _ in range(100)],
        'rating': [round(random.uniform(6.0, 9.5), 1) for _ in range(100)],
        'description': [
            f"这是一部精彩的{random.choice(['动作', '喜剧', '爱情', '科幻', '恐怖'])}电影，讲述了{random.choice(['英雄', '爱情', '冒险', '悬疑', '成长'])}的故事。"
            for _ in range(100)]
    }

    # 用户数据
    users = {
        'user_id': range(1, 51),
        'name': [f"用户{i}" for i in range(1, 51)],
        'age': [random.randint(18, 65) for _ in range(50)],
        'gender': [random.choice(['男', '女']) for _ in range(50)]
    }

    # 评分数据
    ratings = []
    for uid in range(1, 51):
        for _ in range(random.randint(10, 30)):
            mid = random.randint(1, 100)
            rating = random.randint(1, 5)
            ratings.append({'user_id': uid, 'movie_id': mid, 'rating': rating})

    return pd.DataFrame(movies), pd.DataFrame(users), pd.DataFrame(ratings)


# 加载数据
movies_df, users_df, ratings_df = generate_sample_data()


# 基于内容的推荐系统
class ContentBasedRecommender:
    def __init__(self, movies_df):
        self.movies_df = movies_df
        self.tfidf_vectorizer = TfidfVectorizer(stop_words=None)
        self.feature_matrix = self._create_feature_matrix()

    def _create_feature_matrix(self):
        """创建电影特征矩阵"""
        # 组合特征：类型+导演+年份+描述
        features = self.movies_df['genre'] + ' ' + self.movies_df['director'] + ' ' + \
                   self.movies_df['year'].astype(str) + ' ' + self.movies_df['description']
        return self.tfidf_vectorizer.fit_transform(features)

    def search_entities(self, query, top_n=5):
        """搜索实体"""
        # 转换查询为TF-IDF向量
        query_vec = self.tfidf_vectorizer.transform([query])

        # 计算相似度
        sim_scores = cosine_similarity(query_vec, self.feature_matrix).flatten()

        # 获取最相似的结果
        top_indices = sim_scores.argsort()[-top_n:][::-1]
        return self.movies_df.iloc[top_indices]

    def recommend_similar(self, movie_id, top_n=5):
        """推荐相似的电影"""
        idx = self.movies_df[self.movies_df['movie_id'] == movie_id].index[0]
        sim_scores = cosine_similarity(self.feature_matrix[idx], self.feature_matrix).flatten()
        top_indices = sim_scores.argsort()[-top_n - 1:-1][::-1]
        return self.movies_df.iloc[top_indices]


# 协同过滤推荐系统（使用TruncatedSVD替代Surprise）
class CollaborativeFilteringRecommender:
    def __init__(self, ratings_df, movies_df):
        self.ratings_df = ratings_df
        self.movies_df = movies_df
        self.user_ratings = self._prepare_user_ratings()
        self.user_matrix, self.movie_matrix = self._create_factor_matrices()

    def _prepare_user_ratings(self):
        """准备用户评分数据"""
        # 构建用户评分字典
        user_ratings = defaultdict(dict)
        for _, row in self.ratings_df.iterrows():
            user_ratings[row['user_id']][row['movie_id']] = row['rating']
        return user_ratings

    def _create_factor_matrices(self):
        """创建用户和电影的因子矩阵"""
        # 创建用户-电影评分矩阵
        rating_matrix = pd.pivot_table(
            self.ratings_df,
            values='rating',
            index='user_id',
            columns='movie_id',
            fill_value=0
        )

        # 使用SVD分解
        svd = TruncatedSVD(n_components=20, random_state=42)
        user_factors = svd.fit_transform(rating_matrix)
        movie_factors = svd.components_.T

        # 归一化
        scaler = MinMaxScaler()
        user_factors = scaler.fit_transform(user_factors)
        movie_factors = scaler.fit_transform(movie_factors)

        return user_factors, movie_factors

    def predict_rating(self, user_id, movie_id):
        """预测用户对电影的评分"""
        try:
            user_idx = user_id - 1  # 用户ID从1开始，索引从0开始
            movie_idx = movie_id - 1  # 电影ID从1开始，索引从0开始
            return np.dot(self.user_matrix[user_idx], self.movie_matrix[movie_idx]) * 5
        except:
            # 如果用户或电影不存在，返回平均分
            return self.ratings_df['rating'].mean()

    def recommend_for_user(self, user_id, top_n=5):
        """为用户推荐电影"""
        # 获取用户未评分的电影
        rated_movies = set(self.user_ratings[user_id].keys())
        all_movies = set(self.ratings_df['movie_id'].unique())
        unrated_movies = all_movies - rated_movies

        # 预测评分
        predictions = []
        for movie_id in unrated_movies:
            pred_rating = self.predict_rating(user_id, movie_id)
            predictions.append((movie_id, pred_rating))

        # 按预测评分排序
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:top_n]


# 混合推荐系统
class HybridRecommender:
    def __init__(self, content_recommender, cf_recommender, movies_df):
        self.content_rec = content_recommender
        self.cf_rec = cf_recommender
        self.movies_df = movies_df

    def recommend(self, user_id=None, movie_id=None, query=None, top_n=5):
        """混合推荐方法"""
        if query:
            # 基于搜索查询的推荐
            results = self.content_rec.search_entities(query, top_n)
            return results

        elif movie_id and not user_id:
            # 基于内容的相似推荐
            return self.content_rec.recommend_similar(movie_id, top_n)

        elif user_id and not movie_id:
            # 基于协同过滤的个性化推荐
            recommendations = self.cf_rec.recommend_for_user(user_id, top_n)
            # 转换为DataFrame
            rec_df = pd.DataFrame(recommendations, columns=['movie_id', 'predicted_rating'])
            rec_df = rec_df.merge(self.movies_df, on='movie_id')
            return rec_df

        elif user_id and movie_id:
            # 混合推荐：基于内容推荐 + 用户偏好
            content_recs = self.content_rec.recommend_similar(movie_id, top_n * 3)
            # 过滤用户已经看过的
            user_rated = set(self.cf_rec.user_ratings[user_id].keys())
            content_recs = content_recs[~content_recs['movie_id'].isin(user_rated)]

            # 预测用户对这些电影的评分
            predictions = []
            for _, row in content_recs.iterrows():
                pred_rating = self.cf_rec.predict_rating(user_id, row['movie_id'])
                predictions.append((row['movie_id'], pred_rating, row['title'], row['genre']))

            # 按预测评分排序
            predictions.sort(key=lambda x: x[1], reverse=True)
            return pd.DataFrame(predictions[:top_n], columns=['movie_id', 'predicted_rating', 'title', 'genre'])

        else:
            # 默认返回热门电影
            return self.movies_df.sort_values('rating', ascending=False).head(top_n)


# 初始化推荐系统
content_rec = ContentBasedRecommender(movies_df)
cf_rec = CollaborativeFilteringRecommender(ratings_df, movies_df)
hybrid_rec = HybridRecommender(content_rec, cf_rec, movies_df)

# Streamlit界面布局
st.sidebar.title("推荐选项")
option = st.sidebar.radio("选择推荐模式:",
                          ["实体搜索", "基于内容推荐", "个性化推荐", "混合推荐"])

if option == "实体搜索":
    st.subheader("🔍 实体搜索")
    query = st.text_input("输入搜索关键词（类型、导演、内容等）:", "科幻")
    if st.button("搜索"):
        results = hybrid_rec.recommend(query=query, top_n=8)
        st.write(f"找到 {len(results)} 个相关结果:")
        cols = st.columns(4)
        for i, (_, row) in enumerate(results.iterrows()):
            with cols[i % 4]:
                st.image(f"https://picsum.photos/200/300?random={row['movie_id']}",
                         caption=row['title'], width=150)
                st.caption(f"类型: {row['genre']}")
                st.caption(f"评分: {row['rating']}")
                st.caption(f"年份: {row['year']}")

elif option == "基于内容推荐":
    st.subheader("🎬 基于内容推荐")
    selected_movie = st.selectbox("选择一部电影:", movies_df['title'].tolist())
    movie_id = movies_df[movies_df['title'] == selected_movie]['movie_id'].values[0]

    if st.button("推荐相似内容"):
        similar_movies = hybrid_rec.recommend(movie_id=movie_id, top_n=8)
        st.write(f"与 **{selected_movie}** 相似的电影:")
        cols = st.columns(4)
        for i, (_, row) in enumerate(similar_movies.iterrows()):
            with cols[i % 4]:
                st.image(f"https://picsum.photos/200/300?random={row['movie_id']}",
                         caption=row['title'], width=150)
                st.caption(f"类型: {row['genre']}")
                st.caption(f"评分: {row['rating']}")

elif option == "个性化推荐":
    st.subheader("👤 个性化推荐")
    selected_user = st.selectbox("选择用户:", users_df['name'].tolist())
    user_id = users_df[users_df['name'] == selected_user]['user_id'].values[0]

    # 显示用户历史评分
    user_ratings = ratings_df[ratings_df['user_id'] == user_id]
    user_ratings = user_ratings.merge(movies_df, on='movie_id')
    st.write(f"**{selected_user}** 的历史评分:")
    st.dataframe(user_ratings[['title', 'genre', 'rating']].head(10))

    if st.button("生成个性化推荐"):
        recommendations = hybrid_rec.recommend(user_id=user_id, top_n=8)
        st.write(f"为 **{selected_user}** 推荐的电影:")
        cols = st.columns(4)
        for i, (_, row) in enumerate(recommendations.iterrows()):
            with cols[i % 4]:
                st.image(f"https://picsum.photos/200/300?random={row['movie_id']}",
                         caption=row['title'], width=150)
                st.caption(f"类型: {row['genre']}")
                st.caption(f"预测评分: {row['predicted_rating']:.2f}")

elif option == "混合推荐":
    st.subheader("✨ 混合推荐")
    selected_user = st.selectbox("选择用户:", users_df['name'].tolist(), key="user_mixed")
    user_id = users_df[users_df['name'] == selected_user]['user_id'].values[0]

    selected_movie = st.selectbox("选择一部电影:", movies_df['title'].tolist(), key="movie_mixed")
    movie_id = movies_df[movies_df['title'] == selected_movie]['movie_id'].values[0]

    if st.button("生成混合推荐"):
        recommendations = hybrid_rec.recommend(user_id=user_id, movie_id=movie_id, top_n=8)
        st.write(f"基于 **{selected_movie}** 和 **{selected_user}** 的偏好推荐的电影:")
        cols = st.columns(4)
        for i, (_, row) in enumerate(recommendations.iterrows()):
            with cols[i % 4]:
                st.image(f"https://picsum.photos/200/300?random={row['movie_id']}",
                         caption=row['title'], width=150)
                st.caption(f"类型: {row['genre']}")
                st.caption(f"预测评分: {row['predicted_rating']:.2f}")

# 数据概览
st.sidebar.markdown("---")
st.sidebar.subheader("数据概览")
st.sidebar.write(f"🎬 电影数量: {len(movies_df)}")
st.sidebar.write(f"👥 用户数量: {len(users_df)}")
st.sidebar.write(f"⭐ 评分记录: {len(ratings_df)}")

# 热门电影展示
st.sidebar.markdown("---")
st.sidebar.subheader("热门电影")
top_movies = movies_df.sort_values('rating', ascending=False).head(5)
for _, row in top_movies.iterrows():
    st.sidebar.markdown(f"**{row['title']}** ({row['year']}) - ⭐{row['rating']}")
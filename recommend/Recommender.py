import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
from fastapi import FastAPI


class ContentBasedRecommender:
    def __init__(self, data_path):
        self.df = self.load_data(data_path)
        self.tfidf_matrix, self.tfidf_vectorizer = self.prepare_content_features()
        self.feature_weights = {"content": 0.6, "genre": 0.3, "rating": 0.1}

    def load_data(self, path):
        data = {
            "title": [
                "The Shawshank Redemption",
                "The Godfather",
                "The Dark Knight",
                "Forrest Gump",
                "Inception",
                "Pulp Fiction",
            ],
            "genre": [
                "Drama",
                "Crime,Drama",
                "Action,Crime,Drama",
                "Drama,Romance",
                "Action,Adventure,Sci-Fi",
                "Crime,Drama",
            ],
            "director": [
                "Frank Darabont",
                "Francis Ford Coppola",
                "Christopher Nolan",
                "Robert Zemeckis",
                "Christopher Nolan",
                "Quentin Tarantino",
            ],
            "rating": [9.3, 9.2, 9.0, 8.8, 8.8, 8.9],
            "description": [
                "Two imprisoned men bond over a number of years...",
                "The aging patriarch of an organized crime dynasty...",
                "When the menace known as the Joker wreaks havoc...",
                "The presidencies of Kennedy and Johnson...",
                "A thief who steals corporate secrets through...",
                "The lives of two mob hitmen, a boxer...",
            ],
        }
        return pd.DataFrame(data)

    def prepare_content_features(self):
        # 处理文本内容特征（描述+导演）
        tfidf = TfidfVectorizer(stop_words="english")
        combined_text = self.df["description"] + " " + self.df["director"]
        tfidf_matrix = tfidf.fit_transform(combined_text)
        return tfidf_matrix, tfidf

    def search_entity(self, query):
        # 实体搜索功能
        matches = self.df[self.df["title"].str.contains(query, case=False)]
        return matches.to_dict("records")

    def get_recommendations(self, entity_title, top_n=5):
        # 获取目标实体索引
        idx = self.df[self.df["title"] == entity_title].index[0]

        # 计算内容相似度
        content_sim = linear_kernel(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()  # type: ignore

        # 计算类型相似度
        genre_matrix = self.df["genre"].str.get_dummies(",").values
        genre_sim = genre_matrix.dot(genre_matrix[idx])

        # 标准化评分相似度
        rating_sim = (self.df["rating"] - self.df["rating"].min()) / (
            self.df["rating"].max() - self.df["rating"].min()
        )

        # 组合相似度
        combined_sim = (
            self.feature_weights["content"] * content_sim
            + self.feature_weights["genre"] * genre_sim
            + self.feature_weights["rating"] * rating_sim
        )

        # 获取推荐索引
        sim_scores = list(enumerate(combined_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 排除自身并取前N个结果
        sim_scores = sim_scores[1 : top_n + 1]
        movie_indices = [i[0] for i in sim_scores]

        return self.df.iloc[movie_indices].to_dict("records")


# 使用示例
if __name__ == "__main__":
    recommender = ContentBasedRecommender("movies.csv")

    # 实体搜索
    search_results = recommender.search_entity("dark")
    print("Search Results:", search_results)

    # 获取推荐
    if search_results:
        recommendations = recommender.get_recommendations(search_results[0]["title"])
        print("\nRecommendations:")
        for movie in recommendations:
            print(
                f"{movie['title']} (Rating: {movie['rating']}, Genres: {movie['genre']})"
            )

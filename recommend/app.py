from fastapi import FastAPI
from Recommender import ContentBasedRecommender

app = FastAPI()
recommender = ContentBasedRecommender("movies.csv")


@app.get("/search")
async def search_entities(query: str):
    return recommender.search_entity(query)


@app.get("/recommend")
async def get_recommendations(title: str, top_n: int = 3):
    return recommender.get_recommendations(title, top_n)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000)

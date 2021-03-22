from fastapi import FastAPI
from scrapper import get_all_news, ALL_URLS

app = FastAPI()


@app.get("/get_news")
async def root():
    return get_all_news(urls=ALL_URLS)

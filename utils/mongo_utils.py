from pymongo import MongoClient

def save_to_mongodb(data):
    client = MongoClient("mongodb://mongodb_full:27017/")
    db = client['crawler_db']
    collection = db['crawled_data']

    for url, content in data.items():
        collection.insert_one({"url": url, "content": content or "No content"})
    print("Data saved to MongoDB.")

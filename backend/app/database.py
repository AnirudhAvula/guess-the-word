from pymongo import MongoClient

from app.config import settings


client = MongoClient(settings.MONGO_URI)

database = client[settings.DATABASE_NAME]


users_collection = database["users"]
words_collection = database["words"]
games_collection = database["games"]
guesses_collection = database["guesses"]

users_collection.create_index(
    "username",
    unique=True
)

words_collection.create_index(
    "word",
    unique=True
)

games_collection.create_index(
    [
        ("user_id", 1),
        ("game_date", 1)
    ]
)

guesses_collection.create_index(
    [
        ("game_id", 1),
        ("guess_number", 1)
    ],
    unique=True
)
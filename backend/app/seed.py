from app.database import words_collection


WORDS = [
    "APPLE",
    "GRAPE",
    "MANGO",
    "LEMON",
    "HOUSE",
    "CHAIR",
    "PLANT",
    "BREAD",
    "WATER",
    "MUSIC",
    "LIGHT",
    "PHONE",
    "TABLE",
    "TRAIN",
    "CLOUD",
    "RIVER",
    "STONE",
    "WORLD",
    "DREAM",
    "GREEN",
]


def seed_words():
    existing_words = set(
        words_collection.distinct("word")
    )

    new_words = [
        {"word": word}
        for word in WORDS
        if word not in existing_words
    ]

    if new_words:
        words_collection.insert_many(new_words)

        print(
            f"Inserted {len(new_words)} words."
        )
    else:
        print("All words already exist.")


if __name__ == "__main__":
    seed_words()
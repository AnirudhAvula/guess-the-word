from app.database import users_collection
from app.utils.security import hash_password


username = "Admin"
password = "Admin1$"


existing_user = users_collection.find_one(
    {"username": username}
)

if existing_user:
    print("Admin already exists.")

else:
    users_collection.insert_one({
        "username": username,
        "password_hash": hash_password(password),
        "role": "ADMIN"
    })

    print("Admin created successfully.")
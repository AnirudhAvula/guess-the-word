from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.database import (
    users_collection,
    games_collection,
    guesses_collection
)

from app.utils.dependencies import get_current_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ==================================================
# DAILY REPORT
# ==================================================

@router.get("/daily-report")
def daily_report(
    date: str,
    current_admin=Depends(get_current_admin)
):

    # ----------------------------------------------
    # Validate date
    # ----------------------------------------------

    try:

        datetime.strptime(
            date,
            "%Y-%m-%d"
        )

    except ValueError:

        raise HTTPException(
            status_code=400,
            detail="Date must be in YYYY-MM-DD format."
        )

    # ----------------------------------------------
    # Find games played on this date
    # ----------------------------------------------

    games = list(
        games_collection.find({
            "game_date": date
        })
    )

    # ----------------------------------------------
    # Number of users who played
    # ----------------------------------------------

    user_ids = set()

    for game in games:

        user_ids.add(
            str(game["user_id"])
        )

    number_of_users = len(user_ids)

    # ----------------------------------------------
    # Number of correct guesses
    # ----------------------------------------------

    start_date = datetime.fromisoformat(
    f"{date}T00:00:00+00:00"
    )

    end_date = datetime.fromisoformat(
        f"{date}T00:00:00+00:00"
    ).replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=999999
    )

    correct_guesses = guesses_collection.count_documents({
        "created_at": {
            "$gte": start_date,
            "$lte": end_date
        },
        "correct": True
    })

    return {
        "date": date,
        "number_of_users": number_of_users,
        "number_of_correct_guesses": correct_guesses
    }


# ==================================================
# GET ALL PLAYERS
# ==================================================

@router.get("/users")
def get_players(
    current_admin=Depends(get_current_admin)
):

    players = users_collection.find(
        {"role": "PLAYER"},
        {
            "_id": 1,
            "username": 1
        }
    )

    return [
        {
            "id": str(player["_id"]),
            "username": player["username"]
        }
        for player in players
    ]


# ==================================================
# USER REPORT
# ==================================================

@router.get("/user-report/{user_id}")
def user_report(
    user_id: str,
    current_admin=Depends(get_current_admin)
):

    # ----------------------------------------------
    # Validate user ID
    # ----------------------------------------------

    try:

        user_object_id = ObjectId(user_id)

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid user ID."
        )


    # ----------------------------------------------
    # Find user
    # ----------------------------------------------

    user = users_collection.find_one({
        "_id": user_object_id,
        "role": "PLAYER"
    })

    if not user:

        raise HTTPException(
            status_code=404,
            detail="Player not found."
        )


    # ----------------------------------------------
    # Get user's games
    # ----------------------------------------------

    games = list(
        games_collection.find({
            "user_id": user_object_id
        }).sort(
            "game_date",
            -1
        )
    )


    # ----------------------------------------------
    # Group games by date
    # ----------------------------------------------

    daily_data = {}


    for game in games:

        date = game["game_date"]

        if date not in daily_data:

            daily_data[date] = {
                "date": date,
                "words_tried": 0,
                "correct_guesses": 0
            }


        # One game = one word tried

        daily_data[date]["words_tried"] += 1


        # If game was won

        if game.get("won") is True:

            daily_data[date]["correct_guesses"] += 1


    # ----------------------------------------------
    # Convert to list
    # ----------------------------------------------

    report = list(daily_data.values())

    # Sort newest date first

    report.sort(
        key=lambda x: x["date"],
        reverse=True
    )


    return {
        "user_id": str(user["_id"]),
        "username": user["username"],
        "report": report
    }


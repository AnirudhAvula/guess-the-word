import random
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.database import (
    words_collection,
    games_collection,
    guesses_collection
)

from app.schemas.game import GuessRequest
from app.utils.dependencies import get_current_player


router = APIRouter(
    prefix="/game",
    tags=["Game"]
)

# ==================================================
# GAME STATUS
# ==================================================

@router.get("/status")
def game_status(
    current_user=Depends(get_current_player)
):

    user_id = current_user["_id"]

    # Today's date
    today = datetime.now(timezone.utc).date().isoformat()

    # Count games played today
    games_today = games_collection.count_documents({
        "user_id": user_id,
        "game_date": today
    })

    games_remaining = max(0, 3 - games_today)

    return {
        "games_played_today": games_today,
        "games_remaining_today": games_remaining
    }


# ==================================================
# START GAME
# ==================================================

@router.post("/start")
def start_game(
    current_user=Depends(get_current_player)
):

    user_id = current_user["_id"]

    # Today's date
    today = datetime.now(timezone.utc).date().isoformat()

    # ----------------------------------------------
    # Check how many games the user played today
    # ----------------------------------------------

    games_today = games_collection.count_documents({
        "user_id": user_id,
        "game_date": today
    })

    # Maximum 3 games per day
    if games_today >= 3:
        raise HTTPException(
            status_code=400,
            detail="You can play only 3 games per day."
        )

    # ----------------------------------------------
    # Get words from database
    # ----------------------------------------------

    words = list(words_collection.find())

    if not words:
        raise HTTPException(
            status_code=500,
            detail="No words available in database."
        )

    # ----------------------------------------------
    # Pick a random word
    # ----------------------------------------------

    selected_word = random.choice(words)

    target_word = selected_word["word"]

    # Make sure the word is valid
    if len(target_word) != 5:
        raise HTTPException(
            status_code=500,
            detail="Invalid word found in database."
        )

    # ----------------------------------------------
    # Create game
    # ----------------------------------------------

    game = {
        "user_id": user_id,
        "word_id": selected_word["_id"],
        "word": target_word,
        "game_date": today,
        "attempts": 0,
        "won": False,
        "status": "ACTIVE",
        "started_at": datetime.now(timezone.utc)
    }

    result = games_collection.insert_one(game)

    # ----------------------------------------------
    # Return game information
    # ----------------------------------------------

    return {
        "game_id": str(result.inserted_id),
        "message": "Game started",
        "attempts_remaining": 5,
        "games_remaining_today": 3 - games_today - 1
    }


# ==================================================
# CHECK GUESS
# ==================================================

def check_guess(
    target_word: str,
    guessed_word: str
):
    """
    Compare the guessed word with the target word.

    GREEN  -> correct letter and correct position
    ORANGE -> correct letter but wrong position
    GREY   -> letter does not exist / already matched
    """

    # Initially mark every letter as GREY
    result = ["GREY"] * 5

    # Keep track of letters that are still available
    remaining_letters = {}

    # ----------------------------------------------
    # PASS 1: Find GREEN letters
    # ----------------------------------------------

    for i in range(5):

        if guessed_word[i] == target_word[i]:

            result[i] = "GREEN"

        else:

            letter = target_word[i]

            remaining_letters[letter] = (
                remaining_letters.get(letter, 0) + 1
            )

    # ----------------------------------------------
    # PASS 2: Find ORANGE letters
    # ----------------------------------------------

    for i in range(5):

        # Already GREEN
        if result[i] == "GREEN":
            continue

        letter = guessed_word[i]

        if remaining_letters.get(letter, 0) > 0:

            result[i] = "ORANGE"

            remaining_letters[letter] -= 1

    return result


# ==================================================
# SUBMIT GUESS
# ==================================================

@router.post("/guess")
def submit_guess(
    request: GuessRequest,
    current_user=Depends(get_current_player)
):

    # Get values from request body
    game_id = request.game_id
    guess = request.guess

    # ----------------------------------------------
    # Validate game ID
    # ----------------------------------------------

    try:

        game_object_id = ObjectId(game_id)

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid game ID."
        )

    # ----------------------------------------------
    # Find the game
    # ----------------------------------------------

    game = games_collection.find_one({
        "_id": game_object_id,
        "user_id": current_user["_id"]
    })

    if not game:

        raise HTTPException(
            status_code=404,
            detail="Game not found."
        )

    # ----------------------------------------------
    # Check if game is already completed
    # ----------------------------------------------

    if game["status"] == "COMPLETED":

        raise HTTPException(
            status_code=400,
            detail="This game is already completed."
        )

    # ----------------------------------------------
    # Validate guess
    # ----------------------------------------------

    if not guess.isupper():

        raise HTTPException(
            status_code=400,
            detail="Guess must be in uppercase."
        )

    if len(guess) != 5:

        raise HTTPException(
            status_code=400,
            detail="Guess must contain exactly 5 letters."
        )

    if not guess.isalpha():

        raise HTTPException(
            status_code=400,
            detail="Guess must contain only letters."
        )

    # ----------------------------------------------
    # Make sure user has not exceeded 5 guesses
    # ----------------------------------------------

    if game["attempts"] >= 5:

        raise HTTPException(
            status_code=400,
            detail="Maximum 5 guesses allowed."
        )

    # ----------------------------------------------
    # Current attempt number
    # ----------------------------------------------

    attempt_number = game["attempts"] + 1

    # ----------------------------------------------
    # Check the guess
    # ----------------------------------------------

    result = check_guess(
        game["word"],
        guess
    )

    # ----------------------------------------------
    # Check if guess is correct
    # ----------------------------------------------

    is_correct = (
        guess == game["word"]
    )

    # ----------------------------------------------
    # Save guess in database
    # ----------------------------------------------

    guesses_collection.insert_one({
        "game_id": game_object_id,
        "user_id": current_user["_id"],
        "guess": guess,
        "guess_number": attempt_number,
        "result": result,
        "correct": is_correct,
        "created_at": datetime.now(timezone.utc)
    })

    # ==================================================
    # PLAYER WON
    # ==================================================

    if is_correct:

        games_collection.update_one(
            {"_id": game_object_id},
            {
                "$set": {
                    "attempts": attempt_number,
                    "won": True,
                    "status": "COMPLETED",
                    "completed_at": datetime.now(timezone.utc)
                }
            }
        )

        return {
            "correct": True,
            "result": result,
            "message": "Congratulations! You guessed the word.",
            "game_over": True,
            "attempts_used": attempt_number,
            "attempts_remaining": 5 - attempt_number
        }

    # ==================================================
    # PLAYER USED ALL 5 GUESSES
    # ==================================================

    if attempt_number >= 5:

        games_collection.update_one(
            {"_id": game_object_id},
            {
                "$set": {
                    "attempts": attempt_number,
                    "won": False,
                    "status": "COMPLETED",
                    "completed_at": datetime.now(timezone.utc)
                }
            }
        )

        return {
            "correct": False,
            "result": result,
            "message": "Better luck next time!",
            "game_over": True,
            "attempts_used": attempt_number,
            "attempts_remaining": 0
        }

    # ==================================================
    # GAME CONTINUES
    # ==================================================

    games_collection.update_one(
        {"_id": game_object_id},
        {
            "$set": {
                "attempts": attempt_number
            }
        }
    )

    return {
        "correct": False,
        "result": result,
        "message": "Try again!",
        "game_over": False,
        "attempts_used": attempt_number,
        "attempts_remaining": 5 - attempt_number
    }
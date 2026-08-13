from pydantic import BaseModel


class GuessRequest(BaseModel):
    game_id: str
    guess: str
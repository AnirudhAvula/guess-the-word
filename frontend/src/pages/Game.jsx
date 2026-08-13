import { useState, useEffect } from "react";
import API from "../api";

function Game({ username, onLogout }) {

    const [gameId, setGameId] = useState(null);

    const [guesses, setGuesses] = useState([]);

    const [currentGuess, setCurrentGuess] = useState("");

    const [attemptsRemaining, setAttemptsRemaining] = useState(5);

    const [gamesRemaining, setGamesRemaining] = useState(3);

    const [message, setMessage] = useState("");

    const [gameStarted, setGameStarted] = useState(false);

    const [gameOver, setGameOver] = useState(false);

    const [error, setError] = useState("");


    const loadGameStatus = async () => {

        try {

            const token = localStorage.getItem("token");

            const response = await API.get(
                "/game/status",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setGamesRemaining(
                response.data.games_remaining_today
            );

        } catch (error) {

            console.error(
                "Unable to load game status:",
                error
            );
        }
    };

    useEffect(() => {

        loadGameStatus();

    }, []);


    // ==============================================
    // START GAME
    // ==============================================

    const startGame = async () => {

        setError("");
        setMessage("");

        try {

            const token = localStorage.getItem("token");

            const response = await API.post(
                "/game/start",
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setGameId(response.data.game_id);

            setAttemptsRemaining(
                response.data.attempts_remaining
            );

            setGamesRemaining(
                response.data.games_remaining_today
            );

            setGuesses([]);

            setCurrentGuess("");

            setGameStarted(true);


            setGameOver(false);

            setMessage("Game started! Guess the word.");

        } catch (error) {
            await loadGameStatus();

            setError(
                error.response?.data?.detail ||
                "Unable to start game."
            );
        }
    };


    // ==============================================
    // SUBMIT GUESS
    // ==============================================

    const submitGuess = async () => {

        setError("");
        setMessage("");

        if (!gameStarted) {
            return;
        }

        if (currentGuess.length !== 5) {

            setError(
                "Guess must contain exactly 5 letters."
            );

            return;
        }

        if (!/^[A-Z]{5}$/.test(currentGuess)) {

            setError(
                "Guess must contain only uppercase letters."
            );

            return;
        }

        try {

            const token = localStorage.getItem("token");

            const response = await API.post(
                "/game/guess",
                {
                    game_id: gameId,
                    guess: currentGuess
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            const newGuess = {
                word: currentGuess,
                result: response.data.result
            };

            setGuesses([
                ...guesses,
                newGuess
            ]);

            setAttemptsRemaining(
                response.data.attempts_remaining
            );

            setMessage(
                response.data.message
            );

            setCurrentGuess("");

            if (response.data.game_over) {

                setGameOver(true);
            }

        } catch (error) {

            setError(
                error.response?.data?.detail ||
                "Unable to submit guess."
            );
        }
    };


    // ==============================================
    // HANDLE INPUT
    // ==============================================

    const handleGuessChange = (e) => {

        let value = e.target.value;

        value = value
            .toUpperCase()
            .replace(/[^A-Z]/g, "");

        if (value.length > 5) {
            value = value.slice(0, 5);
        }

        setCurrentGuess(value);
    };


    // ==============================================
    // HANDLE ENTER KEY
    // ==============================================

    const handleGuessKeyDown = (e) => {

        if (e.key === "Enter") {

            e.preventDefault();

            submitGuess();
        }
    };


    // ==============================================
    // LOGOUT
    // ==============================================

    const handleLogout = () => {

        localStorage.removeItem("token");

        onLogout();
    };


    // ==============================================
    // COLOR CLASS
    // ==============================================

    const getColorClass = (status) => {

        if (status === "GREEN") {
            return "letter green";
        }

        if (status === "ORANGE") {
            return "letter orange";
        }

        return "letter grey";
    };


    return (
        <div className="game-container">

            {/* HEADER */}

            <div className="game-header">

                <h1>Guess the Word</h1>

                <p>
                    Welcome, <strong>{username}</strong>
                </p>

                <button
                    className="logout-button"
                    onClick={handleLogout}
                >
                    Logout
                </button>

            </div>


            {/* GAME INFORMATION */}

            <div className="game-info">

                <p>
                    Games remaining today:
                    <strong> {gamesRemaining}</strong>
                </p>

                {gameStarted && !gameOver && (
                    <p>
                        Attempts remaining:
                        <strong> {attemptsRemaining}</strong>
                    </p>
                )}

            </div>


            {/* START GAME */}

            {!gameStarted && (

                <div className="start-section">

                    <h2>Ready to play?</h2>

                    <button
                        className="start-button"
                        onClick={startGame}
                        disabled={gamesRemaining === 0}
                    >
                        Start Game
                    </button>

                </div>
            )}


            {/* GAME BOARD */}

            {gameStarted && (

                <div className="game-board">

                    {guesses.map(
                        (guess, rowIndex) => (

                            <div
                                className="guess-row"
                                key={rowIndex}
                            >

                                {guess.word
                                    .split("")
                                    .map(
                                        (letter, index) => (

                                            <div
                                                key={index}
                                                className={getColorClass(
                                                    guess.result[index]
                                                )}
                                            >
                                                {letter}
                                            </div>
                                        )
                                    )}

                            </div>
                        )
                    )}


                    {/* EMPTY ROWS */}

                    {!gameOver &&

                        Array.from({
                            length:
                                attemptsRemaining
                        }).map(
                            (_, index) => (

                                <div
                                    className="guess-row empty-row"
                                    key={`empty-${index}`}
                                >

                                    {[0, 1, 2, 3, 4].map(
                                        (i) => (

                                            <div
                                                className="letter empty"
                                                key={i}
                                            >
                                                {
                                                    index === 0 &&
                                                        i < currentGuess.length
                                                        ? currentGuess[i]
                                                        : ""
                                                }
                                            </div>

                                        )
                                    )}

                                </div>
                            )
                        )
                    }

                </div>
            )}


            {/* INPUT */}

            {gameStarted && !gameOver && (

                <div className="guess-input-section">

                    <input
                        type="text"
                        value={currentGuess}
                        onChange={handleGuessChange}
                        onKeyDown={handleGuessKeyDown}
                        placeholder="ENTER 5 LETTER WORD"
                        maxLength={5}
                    />

                    <button
                        onClick={submitGuess}
                    >
                        Submit Guess
                    </button>

                </div>
            )}


            {/* MESSAGE */}

            {message && (

                <div className="game-result">

                    <p className="game-message">
                        {message}
                    </p>

                </div>
            )}


            {/* ERROR */}

            {error && (

                <p className="game-error">
                    {error}
                </p>
            )}


            {/* PLAY AGAIN */}

            {gameOver && gamesRemaining > 0 && (

                <button
                    className="start-button"
                    onClick={startGame}
                >
                    Play Again
                </button>
            )}

        </div>
    );
}

export default Game;
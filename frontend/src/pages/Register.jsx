import { useState } from "react";
import API from "../api";

function Register({ goToLogin }) {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const handleRegister = async (e) => {

        e.preventDefault();

        setMessage("");
        setError("");

        try {

            await API.post(
                "/auth/register",
                {
                    username,
                    password
                }
            );

            setMessage(
                "Registration successful! Please login."
            );

            setUsername("");
            setPassword("");

        } catch (error) {

            setError(
                error.response?.data?.detail ||
                "Registration failed"
            );
        }
    };

    return (
        <div className="auth-container">

            <div className="auth-box">

                <h1>Guess the Word</h1>

                <h2>Create Account</h2>

                <form onSubmit={handleRegister}>

                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) =>
                            setUsername(e.target.value)
                        }
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) =>
                            setPassword(e.target.value)
                        }
                    />

                    <button type="submit">
                        Register
                    </button>

                </form>

                {message && (
                    <p className="success">
                        {message}
                    </p>
                )}

                {error && (
                    <p className="error">
                        {error}
                    </p>
                )}

                <p>
                    Already have an account?
                </p>

                <button
                    className="secondary-button"
                    onClick={goToLogin}
                >
                    Login
                </button>

            </div>

        </div>
    );
}

export default Register;
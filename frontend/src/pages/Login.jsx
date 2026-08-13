import { useState } from "react";
import API from "../api";


function Login({ onLogin, goToRegister }) {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");


    // ==========================================
    // LOGIN
    // ==========================================

    const handleLogin = async (e) => {

        e.preventDefault();

        setError("");


        try {

            const response = await API.post(
                "/auth/login",
                {
                    username,
                    password
                }
            );


            const token = response.data.access_token;
            const role = response.data.role;
            const loggedInUsername = response.data.username;


            // Save login information

            localStorage.setItem(
                "token",
                token
            );

            localStorage.setItem(
                "role",
                role
            );

            localStorage.setItem(
                "username",
                loggedInUsername
            );


            // Tell App.jsx login was successful

            onLogin(role);


        } catch (error) {

            setError(
                error.response?.data?.detail ||
                "Login failed"
            );
        }
    };


    return (
        <div className="auth-container">

            <div className="auth-box">

                <h1>Guess the Word</h1>

                <h2>Login</h2>


                <form onSubmit={handleLogin}>

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
                        Login
                    </button>

                </form>


                {error && (
                    <p className="error">
                        {error}
                    </p>
                )}


                <p>
                    Don't have an account?
                </p>


                <button
                    type="button"
                    className="secondary-button"
                    onClick={goToRegister}
                >
                    Register
                </button>

            </div>

        </div>
    );
}


export default Login;
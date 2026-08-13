import { useState } from "react";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Game from "./pages/Game";
import AdminDashboard from "./pages/AdminDashboard";


function App() {

    // Get username outside the useState callback
    const username = localStorage.getItem("username");


    const [page, setPage] = useState(() => {

        const token = localStorage.getItem("token");
        const role = localStorage.getItem("role");

        if (!token) {
            return "login";
        }

        if (role === "ADMIN") {
            return "admin";
        }

        return "game";
    });


    // ==========================================
    // LOGIN
    // ==========================================

    const handleLogin = (role) => {

        if (role === "ADMIN") {
            setPage("admin");
        } else {
            setPage("game");
        }
    };


    // ==========================================
    // LOGOUT
    // ==========================================

    const handleLogout = () => {

        localStorage.removeItem("token");
        localStorage.removeItem("role");
        localStorage.removeItem("username");

        setPage("login");
    };


    // ==========================================
    // LOGIN PAGE
    // ==========================================

    if (page === "login") {

        return (
            <Login
                onLogin={handleLogin}
                goToRegister={() =>
                    setPage("register")
                }
            />
        );
    }


    // ==========================================
    // REGISTER PAGE
    // ==========================================

    if (page === "register") {

        return (
            <Register
                goToLogin={() =>
                    setPage("login")
                }
            />
        );
    }


    // ==========================================
    // ADMIN DASHBOARD
    // ==========================================

    if (page === "admin") {

        return (
            <AdminDashboard
                username={username}
                onLogout={handleLogout}
            />
        );
    }


    // ==========================================
    // PLAYER GAME
    // ==========================================

    return (
        <Game
            username={username}
            onLogout={handleLogout}
        />
    );
}


export default App;
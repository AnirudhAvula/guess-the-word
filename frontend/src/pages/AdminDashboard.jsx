import { useState } from "react";

import AdminDailyReport from "./AdminDailyReport";
import AdminUserReport from "./AdminUserReport";


function AdminDashboard({ username, onLogout }) {

    const [activeTab, setActiveTab] = useState("daily");


    return (
        <div className="admin-dashboard">

            {/* HEADER */}

            <div className="admin-header">

                <h1>Admin Dashboard</h1>
                <p>
                    Welcome, <strong>{username}</strong>
                </p>

                <button
                    className="logout-button"
                    onClick={onLogout}
                >
                    Logout
                </button>

            </div>


            {/* TABS */}

            <div className="admin-tabs">

                <button
                    className={
                        activeTab === "daily"
                            ? "admin-tab active"
                            : "admin-tab"
                    }
                    onClick={() => setActiveTab("daily")}
                >
                    📅 Daily Report
                </button>


                <button
                    className={
                        activeTab === "user"
                            ? "admin-tab active"
                            : "admin-tab"
                    }
                    onClick={() => setActiveTab("user")}
                >
                    👤 User Report
                </button>

            </div>


            {/* CONTENT */}

            {activeTab === "daily" && (
                <AdminDailyReport />
            )}

            {activeTab === "user" && (
                <AdminUserReport />
            )}

        </div>
    );
}

export default AdminDashboard;
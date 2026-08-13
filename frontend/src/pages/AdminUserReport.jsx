import { useEffect, useState } from "react";
import API from "../api";


function AdminUserReport() {

    const [users, setUsers] = useState([]);

    const [selectedUser, setSelectedUser] = useState("");

    const [report, setReport] = useState(null);

    const [error, setError] = useState("");

    const [loading, setLoading] = useState(false);


    // ==========================================
    // LOAD PLAYERS
    // ==========================================

    useEffect(() => {

        const loadUsers = async () => {

            try {

                const token = localStorage.getItem("token");

                const response = await API.get(
                    "/admin/users",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );

                setUsers(response.data);

            } catch (error) {

                setError(
                    error.response?.data?.detail ||
                    "Unable to load players."
                );
            }
        };

        loadUsers();

    }, []);


    // ==========================================
    // GET USER REPORT
    // ==========================================

    const getReport = async () => {

        if (!selectedUser) {

            setError("Please select a username.");

            return;
        }

        setError("");
        setReport(null);
        setLoading(true);

        try {

            const token = localStorage.getItem("token");

            const response = await API.get(
                `/admin/user-report/${selectedUser}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setReport(response.data);

        } catch (error) {

            setError(
                error.response?.data?.detail ||
                "Unable to get user report."
            );

        } finally {

            setLoading(false);
        }
    };


    return (
        <div className="report-container">

            <h1>User Report</h1>

            <p className="report-description">
                View detailed game history for a specific player.
            </p>


            {/* USERNAME */}

            <label>
                Username
            </label>

            <select
                value={selectedUser}
                onChange={(e) =>
                    setSelectedUser(e.target.value)
                }
            >

                <option value="">
                    Select a player
                </option>

                {users.map((user) => (

                    <option
                        key={user.id}
                        value={user.id}
                    >
                        {user.username}
                    </option>

                ))}

            </select>


            {/* BUTTON */}

            <button
                onClick={getReport}
                disabled={loading}
            >
                {loading
                    ? "Loading..."
                    : "Get Report"
                }
            </button>


            {/* ERROR */}

            {error && (
                <p className="report-error">
                    {error}
                </p>
            )}


            {/* REPORT */}

            {report && (

                <div className="user-report-results">

                    <h2>
                        Report for: {report.username}
                    </h2>


                    {report.report.length === 0 ? (

                        <p>
                            No games played by this user.
                        </p>

                    ) : (

                        <table className="report-table">

                            <thead>

                                <tr>

                                    <th>
                                        Date
                                    </th>

                                    <th>
                                        Words Tried
                                    </th>

                                    <th>
                                        Correct Guesses
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                {report.report.map(
                                    (item, index) => (

                                        <tr key={index}>

                                            <td>
                                                {item.date}
                                            </td>

                                            <td>
                                                {item.words_tried}
                                            </td>

                                            <td>
                                                {item.correct_guesses}
                                            </td>

                                        </tr>

                                    )
                                )}

                            </tbody>

                        </table>

                    )}

                </div>
            )}

        </div>
    );
}


export default AdminUserReport;
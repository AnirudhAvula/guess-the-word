import { useState } from "react";
import API from "../api";

function AdminDailyReport() {

    const [selectedDate, setSelectedDate] = useState("");
    const [report, setReport] = useState(null);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);


    // ==========================================
    // FORMAT DATE
    // ==========================================

    const formatDate = (date) => {

        if (!date) return "";

        const [year, month, day] = date.split("-");

        const months = [
            "Jan", "Feb", "Mar",
            "Apr", "May", "Jun",
            "Jul", "Aug", "Sep",
            "Oct", "Nov", "Dec"
        ];

        return `${day}-${months[Number(month) - 1]}-${year}`;
    };


    // ==========================================
    // GET REPORT
    // ==========================================

    const getReport = async () => {

        if (!selectedDate) {

            setError("Please select a date.");
            return;
        }

        setError("");
        setReport(null);
        setLoading(true);

        try {

            const token = localStorage.getItem("token");

            const response = await API.get(
                `/admin/daily-report?date=${selectedDate}`,
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
                "Unable to get report."
            );

        } finally {

            setLoading(false);
        }
    };


    return (
        <div className="report-container">

            <h1>Daily Report</h1>

            <p className="report-description">
                View gameplay statistics for a specific date.
            </p>


            {/* DATE */}

            <label>
                Select Date
            </label>

            <input
                type="date"
                value={selectedDate}
                onChange={(e) =>
                    setSelectedDate(e.target.value)
                }
            />


            {/* BUTTON */}

            <button
                onClick={getReport}
                disabled={loading}
            >
                {loading ? "Loading..." : "Get Report"}
            </button>


            {/* ERROR */}

            {error && (
                <p className="report-error">
                    {error}
                </p>
            )}


            {/* RESULTS */}

            {report && (

                <div className="report-results">

                    <h2>
                        Results for {report.date}
                    </h2>


                    <div className="report-cards">

                        {/* USERS */}

                        <div className="report-card">

                            <div className="report-number">
                                {report.number_of_users}
                            </div>

                            <div className="report-label">
                                Users Played
                            </div>

                        </div>


                        {/* CORRECT GUESSES */}

                        <div className="report-card">

                            <div className="report-number">
                                {report.number_of_correct_guesses}
                            </div>

                            <div className="report-label">
                                Correct Guesses (Words Won)
                            </div>

                        </div>

                    </div>

                </div>
            )}

        </div>
    );
}

export default AdminDailyReport;
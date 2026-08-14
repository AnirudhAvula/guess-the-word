# 🎯 Guess the Word

A full-stack word guessing game built using **React**, **FastAPI**, and **MongoDB**.

The application supports two types of users:

- **Player** – Registers, logs in, and plays the word guessing game.
- **Admin** – Views daily and player-wise game reports.

---

## 🚀 Features

### 👤 User Authentication

- Player registration and login
- JWT-based authentication
- Role-based access control
- Two user roles:
  - `PLAYER`
  - `ADMIN`
- Secure password hashing
- Username and password validation
- Logout functionality

### 🎮 Guess the Word Game

- 20 predefined 5-letter English words stored in MongoDB
- A random word is selected when a game starts
- Maximum **3 games per player per day**
- Maximum **5 guesses per game**
- Guesses are displayed in uppercase
- Letter feedback:
  - 🟢 **Green** – Correct letter in the correct position
  - 🟠 **Orange** – Correct letter in the wrong position
  - ⚪ **Grey** – Letter does not exist in the word
- Previous guesses remain visible
- Congratulations message when the player wins
- "Better luck next time!" message when all attempts are used
- The correct answer is not revealed when the player loses

### 📊 Admin Dashboard

Admins can view:

#### Daily Report

Shows:

- Date
- Number of users who played
- Number of correct guesses

#### User Report

Shows:

- Selected player
- Date
- Number of words tried
- Number of correct guesses

### 🗄️ Database

MongoDB stores:

- Users
- Words
- Games
- Guesses

---

## 🛠️ Technologies Used

### Frontend

- React
- JavaScript
- Axios
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- JWT Authentication
- Passlib / bcrypt

### Database

- MongoDB
- PyMongo

### Development Tools

- Git
- GitHub
- VS Code

---

## 📁 Project Structure

```text
guess-the-word/
│
├── backend/
│   │
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── game.py
│   │   │   └── admin.py
│   │   │
│   │   ├── services/
│   │   │   └── auth_service.py
│   │   │
│   │   ├── schemas/
│   │   │   └── auth.py
│   │   │
│   │   ├── utils/
│   │   │   ├── dependencies.py
│   │   │   ├── security.py
│   │   │   └── validators.py
│   │   │
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── create_admin.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   │
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Game.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── AdminDailyReport.jsx
│   │   │   └── AdminUserReport.jsx
│   │   │
│   │   ├── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/guess-the-word.git
```

Move into the project:

```bash
cd guess-the-word
```

### 🐍 Backend Setup

Move to the backend directory:

```bash
cd backend
```

#### Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

### 🗄️ MongoDB Setup

Make sure MongoDB is running.

The application uses MongoDB to store:

- users
- words
- games
- guesses

Configure the MongoDB connection and JWT settings in `backend/.env`.

Example:

```env
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=word_game

JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> ⚠️ Do not commit your real `.env` file to GitHub.

### 👑 Create Admin User

Admin users are not created through the normal registration page.

Create an admin from the backend:

```bash
python -m app.create_admin
```

The admin account can then be used to access the Admin Dashboard.

Normal registration creates only `PLAYER` accounts.

Default admin credentials:

```text
Username: Admin
Password: Admin1$
```

### ▶️ Run the Backend

From the backend directory:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### ⚛️ Frontend Setup

Open another terminal.

Move to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

---

## 🎮 How to Play

1. Register as a player.
2. Login with your username and password.
3. Click **Start Game**.
4. A random 5-letter word is selected.
5. Enter a 5-letter guess.
6. The game provides color-based feedback:
   - Green → Correct position
   - Orange → Wrong position
   - Grey → Letter not present
7. You have a maximum of 5 guesses.
8. You can play a maximum of 3 games per day.

---

## 👨‍💼 Admin Usage

Login using an Admin account.

The Admin Dashboard provides:

### Daily Report

The admin can view game statistics for a particular day.

Example:

| Date       | Users Played | Correct Guesses |
|------------|---------------|------------------|
| 2026-08-14 | 5             | 3                |

### User Report

The admin can select a player and view their game history.

Example:

| Date       | Words Tried | Correct Guesses |
|------------|-------------|------------------|
| 2026-08-14 | 3           | 1                |
| 2026-08-13 | 3           | 0                |

---

## 🔐 Security

The application uses:

- JWT authentication
- Password hashing
- Role-based authorization
- Protected Admin endpoints
- Protected Player endpoints
- Environment variables for configuration
- CORS configuration for frontend-backend communication

Admin functionality is restricted to users with the `ADMIN` role.

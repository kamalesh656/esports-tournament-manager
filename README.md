# 🎮 Esports Tournament Management Platform

A full-stack platform to digitize esports tournament registration, bracket generation, scheduling, and live results — replacing manual spreadsheets and WhatsApp coordination.

## 🧾 Overview
College gaming clubs and small esports organizers currently manage tournaments through WhatsApp groups, Google Forms, and Excel sheets — leading to registration chaos, manual seeding errors, and result disputes. This platform provides a single source of truth: online registration, automated bracket generation, match scheduling, and a live leaderboard.

## 🏗️ Architecture
See `/docs/diagrams/architecture-diagram.png`

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| Frontend | React.js + Tailwind CSS + Axios |
| Backend | Django REST Framework |
| Auth | SimpleJWT |
| Database | SQLite (dev) |
| API Docs | drf-yasg (Swagger) |

## ✨ Features (so far)
- User registration & JWT-based login/authentication
- Role-based users: Admin/Organizer, Team Captain, Team Member
- Team creation and management
- Tournament creation, registration, and payment tracking (models)
- Match and match-result tracking (models)

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git

### Installation
```bash
git clone https://github.com/kamalesh656/esports-tournament-manager.git
cd esports-tournament-manager
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Environment Variables
See `.env.example`

## 📂 Folder Structure
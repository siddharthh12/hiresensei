# HIREsensei 🎓

**HIREsensei** is an intelligent, AI-powered job matching and career development platform designed to bridge the gap between job seekers and their dream roles. By leveraging advanced Natural Language Processing (NLP) and machine learning, HIREsensei analyzes resumes, matches them with relevant job opportunities, and identifies skill gaps to help users upskill effectively.

![HIREsensei Banner](https://via.placeholder.com/1200x400?text=HIREsensei+AI+Job+Matching)

## 🚀 Features

-   **📄 Smart Resume Parsing**: Automatically extracts skills, experience, education, and contact details from PDF and DOCX resumes using NLP (Spacy).
-   **🎯 AI Job Matching**: Matches users with jobs based on a comprehensive score that considers skills, role similarity, experience, and location.
-   **📍 Location-Aware Recommendations**: Prioritizes jobs in your preferred location or remote opportunities.
-   **📊 Skill Gap Analysis**: Identifies missing critical skills for desired roles and provides actionable insights.
-   **📈 Interactive Dashboard**: Visualizes profile completion, application stats, and market skill demand.
-   **💼 Job Tracking**: Keep track of saved, applied, and ignored job opportunities.

## 🛠️ Tech Stack

### Backend
-   **Framework**: FastAPI (Python)
-   **Database**: MongoDB (Motor async driver)
-   **NLP/ML**: Spacy, Scikit-learn
-   **Authentication**: JWT (JSON Web Tokens)

### Frontend
-   **Framework**: Next.js 13+ (App Router)
-   **Styling**: Tailwind CSS v4
-   **Charts**: Recharts
-   **State Management**: React Hooks

## 📂 Project Structure

```
HIREsensei/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── models/          # Pydantic Models
│   │   ├── routes/          # API Endpoints
│   │   ├── services/        # Business Logic (Matching, Parsing)
│   │   └── utils/           # Helper functions
│   └── ...
├── frontend/                # Next.js Frontend
│   ├── app/                 # App Router Pages
│   ├── components/          # Reusable UI Components
│   └── ...
└── README.md
```

## 🚦 Getting Started

### Prerequisites
-   Python 3.9+
-   Node.js 16+
-   MongoDB Instance

### Backend Setup
1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up environment variables (`.env`):
    ```
    MONGODB_URL=mongodb://localhost:27017
    DB_NAME=ai_job_matcher
    SECRET_KEY=your_secret_key
    ```
5.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
4.  Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

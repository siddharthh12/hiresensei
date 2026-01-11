from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, resume, jobs, recommend, job_tracking, dashboard, hybrid_jobs

app = FastAPI()

# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "https://hiresensei.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(jobs.router, prefix="/job", tags=["jobs"])
app.include_router(recommend.router, prefix="/jobs", tags=["recommendations"])
app.include_router(job_tracking.router, prefix="/tracking", tags=["tracking"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

app.include_router(hybrid_jobs.router, prefix="/hybrid-jobs", tags=["hybrid-jobs"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

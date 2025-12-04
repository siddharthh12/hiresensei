from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, resume, jobs, recommend, job_tracking, dashboard, skills

app = FastAPI()

# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
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
app.include_router(skills.router, prefix="/skills", tags=["skills"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

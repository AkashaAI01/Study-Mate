from fastapi import FastAPI

app = FastAPI(
    title="AK - Study Mate",
    description="AK, the WhatsApp AI study assistant",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Hi, I'm AK. Welcome to Study Mate!",
        "status": "Running",
        "project": "Study Mate",
        "agent": "AK",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Study Mate",
        "agent": "AK",
    }

    
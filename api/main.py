
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.pipeline import analyze_news
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Clickbait and Credibility Scoring API",
    description=(
        "Analyze a news headline for clickbait characteristics "
        "and estimate credibility using the trained models."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsRequest(BaseModel):
    headline: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="News headline to analyze",
    )
    article_text: str = Field(
        ...,
        min_length=1,
        description="Full or partial news article text",
    )

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict_news(request: NewsRequest):
    headline = request.headline.strip()
    article_text = request.article_text.strip()

    if not headline:
        raise HTTPException(
            status_code=422,
            detail="Headline cannot be empty or whitespace.",
        )

    if not article_text:
        raise HTTPException(
            status_code=422,
            detail="Article text cannot be empty or whitespace.",
        )
    try:
        result = analyze_news(headline, article_text)
        return result
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check the server logs.",
        ) from exc
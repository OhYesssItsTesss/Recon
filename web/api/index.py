from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import sys

# Add current dir to path to allow lib imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.scouts.trends import TrendScout
from lib.scouts.web import WebScout
from lib.strategist import Strategist

app = FastAPI()

class AnalysisRequest(BaseModel):
    topic: str
    email: Optional[str] = None
    provider: str = "gemini"

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/analyze")
async def analyze_topic(request: AnalysisRequest):
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required")
    
    try:
        # Initialize Scouts
        trend_scout = TrendScout()
        web_scout = WebScout()
        strategist = Strategist(provider=request.provider)
        
        # 1. Gather Data (Reduced depth for speed/lambda limits)
        trend_data = trend_scout.analyze(request.topic)
        discussions = web_scout.search_reddit(request.topic, limit=3)
        
        # 2. Analyze
        report = strategist.generate_report(request.topic, trend_data, discussions)
        
        if "error" in report:
            raise HTTPException(status_code=500, detail=report["error"])
            
        return {
            "topic": request.topic,
            "trends": trend_data,
            "report": report
        }
        
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

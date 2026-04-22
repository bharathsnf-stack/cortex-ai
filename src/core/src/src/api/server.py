"""
FastAPI Server - REST API for Cortex AI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import logging

from src.core.brain import CortexBrain

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cortex AI API",
    description="AI Assistant API",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize brain
brain = CortexBrain(config={})


class QueryRequest(BaseModel):
    """Request model for queries"""
    text: str
    context: Optional[Dict] = None


class QueryResponse(BaseModel):
    """Response model for queries"""
    response: str
    intent: str
    timestamp: str
    confidence: float


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Cortex AI",
        "version": "1.0.0"
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a user query
    
    Args:
        request: QueryRequest with user text
        
    Returns:
        AI-generated response
    """
    try:
        result = await brain.process_input(request.text)
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory")
async def get_memory(limit: int = 10):
    """Retrieve recent memory"""
    return {
        "memory": brain.get_memory(limit=limit)
    }


@app.delete("/memory")
async def clear_memory():
    """Clear brain memory"""
    brain.clear_memory()
    return {"status": "memory cleared"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "memory_size": len(brain.memory),
        "plugins_loaded": len(brain.plugins)
    }

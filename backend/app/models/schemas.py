"""
Pydantic models for request/response validation
"""

# Import Libraries
from pydantic import BaseModel, Field
from datetime import datetime

class HealthCheckResponse(BaseModel):
    """Health Check Endpoint Response"""
    status: str
    timestamp: datetime
    message: str


class ChatRequest(BaseModel):
    
    message: str = Field(..., description="User's Medical Question", min_length=1, max_length=1000)
    language: str = Field(default="en", description="Response Language (en/fr)", pattern="^(en|fr)$")


class ChatResponse(BaseModel):
    
    response: str
    language: str
    timestamp: datetime


class AnalysisRequest(BaseModel):
    """Medical Record Analysis Request (for text input)"""
    text: str = Field(..., description="Medical Record Text to Analyze", min_length=1)
    context: str = Field(default="", description="Additional Context About the Patient")
    language: str = Field(default="en", description="Response Language")


class MedicalAnalysis(BaseModel):
    """Medical Analysis"""
    summary: str = Field(description="Brief Overview of the Medical Record")
    key_findings: list[str] = Field(description="List of Important Findings")
    recommendations: list[str] = Field(description="Health Recommendations")
    next_steps: list[str] = Field(description="Suggested Next Steps")


class AnalysisResponse(BaseModel):
    
    summary: str
    key_findings: list[str]
    recommendations: list[str]
    next_steps: list[str]
    disclaimer: str
    language: str
    timestamp: datetime


class ImageAnalysisResponse(BaseModel):
    """Image Analysis Response"""
    extracted_text: str
    analysis: AnalysisResponse


class ResearchRequest(BaseModel):
    """Research Request Model"""
    query: str = Field(..., description="Medical Topic to Research", min_length=3, max_length=200)
    max_results: str = Field(default=5, description="Number of Results", ge=1, le=10)
    language: str = Field(default="en", description="Response Language")


class ResearchResult(BaseModel):
    """Single Research Result"""
    title: str
    url: str
    content: str
    score: float


class ResearchResponse(BaseModel):
    """Research Response Model"""
    query: str
    results: list[ResearchResult]
    summary: str
    timestamp: datetime

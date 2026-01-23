"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Literal, Optional


# Request Models
class ChatRequest(BaseModel):
    """Chat message request."""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    mode: Literal["assistant", "shopping"] = Field(default="assistant", description="Conversation mode")
    conversation_history: list[dict] = Field(default_factory=list, description="Previous messages")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Help me find a good laptop",
                "mode": "shopping",
                "conversation_history": []
            }
        }


class ShopRequest(BaseModel):
    """Product search request."""
    query: str = Field(..., min_length=1, max_length=200, description="Search query")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "wireless headphones"
            }
        }


# Response Models
class ChatResponse(BaseModel):
    """Chat message response."""
    message: str = Field(..., description="AI assistant response")
    mode: str = Field(..., description="Current conversation mode")
    products: Optional[list[dict]] = Field(default=None, description="Product results if shopping mode")


class Product(BaseModel):
    """Product information."""
    name: str
    price: float
    image: str
    images: list[str]
    description: str
    rating: float
    source: str


class ShopResponse(BaseModel):
    """Product search response."""
    query: str = Field(..., description="Original search query")
    products: list[Product] = Field(..., description="List of products")
    count: int = Field(..., description="Number of products found")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(default="healthy")
    version: str
    openai_configured: bool


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None

"""
NUVEXA Mobile - FastAPI Backend
Main application entry point.
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.models.schemas import (
    ChatRequest, ChatResponse,
    ShopRequest, ShopResponse,
    HealthResponse, ErrorResponse
)
from app.services.openai_service import OpenAIService
from app.services.shopping_service import ShoppingService
from app.middleware.error_handler import (
    validation_exception_handler,
    general_exception_handler
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Initialize services
openai_service = OpenAIService()
shopping_service = ShoppingService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"OpenAI Model: {settings.openai_model}")
    yield
    logger.info("Shutting down application")


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Mobile-first AI assistant with shopping capabilities",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# Routes
@app.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.get("/api/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        openai_configured=bool(settings.openai_api_key)
    )


@app.post("/api/chat", response_model=ChatResponse, tags=["chat"])
async def chat(request: ChatRequest):
    """
    Chat with AI assistant.

    - **message**: User's message
    - **mode**: Conversation mode (assistant/shopping)
    - **conversation_history**: Previous messages for context
    """
    try:
        logger.info(f"Chat request - Mode: {request.mode}, Message length: {len(request.message)}")

        # Get AI response
        ai_response = await openai_service.get_chat_response(
            message=request.message,
            mode=request.mode,
            history=request.conversation_history
        )

        # If shopping mode, search for products
        products = None
        if request.mode == "shopping":
            query = openai_service.extract_product_query(request.message)
            if query:
                product_results = shopping_service.search_products(query)
                if product_results:
                    products = product_results
                    logger.info(f"Found {len(products)} products for query: {query}")

        return ChatResponse(
            message=ai_response,
            mode=request.mode,
            products=products
        )

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat request: {str(e)}"
        )


@app.post("/api/shop", response_model=ShopResponse, tags=["shopping"])
async def shop(request: ShopRequest):
    """
    Search for products.

    - **query**: Product search query
    """
    try:
        logger.info(f"Shop request - Query: {request.query}")

        products = shopping_service.search_products(request.query)

        return ShopResponse(
            query=request.query,
            products=products,
            count=len(products)
        )

    except Exception as e:
        logger.error(f"Shop error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search products: {str(e)}"
        )


@app.get("/api/modes", tags=["modes"])
async def get_modes():
    """Get available conversation modes."""
    return {
        "modes": [
            {
                "id": "assistant",
                "name": "Assistant",
                "icon": "🤖",
                "description": "General AI assistant for help and advice"
            },
            {
                "id": "shopping",
                "name": "Shopping",
                "icon": "🛒",
                "description": "Find and compare products"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

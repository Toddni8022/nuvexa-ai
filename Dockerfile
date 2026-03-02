FROM python:3.12-slim

# Metadata
LABEL maintainer="NUVEXA Team"
LABEL description="NUVEXA AI — Living AI assistant with execution power"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app.py assistant.py config.py database.py shopping.py ./

# Create volume mount point for persistent database
VOLUME ["/app/data"]

# Expose Streamlit default port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
ENTRYPOINT ["python", "-m", "streamlit", "run", "app.py", \
            "--server.port=8501", "--server.address=0.0.0.0"]

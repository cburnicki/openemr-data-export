FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy pyproject.toml first for better layer caching
COPY pyproject.toml .

# Install dependencies using uv with --system flag
RUN uv pip install --system .

# Copy the application code
COPY . .

# Set environment variables with defaults
ENV DB_HOST=mysql
ENV DB_PORT=3306
ENV DB_USER=openemr
ENV DB_PASSWORD=openemr
ENV DB_NAME=openemr

# Create exports directory
RUN mkdir -p exports

# Run the export script
ENTRYPOINT ["python", "main.py"]

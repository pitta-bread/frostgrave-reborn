# Use the official Astral uv Python Bookworm slim image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set workdir
WORKDIR /app

# Copy project files
COPY . .

# Install Python and any dependencies
RUN uv sync

# Expose port (default Django/Gunicorn port)
EXPOSE 8000

# Start the app using the start script
CMD ["./start.sh"]

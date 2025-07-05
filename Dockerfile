# ✅ Use official Selenium base image with Chrome + Python support
FROM selenium/standalone-chrome:latest

# Install Python tools (it's based on Debian, so apt works)
USER root

# Upgrade pip and install required packages
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install --no-cache-dir pytest selenium

# Optional: set working dir
WORKDIR /tests

# Copy test files into the container
COPY . .

# Default command to run tests (can be overridden)
CMD ["pytest", "--maxfail=5", "--disable-warnings", "-q"]

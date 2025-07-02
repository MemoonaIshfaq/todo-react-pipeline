# Use a Selenium-ready Python image (includes Chrome, drivers, Xvfb, GTK, etc.)
FROM seleniarm/python:3.11

# Set environment variables to avoid issues with headless browsers
ENV DISPLAY=:99

# Set the working directory inside the container
WORKDIR /app

# Copy your project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run tests (you can override in docker-compose)
CMD ["pytest", "--maxfail=5", "--disable-warnings", "-q"]

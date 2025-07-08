# Use a compatible Node version
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy only package files first (for layer caching)
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the app
COPY . .

# Build the app
RUN npm run build

# Install serve globally
RUN npm install -g serve

# Expose port and run the app
EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]

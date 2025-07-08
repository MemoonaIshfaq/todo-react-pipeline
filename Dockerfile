# Use lighter Node base image
FROM node:18-alpine AS builder

WORKDIR /app

# Only copy necessary files first for layer caching
COPY package*.json ./

# Install dependencies faster with optional peer dep bypass
RUN npm install --legacy-peer-deps

# Now copy rest of the code
COPY . .

# Build static files
RUN npm run build

# ---------- Production image ----------
FROM node:18-alpine

# Install serve only in production image
RUN npm install -g serve

WORKDIR /app

# Copy only build artifacts from previous stage
COPY --from=builder /app/build ./build

# Serve the static files
EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]

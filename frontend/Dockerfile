# Use an official Node.js base image
FROM node:20-slim

# Set working directory
WORKDIR /app

# Install dependencies first (leverages Docker cache)
COPY package*.json ./
RUN npm install --omit=dev

# Install additional packages explicitly
RUN npm install @types/react @types/react-dom styled-components framer-motion

# Copy all source code
COPY . .

# Expose the frontend port (adjust if your app uses a different one)
EXPOSE 3000

# Default command to start your frontend app
CMD ["npm", "start"]

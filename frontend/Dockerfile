# Use the official Node.js image
FROM node:20

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend source code
COPY . .

# Build the app for production
RUN npm run build

# Install `serve` to serve the production build
RUN npm install -g serve

# Command to serve the built app
CMD ["serve", "-s", "dist"]

# Expose the frontend port
EXPOSE 3000

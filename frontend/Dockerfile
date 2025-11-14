# syntax=docker/dockerfile:1

# Build stage: compile the Vite application
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies first to leverage Docker layer caching
COPY package*.json ./
RUN npm ci

# Copy the rest of the source code and build the production bundle
COPY . .
RUN npm run build

# Production stage: serve the built assets with nginx
FROM nginx:alpine AS production

# Copy the built assets from the build stage to the nginx public folder
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
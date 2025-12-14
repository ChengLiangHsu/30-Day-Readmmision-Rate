# Stage 1: Build Frontend
# Using Debian-based image (slim) instead of Alpine to fix binary compatibility issues (e.g. esbuild)
FROM node:20-slim as build-step
WORKDIR /app/frontend

# Copy ONLY package.json to force fresh dependency resolution for Linux
COPY frontend/package.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Stage 2: Backend
FROM python:3.9-slim

WORKDIR /app

# Copy Backend Requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn

# Copy Backend Code
COPY backend ./backend

# Copy Models & Data (Root files)
COPY *.pkl ./
COPY *.csv ./

# Copy Built Frontend from Stage 1
COPY --from=build-step /app/frontend/dist ./frontend/dist

# Expose Port
EXPOSE 5000

# Run Gunicorn
# app object is in backend/app.py, so module is backend.app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "backend.app:app"]

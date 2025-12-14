# Stage 1: Build Frontend
FROM node:18-alpine as build-step
WORKDIR /app/frontend
COPY frontend/package*.json ./
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

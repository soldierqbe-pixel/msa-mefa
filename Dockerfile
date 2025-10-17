# --- Build Frontend ---
FROM node:18 AS frontend
WORKDIR /frontend
COPY frontend/ ./
RUN npm install && npm run build

# --- Backend (FastAPI) ---
FROM python:3.11-slim
WORKDIR /app

# Copy backend
COPY backend/ ./backend/
WORKDIR /app/backend

# Install deps
RUN pip install --no-cache-dir -r requirements.txt &&     pip install reportlab psycopg2-binary

# Copy built frontend to static/
COPY --from=frontend /frontend/dist /app/backend/app/static

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

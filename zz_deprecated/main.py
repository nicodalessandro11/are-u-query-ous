# Placeholder content for backend/main.py

from fastapi import FastAPI
from backend.db import get_connection

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is working!"}

@app.get("/test")
def get_test_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, value FROM test_data")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "name": r[1], "value": r[2]} for r in rows]

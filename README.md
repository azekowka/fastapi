step-0: python -m venv venv, .\venv\Scripts\activate
step-1: pip install fastapi uvicorn or pip install fastapi[standard] 
step-2: create app.py file
step-3: uvicorn main:app --reload
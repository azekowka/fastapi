from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/", summary="Root endpoint", tags=["General documentation"])
def read_root():
    return {"message": "Hello, FastAPI!"}

if __name__ == "__main__":
    uvicorn.run(app, reload=True)
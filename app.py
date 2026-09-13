from fastapi import FastAPI

app = FastAPI(title="GatherUp Test")

@app.get("/")
def test():
    return {"status": "working"}
from fastapi import FastAPI, Query

app = FastAPI(title="branch-protection-poc-api", version="1.0.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/greet")
def greet(name: str = Query(..., min_length=1)) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}

from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from handlers import fastapi_auto_test_run

app = FastAPI()
app.include_router(fastapi_auto_test_run.router)


@app.get("/")
def home_page():
    html_content = """
    <h1> Welcome !!!! </h1>
    <h3> You can go to "/docs" to view the endpoints to run your test <h3>
    """
    return HTMLResponse(html_content)


if __name__ == "__main__":
    uvicorn.run(app=app)

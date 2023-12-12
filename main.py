from uvicorn import run
from fastapi import FastAPI
from routers import router


app = FastAPI(
    title="Test_Api", version='v0.1',
    description="Description",
    docs_url='/docs', redoc_url='/docs/redoc'
)

app.include_router(router=router)

if __name__ == "__main__":
    run('main:app', host='127.0.0.1', port=8080)
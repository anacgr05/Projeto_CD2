from fastapi import FastAPI
from routers import predict

app = FastAPI(
    title="API de Predição de Fraude",
    description="API da Aula 2 - dados sintéticos, serialização e serving de modelo",
    version="1.0.0"
)

app.include_router(predict.router, prefix="/ml", tags=["ML"])


@app.get("/")
async def root():
    return {
        "message": "API de ML no ar",
        "projeto": "Aula 2 - e03 dados sintéticos"
    }
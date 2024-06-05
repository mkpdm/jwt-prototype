from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    icon = Path(__file__).parent.absolute() / "public/icons/favicon-32x32.png"
    return FileResponse(icon)


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)

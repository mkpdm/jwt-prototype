from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()
"""Design Fundamentals:

    - use hyphens for uri's (/users/items-in-the-box) to allow for crawlers/indexing.
    - use snake_case for keys in models. (increase readability)
    - keep routes in the same routers (don't split /users/ across multiple routers/modules)
    - keep TTR to < 5s. Use callbacks or websockets for long lived connections.
    - https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design
    - https://www.ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf#page=11
"""


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

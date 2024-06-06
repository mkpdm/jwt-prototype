from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from mkapi.routers import auth

app = FastAPI()
"""Design Fundamentals:

    - use hyphens for uri's (/users/items-in-the-box) to allow for crawlers/indexing.
    - use snake_case for keys in models. (increase readability)
    - keep routes in the same routers (don't split /users/ across multiple routers/modules)
    - keep TTR to < 5s. Use callbacks or websockets for long lived connections.
    - https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design
    - https://www.ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf#page=11
"""

# Include the item and user routers
app.include_router(auth.router, tags=["auth"])


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    icon = Path(__file__).parent.absolute() / "public/icons/favicon-32x32.png"
    return FileResponse(icon)


@app.get("/")
def get_root():
    return {"msg": "Hello World"}


@app.get("/info")
def get_info():
    return {"msg": "Info endpoint"}

import uvicorn

from mkapi import app

uvicorn.run(app, port=8080)

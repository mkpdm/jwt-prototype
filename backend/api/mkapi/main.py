import os
from pathlib import Path

import jwt
import boto3
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from passlib.context import CryptContext

from typing import Annotated
from pydantic import BaseModel

from botocore.exceptions import ClientError
from jwt.exceptions import InvalidTokenError


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


# TODO: Investigate what happens if stacks are deployed in multiple regions.
USER_POOL_ID = os.getenv("USERPOOL_ID")
CLIENT_ID = os.getenv("USERPOOL_CLIENT_ID")
REGION = os.getenv("REGION")

USER_POOL_ID = "eu-west-2_SRo9mKuV0"
CLIENT_ID = "2vs6hl0m5q5cf2cc10qsmsrudo"
REGION = "eu-west-2"

jwks_client = jwt.PyJWKClient(
    f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

"""Design Fundamentals:

    - use hyphens for uri's (/users/items-in-the-box) to allow for crawlers/indexing.
    - use snake_case for keys in models. (increase readability)
    - keep routes in the same routers (don't split /users/ across multiple routers/modules)
    - keep TTR to < 5s. Use callbacks or websockets for long lived connections.
    - https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design
    - https://www.ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf#page=11
"""


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    client = boto3.client("cognito-idp", region_name=REGION)
    try:
        response = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": form_data.username,
                "PASSWORD": form_data.password,
            },
            ClientId=CLIENT_ID,
        )
    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    return {
        "access_token": response["AuthenticationResult"]["AccessToken"],
        "token_type": "bearer",
    }


async def user_token(encoded_token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = jwt.decode(
            encoded_token,
            jwks_client.get_signing_key_from_jwt(encoded_token).key,
            algorithms=["RS256"],
            audience=["account"],
        )
        username: str = token.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    if token is None:
        raise credentials_exception
    return token


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


@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected route", "user": token}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

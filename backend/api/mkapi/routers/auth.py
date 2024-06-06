from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from mkapi.core.environment import (
    COGNITO_DOMAIN,
    COGNITO_CLIENT_ID,
    COGNITO_CLIENT_SECRET,
    COGNITO_REDIRECT_URI,
    COGNITO_REGION,
    COGNITO_USER_POOL_ID,
)

router = APIRouter()


# quick and nasty static site for this endpoint, while debugging CDK
# TODO: Move frontend to react-ts / client.
@router.get("/login", response_class=HTMLResponse)
async def login():
    AUTH_URL = f"https://{COGNITO_DOMAIN}/oauth2/authorize"
    TOKEN_URL = f"https://{COGNITO_DOMAIN}/oauth2/token"
    LOGOUT_URL = f"https://{COGNITO_DOMAIN}/logout"

    return f"""
    <html>
        <head>
            <title>Login</title>
        </head>
        <body>
            <form action="{AUTH_URL}" method="get">
                <input type="hidden" name="response_type" value="code" />
                <input type="hidden" name="client_id" value="{COGNITO_CLIENT_ID}" />
                <input type="hidden" name="redirect_uri" value="{COGNITO_REDIRECT_URI}" />
                <input type="submit" value="Login with AWS Cognito" />
            </form>
        </body>
    </html>
    """

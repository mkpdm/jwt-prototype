import os
from pathlib import Path

from dotenv import load_dotenv

from typing import Final

# TODO: OOP singleton pattern may be a better way to define stage/environment config.

# DOTENV PATHS
ENV_PATH_ROOT: Final = Path(__file__).parent.parent.absolute()
DOTENV_SHARED_PATH: Final = ENV_PATH_ROOT / ".env"
DOTENV_DEV_PATH: Final = ENV_PATH_ROOT / ".env.dev"

load_dotenv(DOTENV_SHARED_PATH)

STAGE: Final = (
    os.environ.get("MKPDM_API_STAGE")
    if os.environ.get("MKPDM_API_STAGE") is not None
    else "DEV"
)

match STAGE:
    case "PROD":
        raise NotImplementedError(
            "Prod stage has not yet been implemented. please change stage."
        )
    case "DEV" | _:
        load_dotenv(DOTENV_DEV_PATH)

COGNITO_DOMAIN = os.environ.get("COGNITO_DOMAIN")
COGNITO_REGION = os.environ.get("COGNITO_REGION")

COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
COGNITO_CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.environ.get("COGNITO_CLIENT_SECRET")
COGNITO_REDIRECT_URI = os.environ.get("COGNITO_REDIRECT_URI")

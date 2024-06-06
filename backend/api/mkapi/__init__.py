"""MKPDM API prototype built on fastapi."""

__version__ = "0.1.0"
from .main import app as app
# TODO: Having __main__ outside of package does not seem correct. Need to refine absolute import pattern. below are some potential solutions.
# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
# __all__ = ["models", "core", "routers", "core.config"]

# from .core.config import environment as environment
# from .core.config import pydantic as pydantic
# from .core.config import cognito as cognito
# from .routers import auth as auth

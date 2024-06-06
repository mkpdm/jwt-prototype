from constructs import Construct
from aws_cdk import Stack

import aws_cdk.aws_cognito as cognito

from typing_extensions import Final

AUTH_POOL_ID: Final = "auth_pool"
AUTH_POOL_NAME: Final = "auth_pool"

MFA_ENABLED: Final = cognito.Mfa.OPTIONAL
MFA_MESSAGE: Final = "Your Authentication Code for mkpdm is {####}."

USER_VERIFICATION_CONFIG = cognito.UserVerificationConfig(
    email_body="The verification code to your new account is {####}' if VerificationEmailStyle.CODE is chosen, 'Verify your account by clicking on {##Verify Email##}"
)


class AuthStack(Stack):
    """Stack containing Cognito Resources"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.userpool = cognito.UserPool(
            self,
            AUTH_POOL_ID,
            user_pool_name=AUTH_POOL_NAME,
            sign_in_aliases={"username": True, "email": True, "phone": True},
            mfa=MFA_ENABLED,
            mfa_message=MFA_MESSAGE,
            user_verification=USER_VERIFICATION_CONFIG,
        )

        self.appclient = cognito.UserPoolClient(
            self,
            f"{AUTH_POOL_NAME}_client",
            user_pool=self.userpool,
            user_pool_client_name=f"{AUTH_POOL_NAME}_client",
        )

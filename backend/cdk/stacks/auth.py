from constructs import Construct
from aws_cdk import Stack

import aws_cdk.aws_ssm as ssm
import aws_cdk.aws_cognito as cognito
import aws_cdk.aws_secretsmanager as secretsmanager

from typing_extensions import Final

USERPOOL_ID: Final = "auth_pool"
USERPOOL_CLIENT_ID: Final = "auth_client"

USERPOOL_NAME: Final = "auth_pool"
USERPOOL_CLIENT_NAME: Final = "auth_client"

MFA_ENABLED: Final = cognito.Mfa.OPTIONAL
MFA_MESSAGE: Final = "Your Authentication Code for mkpdm is {####}."

USER_VERIFICATION_CONFIG = cognito.UserVerificationConfig(
    email_body="The verification code to your new account is {####}' if VerificationEmailStyle.CODE is chosen, 'Verify your account by clicking on {##Verify Email##}"
)


class AuthStack(Stack):
    """Stack containing Cognito Resources"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # constructs
        self.userpool = cognito.UserPool(
            self,
            USERPOOL_ID,
            user_pool_name=USERPOOL_NAME,
            sign_in_aliases={"username": True, "email": True, "phone": True},
            mfa=MFA_ENABLED,
            mfa_message=MFA_MESSAGE,
            user_verification=USER_VERIFICATION_CONFIG,
        )

        self.appclient = cognito.UserPoolClient(
            self,
            USERPOOL_CLIENT_ID,
            user_pool=self.userpool,
            user_pool_client_name=USERPOOL_CLIENT_NAME,
            generate_secret=True,
        )

        # outputs - REGION, USERPOOL_ID, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
        # TODO:/{stack_name}/{module}/{key} would be better.
        # e.g /auth/cognito/userpool_id
        config_outputs = {
            "userpool/id": self.userpool.user_pool_id,
            "userpool/client_id": self.appclient.user_pool_client_id,
            # self.appclient.o_auth_flows - TODO: CALLBACK URI
        }

        secret_outputs = {
            "userpool/client_secret": self.appclient.user_pool_client_secret
        }

        for key, output in config_outputs.items():
            ssm.StringParameter(
                scope=self,
                id=f"/ssm/{construct_id}/{key}",
                parameter_name=f"/{construct_id}/{key}",
                string_value=output,
            )

        for key, secret in secret_outputs.items():
            secretsmanager.Secret(
                scope=self,
                id=f"/ssm/{construct_id}/{key}",
                secret_name=f"/{construct_id}/{key}",
                secret_string_value=secret,
            )

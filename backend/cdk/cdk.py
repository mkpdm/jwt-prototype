import aws_cdk

from stacks.auth import AuthStack
from stacks.api import FastAPIStack

CDK_DEFAULT_ACCOUNT = "default"

app = aws_cdk.App()

stack = AuthStack(
    app,
    "AuthStack",
    env={"region": "eu-west-2"},
)

stack = FastAPIStack(
    app,
    "FastAPIStack",
    env={"region": "eu-west-2"},
)


app.synth()

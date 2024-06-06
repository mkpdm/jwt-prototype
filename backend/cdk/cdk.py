import aws_cdk
from stacks.auth import AuthStack

app = aws_cdk.App()
AuthStack(app, "AuthStack")
app.synth()
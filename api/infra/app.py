import aws_cdk as cdk

from infra_cdk.infra_cdk_stack import InfraCdkStack

app = cdk.App()
InfraCdkStack(app, "InfraCdkStack")

app.synth()

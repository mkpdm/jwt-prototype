from constructs import Construct
from aws_cdk import Stack

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ssm as ssm
import aws_cdk.aws_ecs_patterns as ecs_patterns

from typing_extensions import Final

AUTH_STACK_ID: Final = "AuthStack"

VPC_ID: Final = "jwt_vpc"
ECS_CLUSTER_ID: Final = "jwt_cluster"
ECS_SERVICE_ID: Final = "jwt_service"

ECS_CLUSTER_NAME: Final = None


class FastAPIStack(Stack):
    """Stack to deploy FastAPI ECS Cluster."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # secrets to be injected into Docker Build Env / FASTAPI
        userpool_id = ssm.StringParameter.value_for_string_parameter(
            scope=self,
            parameter_name=f"/{AUTH_STACK_ID}/userpool/id",
        )
        userpool_client_id = ssm.StringParameter.value_for_string_parameter(
            scope=self,
            parameter_name=f"/{AUTH_STACK_ID}/userpool/client_id",
        )

        # directory is relative from cdk executable
        task_image = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_asset(
                asset_name="fastapi",
                directory="../api",
            ),
            environment={
                "USERPOOL_ID": userpool_id,
                "USERPOOL_CLIENT_ID": userpool_client_id,
                "REGION": self.region,
            },
        )

        self.vpc = ec2.Vpc(self, VPC_ID)

        self.ecs_cluster = ecs.Cluster(
            self,
            ECS_CLUSTER_ID,
            cluster_name=ECS_CLUSTER_NAME,
            vpc=self.vpc,
            container_insights=False,
        )

        self.ecs_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            ECS_SERVICE_ID,
            desired_count=2,
            cpu=256,
            memory_limit_mib=512,
            cluster=self.ecs_cluster,
            task_image_options=task_image,
        )

import os
import subprocess
import configparser
from aws_cdk import (
    Stack,
    aws_lambda as function,
    aws_apigateway as api
)
from constructs import Construct

class LambdaReadZipStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        read_zip_lambda_name = "read-zip-function"
        read_zip_api_name = "read-zip-api"

        dependencies_layer = self.create_dependencies_layer(
            self.stack_name, read_zip_lambda_name
        )

        configs = self.get_configs()

        read_zip_lambda = function.Function(
            self,
            read_zip_lambda_name,
            handler="function.handler",
            runtime=function.Runtime.PYTHON_3_8,
            code=function.Code.from_asset("src/lambdas/zip"),
            layers=[dependencies_layer],
        )
        read_zip_lambda.add_environment("URL", configs["url"])

        api.LambdaRestApi(
            self,
            read_zip_api_name,
            handler=read_zip_lambda
        )

    def get_configs(self):
        config = configparser.ConfigParser()
        config.read("environment.ini")
        return config.defaults()

    def create_dependencies_layer(self, stack_name, function_name):
        requirements_file = "src/requirements.txt"
        output_dir = f"layer/{function_name}"

        if not os.environ.get("SKIP_PIP"):
            subprocess.check_call(
                f"pip install -r {requirements_file} -t {output_dir}/python --upgrade".split()
            )

        layer_id = f"{stack_name}-{function_name}-dependencies"
        layer_code = function.Code.from_asset(output_dir)
        return function.LayerVersion(self, layer_id, code=layer_code)

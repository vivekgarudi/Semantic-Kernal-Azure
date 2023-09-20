import math
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
import requests
import csv
import json
from semantic_kernel.orchestration.sk_context import SKContext
from azure.devops.v7_1.py_pi_api import JsonPatchOperation
import os
import sys
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import base64
import requests
from semantic_kernel import ContextVariables, Kernel
import re
import os
import pandas as pd
from datetime import timedelta
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
import plotly.express as px
class sloganalytics:
    def __init__(self, kernel: Kernel):
        self._kernel = kernel
    @sk_function(
        description="create a Azure DevOps feature with description",
        name="slquery",
    )
    @sk_function_context_parameter(
        name="title",
        description="the tile of the feature",
    )
    @sk_function_context_parameter(
        name="description",
        description="Description of the feature",
    )
    async def create_feature(self, context: SKContext) -> str:
       # Copyright (c) Microsoft Corporation. All rights reserved.
        # [START client_auth_with_token_cred]
        print("we are here")
        get_feature = self._kernel.skills.get_function("AzureMonitor", "KQLquery")
        Ctxtquery = get_feature(context["title"])
        credential  = DefaultAzureCredential()
        client = LogsQueryClient(credential)
        txtquery=str(Ctxtquery)
        #txtquery='"' + txtquery + '"' 
        print(txtquery)
        LOGS_WORKSPACE_ID="81a662b5-8541-481b-977d-5d956616ac5e"
        response = client.query_workspace(LOGS_WORKSPACE_ID,txtquery,timespan=timedelta(days=1))
        try: 
            print(txtquery)           
            if response.status == LogsQueryStatus.PARTIAL:
                error = response.partial_error
                data = response.partial_data
            elif response.status == LogsQueryStatus.SUCCESS:
                viz = response.visualization
                data = response.tables
            for table in data:
                df = pd.DataFrame(data=table.rows, columns=table.columns)
                context["df"] = df
                return df
        except HttpResponseError as err:
            print (err)
            return err
       
    

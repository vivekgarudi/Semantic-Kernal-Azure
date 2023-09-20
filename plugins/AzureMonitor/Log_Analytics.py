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
class loganalytics:
    def __init__(self, kernel: Kernel):
        self._kernel = kernel
    @sk_function(
        description="create a Azure DevOps feature with description",
        name="lquery",
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
        credential  = DefaultAzureCredential()
        client = LogsQueryClient(credential)
        # [END client_auth_with_token_cred]
        # [START send_logs_query]
        # Add some documents to the semantic memory
        import csv
        csv_file_path=r"C:\Users\vigarudi\Documents\code\Python\All_togather\plugins\AzureMonitor\Query.csv"
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            x=0
            # Loop through each row in the CSV file
            for row in reader:
            # Each row is a list of values
            # Access values by index, e.g., row[0], row[1], ...        
                if row[0] != "context":
                    txq=row[0]+":"+row[1]
                    infoid="info"+str(x)
                    await self._kernel.memory.save_information_async("Query", id=infoid, text=txq)
                x=x+1    
        query= await self._kernel.memory.search_async("Query", context["title"])
        txtquery=query[0].text.split(":")[1]      
        print(txtquery)  
        LOGS_WORKSPACE_ID="81a662b5-8541-481b-977d-5d956616ac5e"
        
        try:
            response = client.query_workspace(LOGS_WORKSPACE_ID, txtquery, timespan=timedelta(days=1))
            if response.status == LogsQueryStatus.PARTIAL:
                error = response.partial_error
                data = response.partial_data
                print(error)
            elif response.status == LogsQueryStatus.SUCCESS:
                viz = response.visualization
                data = response.tables
            for table in data:
                df = pd.DataFrame(data=table.rows, columns=table.columns)
                #print(df)
            context["df"] = df
            return df
                #print(df)                
            # Output visualization to a file.
            #
        except HttpResponseError as err:
            print(txtquery)
            print (err)
            return err
       
    

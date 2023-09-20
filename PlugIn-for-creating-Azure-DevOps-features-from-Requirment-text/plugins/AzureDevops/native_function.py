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
class feature:
    def __init__(self, kernel: Kernel):
        self._kernel = kernel
    @sk_function(
        description="create a Azure DevOps feature with description",
        name="create",
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
        feature_title = context["title"]
        get_feature = self._kernel.skills.get_function("AzureDevOps", "FeatureDescription")
        #getfeatureContext = (
        #    await self._kernel.run_async(get_feature, input_str=feature_title)
        #).result
        fdetails = get_feature(feature_title)
        # Define a regular expression pattern to match the feature title
        pattern = r"Feature Title:\s+(.+)"
        # Search for the pattern in the input string
        match = re.search(pattern, str(fdetails))
        # Check if a match was found
        if match:
            feature_title = match.group(1)
        # Define a regular expression pattern to match the feature description
        # Split the string into lines
        lines = str(fdetails).split('\n')
        lines = [line for index, line in enumerate(lines) if index not in [0]]
        description = '\n'.join(lines)
        relationPatchList = []
        jsonPatchList = []
        workObjects = []        
        #description=context["description"]
        targetOrganizationName= "XXX"
        targetProjectName= "test"
        targetOrganizationPAT = "XXXXXX"
        workItemCsvFile= "abc"
        teamName = "test Team"
        areaName = teamName
        iterationName ="Sprint 1"
        targetOrganizationUri='https://dev.azure.com/'+targetOrganizationName
        credentials = BasicAuthentication('', targetOrganizationPAT)
        connection = Connection(base_url=targetOrganizationUri, creds=credentials)
        userToken = "" + ":" + targetOrganizationPAT
        base64UserToken = base64.b64encode(userToken.encode()).decode()
        headers = {'Authorization': 'Basic' + base64UserToken}
        core_client = connection.clients.get_core_client()
        targetProjectId = core_client.get_project(targetProjectName).id
        workItemObjects = [
                {
                    'op': 'add',
                    'path': '/fields/System.WorkItemType',
                    'value': "Feature"
                },
                {
                    'op': 'add',
                    'path': '/fields/System.Title',
                    'value': feature_title
                },
                {
                    'op': 'add',
                    'path': '/fields/System.State',
                    'value': "New"
                },
                {
                    'op': 'add',
                    'path': '/fields/System.Description',
                    'value': description
                },
                {
                    'op': 'add',
                    'path': '/fields/Microsoft.VSTS.Common.AcceptanceCriteria',
                    'value': "acceptance criteria"
                },      
                {
                    'op': 'add',
                    'path': '/fields/System.IterationPath',
                    'value': targetProjectName+"\\"+iterationName
                }
            ]
        jsonPatchList = JsonPatchOperation(workItemObjects)
        work_client = connection.clients.get_work_item_tracking_client()
        try:
            WorkItemCreation = work_client.create_work_item(jsonPatchList.from_, targetProjectName, "Feature")
        except Exception as e:
            return feature_title+"Feature created unsuccessfully"
        return feature_title+" Feature created successfully"
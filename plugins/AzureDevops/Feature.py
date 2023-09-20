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

class feature:
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
        relationPatchList = []
        jsonPatchList = []
        workObjects = []
        feature_title = context["title"]
        description=context["description"]
        targetOrganizationName= "vigarudi0944"
        targetProjectName= "test"
        targetOrganizationPAT = "mzt352ysyicsfwe75rl2bw3y6jhvu75js3pnraowkmr3e32uy42a"
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
        WorkItemCreation = work_client.create_work_item(jsonPatchList.from_, targetProjectName, "Feature")
        return "feature created successfully"
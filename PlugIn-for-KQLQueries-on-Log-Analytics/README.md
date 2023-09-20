# Creating a Semantic Function-Based Solution for KQL Queries

In this blog post, we will walk through the process of creating a semantic function-based solution that can accept a string like "please share all sign-in locations?" and generate a KQL (Kusto Query Language) query. This query will be used to retrieve log analytics data from the signin table.

## Step 1: Setting up enviornment 

### Pre-requisite
- Visual studio code
Please install below extension
    - Jupyter (Publisher- Microsoft)
    - Python (Publisher- Microsoft)
    - Pylance (Publisher- Microsoft)
    - Semantic Kernel Tools (Publisher- Microsoft)
- Python
Please install below packages
    - PIP
    - semantic-kernel
- [Download](https://github.com/vivekgarudi/Semantic-Kernal-Azure/tree/main/PlugIn-for-KQLQueries-on-Log-Analytics) the content of github repo

## Step 2: Define the Semantic Function to genrate KQL query

Now that you have below mentioned folder structure 
![Alt text](../.media/image.png)

### Create Semantic function

The first step is to define a semantic function that can interpret the input string and map it to a specific action. In our case, the action is to generate a KQL query. The function could look something like this:
 1. Create folder structure and declare 
    - Create /plugins folder
    - Create folder for semantic Skill, in this case its "AzureMonitor". (For more details on Skills)
    - Create Folder for semantic function inside the skills folder ie '/plugin/AzureMonitor', in this case "KQLquery-Signin" (For more details on Skills)
2. Define function
    - Once we have folder structure in place lets define the function by having 
        'config.json' with below JSON content for more details on content refer here.

        `

            {
                "schema": 1,
                "description": "Create KQL query for Signin table",
                "type": "completion",
                "completion": {
                    "max_tokens": 500,
                    "temperature": 0.0,
                    "top_p": 0.0,
                    "presence_penalty": 0.0,
                    "frequency_penalty": 0.0
                },
                    "input": {
                        "parameters": [
                            {
                            "name": "input",
                            "description": "the input data asking for the query",
                            "defaultValue": ""
                            }
                        ]
                    }
            }
        `
        In above file, we are defining semantic function which accept 'input' parameter to perform "Create KQL query for Signin table" as mentioned in Description section
    - Now lets put the multi-shot prompt for our semantic function in 'skprompt.txt'. where '{{input}}' where our input ask would be replaced.

        `

            Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
            Use the following format:

            Question: Question here
            Answer: KQL Query to run

            Only use the following tables: SigninLogs
            sample data 
            TenantId,SourceSystem,TimeGenerated [UTC],ResourceId,OperationName,OperationVersion,Category,ResultType,ResultSignature,ResultDescription,DurationMs,CorrelationId,Resource,ResourceGroup,ResourceProvider,Identity,Level,Location,AlternateSignInName,AppDisplayName,AppId,AuthenticationContextClassReferences,AuthenticationDetails,AppliedEventListeners,AuthenticationMethodsUsed,AuthenticationProcessingDetails,AuthenticationRequirement,AuthenticationRequirementPolicies,ClientAppUsed,ConditionalAccessPolicies,ConditionalAccessStatus,CreatedDateTime [UTC],DeviceDetail,IsInteractive,Id,IPAddress,IsRisky,LocationDetails,MfaDetail,NetworkLocationDetails,OriginalRequestId,ProcessingTimeInMilliseconds,RiskDetail,RiskEventTypes,RiskEventTypes_V2,RiskLevelAggregated,RiskLevelDuringSignIn,RiskState,ResourceDisplayName,ResourceIdentity,ResourceServicePrincipalId,ServicePrincipalId,ServicePrincipalName,Status,TokenIssuerName,TokenIssuerType,UserAgent,UserDisplayName,UserId,UserPrincipalName,AADTenantId,UserType,FlaggedForReview,IPAddressFromResourceProvider,SignInIdentifier,SignInIdentifierType,ResourceTenantId,HomeTenantId,UniqueTokenIdentifier,SessionLifetimePolicies,AutonomousSystemNumber,AuthenticationProtocol,CrossTenantAccessType,AppliedConditionalAccessPolicies,RiskLevel,Type
            XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,Azure AD,"9/19/2023, 1:45:17.287 PM",/tenants/XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX/providers/Microsoft.aadiam,Sign-in activity,1,SignInLogs,0,None,,0,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,Microsoft.aadiam,Microsoft.aadiam,,,4,US,,Azure Portal,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,"[{""id"":""urn:microsoft:req1"",""detail"":""previouslySatisfied""}]","[{""authenticationStepDateTime"":""2023-09-19T13:42:37.8484953+00:00"",""authenticationMethod"":""Previously satisfied"",""succeeded"":true,""authenticationStepResultDetail"":""First factor requirement satisfied by claim in the token"",""authenticationStepRequirement"":""Primary authentication"",""StatusSequence"":0,""RequestSequence"":0}]",,,"[{""key"":""Login Hint Present"",""value"":""True""},{""key"":""Legacy TLS (TLS 1.0, 1.1, 3DES)"",""value"":""False""},{""key"":""Is CAE Token"",""value"":""False""}]",singleFactorAuthentication,[],Browser,,notApplied,"9/19/2023, 1:42:37.848 PM","{""deviceId"":""{PII Removed}"",""displayName"":""{PII Removed}"",""operatingSystem"":""Windows10"",""browser"":""Edge 117.0.2045"",""isCompliant"":true,""isManaged"":true,""trustType"":""Azure AD joined""}",TRUE,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,,,,,[],XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,330,none,[],[],none,none,none,Windows Azure Service Management API,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,,,"{""errorCode"":0}",,AzureAD,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31 OS/10.0.22621",,,,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,Guest,,,,,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,72f988bf-86f1-41af-91ab-2d7cd011db47,Vb25Vsw2gEG5lycPpuYaAA,"[{""expirationRequirement"":""rememberMultifactorAuthenticationOnTrustedDevices"",""detail"":""Remember MFA""}]",20115,none,b2bCollaboration,,,SigninLogs
            XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,Azure AD,"9/19/2023, 1:46:55.434 PM",/tenants/XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX/providers/Microsoft.aadiam,Sign-in activity,1,SignInLogs,50140,None,This error occurred due to 'Keep me signed in' interrupt when the user was signing-in.,0,3033e807-77c5-4e7b-bfad-323d7db37235,Microsoft.aadiam,Microsoft.aadiam,,,4,VN,,Azure Portal,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,"[{""id"":""urn:microsoft:req1"",""detail"":""previouslySatisfied""}]","[{""authenticationStepDateTime"":""2023-09-19T11:21:02.1459396+00:00"",""authenticationMethod"":""Password"",""authenticationMethodDetail"":""Password in the cloud"",""succeeded"":true,""authenticationStepResultDetail"":""Correct password"",""authenticationStepRequirement"":""Primary authentication"",""StatusSequence"":0,""RequestSequence"":1}]",,,"[{""key"":""Legacy TLS (TLS 1.0, 1.1, 3DES)"",""value"":""False""},{""key"":""Is CAE Token"",""value"":""False""}]",singleFactorAuthentication,[],Browser,,notApplied,"9/19/2023, 11:21:02.145 AM","{""deviceId"":"""",""operatingSystem"":""Windows10"",""browser"":""Edge 117.0.2045""}",TRUE,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,,,,,[],XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,118,none,"[""unfamiliarFeatures"",""unlikelyTravel""]","[""unfamiliarFeatures"",""unlikelyTravel""]",medium,high,atRisk,Windows Azure Service Management API,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,,,"{""errorCode"":50140,""failureReason"":""This error occurred due to 'Keep me signed in' interrupt when the user was signing-in.""}",,AzureAD,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31 OS/10.0.22621",,,,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,Member,,,,,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX,WLtpsEhPQU-TgOJsPWy2AA,"[{""expirationRequirement"":""rememberMultifactorAuthenticationOnTrustedDevices"",""detail"":""Remember MFA""}]",7552,none,none,,,SigninLogs

            Some examples of SQL queries that corrsespond to questions are:

            Question:Show all SiginLogs events
            Answer:SigninLogs| project UserDisplayName, Identity,UserPrincipalName,  AppDisplayName, AppId, ResourceDisplayName
            Question:Show all Failed MFA challenge
            Answer:SigninLogs| where ResultType == 50074| project UserDisplayName, Identity,UserPrincipalName, ResultDescription,  AppDisplayName, AppId, ResourceDisplayName| summarize FailureCount=count(), FailedResources=dcount(ResourceDisplayName), ResultDescription=any(ResultDescription) by UserDisplayName
            Question:Show allFailed login Count
            Answer:SigninLogs| where ResultType !=0| summarize FailedLoginCount=count() by ResourceDisplayName| sort by FailedLoginCount desc nulls last
            Question:Show all Signin Locations
            Answer:SigninLogs| summarize Successful=countif(ResultType==0), Failed=countif(ResultType!=0) by Location

            Question: {{$input}}
            Answer:

        `

### Execute above semantic function function in action.

   - Rename ".env.example' as '.env' and update the parameters with actual values
   - Open open notebook "PlugIn-for-KQLQueries-on-Log-Analytics" in visula studio code and follow the steps mentioned to test
        - Step 1 Install all python libraries

        `

            !python -m pip install semantic-kernel
            !python -m pip install azure.monitor
            !python -m pip install pandas
            !python -m pip install azure.identity
            !python -m pip install azure.core
        `
            
        
        - Step 2 Import Packages required Prepare a semantic kernel instance first
        
            `

                import os
                import sys
                import asyncio
                from dotenv import dotenv_values
                import semantic_kernel as sk
                from semantic_kernel import ContextVariables, Kernel # Context to store variables and Kernel to interact with the kernel
                from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion ,AzureTextEmbedding # AI services
                from semantic_kernel.planning.sequential_planner import SequentialPlanner # Planner
                from semantic_kernel.planning.basic_planner import BasicPlanner # Planner
                import pandas as pd


                kernel = sk.Kernel() # Create a kernel instance
                kernel1 = sk.Kernel() #create another kernel instance for not having semanitc function in the same kernel 

                useAzureOpenAI = True
                config = dotenv_values(".env")
                AZURE_OPENAI_API_KEY = config["AZURE_OPENAI_API_KEY"]
                AZURE_OPENAI_ENDPOINT = config["AZURE_OPENAI_ENDPOINT"]
                AZURE_OPENAI_DEPLOYMENT_NAME = config["AZURE_OPENAI_DEPLOYMENT_NAME"]
                # Configure AI service used by the kernel
                if useAzureOpenAI:
                    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
                    kernel.add_chat_service("chat_completion", AzureChatCompletion(deployment, endpoint, api_key))
                    kernel1.add_chat_service("chat_completion", AzureChatCompletion(deployment, endpoint, api_key))
                else:
                    api_key, org_id = sk.openai_settings_from_dot_env()
                    kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))
            `
            
        - Step 3 Importing skills and function from folder

            `

                plugins_directory = "./plugins"
                DevFunctions=kernel1.import_semantic_skill_from_directory(plugins_directory, "AzureMonitor") # import the skill from the folder
                FDesFunction = DevFunctions["KQLquerySignin"]  # get the semantic function
            `
           
        - Step 4 calling the semantic function with string

            `          

                resultFD = FDesFunction("please share all sign-in location?")
                print(resultFD)
            `
### Create native function to execute this query again Log analytics 

    - Create file "native_function.py" under "AzureMonitor"or [download](./plugins/AzureMonitor/native_function.py) the file from repo.
    - Copy the code base and update log analytics workspace ID at "XXX-XXX-XXX". you can access this as context parameter but for similicity of this excercise, we kept it as hardcoded.please find below code flow
        - Importing python packages
        - Defining class 'sloganalytics' and native function as "slquery" under "@sk_function"
        - call semantic function 

    `

        import math
        from semantic_kernel.skill_definition import (
            sk_function,
            sk_function_context_parameter,
        )
        import requests
        import csv
        import json
        from semantic_kernel.orchestration.sk_context import SKContext
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
                get_feature = self._kernel.skills.get_function("AzureMonitor", "KQLquerySignin")
                Ctxtquery = get_feature(context["title"])
                credential  = DefaultAzureCredential()
                client = LogsQueryClient(credential)
                txtquery=str(Ctxtquery)
                #txtquery='"' + txtquery + '"' 
                print(txtquery)
                LOGS_WORKSPACE_ID="XXXXXXX-XXXX-XXXX-XXXX-XXXXXXX"
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
       `

### Lets test this native function as end to end solution
    - Lets go back to notebook
        -   Step 5 Importing native function

            `

            from plugins.AzureMonitor.native_function import sloganalytics
            Mon_plugin = kernel.import_skill(sloganalytics(kernel1), skill_name="AzureMonitor") # import the skill
            variables = ContextVariables()
            variables["description"] = "test"
            `

        -   Step 6 Executing native function by puting natural language queries in title field

            `

            variables["title"] = "please share all sign-in location?"
            result = await kernel.run_async( Mon_plugin["slquery"], input_vars=variables )
            print(variables["Df"])
            `

The returned data is panda dataframe which can be used for visualize 

By following these steps, you can create a semantic function-based solution that can interpret natural language queries and use them to retrieve specific signin log analytics data. This can be a powerful tool for making your log analytics more accessible and user-friendly.

The scope of this can be expanded to cover other log analytics tables by having different skills for each table and use planner or using semantic memory for incorporating dynamic prompt in KQLquery semantic function.


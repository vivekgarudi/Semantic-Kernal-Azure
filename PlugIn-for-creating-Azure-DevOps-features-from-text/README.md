## Creating a Semantic Function-Based Solution for KQL Queries

In this blog post, we will walk through the process of creating a semantic function-based solution that can accept a string like "please share all sign-in locations?" and generate a KQL (Kusto Query Language) query. This query will be used to retrieve log analytics data from the signin table.

### Step 1: Define the Semantic Function to genrate KQL query

The first step is to define a semantic function that can interpret the input string and map it to a specific action. In our case, the action is to generate a KQL query. The function could look something like this:

'''Semantic Function
Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: Question here
Answer: KQL Query to run

Only use the following tables: SigninLogs
sample data 
TenantId,SourceSystem,TimeGenerated [UTC],ResourceId,OperationName,OperationVersion,Category,ResultType,ResultSignature,ResultDescription,DurationMs,CorrelationId,Resource,ResourceGroup,ResourceProvider,Identity,Level,Location,AlternateSignInName,AppDisplayName,AppId,AuthenticationContextClassReferences,AuthenticationDetails,AppliedEventListeners,AuthenticationMethodsUsed,AuthenticationProcessingDetails,AuthenticationRequirement,AuthenticationRequirementPolicies,ClientAppUsed,ConditionalAccessPolicies,ConditionalAccessStatus,CreatedDateTime [UTC],DeviceDetail,IsInteractive,Id,IPAddress,IsRisky,LocationDetails,MfaDetail,NetworkLocationDetails,OriginalRequestId,ProcessingTimeInMilliseconds,RiskDetail,RiskEventTypes,RiskEventTypes_V2,RiskLevelAggregated,RiskLevelDuringSignIn,RiskState,ResourceDisplayName,ResourceIdentity,ResourceServicePrincipalId,ServicePrincipalId,ServicePrincipalName,Status,TokenIssuerName,TokenIssuerType,UserAgent,UserDisplayName,UserId,UserPrincipalName,AADTenantId,UserType,FlaggedForReview,IPAddressFromResourceProvider,SignInIdentifier,SignInIdentifierType,ResourceTenantId,HomeTenantId,UniqueTokenIdentifier,SessionLifetimePolicies,AutonomousSystemNumber,AuthenticationProtocol,CrossTenantAccessType,AppliedConditionalAccessPolicies,RiskLevel,Type
81a662b5-8541-481b-977d-5d956616ac5e,Azure AD,"9/19/2023, 1:45:17.287 PM",/tenants/4b2462a4-bbee-495a-a0e1-f23ae524cc9c/providers/Microsoft.aadiam,Sign-in activity,1,SignInLogs,0,None,,0,e9202c39-aad0-4ae4-8ee5-6a3459a7e034,Microsoft.aadiam,Microsoft.aadiam,,,4,US,,Azure Portal,c44b4083-3bb0-49c1-b47d-974e53cbdf3c,"[{""id"":""urn:microsoft:req1"",""detail"":""previouslySatisfied""}]","[{""authenticationStepDateTime"":""2023-09-19T13:42:37.8484953+00:00"",""authenticationMethod"":""Previously satisfied"",""succeeded"":true,""authenticationStepResultDetail"":""First factor requirement satisfied by claim in the token"",""authenticationStepRequirement"":""Primary authentication"",""StatusSequence"":0,""RequestSequence"":0}]",,,"[{""key"":""Login Hint Present"",""value"":""True""},{""key"":""Legacy TLS (TLS 1.0, 1.1, 3DES)"",""value"":""False""},{""key"":""Is CAE Token"",""value"":""False""}]",singleFactorAuthentication,[],Browser,,notApplied,"9/19/2023, 1:42:37.848 PM","{""deviceId"":""{PII Removed}"",""displayName"":""{PII Removed}"",""operatingSystem"":""Windows10"",""browser"":""Edge 117.0.2045"",""isCompliant"":true,""isManaged"":true,""trustType"":""Azure AD joined""}",TRUE,56b9bd55-36cc-4180-b997-270fa6e61a00,,,,,[],56b9bd55-36cc-4180-b997-270fa6e61a00,330,none,[],[],none,none,none,Windows Azure Service Management API,797f4846-ba00-4fd7-ba43-dac1f8f63013,45c7112a-39d4-4aa7-8dda-3d2c7c0fe1f4,,,"{""errorCode"":0}",,AzureAD,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31 OS/10.0.22621",,,,4b2462a4-bbee-495a-a0e1-f23ae524cc9c,Guest,,,,,4b2462a4-bbee-495a-a0e1-f23ae524cc9c,72f988bf-86f1-41af-91ab-2d7cd011db47,Vb25Vsw2gEG5lycPpuYaAA,"[{""expirationRequirement"":""rememberMultifactorAuthenticationOnTrustedDevices"",""detail"":""Remember MFA""}]",20115,none,b2bCollaboration,,,SigninLogs
81a662b5-8541-481b-977d-5d956616ac5e,Azure AD,"9/19/2023, 1:46:55.434 PM",/tenants/4b2462a4-bbee-495a-a0e1-f23ae524cc9c/providers/Microsoft.aadiam,Sign-in activity,1,SignInLogs,50140,None,This error occurred due to 'Keep me signed in' interrupt when the user was signing-in.,0,3033e807-77c5-4e7b-bfad-323d7db37235,Microsoft.aadiam,Microsoft.aadiam,,,4,VN,,Azure Portal,c44b4083-3bb0-49c1-b47d-974e53cbdf3c,"[{""id"":""urn:microsoft:req1"",""detail"":""previouslySatisfied""}]","[{""authenticationStepDateTime"":""2023-09-19T11:21:02.1459396+00:00"",""authenticationMethod"":""Password"",""authenticationMethodDetail"":""Password in the cloud"",""succeeded"":true,""authenticationStepResultDetail"":""Correct password"",""authenticationStepRequirement"":""Primary authentication"",""StatusSequence"":0,""RequestSequence"":1}]",,,"[{""key"":""Legacy TLS (TLS 1.0, 1.1, 3DES)"",""value"":""False""},{""key"":""Is CAE Token"",""value"":""False""}]",singleFactorAuthentication,[],Browser,,notApplied,"9/19/2023, 11:21:02.145 AM","{""deviceId"":"""",""operatingSystem"":""Windows10"",""browser"":""Edge 117.0.2045""}",TRUE,b069bb58-4f48-4f41-9380-e26c3d6cb600,,,,,[],b069bb58-4f48-4f41-9380-e26c3d6cb600,118,none,"[""unfamiliarFeatures"",""unlikelyTravel""]","[""unfamiliarFeatures"",""unlikelyTravel""]",medium,high,atRisk,Windows Azure Service Management API,797f4846-ba00-4fd7-ba43-dac1f8f63013,45c7112a-39d4-4aa7-8dda-3d2c7c0fe1f4,,,"{""errorCode"":50140,""failureReason"":""This error occurred due to 'Keep me signed in' interrupt when the user was signing-in.""}",,AzureAD,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31 OS/10.0.22621",,,,4b2462a4-bbee-495a-a0e1-f23ae524cc9c,Member,,,,,4b2462a4-bbee-495a-a0e1-f23ae524cc9c,4b2462a4-bbee-495a-a0e1-f23ae524cc9c,WLtpsEhPQU-TgOJsPWy2AA,"[{""expirationRequirement"":""rememberMultifactorAuthenticationOnTrustedDevices"",""detail"":""Remember MFA""}]",7552,none,none,,,SigninLogs

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
'''
Step 2: Interpret the Input StringThe next step is to interpret the input string. This involves parsing the string and identifying key phrases or words that indicate what kind of data the user is asking for. For example, if the user asks for "all sign-in locations", we know they want data from the signin table.

def interpret_input_string(input_string):
    # Parse the input string and identify key phrases or words
    ...
    return table_name, data_type

Step 3: Generate the KQL QueryOnce we have identified what data the user is asking for, we can generate the appropriate KQL query. This involves using the table name and data type to construct a query that will retrieve the desired data.

def generate_kql_query(table_name, data_type):
    # Use the table name and data type to construct a KQL query
    ...
    return kql_query

Step 4: Retrieve Log Analytics DataThe final step is to use the generated KQL query to retrieve log analytics data. This involves connecting to your log analytics service, executing the query, and returning the results.

def retrieve_log_analytics_data(kql_query):
    # Connect to your log analytics service, execute the query, and return the results
    ...
    return results

By following these steps, you can create a semantic function-based solution that can interpret natural language queries and use them to retrieve specific log analytics data. This can be a powerful tool for making your log analytics more accessible and user-friendly.

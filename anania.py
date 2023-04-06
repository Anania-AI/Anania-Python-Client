import requests

class Config():

    API_KEY = None
    
    ## ENDPOINTS
    _API_BASE = "https://api.anania.ai/v1/"
    _ENDPOINT_TRAINING = f"{_API_BASE}training"
    _ENDPOINT_USER = f"{_API_BASE}user/get_information"
    _ENDPOINT_QUESTION = f"{_API_BASE}question"
    _ENDPOINT_QUESTION_DOC = f"{_API_BASE}question/doc"
    _ENDPOINT_METADATA = f"{_API_BASE}metadata"
    _ENDPOINT_DB_CHECK = f"{_API_BASE}get_all_tables"
    _ENDPOINT_QUESTION_FLAG = f"{_API_BASE}question/flag"
    _ENDPOINT_DELETE_PROJECT = f"{_API_BASE}project"
    _ENDPOINT_UPDATE_API_KEY = f"{_API_BASE}user/new_api_key"

    ## PROJECT TYPES
    TYPE_URL = "url_QA"
    TYPE_CHAT = "chat_QA"
    TYPE_PDF = "pdf_QA"
    TYPE_CSV = "csv"
    TYPE_DB = "db"


class Create(Config):

    def get_all_db_tables(connection_string, ssl=False):
        headers = {"api_key": Config.API_KEY} 
        body = {connection_string: connection_string, ssl: ssl}

        response = requests.post(url=Config._ENDPOINT_DB_CHECK,headers=headers,json=body)

        if response.status_code == 200:
            response = response.json()
            if response["Status"] == "Success":
              return response["all_tables"]
            else:
              print(f'Status: {response["Status"]}, Error message: {response["Output"]}')
        else:
            raise Exception(f'Error creating project: {response.text}')


    def create_project(project_name, input_type=Config.TYPE_CHAT, **kwargs):

        headers = {"api_key": Config.API_KEY} 
        body = {"input_type": input_type, "project_name": project_name}

        if input_type == Config.TYPE_URL:
          body.update({"urls":kwargs.get("urls"), "crawl":kwargs.get("crawl")})
        elif input_type in [Config.TYPE_PDF,Config.TYPE_CSV]:
          body.update({"data":kwargs.get("data")})
        elif input_type == Config.TYPE_DB:
          body.update({"connection_string":kwargs.get("connection_string"), "table_names":kwargs.get("table_names")})
        
        response = requests.post(url=Config._ENDPOINT_TRAINING,headers=headers,json=body)
        
        if response.status_code == 200:
            response = response.json()
            if response["Status"] == "Success":
              return response["Output"]
            else:
              print(f'Status: {response["Status"]}, Error message: {response["Output"]}')
        else:
            raise Exception(f'Error creating project: {response.text}')


class Ask(Config):

    def ask_question_base(question, project_key, endpoint, **kwargs):
        headers = {'api_key': Config.API_KEY}
        body = {"project_key":project_key,"question":question}

        response = requests.post(endpoint, headers=headers, json=body)
        if response.status_code == 200:
            response = response.json()
            if response["Status"] == "Success":
              return response
            else:
              raise Exception(f'Status: {response["Status"]}, Error message: {response["Error_message"]}')
        else:
            raise Exception(f'Error asking question: {response.text}')

    def ask_chat(question, project_key, endpoint=Config._ENDPOINT_QUESTION):
        response = Ask.ask_question_base(question, project_key, endpoint)
        if response["Output"]:
            return response["Output"] 

    def ask_document(question, project_key, endpoint=Config._ENDPOINT_QUESTION_DOC):
        response = Ask.ask_question_base(question, project_key, endpoint)
        if response["Output"]:
            return response["Output"]

    def ask_tabular(question, project_key, endpoint=Config._ENDPOINT_QUESTION):
        response = Ask.ask_question_base(question, project_key, endpoint)
        
        if not response["Output"]:
            required_keys = ["SQL"]
        else:
            required_keys = ["Output","Output type", "SQL"]
            if response["Chart exist"]:
                required_keys.append("Output Chart")
        response = {i:response[i] for i in required_keys}
        if response:
            return response

    def ask(question, project_type, project_key, **kwargs):
        if project_type in [Config.TYPE_CSV,Config.TYPE_DB]:
            Ask.ask_tabular(question, project_key)
        elif project_type in [Config.TYPE_PDF, Config.TYPE_URL]:
            Ask.ask_document(question, project_key)
        elif project_type in [Config.TYPE_CHAT]:
            Ask.ask_chat(question, project_key)
        else:
            raise Exception(f"Unsupported project type: {project_type}")

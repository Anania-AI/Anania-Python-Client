import requests
import pandas as pd
from typing import Union
from dataclasses import dataclass

@dataclass
class Answer:
    
    """
    DataClass for easier access to Anania's answers.
    """
    question_id: str
    status: str
    sql: str
    result: Union[str, int, pd.DataFrame]
    chart: dict
        

##WARNING: none of the functions is actually checking the request status
class Anania:
    
    """
    Python Client to Anania's API. Handles Project creation and Q&A for registered users with API Key.
    
    Arguments:
        API_KEY (str): API key for the user. Available on the user interface.
        PROJECT_KEY (str): project key. will be automatically setup once create_project() is called.

    """
    
    API_KEY = None
    
    _API_BASE = "https://anania-api.herokuapp.com/v1/"
    _ENDPOINT_TRAINING = f"{_API_BASE}training"
    _ENDPOINT_USER = f"{_API_BASE}user/get_information"
    _ENDPOINT_QUESTION = f"{_API_BASE}question"
    _ENDPOINT_METADATA = f"{_API_BASE}metadata"
    _ENDPOINT_DB_CHECK = f"{_API_BASE}get_all_tables"
    _ENDPOINT_QUESTION_FLAG = f"{_API_BASE}question/flag"
    _ENDPOINT_DELETE_PROJECT = f"{_API_BASE}project"
    _ENDPOINT_UPDATE_API_KEY = f"{_API_BASE}user/new_api_key"

    
    def __init__(self, project_key=None):
        self.question_id=None
        self.PROJECT_KEY = project_key
            
    
    ##WARNING: need to add check on wherher API_KEY is provided
    def create_project(self,input_type: str,project_name: str, connection_string=None,table_names=None,data=None):
        
        """
        Creates projects from db or via file upload.
        In case of db connection db connection string and table_names should be provided, othervise the data in the given formats should be given as input.
        Gets the data from the given source and Posts to Anania's server by creating a Project and returning its key.
        
        Args:
            input_type (str): Which of the possible types of data input is chosen. Possible values are ['db','csv','json']
            project_name (str): Project name 
            connection_string (str): DB connection string
            table_names (list): List of tables that are chosen to be included in the projects.Maximum number of tables is 3.
            data (pd.DataFrame,dict): Dataset/table to be analyzed.Defaults to None.
            
        Returns:
            PROJECT_KEY (str): The Project Key for the newly created project as an Attribute.
        """
        
        headers = {"api_key":self.API_KEY} 
        if input_type =='db':
            body = {"project_name":project_name,"input_type":input_type,'connection_string':connection_string,'table_names':table_names}
        else:
            if isinstance(data,pd.DataFrame):
                data = data.to_json(orient="records")
            body = {"project_name":project_name,"input_type":input_type,'data':data}
        response = requests.post(url=Anania._ENDPOINT_TRAINING,headers=headers,json=body)
        response = response.json()
        if response["Status"]=="Success":
            self.PROJECT_KEY = response["Output"]
            return self.PROJECT_KEY
        else:
            return response
    
    def get_my_project_ids(self,email: str,user_id: str):
        
        """
        Uses API KEY to provide IDs of all non-demo projects created by the User.
        Args:
            email (str): user email address
            user_id: user id
        Returns:
            PROJECT_KEY (str): The Project Key for the newly created project as an Attribute.
        """
        
        headers = {"api_key":self.API_KEY}
        body = {"mail":email,"user_id": user_id}
        response = requests.post(url=Anania._ENDPOINT_USER,headers=headers,json=body)
        project_keys = [i['project_key'] for i in response.json()["user_projects"]]
        return project_keys
    
    ##WARNING: need to add check on wherher API_KEY and PROJECT_KEY are provided
    def ask_question(self,question):
        
        """
        Sends questions and Project Key to API and returns the answer as a response.
        
        Args:
            question (str): Question in plain English that is asked to Anania.
        
        Returns:
            anania.Answer: The API response including Anania's answer in "Answer" DataClass.        
        """
        
        headers = {"api_key":self.API_KEY}
        body = {"project_key":self.PROJECT_KEY,"question":question}
        response = requests.post(url=self._ENDPOINT_QUESTION,headers=headers,json=body)
        if response.status_code ==200:
            response = response.json()
            print('question_id',response['question_id'])
            self.question_id=response['question_id']
            if response["Output type"] == "TABLE":
                response["Output"] = pd.DataFrame(response["Output"]["data"],columns=response["Output"]["columns"])
                if 'index' in response["Output"].columns:
                    response["Output"].drop(["index"],axis=1,inplace=True)
            return Answer(response['question_id'],response["Status"],response["SQL"],response["Output"],response['Output chart'])
        else:
            response
    
    def flag_question(self,flag: str,question_id=None):
        """Flag the question if the answer was not correct.

        Args:
            flag (str): Text that describes the situation, the correct SQL is possible.
            question_id (str, optional): The id of the question which you want to flag. If not provided the last question is flagged. Defaults to None.

        Returns:
            response: the response of the request
        """
        headers = {"api_key":self.API_KEY}
        if question_id:
            body = {"question_id":question_id,'flag':flag}
        else:
            body = {"question_id":self.question_id,'flag':flag}
        response = requests.post(url=self._ENDPOINT_QUESTION_FLAG,headers=headers,json=body)
        return response
            
            
    # metadata is prohect level now
    def send_metadata(self,metadata):
        
        """
        Sends metadata and project key to API for training.
        
        Args:
            metadata (dict): Key value pairs for acronyms or other information matching.
        
        Returns:
            Status (str): Status to make sure metadata was added successfully.    
        """
        headers = {"api_key":self.API_KEY}
        body = {"project_key":self.PROJECT_KEY,"metadata":str(metadata)}
        response = requests.post(url=Anania._ENDPOINT_METADATA,headers=headers,json=body)
        
        return response.json()             
        
    def delete_project(self,project_key=None):
        """Delete an existing project.
        Args:
            project_key (str, optional): The key of the project to be deleted.If not provided the current project is deleted. Defaults to None.

        Returns:
            response: the response of the request
        """
        headers = {"api_key":self.API_KEY}
        if project_key:
            body = {"project_key":project_key}
        else:
            body = {"project_key":self.project_key}
        response = requests.delete(url=self._ENDPOINT_DELETE_PROJECT,headers=headers,json=body)
        return response
        
        
    def get_all_tables_db(self,connection_string):
        """Connects to tb and return the list of all tables available in the db

        Args:
            connection_string (str): the db connection string

        Returns:
            response: the response of the request
            all_tables (list,None) : the list of all tables in the db, None if the connection was not succesfull
        """
        headers = {"api_key":self.API_KEY}
        body = {"connection_string":connection_string}
        response = requests.post(url=Anania._ENDPOINT_DB_CHECK,headers=headers,json=body)
        if response.status_code==200:
            response=response.json()
            all_tables = response['all_tables']
        else:
            all_tables=None
        return response,all_tables
        
    def update_api_key(self):
        """Updates the user api key.

        Returns:
            response: response of the request
        """
        headers = {"api_key":self.API_KEY}
        response = requests.post(url=Anania._ENDPOINT_UPDATE_API_KEY,headers=headers)
        if response.status_code ==200:
            if response.json()['Status']=='Success':
                self.API_KEY = response.json()['new_api_key']
        return response

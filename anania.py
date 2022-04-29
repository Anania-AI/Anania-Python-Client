import requests
import pandas as pd
from typing import Union
from dataclasses import dataclass

@dataclass
class Answer:
    
    """
    DataClass for easier access to Anania's answers.
    """
    
    status: str
    sql: str
    result: Union[str, int, pd.DataFrame]

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
    
    def __init__(self, project_key=None):
        if project_key:
            self.PROJECT_KEY = project_key
        else:
            try:
                self.get_my_project_ids()
            except:
                pass
    
    ##WARNING: need to add check on wherher API_KEY is provided
    def create_project(self, data: pd.DataFrame,filename: str):
        
        """
        Converts data to JSON string and Posts to Anania's server by creating a Project and returning its key.
        
        Args:
            data (pd.DataFrame): Dataset/table to be analyzed.
        
        Returns:
            PROJECT_KEY (str): The Project Key for the newly created project as an Attribute.
        """
        
        headers = {"api_key":self.API_KEY}
        
        if isinstance(data,pd.DataFrame):
            data = data.to_json(orient="records")
        body = {"data":data,"filename":filename}
        response = requests.post(url=Anania._ENDPOINT_TRAINING,headers=headers,json=body)
        response = response.json()
        if response["Status"]=="Success":
            self.PROJECT_KEY = response["Output"]
            return self.PROJECT_KEY
        else:
            return response
    
    ##WARNING: need to check whether API_KEY is provided AND FAILS if !=1 projects are created
    def get_my_project_ids(self,email: str,user_id: str):
        
        """
        Uses API KEY to provide IDs of all non-demo projects created by the User.
        The function is autoamtically called during initialization if no project key is provided.
        
        Returns:
            PROJECT_KEY (str): The Project Key for the newly created project as an Attribute.
        """
        
        headers = {"api_key":self.API_KEY}
        body = {"mail":email,"user_id": user_id}
        response = requests.post(url=Anania._ENDPOINT_USER,headers=headers,body=body)
        self.PROJECT_KEY = response.json()["user_projects"][0]["project_key"]
        if isinstance(self.PROJECT_KEY,str):
            return self.PROJECT_KEY
        else:
            None
    
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
        response = requests.post(url=Anania._ENDPOINT_QUESTION,headers=headers,json=body)
        if response.status_code ==200:
            response = response.json()
            if response["Output type"] == "TABLE":
                response["Output"] = pd.DataFrame(response["Output"]["data"],columns=response["Output"]["columns"])
                if 'index' in response["Output"].columns:
                    response["Output"].drop(["index"],axis=1,inplace=True)
            return Answer(response["Status"],response["SQL"],response["Output"])
        else:
            response
    
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
        

import pandas as pd
from anania import Anania
import os 
import random

Anania.API_KEY = os.environ.get('API_KEY')
user_id = os.environ.get('user_id')
email = os.environ.get('email')
connection_string=os.environ.get('connection_string')

data = pd.read_csv("https://raw.githubusercontent.com/Metricam/Public_data/master/MARKET_Car_Prices.csv")

#check your projects
project = Anania()
my_proj = project.get_my_project_ids(email,user_id)

##for creating new project and asking questions
project = Anania()
print(project.create_project(input_type = 'json',project_name='MARKET_Car_Prices',data=data))

# for creating a project from db
project=Anania()
resp,all_tables = project.get_all_tables_db(connection_string)

#choose 1-3 out of all tables (just choosing randomly here)
table_names = random.sample(all_tables,2)
print(project.create_project(input_type = 'db',project_name='MARKET_Car_Prices',connection_string=connection_string,table_names=table_names))

# asking questions
answer = project.ask_question("show me all rows")
answer

##for asking questions on existing project
project_key = os.environ.get('project_key')
project = Anania(project_key)
answer = project.ask_question("show me first row")
print(answer.result)

# for flagging an answer to the question, you can provide the correct SQL if possible
#you can flag the last question by just sendig the flag or specify the question_id as input here for older questions 
project.flag_question(flag='select * from table where a=b')

#for deleting a project
project.delete_project(project_key=project_key).json()

# in case you want to update your api key
update = project.update_api_key()

#for adding metadata to the project
metadata={'num_of_doors':'number of doors'}
project.send_metadata(metadata)
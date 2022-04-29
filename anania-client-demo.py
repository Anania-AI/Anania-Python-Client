import pandas as pd
from anania import Anania
import os 

Anania.API_KEY = os.environ.get('API_KEY')
data = pd.read_csv("https://raw.githubusercontent.com/Metricam/Public_data/master/MARKET_Car_Prices.csv").head()

##for creating new project and asking questions
project = Anania()
print(project.create_project(data,'MARKET_Car_Prices.csv'))
answer = project.ask_question("show me first row")
answer.result

##for asking questions on existing project
project_key = os.environ.get('project_key')
project = Anania(project_key)
answer = project.ask_question("show me first row")
answer.result

#for adding metadata to the project
metadata={'num_of_doors':'number of doors'}
project.send_metadata(metadata)
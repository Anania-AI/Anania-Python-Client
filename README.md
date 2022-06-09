# Anania-Python-Client

Simple Python client for working with Training and Question APIs. You can find API documentation [here](https://api.anania.ai/docs).

ToDo:
 - Add error handlers and validity checks

```
import pandas as pd
from anania import Anania

Anania.API_KEY = "YOUR API KEY"
data = pd.read_csv("YOUR DATA PATH")

##for creating new project from table
project = Anania()
print(project.create_project(input_type = 'json',project_name='YOUR PROJECT NAME',data=data))

# for creating a project from db
project=Anania()
print(project.create_project(input_type = 'db',project_name='MARKET_Car_Prices',connection_string='YOUR CONNECTION STRING',table_names=['TABLE 1','TABLE 2']))

# asking questions
answer = project.ask_question("show me all rows")
print(answer.result)
```
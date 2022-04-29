# Anania-Python-Client

Simple Python client for working with Training and Question APIs. You can find API documentation [here](https://api.anania.ai/docs).

ToDo:
 - Add error handlers and validity checks

```
import pandas as pd
from anania import Anania

Anania.API_KEY = "YOUR API KEY"
data = pd.read_csv("YOUR DATA PATH")

##for creating new project and asking questions
project = Anania()
project.create_project(data)
answer = project.ask_question("show me first row")
print(answer.result)

##for asking questions on existing project
project = Anania("YOUR PROJECT KEY")
answer = project.ask_question("show me first row")
print(answer.result)
```

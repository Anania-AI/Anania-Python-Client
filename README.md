# Anania-Python-Client

Simple Python client for working with Training and Question APIs. You can find API documentation [here](https://api.anania.ai/docs).

ToDo:
 - Add Metadata endpoint
 - Add wheel to PyPI

```
from anania import Config, Anania

Config.API_KEY = "YOUR API KEY"

## Using existing project
Anania.ask_document(question = "YOUR QUESTION", project_key = "YOUR PROJECT KEY")

## Creating a new project and using it
project_key_url = Anania.create_project_url(project_name = "YOUR PROJECT NAME", urls = ["https://metric.am/"], crawl = False)
Anania.ask_document("YOUR QUESTION", project_key = project_key_url)
```

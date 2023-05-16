from anania import Config, Create, Ask

Config.API_KEY = "YOUR API KEY"

## Using existing project
Ask.ask_document(question = "YOUR QUESTION", project_key = "YOUR PROJECT KEY")

## Creating a new project and using it
project_key_url = Create.create_project_url(project_name = "YOUR PROJECT NAME", urls = ["https://metric.am/"], crawl = False)
Ask.ask_document("YOUR QUESTION", project_key = project_key_url)
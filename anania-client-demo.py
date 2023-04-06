from anania import Config, Create, Ask

Config.API_KEY = "YOUR API KEY"

## Using existing project
Config.PROJECT_KEY = "YOUR PROJECT KEY"
Ask.ask_document("YOUR QUESTION")

## Creating a new project and using it
Create.create_project()
Ask.ask_chat("YOUR QUESTION")

# Deploy Instructions

- run terminal command
 ```
 pip install python-decouple
 ```

- place a .env file in your root folder and populate:
 ```
 host_url=
 username=
 password=

 GlobalScripts_run=True
 GlobalScripts_delete=False

 CustomTemplates_run=True
 CustomTemplates_delete=False

 UserTypes_run=True
 UserTypes_delete=False

 CustomTables_run=True
 CustomTables_delete=False

 ```

- run the Deploy.py script
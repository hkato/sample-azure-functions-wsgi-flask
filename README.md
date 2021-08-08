# Azure Functions + WSGI + Flask sample

## Directory Structure

```
.
├── flask_app           # Flask/WSGI WebApp
│   ├── __init__.py
│   └── app.py
├── functions_wsgi      # Functions entry -> WSGI
│   ├── __init__.py
│   └── function.json
├── host.json
└── requirements.txt
```

## Saffolding

ref.
https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python

Create project directory and virtual env.

```sh
$ mkdir myproject
$ cd myproject
```
```sh
$ pyenv local 3.8.6
$ python -m venv .venv
$ source .venv/bin/activate
```

Create functions config from template

```sh
$ func init .
Select a number for worker runtime:
1. dotnet
2. dotnet (isolated process)
3. node
4. python
5. powershell
6. custom
Choose option: 4
python
Found Python version 3.8.6 (python3).
Writing requirements.txt
Writing .funcignore
Writing .gitignore
Writing host.json
Writing local.settings.json
Writing /Users/username/Workspaces/myproject/.vscode/extensions.json
```

Add function entry

```sh
$ func new --template "Http Trigger" --name functions_wsgi
```

## Integrate Flask/WSGI app

Add wildcard route : `functions_wsgi/function.json` file

```diff
   "scriptFile": "__init__.py",
   "bindings": [
     {
+      "route": "{*route}",
       "authLevel": "function",
       "type": "httpTrigger",
       "direction": "in",
```

Remove default `/api` route prefix : `host.json` file

```diff
   "extensionBundle": {
     "id": "Microsoft.Azure.Functions.ExtensionBundle",
     "version": "[2.*, 3.0.0)"
+  },
+  "extensions": {
+    "http": {
+      "routePrefix": ""
+    }
   }
 }
```

Use WsgiMiddleware to call the WSGI/Flask App from the function entry 

```python
import azure.functions as func

from flask_app.app import app


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:

    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)
```

## Local debug

### Azure Functions Core Tools  

```sh
$ func start
Found Python version 3.8.6 (python3).

Azure Functions Core Tools
Core Tools Version:       3.0.3477 Commit hash: 5fbb9a76fc00e4168f2cc90d6ff0afe5373afc6d  (64-bit)
Function Runtime Version: 3.0.15584.0
.
.
.
	functions_wsgi: [GET,POST] http://localhost:7071/{*route}
```

```sh
$ curl -X GET 'http://localhost:7071/hello'
This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.
```
```sh
$ curl -X GET 'http://localhost:7071/hello?name=hoge'
Hello, hoge. This HTTP triggered function executed successfully.
```
```sh
$ curl -X POST 'http://localhost:7071/hello' -H "Content-Type: application/json" -d '{"name": "hoge"}'
Hello, hoge. This HTTP triggered function executed successfully.
```
```sh
$ curl -X GET 'http://localhost:7071/foo'  
test
```
```sh
$ curl -X GET 'http://localhost:7071/bar'
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>
```
```sh
$ curl -X POST 'http://localhost:7071/bar' -H "Content-Type: application/json" -d '{"name": "hoge"}'
{"name":"hoge"}
```

### Werkzeug

You can also use default the web server

```sh
$ python flask_app/app.py
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

## Deploy

```sh
$ func azure functionapp publish xxxxxxxx
Getting site publishing info...
Creating archive for current directory...
Performing remote build for functions project.
Deleting the old .python_packages directory
Uploading 4.83 KB [###############################################################################]
Remote build in progress, please wait...
Updating submodules.
.
.
.
Detecting platforms...
Detected following platforms:
  python: 3.8.6
Version '3.8.6' of platform 'python' is not installed. Generating script to install it...
.
.
.
Resetting all workers for xxxxxxxx.azurewebsites.net
Deployment successful.
Remote build succeeded!
Syncing triggers...
Functions in xxxxxxxx:
    functions_wsgi - [httpTrigger]
        Invoke url: https://xxxxxxxx.azurewebsites.net/{*route}?code=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

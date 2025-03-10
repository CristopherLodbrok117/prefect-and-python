# Scripting with python and prefect

<br>

Prefect is a workflow orchestration framework for building resilient data pipelines in Python. Empowers developers to build and scale workflows quickly. For more information visit: [prefect](https://docs.prefect.io/3.0/get-started/quickstart)

Flows are defined as Python functions. They can take inputs, perform work, and return a result.
Adding @task decorators to any functions called by the flow converts them to tasks. The easiest way to convert a Python script into a workflow is to add a @flow decorator to the script’s entrypoint. This will create a corresponding flow. 

We define our script the next way:

```python
import shutil
import os
from prefect import task, flow

# Define a task to copy files from origin to dastination folder
@task
def copy_files(source_dir, target_dir):

    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Copy each file
        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)
            if os.path.isfile(file_path):
                shutil.copy(file_path, target_dir)

                print(f"Archivo {filename} copiado a {target_dir}")

    except Exception as e:
        print(f"Error al copiar archivos: {str(e)}")

# We define our flow
@flow
def copy_files_flow():
    # Specify our origin and destination folders
    source_directory = "C:\\Users\\kim_j\\OneDrive\\Escritorio\\CTF\\Origin"
    target_directory = "C:\\Users\\kim_j\\OneDrive\\Escritorio\\CTF\\Dest"
    
    # Call the task we defined previously
    copy_files(source_directory, target_directory)


#copy_files_flow()
if __name__ == '__main__':
    copy_files_flow()
```

<br>

Flows are uniquely identified by name. You can provide a name parameter value for the flow, but if you don’t provide a name, Prefect uses the flow function name.

This script makes a files backup from an origin folder to any other destination. We can backup any kind of file as we can see. Also it will override the files if they already exist, so don't worry about duplicate files.

<br>

Origin folder:

![origin folder](https://github.com/CristopherLodbrok117/python-scripting-with-prefect/blob/e663fa1c550313ac4b13075bb2a4c0ff34f14c02/screenshots/02%20-%20orig.png)

<br>

Destination folder (empty for now):

![destination folder](https://github.com/CristopherLodbrok117/python-scripting-with-prefect/blob/e663fa1c550313ac4b13075bb2a4c0ff34f14c02/screenshots/01%20-%20dest.png)

<br>

## Install Prefect

<br>

It's recommended to create a python virtual environment first and activate it. We can do it by executing the next lines (with Git Bash)
* `python -m venv virtual-environment-name`
* `source virtual-environment-name/scripts/activate`

Visit the [python-virtual-environment documentation](https://docs.python.org/3/library/venv.html) for more information

<br>

Now we can install prefect with: `pip install -U prefect`

![install prefect](https://github.com/CristopherLodbrok117/python-scripting-with-prefect/blob/799a02d754d105fad4e1b8ed3864cfd721aa3265/screenshots/0%20-%20install%20prefect.png)

<br>

Excecute `prefect server start` to connect to prefect

![prefect server](https://github.com/CristopherLodbrok117/python-scripting-with-prefect/blob/e2f40f1ff3c0847e431d4d0ff94c2500ae61829b/screenshots/999%20-%20prefect%20server.png)

Before visiting the prefect UI dashboard. Lets configure our workflows

<br>

## Deployment

<br>

Open a new terminal and execute `prefect init`. Choose your recipe and click enter. In this example we're using the local storage 

![init](https://github.com/CristopherLodbrok117/python-scripting-with-prefect/blob/e2f40f1ff3c0847e431d4d0ff94c2500ae61829b/screenshots/03%20-%20init.png)

A yaml file is created automatically. Since we are using the default settings there's no need to modify the file . For more recipe or yaml configuration options visit [prefect deployments](https://docs.prefect.io/3.0/deploy/infrastructure-concepts/prefect-yaml#define-deployments-with-yaml)

<br>

To continue the condiguration
1. Execute the line `prefect deploy` in the terminal.
2. Select the flow to deploy
3. Set a schedule for our flow run (in seconds)
4. Activate the deployment schedule (if you don't want to activate it immediately you can do it manually in the prefect dashboard later)

![deploy](https://github.com/CristopherLodbrok117/python-scripting-with-prefect/blob/e2f40f1ff3c0847e431d4d0ff94c2500ae61829b/screenshots/04%20-%20prefect%20deploy.png)


<br>

Select the work pool. If prefect doesn't shows a list like below, it will ask you to configure one quickly by asking a few questions like before. After choosing the work pool the next message is deployed, with some interesting commands to execute and a link to the UI prefect deployment

![deployment condigured](https://github.com/CristopherLodbrok117/python-scripting-with-prefect/blob/e2f40f1ff3c0847e431d4d0ff94c2500ae61829b/screenshots/05%20-%20pool.png)

You can also create a work pool manually before the deployment configuration following these instructions [prefect-work-pool](https://docs.prefect.io/3.0/deploy/infrastructure-concepts/work-pools#configure-dynamic-infrastructure-with-work-pools)

<br>

## Flow runs 

<br>

Open a new terminal and run the next line `prefect worker start --pool 'copy-file-pool'`.

![worker start](https://github.com/CristopherLodbrok117/python-scripting-with-prefect/blob/e663fa1c550313ac4b13075bb2a4c0ff34f14c02/screenshots/06%20-%20worker%20start.png)

<br>

Prefect runs locally using port 4200. Open the web browser and visit: http://localhost:4200/dashboard
This UI allow us to manage everything with just a few clicks from now on. We can explore our tasks, flows, pools and deployments.

![prefect dashboard](https://github.com/CristopherLodbrok117/python-scripting-with-prefect/blob/e663fa1c550313ac4b13075bb2a4c0ff34f14c02/screenshots/12%20-%20prefect%20dashboard.png)

<br>

When we open the deployments section we can see the progress and details of every run. Prefect lists those ones that have already completed, by clicking on them we can see the details. We can also see the next run

![prefect deployment ui](https://github.com/CristopherLodbrok117/prefect-and-python/blob/b6537460387e505cd44ee3cab9a8185d7965c63e/screenshots/13%20-%20runs.png)

<br>

Remember that we activated the schedule from the terminal, that's why the flow started right away. But we can activate and stop the schedule from this section anytime we want

![activade schedule](https://github.com/CristopherLodbrok117/prefect-and-python/blob/b6537460387e505cd44ee3cab9a8185d7965c63e/screenshots/14%20-%20activate.png)

<br>

If we open a run we can observe relevant details and logs

![prefect run details](https://github.com/CristopherLodbrok117/prefect-and-python/blob/b6537460387e505cd44ee3cab9a8185d7965c63e/screenshots/08%20-%20prefect%20deployment.png)

![prefect run logs](https://github.com/CristopherLodbrok117/prefect-and-python/blob/b6537460387e505cd44ee3cab9a8185d7965c63e/screenshots/10%20-%20deployment%20details.png)

<br>

Now we have automatic backups in fixed intervals (Remember that we can change the origin/destination by modyfing the route, try with other folders and different devices and see the result)

![backup succesful](https://github.com/CristopherLodbrok117/prefect-and-python/blob/b6537460387e505cd44ee3cab9a8185d7965c63e/screenshots/15%20-%20backup%20completed.png)




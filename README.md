Very Good Project
Directory structure:
 - Src code:
    - src/UI_Integrations
    - src/auth_server
 ** Ignore anything else

Flask + Venv Setup (For initial prototype)
Pull bluefoot repo
Navigate to main bluefoot directory. Run python3 -m venv <name of venv here>
Note that the last argument will be the name of the newly created virtual environment directory.
This creates the necessary files for your Flask project's venv. To activate the venv run the following command:
For Windows machines: <name of venv here>\Scripts\activate.bat
For Linux/macOS machines: source <name of venv here>/bin/activate
Run pip install flask
The venv comes bundled with pip. The command above installs flask ONLY to the venv, not your system. You must activate the venv using step 5 before deploying your Flask projects
Install turbo-flask: pip install turbo-flask
Navigate to bluefoot/src/UI_Integrations
IMPORTANT: IF DEPLOYING PUBLICLY, GO INTO UI.PY AND DISABLE DEBUG MODE. Debug mode allows for arbitrary code executions from the deployed site. Don't pull a log4j.
Run python3 UI.py to deploy the app locally. Navigate to localhost:5000/

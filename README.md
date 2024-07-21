Python - Django
======================
This is a simple Python - Django application. This application serves as a basic template for a web server using python for the backend, django as the web application framework.

What does this application do?
-------------------------------
This application serves a simple web server that listens on defined port, default: `8000`.


# How to run?
You can run the application in one of the following ways:

1. Press `F5`. This will start the application in debug mode.

2. Open a terminal by going to 'View' -> 'Terminal'. Then, run following command: 
   > `python manage.py runserver 0.0.0.0:8000`

This will start the application in development mode.


### View output

Studio will automatically open the app in a new browser tab. If not, you can use either of the following methods to access react app within studio:

1. From VS Code command pallette(`Ctrl/Cmd + Shift + P`), run **Studio Manager: SimpleBrowser Default URL** command. This will open the app in a new browser tab.

2. Your app runs on hosted env which can be accessed using host id, port provided in file **.vscode/.studio/studio-env.json**. Use values to create the URL as follows:

   `https://<STUDIO_HOST_ID>-<APP_PORT>.<STUDIO_DOMAIN>`

   For example, if `STUDIO_HOST` is `2e083969-f56e-4d36-bb7e-56ef9cad9946`, `APP_PORT` is `8000` then the URL will be:

   `https://2e083969-f56e-4d36-bb7e-56ef9cad9946-8000.ocws.app`

NOTE: Make following changes in `settings.py` to allow the app to be loaded within VSCode browser:
1. Set the value `ALLOWED_HOSTS` to allow all hosts.
   > `ALLOWED_HOSTS = ['*']`
2. Remove `django.middleware.clickjacking.XFrameOptionsMiddleware` from `MIDDLEWARE` list.


Via curl command:
-----------------
1. Open a terminal.
2. Type the following command: 
   > `curl http://localhost:8000`
3. Press 'Enter' to make the request.

Via Thunder Client:
-------------------
1. Click on the Thunder Client icon on the activity bar on the side. If you can't find it, you can search for 'Thunder Client' in the 'View' -> 'Extensions' menu.
2. Once Thunder Client is open, click on 'New Request'.
3. In the 'Request URL' field, enter the URL of your application (e.g., http://localhost:8000) and select the HTTP method from the dropdown menu.
5. Click on 'Send' to make the request.


Visit [Django Quickstart](https://docs.djangoproject.com/en/5.0/intro/tutorial01/) for more information.

Happy coding! 🙂
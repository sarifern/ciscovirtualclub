# Cisco Running

Repo for Web APP Cisco Running
# Installation

1. Clone the project.

2. Set up your git global config

``` 
git config --global user.name "<Your name>"     
git config --global user.email "<Your email>"
``` 

3. Install PostgreSQL app.
https://postgresapp.com/downloads.html

4. Create a virtual environment for Python 3.7.3, and install the requirements

``` 
pip install -r requirements.txt
``` 

5. Please add the .secrets and local-settings.py files. Ask for them to the admins lurifern@cisco.com
Set .secrets at the parent folder, and local-settings.py under the ic_marathon_site folder
Add the environment variables to your ENV:

``` 
export $(grep -v '^#' .secrets | xargs)
``` 

6. Make the DB migrations

``` 
python manage.py migrate
``` 

7. Create a superuser

``` 
python manage.py createsuperuser
```  

# Running the project locally

In VSCode, you can use the debugging option, as the .vscode/launch.json has the right runserver arguments.
Manually, the command would be

``` 
python manage.py runserver --settings==ic_marathon_site.local_settings
``` 

# Heroku deployment

Make sure you have the Heroku CLI tool.

https://devcenter.heroku.com/articles/heroku-cli

Login to heroku with the HEROKU_ADMIN and HEROKU_PASSWORD variables

``` 
heroku login
``` 

To set environment variables, use the heroku config command

``` 
heroku config:set DJANGO_SECRET_KEY=############ -a ciscorunning
``` 

Since the app is already configured in Heroku (ciscorunning), there is no further configuration.

Once the changes are committed and push to the repo, Heroku will automatically build the new app and deploy it.
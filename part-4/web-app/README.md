# IRWA Final Project
## Search Engine with Web Analytics

Code creators:

- Malena Díaz: u172961
- Cristina Galvez: u172954

### Included in this Project

This code includes a series of python, CSS and HTML files and is based on the Skeleton Project https://github.com/irwa-labs/search-engine-web-app.

By running it, a web application with a search engine is shown, including the following sections:
- Search
- Stats
- Sentiment
- Dashboard
- Session

The user can search with text queries in a corpus of tweet documents about COVID-19 Vaccination. The results are ranked using a ranking algorithm and displayed on screen. The documents can also be individually accessed, where more detailed information can be found. Web-analytics information is recorded from each session and used for the stats and dashboard sections.

This project contains the startup Flask files for developing a web application.

All the datasets that the application uses are also uploaded in this repository for simplicity purposes. 

## How to Run the Web Application

Based on https://github.com/irwa-labs/search-engine-web-app.

### To download this repo locally

Open a terminal console and execute:

```
cd <your preferred projects root directory>

git clone https://github.com/irwa-labs/search-engine-web-app.git

```


### Starting the Web App

```bash
python -V
# Make sure we use Python 3
cd search-engine-web-app
```
The above will start a web server with the application:
```
 * Serving Flask app 'web-app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8088/ (Press CTRL+C to quit)
```

Open Web app in your Browser:  
[http://127.0.0.1:8088/](http://127.0.0.1:8088/) or [http://localhost:8088/](http://localhost:8088/)


### Virtualenv for the project (first time use)
#### Install virtualenv
Having different version of libraries for different projects.  
Solves the elevated privilege issue as virtualenv allows you to install with user permission.

In the project root directory execute:
```bash
pip3 install virtualenv
virtualenv --version
```
virtualenv 20.10.0

#### Prepare virtualenv for the project
In the root of the project folder run:
```bash
virtualenv .
```

If you list the contents of the project root directory, you will see that it has created several sub-directories, including a bin folder (Scripts on Windows) that contains copies of both Python and pip. Also, a lib folder will be created by this action.

The next step is to activate your new virtualenv for the project:

```bash
source bin/activate
```

or for Windows...
```cmd
.\Scripts\activate.bat
```

This will load the python virtualenv for the project.

#### Installing Flask and other packages in your virtualenv

We created a file named requirements.txt so that the installation is much easier. The user should run

```bash
pip install -r requirements.txt
```





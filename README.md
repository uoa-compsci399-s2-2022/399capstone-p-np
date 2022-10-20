# Capstone for Bachelor of Computer science course 399


## Description

This website is written in Python for the backend interfasing the database and GUI, Sql is used to get data from the 
database, we use HTML and CSS to create the website pages and these have some Java in them to create the dynamic interfaces.
The python uses the flask framework and the jinja is used to create the pages.

We have also created an application that will allow the university staff to eddit what courses are avalible and remove courses that don't exist or make changes to them. This is in the "GUI for back end admin updates" folder.

The download button is set to download to within the project so you won't have misilanious .txt files floating around from our assignment.
## Python version

Please use Python version 3.6 or newer versions for development. Some of the depending libraries of our web application do not support Python versions below 3.6!


## Installation

**Installation via requirements.txt**

```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```
(You might need to also type in pip install markupsafe==2.0.1, if (ImportError: cannot import name 'soft_unicode' from 'markupsafe))

When using PyCharm for requirements installation, set the virtual environment using 'File'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution of the web application

To run the website you must run the file called wsgi.py. This will create the website and post a link to it in the console where you run it. The link for you should be showen below.
````
http://localhost:5000/
```` 

## Data collection

We have collected the data from 
(https://www.calendar.auckland.ac.nz/en/courses/faculty-of-science/chemistry.html). We had to use a web scraper to collect all the data and we are unable to determine what courses are still running but have made it update every year so when the courses change the database is automaticly updated
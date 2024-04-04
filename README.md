## Installing required Packages:

First install the packages required for the application.

    pip install -r requirements.txt
(or)

    pip install fastapi psycopg2-binary uvicorn python-dotenv python-multipart
        
Note: make sure on python-dotenv not dotenv

## Understand before running the file:
    
This file can run on git codespaces as well as render free hosting website. The python file runs on uvicorn server for hosting purpose. 

If you want run on your local machine, then remove the if condition which declared the uvicorn server to run as app.

### Environment file:
    
.env file is used in this application to maintain the hostname, port, username, password and database credentials.

I have used in the python file by importing dotenv package of load_dotenv and it is used in main method which loads on loading of the file.
    
Using os package, accessing environment variables by using os.getenv("env_var") method.

### Connectivity:
    
In this application, we use fastapi with posgresSQL which is hosted from render hosting websites.

### Functionality:
    
In this application, we connected posgresSQL with fastapi to return response to ReactUI which store and get data from files table in database.

This application has multiple functionality like file upload, see list of files, see the content of file and finally clearing the screen.

File are uploaded in table with name, extension and content and retrieved using name.extension. We can check the list of files upload using Get all list button.
    
Added CORS, to run in any environment.
    
We can test it without UI also by running the url and add /docs#/ at the end to get Swagger documentation and run the apis to test.

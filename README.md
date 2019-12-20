# iCRM-Django
Interactive CRM in Django.

Follow these instructions to setup:

    • In Project folder 'real_project' open settings.py update the configure the database NAME, USER, PASSWORD and HOST for PostgreSQL
    • Open teminal in the root directory where there is a manage.py file and run following commands:
        •python -m virtualenv crmenv
        •.\crmenv\Scripts\activate

        •pip install -r requirements.txt 
        or 
        •python -m pip install -r requirements.txt

        •python manage.py collectstatic 

        •python manage.py makemigrations employee
        •python manage.py makemigrations leads
        •python manage.py makemigrations records
        •python manage.py makemigrations accounts
        •python manage.py migrate
        

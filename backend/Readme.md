Readme.txt


# Delete all Case objects from the database

python manage.py shell

from case.models import Case
Case.objects.all().delete()



# Retrieve all Case objects from the database

python manage.py shell

from case.models import Case
cases = Case.objects.all()
for case in cases:
    print(case.id)


# Add Field
python manage.py shell < case/import_cases.py
python manage.py makemigrations
python manage.py migrate


# Search
python manage.py shell
from search_index import create_index
create_index()
from search_index import perform_search
results = perform_search("煤矿")
print(results)

导入数据后运行
~~~
 python manage.py rebuild_index
~~~

超级用户：`用户名：xty；密码：xty`
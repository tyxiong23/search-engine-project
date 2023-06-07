import os
# from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'judicature_search.settings')
import django
django.setup()
from case.models import Law, Case

import time

t1 = time.time()
for i in range(1,10000):
    object = Case.objects.get(id=i)
print(time.time() - t1)
# object.head = "山西省长治县人民法院 刑事附带民事判决书 （2017）晋0421刑初173号"
# object.save()
print(object)
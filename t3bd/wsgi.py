import os
from dj_static import Cling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "t3bd.settings")
application = Cling(get_wsgi_application())

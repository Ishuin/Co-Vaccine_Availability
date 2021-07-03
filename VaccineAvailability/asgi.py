# import os
#
# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VaccineAvailability.settings')
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
# })


import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VaccineAvailability.settings")
django.setup()
application = get_default_application()

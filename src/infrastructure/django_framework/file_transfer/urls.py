from shared.utils.setup_startup import setup_startup
from .factories import *


setup_startup(lambda: startup_factory().run())

urlpatterns = [
]

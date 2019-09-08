from shared.di import obj_graph
from web.startup import WebStartup


def startup_factory() -> WebStartup:
    return obj_graph().provide(WebStartup)
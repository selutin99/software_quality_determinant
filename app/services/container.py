from typing import NoReturn

from app import injector, InitialSettings, app


def container() -> NoReturn:
    """
    Dependency initialize container.
    Please do not change initialization order.
    """
    # Utils classes
    injector.map(init_settings=InitialSettings(app=app))
    # Process services
    pass

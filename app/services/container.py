from typing import NoReturn

from app import injector, InitialSettings, app
from services.integrity_service import IntegrityService
from utils.utils import Utils


def container() -> NoReturn:
    """
    Dependency initialize container.
    Please do not change initialization order.
    """
    # Utils classes
    injector.map(init_settings=InitialSettings(app=app))
    injector.map(utils=Utils())
    # Process services
    injector.map(integrity_service=IntegrityService(utils=injector.get('utils')))

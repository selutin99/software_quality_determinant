from typing import NoReturn

from app import injector, InitialSettings, app
from services.calculation_service import CalculationService
from services.polynomial_service import PolynomialService
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
    injector.map(polynomial_service=PolynomialService(utils=injector.get('utils')))
    injector.map(calculation_service=CalculationService(utils=injector.get('utils')))

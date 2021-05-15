import os
from typing import NoReturn

from flask import Flask

from utils.constants import Constants


class InitialSettings:
    def __init__(self, app: Flask):
        self.app = app

    def blueprint_registration(self) -> NoReturn:
        # blueprint for auth routes
        from app.routes.main import main as main_blueprint
        self.app.register_blueprint(main_blueprint)

        from app.routes.calculation import calculation as calculation_blueprint
        self.app.register_blueprint(calculation_blueprint)

    def create_storage_folder(self) -> NoReturn:
        if not os.path.exists(Constants.PATH_TO_CALC_STORAGE_FILE):
            os.makedirs(Constants.PATH_TO_CALC_STORAGE_FILE)
        if not os.path.exists(Constants.PATH_SOLUTION_GRAPHS_IMAGE):
            os.makedirs(Constants.PATH_SOLUTION_GRAPHS_IMAGE)

    def error_handlers(self):
        # Import HTTP base error handlers
        from app.routes.error_handlers import page_not_found
        from app.routes.error_handlers import page_not_avaliable
        from app.routes.error_handlers import page_forbidden

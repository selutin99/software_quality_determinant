import os
from typing import NoReturn

from flask import Flask


class InitialSettings:
    def __init__(self, app: Flask):
        self.app = app

    def blueprint_registration(self) -> NoReturn:
        # blueprint for auth routes
        from app.routes.main import main as main_blueprint
        self.app.register_blueprint(main_blueprint)

        from app.routes.variables import variables as variables_blueprint
        self.app.register_blueprint(variables_blueprint)

    def create_storage_folder(self) -> NoReturn:
        storage_path = 'app/static/calc_storage'

        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

    def error_handlers(self):
        # Import HTTP base error handlers
        from app.routes.error_handlers import page_not_found
        from app.routes.error_handlers import page_not_avaliable
        from app.routes.error_handlers import page_forbidden

        # Import exception handlers
        # from app.routes.error_handlers import handle_base_exception

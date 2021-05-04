from flask import Flask

from initial_settings import InitialSettings
from utils.flask_inject import Inject

app = Flask(__name__)

# Dependency injection container
injector = Inject(app)


def create_app() -> Flask:
    init_settings: InitialSettings = dependency_injection_container_initialize()
    # Create folders for store data
    init_settings.create_storage_folder()
    # Function for registration blueprints of routes in app
    init_settings.blueprint_registration()
    # Import error handlers
    init_settings.error_handlers()

    return app


def dependency_injection_container_initialize() -> InitialSettings:
    from app.services.container import container
    container()
    return injector.get('init_settings')

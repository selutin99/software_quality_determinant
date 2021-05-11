import atexit
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from initial_settings import InitialSettings
from services.scheduled_service import ScheduledService
from utils.flask_inject import Inject

# Create Flask application object and
# set secret key for this object
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Dependency injection container
injector = Inject(app)

# Create scheduler with scheduled task which removes
# old calculation json files from static dir
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(ScheduledService.remover, 'interval', minutes=50)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


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

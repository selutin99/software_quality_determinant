import glob
import os

from utils.constants import Constants
from utils.utils import Utils


class ScheduledService:
    """
    Service not include in DI container
    because it contains only static methods
    """
    JSON_FILE_EXTENSION = '*.json'
    PNG_FILE_EXTENSION = '*.png'
    ONE_DAY_IN_MILLISECONDS: int = 86_400_000

    @staticmethod
    def remove_old_sessions_task():
        # Get service from DI container
        from app import injector
        utils: Utils = injector.get('utils')
        current_timestamp: int = int(utils.get_current_timestamp_millis())

        # Get files for check it on delete
        list_of_json_files: list = glob.glob(Constants.PATH_TO_CALC_STORAGE_FILE + ScheduledService.JSON_FILE_EXTENSION)
        list_of_images_files: list = glob.glob(Constants.PATH_SOLUTION_GRAPHS_IMAGE + ScheduledService.PNG_FILE_EXTENSION)
        list_of_filenames: list = [os.path.splitext(os.path.basename(path))[0] for path in list_of_json_files]

        # Remove old files
        for index, filename in enumerate(list_of_filenames):
            if abs(current_timestamp - int(filename)) > ScheduledService.ONE_DAY_IN_MILLISECONDS:
                os.remove(list_of_json_files[index])
                os.remove(list_of_images_files[index])

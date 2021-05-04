from typing import NoReturn

from utils.constants import Constants


class IntegrityService:
    def create_calc_storage_file(self, calculation_id) -> NoReturn:
        calculation_storage_empty_file = open(
            '{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id),
            'w'
        )
        calculation_storage_empty_file.close()

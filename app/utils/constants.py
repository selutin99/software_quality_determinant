class Constants:
    # Cookie names
    CALCULATION_ID_COOKIE_NAME = 'calculation_id'
    PAGE_COUNTER_COOKIE_NAME = 'page_counter'

    # Variables description
    LAST_VARIABLE_NUMBER = '15'
    FINAL_SETUP_NUMBER = '16'

    VARIABLES_DESCRIPTION = {
        '1': {
            'lower_bound': 1,
            'upper_bound': 7,
            'variable_title': 'L1 надёжность',
            'variable_name': 'L1 (надёжность)',
            'incremental_related_variables': [
                4, 5, 6, 9, 12, 13
            ],
            'decremental_related_variables': [

            ]
        },
        '2': {
            'lower_bound': 7,
            'upper_bound': 12,
            'variable_title': 'L2 практичность',
            'variable_name': 'L2 (практичность)',
            'incremental_related_variables': [
                2, 11, 12, 13, 14
            ],
            'decremental_related_variables': [

            ]
        },
        '3': {
            'lower_bound': 12,
            'upper_bound': 19,
            'variable_title': 'L3 эффективность',
            'variable_name': 'L3 (эффективность)',
            'incremental_related_variables': [
                4, 5, 6, 9, 12, 13, 14
            ],
            'decremental_related_variables': [

            ]
        },
        '4': {
            'lower_bound': 19,
            'upper_bound': 29,
            'variable_title': 'L4 сопровождаемость',
            'variable_name': 'L4 (сопровождаемость)'
        },
        '5': {
            'lower_bound': 29,
            'upper_bound': 37,
            'variable_title': 'L5 защищенность',
            'variable_name': 'L5 (защищенность)'
        },
        '6': {
            'lower_bound': 37,
            'upper_bound': 43,
            'variable_title': 'L6 согласованность',
            'variable_name': 'L6 (согласованность)'
        },
        '7': {
            'lower_bound': 43,
            'upper_bound': 48,
            'variable_title': 'L7 завершенность',
            'variable_name': 'L7 (завершенность)'
        },
        '8': {
            'lower_bound': 48,
            'upper_bound': 56,
            'variable_title': 'L8 анализируемость',
            'variable_name': 'L8 (анализируемость)'
        },
        '9': {
            'lower_bound': 56,
            'upper_bound': 63,
            'variable_title': 'L9 изменяемость',
            'variable_name': 'L9 (изменяемость)'
        },
        '10': {
            'lower_bound': 63,
            'upper_bound': 70,
            'variable_title': 'L10 стабильность',
            'variable_name': 'L10 (стабильность)'
        },
        '11': {
            'lower_bound': 70,
            'upper_bound': 77,
            'variable_title': 'L11 тестируемость',
            'variable_name': 'L11 (тестируемость)'
        },
        '12': {
            'lower_bound': 77,
            'upper_bound': 81,
            'variable_title': 'L12 простота установки',
            'variable_name': 'L12 (простота установки)'
        },
        '13': {
            'lower_bound': 81,
            'upper_bound': 88,
            'variable_title': 'L13 устойчивость',
            'variable_name': 'L13 (устойчивость)'
        },
        '14': {
            'lower_bound': 88,
            'upper_bound': 92,
            'variable_title': 'L14 восстанавливаемость',
            'variable_name': 'L14 (восстанавливаемость)'
        },
        '15': {
            'lower_bound': 92,
            'upper_bound': 99,
            'variable_title': 'L15 понятность',
            'variable_name': 'L15 (понятность)'
        }
    }

    # Paths
    PATH_TO_CALC_STORAGE_FILE = 'app/static/calc_storage/'
    PATH_SOLUTION_GRAPHS_IMAGE = 'app/static/solution_graphs/'


from ..models import Employee


def get_default_status():
    '''
    Get default status options
    Returns:
        data (dict): status options
    '''
    data = {
        "status": {
            k: str(v) for k, v in dict(Employee.StatusOptions.choices).items()},
    }
    return data
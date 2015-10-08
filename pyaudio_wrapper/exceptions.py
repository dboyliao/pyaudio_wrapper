
class DeviceTypeError(Exception): 
    """
    This error will be raise if there is any inconsistency 
    with the device type.
    """
    pass

class PauseTimeout(Exception):
    """
    Raised when there is a pause timeout. eg: recording sound pause timeout.
    """
    pass
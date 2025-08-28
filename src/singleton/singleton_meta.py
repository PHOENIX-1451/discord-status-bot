
class SingletonMeta(type):
    # Dictionary to store multiple singleton subclasses
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # Check if class has already been initialised
        if cls not in SingletonMeta._instances:
            # Initialise class and add to dict
            SingletonMeta._instances[cls] = super().__call__(*args, **kwargs)
        # Return singleton
        return SingletonMeta._instances[cls]
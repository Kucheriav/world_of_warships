class FileEvents(Exception):
    pass


class NoSuchFileError(FileEvents):
    pass


class CorruptedSettingsFileError(FileEvents):
    pass


class FileImportAbortionError(FileEvents):
    def __init__(self):
        super().__init__('Error while importing from file')


class MapEvents(Exception):
    pass


class PlacingShipEvents(MapEvents):
    pass


class StartOutOfBoundError(PlacingShipEvents):
    def __init__(self):
        super().__init__('Start of your ship is out of bound!')


class LengthOutOfBoundError(PlacingShipEvents):
    def __init__(self):
        super().__init__('End of your ship is out of bound!')


class ShipCollisionError(PlacingShipEvents):
    def __init__(self):
        super().__init__('Your ship collides with existing one!')


class ShootOutOfBoundError(PlacingShipEvents):
    def __init__(self):
        super().__init__('You shoot out of bound!')


class ShootingEvents(MapEvents):
    pass


class MissShip(ShootingEvents):
    pass


class HitShip(ShootingEvents):
    pass

class FileEvents(Exception):
    pass


class NoSuchFileError(FileEvents):
    pass


class CorruptedSettingsFileError(FileEvents):
    pass


class MapEvents(Exception):
    pass


class PlacingShipEvents(MapEvents):
    pass


class StartOutOfBound(PlacingShipEvents):
    def __init__(self):
        super().__init__('Start of your ship is out of bound!')


class LengthOutOfBound(PlacingShipEvents):
    def __init__(self):
        super().__init__('End of your ship is out of bound!')


class ShipCollision(PlacingShipEvents):
    def __init__(self, ):
        super().__init__('Your ship collides with existing one!')


class ShootOutOfBound(PlacingShipEvents):
    def __init__(self, ):
        super().__init__('You shoot out of bound!')


class ShootingEvents(MapEvents):
    pass


class MissShip(ShootingEvents):
    pass


class HitShip(ShootingEvents):
    pass

import Config
from tourtament_systems import tourtament_systems


class NoSuchTourtamentSystemException:
    pass


class TourtamentSystemFactory:
    def run(config):
        if (config.tourtament_system in tourtament_systems):
            return tourtament_systems[config.tourtament_system]
        else:
            raise NoSuchTourtamentSystemException("There is no such tourtament system")
           

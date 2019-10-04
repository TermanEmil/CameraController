from business.scheduling import timelapse_repository
from camera_ctrl import models
from enterprise.scheduling.timelapse import Timelapse
from shared.repositories.crud_repository import CrudRepository


class TimelapseRepository(CrudRepository, timelapse_repository.TimelapseRepository):
    model = models.Timelapse
    dto_type = Timelapse
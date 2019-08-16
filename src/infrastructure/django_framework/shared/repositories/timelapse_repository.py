from business.scheduling import timelapse_repository
from enterprise.scheduling.timelapse import Timelapse
from shared.repositories.crud_repository import CrudRepository
from scheduling import models


class TimelapseRepository(CrudRepository, timelapse_repository.TimelapseRepository):
    model = models.Timelapse
    dto_type = Timelapse
from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    @staticmethod
    def build_default_profile():
        profile = Profile(name='default')
        profile.name = 'default'
        profile.save()

        shutterspeed = FavField()
        shutterspeed.profile = profile
        shutterspeed.name_pattern = 'shutterspeed'
        shutterspeed.label = 'Shutter speed'
        shutterspeed.save()

        iso = FavField()
        iso.profile = profile
        iso.name_pattern = 'iso'
        iso.label = 'ISO'
        iso.save()

        return profile


class FavField(models.Model):
    profile = models.ForeignKey(Profile, related_name='fields', on_delete=models.CASCADE)
    name_pattern = models.CharField(max_length=128)
    label = models.CharField(max_length=128)

    def __str__(self):
        return '{0}/{1}'.format(self.profile.name, self.name_pattern)



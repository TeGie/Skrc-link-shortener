from django.db import models

from shorty.models import SkrcUrl


class ClickEventManagers(models.Manager):
    def create_event(self, instance):
        if isinstance(instance, SkrcUrl):
            obj, created = self.get_or_create(skrc_url=instance)
            obj.count += 1
            obj.save()
            return obj.count

        return None


class ClickEvent(models.Model):
    skrc_url = models.OneToOneField(SkrcUrl, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    objects = ClickEventManagers()

    def __str__(self):
        return str(self.count)

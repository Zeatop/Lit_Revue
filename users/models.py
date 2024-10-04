from django.db import models
from django.contrib.auth import models as modelsAuth

class CustomUser(modelsAuth.AbstractUser):
    followed_users = models.ManyToManyField('self', symmetrical=False, related_name='followers_set')

    def subscribe(self, user):
        if user != self:
            self.followed_users.add(user)

    def unsubscribe(self, user):
        self.followed_users.remove(user)

    def is_following(self, user):
        return self.followed_users.filter(id=user.id).exists()


# Create your models here.


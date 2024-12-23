from django.db import models
from django.contrib.auth import models as modelsAuth

class UserFollows(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='followers')
    #+ FollowedUser

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )

class CustomUser(modelsAuth.AbstractUser):
    followed_users = models.ManyToManyField('self', through=UserFollows,  symmetrical=False, related_name='followers_set')

    def subscribe(self, user):
        if user != self:
            UserFollows.objects.get_or_create(user=self, followed_user=user)

    def unsubscribe(self, user):
        UserFollows.objects.filter(user=self, followed_user=user).delete()

    def is_following(self, user):
        return self.followed_users.filter(id=user.id).exists()


# Create your models here.


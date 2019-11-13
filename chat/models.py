from django.db import models

from django.contrib.auth import settings


from content.models import Post

class Chatroom(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)

    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
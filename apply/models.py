from django.db import models
from django.conf import settings
# Create your models here.
from content.models import Post

class Apply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now=True)



    def __str__(self):
        return '{}  {}'.format(self.user,self.post)
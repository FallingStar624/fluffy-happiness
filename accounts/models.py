from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    image = ProcessedImageField(upload_to='avatars',
                                processors=[ResizeToFill(400, 400)],
                                format='JPEG',
                                options={'quality': 60}
            )


    def __str__(self):
        return self.username
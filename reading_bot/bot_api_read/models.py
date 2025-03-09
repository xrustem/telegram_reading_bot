from django.db import models
from gtts import gTTS
import os
from django.conf import settings

class Letter(models.Model):
    text = models.CharField(max_length=1, unique=True)
    image = models.ImageField(upload_to='letters/', blank=True, null=True)
    audio = models.FileField(upload_to='sounds/letters/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Генерация аудио
        if not self.audio:
            audio_path = os.path.join(settings.MEDIA_ROOT, f"sounds/letters/{self.text}.mp3")
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)

            tts = gTTS(self.text, lang="ru")
            tts.save(audio_path)

            self.audio.name = f"sounds/letters/{self.text}.mp3"

        super().save(*args, **kwargs)


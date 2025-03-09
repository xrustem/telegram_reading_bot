from django.contrib import admin
from .models import Letter

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('id','text', 'image_preview', 'audio_preview')
    readonly_fields = ('image_preview', 'audio_preview')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
        return "(Нет изображения)"
    
    def audio_preview(self, obj):
        if obj.audio:
            return f'<audio controls><source src="{obj.audio.url}" type="audio/mpeg"></audio>'
        return "(Нет аудио)"
    
    image_preview.allow_tags = True
    image_preview.short_description = "Превью изображения"
    
    audio_preview.allow_tags = True
    audio_preview.short_description = "Превью аудио"


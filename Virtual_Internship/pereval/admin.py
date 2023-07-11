from django.contrib import admin

from .models import Passage, Coords, Level, Images, User


class CoordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'height',)


class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'winter', 'summer', 'autumn', 'spring',)


# Register your models here.
admin.site.register(Passage)
admin.site.register(Coords, CoordsAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Images)
admin.site.register(User)

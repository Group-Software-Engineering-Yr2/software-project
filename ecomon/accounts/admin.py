from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        '''Called when admin site is altering the form'''
        form = super(ProfileAdmin, self).get_form(request, obj, **kwargs)
        for field in form.base_fields:
            if field not in ['deck_card_1', 'deck_card_2', 'deck_card_3']:
                form.base_fields[field].required = True
            else:
                form.base_fields[field].required = False
        return form

admin.site.register(Profile, ProfileAdmin)
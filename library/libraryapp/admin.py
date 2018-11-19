from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models, forms

class CustomUserAdmin(UserAdmin):
    add_form = forms.CustomUserCreationForm
    form = forms.CustomUserUpdateForm
    model = models.CustomUser
    list_display = ('username', 'email')
    # add_fieldsets = UserAdmin.fieldsets + (
    #     (
    #         None,
    #         {
    #             'fields': ('status', 'description', 'photo'),
    #         }
    #     ), # this comma is necessary here!
    # )
    fieldsets = UserAdmin.fieldsets + (
        (
          None,
          {
              'fields': ('status', 'description', 'photo'),
          }
        ),
    )


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Author)
admin.site.register(models.Book)
admin.site.register(models.Comment)

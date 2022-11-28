from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff')
    search_fields = ('email', 'username',)
    list_filter = ('email', 'username',)
    list_editable = ('email', 'username',)
    empty_value_display = '-пусто-'

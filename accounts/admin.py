from django.contrib import admin

# Register your models here.
from .models import UserDefaultAddress, UserStripe, EmailConfirmed, EmailMarketingSignUp, UserAddress

class UserAddressAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAddress


admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)
admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(UserDefaultAddress)

class EmailMarketingSignUpAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'timestamp', 'updated'] 

admin.site.register(EmailMarketingSignUp)
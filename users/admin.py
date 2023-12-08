from django.contrib import admin

from users.models import Customer, CustomerProfile, Purchase

admin.site.register(Customer)
admin.site.register(CustomerProfile)
admin.site.register(Purchase)

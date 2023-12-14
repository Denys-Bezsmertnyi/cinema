from django.contrib import admin

from users.models import Customer, CustomerProfile

admin.site.register(Customer)
admin.site.register(CustomerProfile)

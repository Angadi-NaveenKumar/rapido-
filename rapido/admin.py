from django.contrib import admin
from .models import (
    Captain, Customer, Ride, RideRating,
    PromoCode, WalletTransaction,
    Notification, RideCancellation
)

admin.site.register(Captain)
admin.site.register(Customer)
admin.site.register(Ride)
admin.site.register(RideRating)
admin.site.register(PromoCode)
admin.site.register(WalletTransaction)
admin.site.register(Notification)
admin.site.register(RideCancellation)


from django.db import models
from django.contrib.auth.models import User


# ──────────────────────────────────────────
# 1. CAPTAIN (Bike Rider / Driver)
# ──────────────────────────────────────────
class Captain(models.Model):
    """Rapido bike captain (driver) profile."""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending_verification', 'Pending Verification'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='captain')
    phone = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='captains/', blank=True, null=True)

    # Vehicle Info
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_model = models.CharField(max_length=100)
    vehicle_color = models.CharField(max_length=50)

    # Documents
    driving_license = models.CharField(max_length=50, unique=True)
    aadhar_number = models.CharField(max_length=12, unique=True)

    # Status & Ratings
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending_verification')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    total_rides = models.PositiveIntegerField(default=0)
    is_online = models.BooleanField(default=False)

    # Location (last known)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Captain: {self.user.get_full_name()} ({self.vehicle_number})"

    class Meta:
        ordering = ['-created_at']


# ──────────────────────────────────────────
# 2. CUSTOMER
# ──────────────────────────────────────────
class Customer(models.Model):
    """Rapido app customer/rider."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='customers/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    total_rides = models.PositiveIntegerField(default=0)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customer: {self.user.get_full_name()} ({self.phone})"

    class Meta:
        ordering = ['-created_at']


# ──────────────────────────────────────────
# 3. RIDE
# ──────────────────────────────────────────
class Ride(models.Model):
    """A single ride booking from customer to destination."""

    RIDE_TYPE_CHOICES = [
        ('bike', 'Bike'),
        ('auto', 'Auto'),
        ('cab', 'Cab Economy'),
    ]

    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('captain_assigned', 'Captain Assigned'),
        ('captain_arrived', 'Captain Arrived'),
        ('ride_started', 'Ride Started'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='rides')
    captain = models.ForeignKey(Captain, on_delete=models.SET_NULL, null=True, blank=True, related_name='rides')

    ride_type = models.CharField(max_length=10, choices=RIDE_TYPE_CHOICES, default='bike')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')

    pickup_address = models.TextField()
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6)

    drop_address = models.TextField()
    drop_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    drop_longitude = models.DecimalField(max_digits=9, decimal_places=6)

    estimated_fare = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    final_fare = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)

    payment_method = models.CharField(
        max_length=20,
        choices=[('cash', 'Cash'), ('wallet', 'Wallet'), ('upi', 'UPI'), ('card', 'Card')],
        default='cash'
    )
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')

    promo_code = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, null=True, blank=True, related_name='rides')
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    requested_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Ride #{self.id} | {self.customer} → {self.drop_address[:30]} ({self.status})"

    class Meta:
        ordering = ['-requested_at']


# ──────────────────────────────────────────
# 4. RIDE RATING
# ──────────────────────────────────────────
class RideRating(models.Model):
    """Rating given after a completed ride."""

    ride = models.OneToOneField(Ride, on_delete=models.CASCADE, related_name='rating')
    rating_by_customer = models.PositiveSmallIntegerField(null=True, blank=True)
    rating_by_captain = models.PositiveSmallIntegerField(null=True, blank=True)
    review_by_customer = models.TextField(blank=True, null=True)
    review_by_captain = models.TextField(blank=True, null=True)
    tip_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00,
        help_text="Optional tip given by customer to captain after the ride")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating for Ride #{self.ride.id}"


# ──────────────────────────────────────────
# 5. PROMO CODE
# ──────────────────────────────────────────
class PromoCode(models.Model):
    """Discount promo codes for rides."""

    DISCOUNT_TYPE_CHOICES = [
        ('flat', 'Flat Amount'),
        ('percent', 'Percentage'),
    ]

    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=6, decimal_places=2)
    max_discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    min_ride_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    valid_from = models.DateField()
    valid_until = models.DateField()
    usage_limit = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Promo: {self.code} ({self.discount_type} - {self.discount_value})"

    class Meta:
        ordering = ['-valid_until']


# ──────────────────────────────────────────
# 6. WALLET TRANSACTION
# ──────────────────────────────────────────
class WalletTransaction(models.Model):
    """Records every money movement in a customer's wallet."""

    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
        ('refund', 'Refund'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    ride = models.ForeignKey(Ride, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.user.username} | {self.transaction_type} ₹{self.amount}"

    class Meta:
        ordering = ['-created_at']


# ──────────────────────────────────────────
# 7. NOTIFICATION
# ──────────────────────────────────────────
class Notification(models.Model):
    """Push notifications sent to customer or captain."""

    RECIPIENT_TYPE = [
        ('customer', 'Customer'),
        ('captain', 'Captain'),
    ]

    recipient_type = models.CharField(max_length=10, choices=RECIPIENT_TYPE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    captain = models.ForeignKey(Captain, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification → {self.recipient_type}: {self.title}"

    class Meta:
        ordering = ['-created_at']


# ──────────────────────────────────────────
# 8. RIDE CANCELLATION
# ──────────────────────────────────────────
class RideCancellation(models.Model):
    """Stores detailed cancellation info whenever a ride is cancelled."""

    CANCELLED_BY_CHOICES = [
        ('customer', 'Customer'),
        ('captain', 'Captain'),
        ('system', 'System'),
    ]

    REASON_CHOICES = [
        ('driver_not_arriving', 'Driver Not Arriving'),
        ('wrong_location', 'Wrong Location'),
        ('change_of_plans', 'Change of Plans'),
        ('high_fare', 'High Fare'),
        ('others', 'Others'),
    ]

    ride = models.OneToOneField(Ride, on_delete=models.CASCADE, related_name='cancellation')
    cancelled_by = models.CharField(max_length=10, choices=CANCELLED_BY_CHOICES)
    reason = models.CharField(max_length=30, choices=REASON_CHOICES, default='others')
    additional_comments = models.TextField(blank=True, null=True)
    penalty_charged = models.BooleanField(default=False)
    penalty_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    cancelled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancellation for Ride #{self.ride.id} by {self.cancelled_by}"

    class Meta:
        ordering = ['-cancelled_at']


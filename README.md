# Rapido Ride Booking Backend

## Overview

Rapido Ride Booking Backend is a Django-based REST API project that simulates a ride-hailing platform similar to Rapido. The system manages customers, captains (drivers), rides, ride ratings, wallet transactions, promo codes, notifications, and ride cancellations.

## Features

### Captain Management

* Captain registration and profile management
* Vehicle information tracking
* Online/offline status management
* Rating and ride statistics

### Customer Management

* Customer profile management
* Wallet balance tracking
* Ride history management

### Ride Management

* Ride booking and assignment
* Ride status tracking
* Fare estimation and payment handling
* Ride completion and cancellation support

### Ride Ratings

* Customer and captain ratings
* Ride reviews
* Optional tip amount support

### Promo Codes

* Flat and percentage-based discounts
* Usage limits and validity periods

### Wallet Transactions

* Credit, debit, and refund tracking
* Transaction history management

### Notifications

* Customer and captain notifications
* Read/unread status tracking

### Ride Cancellation

* Detailed cancellation tracking
* Cancellation reasons
* Penalty management

## Technologies Used

* Python 3.x
* Django 5.x
* Django REST Framework
* SQLite3
* Pillow

## Project Structure

```text
rapido_project/
│
├── manage.py
├── db.sqlite3
│
├── rapido/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── migrations/
│
└── rapido_project/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
```

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd rapido_project
```

### Install Dependencies

```bash
pip install django djangorestframework pillow
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Start Server

```bash
python manage.py runserver
```

Server URL:

```text
http://127.0.0.1:8000/
```

Admin Panel:

```text
http://127.0.0.1:8000/admin/
```

## Database Models

* Captain
* Customer
* Ride
* RideRating
* PromoCode
* WalletTransaction
* Notification
* RideCancellation

## Future Enhancements

* JWT Authentication
* Real-Time Ride Tracking
* GPS Integration
* Payment Gateway Integration
* Push Notifications
* Ride Analytics Dashboard
* Mobile Application Support

## Author

Naveen Angadi

## License

This project is developed for educational and learning purposes.


Vendor Management System with Performance Metrics
This repository contains a Vendor Management System developed using Django and Django REST Framework. 
The system enables users to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

Objective
The objective of this project is to create a Vendor Management System that simplifies vendor-related tasks and provides insights into vendor performance.

Core Features
Vendor Profile Management:
Create, retrieve, update, and delete vendor profiles.

API Endpoints:
POST /api/vendors/: Create a new vendor.
GET /api/vendors/: List all vendors.
GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
PUT /api/vendors/{vendor_id}/: Update a vendor's details.
DELETE /api/vendors/{vendor_id}/: Delete a vendor.

Purchase Order Tracking:
Track purchase orders with relevant details.

API Endpoints:
POST /api/purchase_orders/: Create a purchase order.
GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.
GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
PUT /api/purchase_orders/{po_id}/: Update a purchase order.
DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.

Vendor Performance Evaluation:
Calculate performance metrics including on-time delivery rate, quality rating average, average response time, and fulfilment rate.

API Endpoints:
GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance metrics.

Update Acknowledgment Endpoint:
Consider an endpoint like POST /api/purchase_orders/{po_id}/acknowledge for vendors to acknowledge POs.

Setup Instructions
To set up the project locally, follow these steps:

Clone this repository.
Install Python and Django.
Install required dependencies (pip install -r requirements.txt).
Run migrations (python manage.py migrate).
Start the development server (python manage.py runserver).

Test :
1. you can test the code the using POSTMAN

OR using python requests file follow the code given bellow
Example:-

import requests

url = 'http://127.0.0.1:8000/api/vendors/'

header = {"Authorization": "Token 6863550cc647d7a3501445863e83b0f5cda5f621"}
get_response = requests.get(url, headers=header)
print(get_response.json())





from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('register', views.RegisterView)
router.register('vendors', views.VendorView)
router.register('purchase_orders', views.PurchaseOrderView)


urlpatterns = [
    path('auth/', obtain_auth_token),
    path('login/', views.CustomAuthToken.as_view()),
    path('', include(router.urls)),
    path('vendors/<int:id>/performance/', views.VendorPerformanceView.as_view()),
    # path('purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order),
    path('purchase_orders/<int:id>/acknowledge/', views.PurchaseOrderAcknowledgmentViewSet.as_view()),

]

from rest_framework import routers
from produce.api_views import ProductModalViewSet


router = routers.DefaultRouter()
router.register('', ProductModalViewSet, basename='product-modal')
urlpatterns = router.urls

from django.conf.urls import include, url, patterns
from rest_framework import routers

from authentication.views import AccountViewSet, LoginView, LogoutView
from workflow.views import ProjectViewSet, OrderViewSet

router = routers.SimpleRouter()
router.register(u'accounts', AccountViewSet)
router.register(u'projects', ProjectViewSet)
router.register(u'orders', OrderViewSet)

urlpatterns = [
    url('^api/v1/', include(router.urls)),
    url('^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url('^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
]

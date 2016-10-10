from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth import views as auth

from rest_framework import routers

from authentication.views import AccountViewSet, LoginView, LogoutView
from workflow.views import ProjectViewSet, OrderViewSet
from viewflow.flow import views as viewflow

router = routers.SimpleRouter()
router.register(u'accounts', AccountViewSet)
router.register(u'projects', ProjectViewSet)
router.register(u'orders', OrderViewSet)

from workflow.flows import OrderCompleteProjectFlow

flows = {
    'order-complete-project': OrderCompleteProjectFlow,
}

urlpatterns = [
    url(r'^$', viewflow.AllProcessListView.as_view(ns_map=flows), name="index"),
    url(r'^tasks/$', viewflow.AllTaskListView.as_view(ns_map=flows), name="tasks"),
    url(r'^queue/$', viewflow.AllQueueListView.as_view(ns_map=flows), name="queue"),

    url(r'^order-workflows/', include('workflow.urls'), name='order-workflows'),

    url(r'^accounts/login/$', auth.login, name='login'),
    url(r'^accounts/logout/$', auth.logout, name='logout'),

    url('^api/v1/', include(router.urls)),
    url('^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url('^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
]

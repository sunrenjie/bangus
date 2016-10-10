from viewflow.flow import routers
from .flows import OrderCompleteProjectFlow

urlpatterns = routers.FlowRouter(OrderCompleteProjectFlow).urls

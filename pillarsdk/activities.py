from .resource import List
from .resource import Find
from .resource import Update
from .resource import Create


class Activity(List, Find):
    """Activities class wrapping the REST activities endpoint
    """
    path = "activities"


class Notification(List, Find, Update):
    """Notifications class wrapping the REST notifications endpoint
    """
    path = "notifications"

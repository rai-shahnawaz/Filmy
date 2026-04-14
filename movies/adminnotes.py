from neomodel import StructuredNode, StringProperty, DateTimeProperty, UniqueIdProperty
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

class AdminNote(StructuredNode):
    uid = UniqueIdProperty()
    object_type = StringProperty(required=True)
    object_uid = StringProperty(required=True)
    user_id = StringProperty(required=True)
    note = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)

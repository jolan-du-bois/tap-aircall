"""Stream type classes for tap-aircall."""

from typing import Optional

from tap_aircall.client import aircallStream
from .schemas import user_properties, call_properties


class UsersStream(aircallStream):
    """Define custom stream."""
    name = "users"
    path = "v1/users"
    primary_keys = ["id"]
    replication_key = "created_at"
    schema = user_properties.to_dict()
    records_jsonpath = "$.users[*]"  # Or override `parse_response`.

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "user_id": record["id"]
        }

class CallsStream(aircallStream):
    """Define custom stream."""
    name = "calls"
    path = "v1/calls"
    primary_keys = ["id"]
    replication_key = "started_at"
    schema = call_properties.to_dict()
    records_jsonpath = "$.calls[*]"  # Or override `parse_response`.

class UserStream(aircallStream):
    """Define custom stream."""
    name = "user"
    parent_stream_type = UsersStream
    path = "v1/users/{user_id}"

    primary_keys = ["id"]
    replication_key = "created_at"
    schema = user_properties.to_dict()
    records_jsonpath = "$.users[*]"  # Or override `parse_response`.
    #  not to store any state bookmarks for the child stream
    state_partitioning_keys = []

#: Task state is unknown (assumed pending since you know the id).
PENDING = "PENDING"
#: Task was received by a worker (only used in events).
RECEIVED = "RECEIVED"
#: Task was started by a worker (:setting:`task_track_started`).
STARTED = "STARTED"
#: Task succeeded
SUCCESS = "SUCCESS"
#: Task failed
FAILURE = "FAILURE"
#: Task was revoked.
REVOKED = "REVOKED"
#: Task was rejected (only used in events).
REJECTED = "REJECTED"
#: Task is waiting for retry.
RETRY = "RETRY"
IGNORED = "IGNORED"

READY_STATES = frozenset({SUCCESS, FAILURE, REVOKED})

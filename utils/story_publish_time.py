from time import time
import datetime

# Instructions:
#     - append `?format=json`
#     - search "scheduledPublishAt"
#     - copy the value
#     - paste below
#     - `python story_publish_time.py`

future = int(1707408900000) / 1000
present = int(time())
totsec = future - present
secs = str(int(totsec % 60))
mins = str(int((totsec % 3600) / 60))
hours = str(int((totsec % 86400) / 3600))
days = str(int((totsec % (86400 * 30)) / 86400))
futuredate = datetime.datetime.fromtimestamp(future)
print("Your story is scheduled to be published on\n")
print(str(futuredate) + " GMT. i.e.,\n")
print(
    "In " + days + " days " + hours + " hours " + mins + " minutes " + secs + " seconds"
)

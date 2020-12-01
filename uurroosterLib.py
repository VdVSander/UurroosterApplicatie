import os
import pickle
import datetime
from googleapiclient.discovery import build


# Define a class for the courses
class Course:
    def __init__(self, name, start_time, end_time, location):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.location = location


# Define a class for time differences
class TimeDelta:
    def __init__(self, days, hours, minutes, seconds):
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds


def format_course(course):
    # Get start and end date and time of course
    event_start = course['start']['dateTime']
    event_start = event_start.replace("T", " ")
    event_start = event_start[:-6]
    event_start = datetime.datetime.strptime(event_start, "%Y-%m-%d %H:%M:%S")
    event_end = course['end']['dateTime']
    event_end = event_end.replace("T", " ")
    event_end = event_end[:-6]
    event_end = datetime.datetime.strptime(event_end, "%Y-%m-%d %H:%M:%S")

    # Get name of course
    event_name = course['summary']

    # Try to obtain location of the event
    try:
        event_location = course['location']
    except:
        event_location = ""
    event_name, rest = event_name.split('(')
    return event_name, event_start, event_end, event_location


def calculate_time_delta(time):
    current_time = datetime.datetime.now()
    delta = time - current_time
    seconds = int(delta.total_seconds())
    seconds_in_day = 86400
    seconds_in_hour = 3600
    seconds_in_minute = 60

    days = seconds // seconds_in_day
    seconds -= days * seconds_in_day

    hours = seconds // seconds_in_hour
    seconds -= hours * seconds_in_hour

    minutes = seconds // seconds_in_minute
    seconds -= minutes * seconds_in_minute

    time_delta = TimeDelta(days, hours, minutes, seconds)

    return time_delta


def load_events(amount):
    # Call the Calendar API
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print("Getting List first " + str(amount) + " events")
        events_result = service.events().list(
            calendarId='s3p9tq7pip9k8vhf14lr5bf6md1c3ipb@import.calendar.google.com', timeMin=now,
            maxResults=amount, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events
    else:
        print("ERROR: Credentials do not exist")


def get_courses(events):
    if not events:
        courses = []
        return courses
    else:
        courses = []
        for i in range(0, len(events)):
            name, event_start, event_end, location = format_course(events[i])
            courses.append(Course(name, event_start, event_end, location))
        return courses

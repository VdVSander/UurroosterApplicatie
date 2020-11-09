import datetime
from call_setup import get_calendar_service


class Course:
    def __init__(self, name, start_time, end_time):
        self.name = name
        #self.location = location
        self.start_time = start_time
        self.end_time = end_time


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
    print(course['location'])
    event_name, rest = event_name.split('(')
    return event_name, event_start, event_end


def calc_tdelta(seconds):
    seconds_in_day = 86400
    seconds_in_hour = 3600
    seconds_in_minute = 60

    days = seconds // seconds_in_day
    seconds -= days * seconds_in_day

    hours = seconds // seconds_in_hour
    seconds -= hours * seconds_in_hour

    minutes = seconds // seconds_in_minute
    seconds -= minutes * seconds_in_minute

    return days, hours, minutes, seconds


def main():
    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting List first 2 events')
    events_result = service.events().list(
        calendarId='s3p9tq7pip9k8vhf14lr5bf6md1c3ipb@import.calendar.google.com', timeMin=now,
        maxResults=2, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    curr_time = datetime.datetime.now()
    print("Current time: " + curr_time.strftime("%Y-%m-%d %H:%M:%S"))
    print("-----------------------------------")

    courses = []

    if not events:
        print('No upcoming events found.')
    else:
        for i in range(0, 2):
            name, event_start, event_end = format_course(events[i])
            courses.append(Course(name, event_start, event_end))

        if (curr_time > courses[0].start_time) and (curr_time < courses[0].end_time):
            print("Je hebt momenteel les.")
            print(courses[0].end_time - curr_time)
            print("volgende les begint op: " + courses[1].start_time.strftime("%H:%M:%S"))
        else:
            print("Je hebt momenteel geen les.")
            print("Volgende les: " + courses[0].name)
            tdelta = courses[0].start_time - curr_time
            tdelta_days, tdelta_hours, tdelta_minutes, tdelta_seconds = calc_tdelta(int(tdelta.total_seconds()))
            print("Les begint in: " + str(tdelta_days) + " dagen, " + str(tdelta_hours) + " uren, " + str(tdelta_minutes) + " minuten en " + str(tdelta_seconds) + " seconden.")



if __name__ == '__main__':
    main()

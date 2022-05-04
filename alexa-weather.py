from datetime import datetime, timezone
from notifyme import send_notification
from nws import get_latest_temperature_in_c_for_coordinates
from time import sleep

import pytz

DEFAULT_COORDINATES = '0.00001, 0.00001'
NOTIFY_TEMPERATURE = 26.666
DEFAULT_OVER_TEMPERATURE_MESSAGE = 'At %s it is over 80 degrees outside so bring in dog'
DEFAULT_UNDER_TEMPERATURE_MESSAGE = 'At %s it is under 80 degrees so dog can go back outside'

RISING_SLEEP_PERIOD_IN_MIN = 15
WAITING_SLEEP_PERIOD_IN_MIN = 60

def main():
    while True:
        if wait_until_above_notify_temperature():
            print(f'Over {NOTIFY_TEMPERATURE} degrees')
            current_time = datetime.now(tz=pytz.timezone("America/Los_Angeles")).strftime('%H:%M')
            send_notification(DEFAULT_OVER_TEMPERATURE_MESSAGE % current_time)

        if wait_until_under_notify_temperature():
            print(f'Under {NOTIFY_TEMPERATURE} degrees')
            current_time = datetime.now(tz=pytz.timezone("America/Los_Angeles")).strftime('%H:%M')
            send_notification(DEFAULT_UNDER_TEMPERATURE_MESSAGE % current_time)

def wait_until_above_notify_temperature():
    latest_temperature = 0
    while True:
        current_time = datetime.now(tz=pytz.timezone("America/Los_Angeles"))
        prior_temperature = latest_temperature
        latest_temperature = get_latest_temperature_in_c_for_coordinates(DEFAULT_COORDINATES)
        print(f'Checking for rising temperature at {current_time} and temperature is {latest_temperature}')
        if not latest_temperature:
            print('Unable to get temperature from weather service...  Trying again in 1 minute')
            sleep(60)
            continue
        if latest_temperature > NOTIFY_TEMPERATURE:
            return True
        # If more than 5 degrees C below or more than 0.5 degrees C from last temperature (still lowering), wait longer
        if latest_temperature < (NOTIFY_TEMPERATURE - 5) or latest_temperature < (prior_temperature - 0.5):
            print(f'Waiting {WAITING_SLEEP_PERIOD_IN_MIN} minutes...')
            sleep(WAITING_SLEEP_PERIOD_IN_MIN * 60)
        else:
            print(f'Waiting {RISING_SLEEP_PERIOD_IN_MIN} minutes...')
            sleep(RISING_SLEEP_PERIOD_IN_MIN * 60)
        
def wait_until_under_notify_temperature():
    latest_temperature = 1000
    while True:
        current_time = datetime.now(tz=pytz.timezone("America/Los_Angeles"))
        prior_temperature = latest_temperature
        latest_temperature = get_latest_temperature_in_c_for_coordinates(DEFAULT_COORDINATES)
        print(f'Checking for falling temperature at {current_time} and temperature is {latest_temperature}')
        if latest_temperature < NOTIFY_TEMPERATURE:
            return True
        # If more than 5 degrees C above or more than 0.5 degrees C from last temperature (still raising), wait longer
        if latest_temperature > (NOTIFY_TEMPERATURE + 5) or latest_temperature > (prior_temperature + 0.5):
            print(f'Waiting {WAITING_SLEEP_PERIOD_IN_MIN} minutes...')
            sleep(WAITING_SLEEP_PERIOD_IN_MIN * 60)
        else:
            print(f'Waiting {RISING_SLEEP_PERIOD_IN_MIN} minutes...')
            sleep(RISING_SLEEP_PERIOD_IN_MIN * 60)
        


if __name__ == '__main__':
    main()

from datetime import datetime, timezone
from notifyme import send_notification
from nws import get_latest_temperature_in_c_for_coordinates
from time import sleep

import pytz

DEFAULT_COORDINATES = '33.632802,-117.693676'
NOTIFY_TEMPERATURE = 26.666
DEFAULT_OVER_TEMPERATURE_MESSAGE = 'At %s it is over 80 degrees outside so bring in Lacey'
DEFAULT_UNDER_TEMPERATURE_MESSAGE = 'At %s it is under 80 degrees so Lacey can go back outside'

RISING_SLEEP_PERIOD_IN_MIN = 15
WAITING_SLEEP_PERIOD_IN_MIN = 60

def main():
    while True:
        if wait_until_above_notify_temperature():
            print('Over {} degrees'.format(NOTIFY_TEMPERATURE))
            current_time = datetime.now(tz=pytz.timezone("America/Los_Angeles")).strftime('%H:%M')
            send_notification(DEFAULT_OVER_TEMPERATURE_MESSAGE % current_time)

        if wait_until_under_notify_temperature():
            print('Under {} degrees'.format(NOTIFY_TEMPERATURE))
            current_time = datetime.now(tz=pytz.timezone("America/Los_Angeles")).strftime('%H:%M')
            send_notification(DEFAULT_UNDER_TEMPERATURE_MESSAGE % current_time)

def wait_until_above_notify_temperature():
    latest_temperature = 0
    while True:
        current_time = datetime.now(tz=pytz.timezone("America/Los_Angeles"))
        prior_temperature = latest_temperature
        latest_temperature = get_latest_temperature_in_c_for_coordinates(DEFAULT_COORDINATES)
        print('Checking for rising temperature at {} and temperature is {}'.format(current_time, latest_temperature))
        if not latest_temperature:
            print('Unable to get temperature from weather service...  Trying again in 1 minute')
            sleep(60)
            continue
        if latest_temperature > NOTIFY_TEMPERATURE:
            return True
        # If more than 5 degrees C below or more than 0.5 degrees C from last temperature (still lowering), wait longer
        if latest_temperature < (NOTIFY_TEMPERATURE - 5) or latest_temperature < (prior_temperature - 0.5):
            print('Waiting {} minutes...'.format(WAITING_SLEEP_PERIOD_IN_MIN))
            sleep(WAITING_SLEEP_PERIOD_IN_MIN * 60)
        else:
            print('Waiting {} minutes...'.format(RISING_SLEEP_PERIOD_IN_MIN))
            sleep(RISING_SLEEP_PERIOD_IN_MIN * 60)
        
def wait_until_under_notify_temperature():
    latest_temperature = 1000
    while True:
        current_time = datetime.now(tz=pytz.timezone("America/Los_Angeles"))
        prior_temperature = latest_temperature
        latest_temperature = get_latest_temperature_in_c_for_coordinates(DEFAULT_COORDINATES)
        print('Checking for falling temperature at {} and temperature is {}'.format(current_time, latest_temperature))
        if latest_temperature < NOTIFY_TEMPERATURE:
            return True
        # If more than 5 degrees C above or more than 0.5 degrees C from last temperature (still raising), wait longer
        if latest_temperature > (NOTIFY_TEMPERATURE + 5) or latest_temperature > (prior_temperature + 0.5):
            print('Waiting {} minutes...'.format(WAITING_SLEEP_PERIOD_IN_MIN))
            sleep(WAITING_SLEEP_PERIOD_IN_MIN * 60)
        else:
            print('Waiting {} minutes...'.format(RISING_SLEEP_PERIOD_IN_MIN))
            sleep(RISING_SLEEP_PERIOD_IN_MIN * 60)
        


if __name__ == '__main__':
    main()

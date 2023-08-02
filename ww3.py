import datetime
import time
import signal
from RPLCD.i2c import CharLCD

# Replace 0x27 with the I2C address of your LCD module
lcd = CharLCD('PCF8574', 0x27)

lcd.backlight_enabled = True  # Turn on backlight initially

target_date = datetime.datetime(2023, 11, 23, 18, 0, 0)

def cleanup_handler(signum, frame):
    lcd.clear()
    lcd.write_string("Exiting...")
    time.sleep(2)
    lcd.clear()
    lcd.backlight_enabled = False  # Turn off backlight before exiting
    lcd.close(clear=True)  # Close the LCD connection
    exit(0)

signal.signal(signal.SIGINT, cleanup_handler)

try:
    while True:
        current_time = datetime.datetime.now()
        time_elapsed = current_time - target_date

        if time_elapsed.total_seconds() >= 0:
            lcd.clear()
            lcd.write_string("Countdown finished!")
            lcd.backlight_enabled = False  # Turn off backlight
            time.sleep(2)  # Wait for 2 seconds to display the message
            cleanup_handler(None, None)

        time_remaining = abs(time_elapsed)
        days, seconds = divmod(time_remaining.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        countdown_str = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

        lcd.cursor_pos = (0, 0)
        lcd.write_string("Time remaining:")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(countdown_str)

        lcd.backlight_enabled = True  # Turn on backlight
        time.sleep(1)

except KeyboardInterrupt:
    cleanup_handler(None, None)

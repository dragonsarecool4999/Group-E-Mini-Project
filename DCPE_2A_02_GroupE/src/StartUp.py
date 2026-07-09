import time
import queue
from threading import Thread

from hal import hal_lcd as LCD
from hal import hal_keypad as keypad

IDLE_TIMEOUT_SECONDS = 60

shared_keypad_queue = queue.Queue()


def key_pressed(key):
    shared_keypad_queue.put(key)


def display_main_menu(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("1. Collect Books", 1)
    lcd.lcd_display_string("2. Return Books", 2)


def drain_stale_keys():
    # Discard any keypress that arrived while we were busy in another
    # flow (e.g. during input() for a barcode scan) so it can't be
    # mistaken for a fresh key and silently reset the idle timer.
    while not shared_keypad_queue.empty():
        shared_keypad_queue.get_nowait()


def wait_for_key_or_timeout(lcd, timeout_seconds):
    drain_stale_keys()
    start = time.monotonic()

    while True:
        elapsed = time.monotonic() - start
        remaining = timeout_seconds - elapsed

        if remaining <= 0:
            print("No key pressed for {}s -> entering low power mode".format(timeout_seconds))
            return None

        try:
            key = shared_keypad_queue.get(timeout=remaining)
            print("Key received:", key, "-> resetting idle timer")
            return key
        except queue.Empty:
            return None


def user_authentication_flow(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("Scan NRIC", 1)
    nric = input("Scan NRIC barcode: ").strip()

    # TODO: validate NRIC / look up borrower once REQ-07 is defined

    lcd.lcd_clear()
    lcd.lcd_display_string("Books dispensed", 1)
    lcd.lcd_display_string("for collection", 2)
    time.sleep(2)


def book_return_flow(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("Scan ISBN", 1)
    isbn = input("Scan ISBN barcode: ").strip()

    # TODO: process the return once REQ-16 is defined

    lcd.lcd_clear()
    lcd.lcd_display_string("Book returned", 1)
    time.sleep(2)


def enter_low_power_mode(lcd):
    # REQ-26 placeholder: turn off the backlight and block here until any
    # key is pressed, so low power mode is visibly persistent rather than
    # a blink-and-continue.
    lcd.lcd_clear()
    lcd.backlight(0)
    print("LCD backlight off. Waiting for a key press to wake up...")

    drain_stale_keys()
    shared_keypad_queue.get()  # block indefinitely until any key wakes it

    print("Key pressed -> waking up")
    lcd.backlight(1)


def main():
    lcd = LCD.lcd()

    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key, daemon=True)
    keypad_thread.start()

    while True:
        display_main_menu(lcd)

        key = wait_for_key_or_timeout(lcd, IDLE_TIMEOUT_SECONDS)

        if key is None:
            enter_low_power_mode(lcd)
            continue

        if key == 1:
            user_authentication_flow(lcd)
        elif key == 2:
            book_return_flow(lcd)


if __name__ == '__main__':
    main()
from threading import Thread
from hal import hal_lcd as LCD
from time import sleep
from hal import hal_keypad as keypad
import config


user_input =""


def keypad_check(key):
    global user_input
    if key is not None:
        user_input += str(key)
    
    if (len(user_input)==1):
        if key ==1:
            config.return_books=1
        elif key ==2:
            config.collect_books=1
        elif key==3:
            config.extend_return_period=1
        elif key <1 or key>3:
            config.outside_range=1
        sleep(0.3)

def main():
    global user_input
    lcd= LCD.lcd()
    lcd.lcd_clear()
    keypad.init(keypad_check)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    last_state =None
    while True:
        if config.return_books==1:
            if last_state != "return":
                lcd.lcd_clear()      
                last_state = "return" 
            lcd.lcd_display_string("Book return selected",1)
            lcd.lcd_display_string("Processing...",2)
            #if return_books_success==1:
                #lcd.lcd_display_string("Successful",1)
                #lcd.lcd_display_string("Thank you for return your books")
        elif config.collect_books==1:
            if last_state != "collect":
                lcd.lcd_clear()
                last_state="collect"
            lcd.lcd_display_string("Book collection selected",1)
            lcd.lcd_display_string("Processing...",2)
            #if collect_books_success==1:
                #lcd.lcd_display_string("Successful",1)
                #lcd.lcd_display_string("Book has been disepensed")
        elif config.extend_return_period==1:
            if last_state != "extend":
                lcd.lcd_clear()
                last_state= "extend"
            lcd.lcd_display_string("Book extension requested",1)
            lcd.lcd_display_string("Processing...",2)
            #if extend_return_period_sucess==1:
                #lcd.lcd_display_string("Successful",1)
                #lcd.lcd_display_string("Book return period has been extended",2)
        elif config.outside_range==1:
            if last_state!="ofr":
                lcd.lcd_clear()
                last_state="ofr"
            lcd.lcd_display_string("Number inputted was out of range",1)
            lcd.lcd_display_string("Please input a number a between 1-3",2)
            config.outside_range =0
            user_input=""
        else:
            if last_state != 'idle':
                lcd.lcd_clear()
                last_state ="idle"

            lcd.lcd_display_string("Library book system",1)
            lcd.lcd_display_string("1-ret, 2-col, 3-ext: "+user_input,2)

        sleep(0.3)
        # should be scaled in the future to display if an error has happened due to borrowing too many books, not being a valid 
        #user or if the user has already extended his return period etc. after the database has been completed
if __name__=='__main__':
    main()
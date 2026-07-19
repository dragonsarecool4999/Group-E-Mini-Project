from threading import Thread
from DCPE_2A_02_GroupE.hal import hal_lcd as LCD
from time import sleep
from DCPE_2A_02_GroupE.hal import hal_keypad as keypad
import config
import time
from src import valid_status_fine_management

user_input =""
selected = 0
timeout_duration = 60
last_activity_time = time.time()
lcd_backlight_on=True
lcd = None
#barcode_scanned = 0
success = None

def keypad_check(key):
    global user_input, timeout_duration, last_activity_time, lcd_backlight_on, lcd

    if key is not None:

        last_activity_time=time.time()
        if lcd_backlight_on == 0 and lcd is not None:
            lcd.backlight(1)
            lcd_backlight_on==1
            user_input += str(key)
    
    if (len(user_input)==1):
        if key ==1: #
            config.return_books=1
        elif key ==2:
            config.collect_books=1
        elif key==3:
            config.extend_return_period=1
        elif key <1 or key>3:
            config.outside_range=1
        sleep(0.3)
    if config.extend_return_period == 1 and config.extension_step==1:
        if len(user_input)==1:
            selected = int(user_input)
            if 0<=selected<=9:
                if selected ==0:
                    config.chosen_book_key=10
                else:
                    config.chosen_book_key=key
                config.extension_step=2
                user_input=""
            else:
                user_input =""# allows the user to type their book index again if they pressed a non-numeric value on the keypad
                    



def main():
    global user_input
    lcd= LCD.lcd()
    lcd.lcd_clear()
    keypad.init(keypad_check)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    last_state =None
    execution_result = ""
    while True: # okay so after a button is pressed, it should prompt the user to scan their id and then after that the program should check for fines. If there are any, the program should prompt the user to pay for them
        if time.time()-last_activity_time>=timeout_duration: #REQ-04
            if lcd_backlight_on:
                lcd.backlight(0)
                lcd_backlight_on=False
                sleep(0.5)
                continue 
        if config.return_books==1: #REQ-03
            if last_state != "return":
                lcd.lcd_clear()      
                last_state = "return" 
            lcd.lcd_display_string("Book return selected",1)
            lcd.lcd_display_string("Processing...",2)
            #barcode_scanned = [insert function which scans barcode]
            #success=valid_status_fine_management.book_return(config.user_id, barcode_scanned)
            #if success ==0:
                #if config.user_na ==1:
                    #lcd.lcd_clear()
                    #lcd.lcd_display_string("User not found",1)
                    #sleep(3)
                   
                #if config.book_not_checked_out_by_user==1:
                    #lcd.lcd_clear()
                    #lcd.lcd_display_string("Book was not",1)
                    #lcd.lcd_display_string("checked out by user",2)
                    #sleep(3)
            #else:
                #lcd.lcd_clear()
                #lcd.lcd_display_string("Book successfully",1)
                #lcd.lcd_display_string("Returned!",2)
                #sleep(3)
            success = None
            config.return_books=0
            last_state ="idle" 


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
            if config.extension_step==0:
                if last_state != "extend_init":
                    lcd.lcd_clear()
                    last_state = "extend_init"
                lcd.lcd_display_string("Book extension requested",1)
                lcd.lcd_display_string("Processing...",2)
                sleep(2.0)
                lcd.lcd_clear()
                config.extension_step=1
            elif config.extension_step==1:
                if last_state != "extend_prompt":
                    last_state = "extend_prompt"
                lcd.lcd_display_string("Select Book No:",1)
                lcd.lcd_display_string("0-9, 0 for 10th book",2)
            elif config.extension_step==2:
                lcd.lcd_clear()
                lcd.lcd_display_string("Processing...",1)
                sleep(1.5)
                target_index = config.chosen_book_key-1
                execution_result = valid_status_fine_management.book_loan_extension(target_index)
                if execution_result =="Success":
                    updated_book = config.library_database[config.user_id]["books_borrowed"][target_index]
                    raw_timestamp = updated_book["expiry_timestamp"]
                    formatted_date = time.strftime("%d/%m/%Y",time.localtime(raw_timestamp))
                    lcd.lcd_display_string("Extension granted",1)
                    lcd.lcd_display_string("New Deadline:{formatted_date}",2)
                elif execution_result == "Already Done":
                    lcd.lcd_display_string=("Limit reached",1)
                    lcd.lcd_display_string=("Max of 1 extension",2)
                else:
                    lcd.lcd_display_string("Invalid choice",1)
                    lcd.lcd_display_string("No book found",2)
                sleep(3.5)
            config.extend_return_period = 0
            config.extension_step = 0
            config.chosen_book_key =0 
            last_state="idle"
            lcd.lcd_clear()


        elif config.outside_range==1:
            if last_state!="ofr":
                lcd.lcd_clear()
                last_state="ofr"
            lcd.lcd_display_string("Number inputted was out of range",1)
            lcd.lcd_display_string("Please input a number a between 1-3",2)
            config.outside_range =0
            user_input=""
        else:
            if last_state != 'idle': #REQ-01
                lcd.lcd_clear()
                last_state ="idle"

            lcd.lcd_display_string("Library book system",1)
            lcd.lcd_display_string("1-ret, 2-col, 3-ext: "+user_input,2)

        sleep(0.3)
        # should be scaled in the future to display if an error has happened due to borrowing too many books, not being a valid 
        #user or if the user has already extended his return period etc. after the database has been completed
if __name__=='__main__':
    main()
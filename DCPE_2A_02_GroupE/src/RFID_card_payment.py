from DCPE_2A_02_GroupE.hal import hal_rfid_reader 
import time 
import config
import threading
from hal import hal_lcd as LCD

scanned_id = None # This is the card scanned by the RFID card reader
card_scanned_event = threading.Event()
def RFID_CARD_DETECTION():
    global scanned_id
    while card_scanned_event.is_set()==0: # This checks whether the card has been scanned yet
        card_id = hal_rfid_reader.read_card()
        if card_id is not None:
            scanned_id = card_id
            card_scanned_event.set() # This confirms that card scanning has complete 
            break 
        time.sleep(0.1)
def RFID_CARD_PAYMENT(fine_total):
    lcd= LCD.lcd()
    global scanned_id
    start_time = time.time()
    timeout_duration = 30
    lcd.lcd_clear()
    lcd.lcd_display_string("Please tap your card to pay ${fine_total:.2f}",1)
    while not card_scanned_event.is_set():
        elapsed_time = time.time()-start_time
        remaining_time = int(timeout_duration - elapsed_time)

        if elapsed_time>= timeout_duration:
            card_scanned_event.set()
            lcd.lcd_clear()
            lcd.lcd_display_string("30 seconds exceeded",1)
            lcd.lcd_display_string("Transaction cancelled",2)
            config.timeout_payment=1
            return False
        
        if remaining_time %5 ==0:
            lcd.lcd_clear()
            lcd.lcd_display_string("Remaining Time:",1)
            lcd.lcd_display_string("{remaining_time}s",2)
        time.sleep(0.2)
    lcd.lcd_clear()
    lcd.lcd_display_string("Card Detected!",1)
    try:
        card_key = int(scanned_id)
    except(ValueError,TypeError):
        card_key = scanned_id
    if card_key not in config.RFID_CARD_DATABASE:
        lcd.lcd_display_string("Card ID:{card_key}",1)
        lcd.lcd_display_string("is not registered",2)
        return False
    current_balance = config.RFID_CARD_DATABASE[card_key]
    if current_balance < fine_total:
        lcd.lcd_display_string("Transaction Declined",1)
        lcd.lcd_display_string("Insufficient funds",2)
        return False
    config.RFID_CARD_DATABASE[card_key] -= fine_total
    new_balance = config.RFID_CARD_DATABASE[card_key]
    lcd.lcd_display_string("Deducted {fine_total:.2f}",1)
    lcd.lcd_display_string("from card: {card_key}",2)
    time.sleep(3)
    lcd.lcd_clear()
    lcd.lcd_display_string("New balance: ",1)
    lcd.lcd_display_string("{new_balance:2f},2")
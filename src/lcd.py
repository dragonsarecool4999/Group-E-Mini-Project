#to be scaled when the project expands
from hal import hal_lcd as lcd
import time
import keypad 

stage = keypad.process_detection()

display = lcd()
text_printed = False
stage2= 2 # This is a temporary variable and should be replaced with a function that returns a value indicating that the selected operation is completed
while(stage==0):
    stage = keypad.process_detection()
    time.sleep(0.01)
if(stage==1):# return books
    display.backlight(1)
    display.lcd_display_string("Returning books ",line=1,pos=0)
    display.lcd_display_string("function selected... ",line=2,pos=0)

    while(stage2==0):
        if text_printed == False:
            display.lcd_clear()
            display.lcd_display_string("Returning books", line=1,pos=0)
            display.lcd_display_string("function processing...",line=2,pos=0)
            text_printed = True
        #an extra line here is added here to check on the stage of the operation to prevent an infinite loop
    if(stage2==1): #This function will be changed to display the reason for terminating(eg. the user has borrowed too many books)
        display.lcd_clear()
        display.lcd_display_string("Error with process",line=1,pos=0)
        display.lcd_display_string("terminating return function",line=2,pos=1) 
        
    elif(stage2==2):
        display.lcd.clear()
        display.lcd_display_string("Books has been",line=1,pos=0)
        display.lcd_display_string("successfully returned",line=2,pos=0)
    else:
        display.lcd_display_string("An error occured",line=1,pos=0)
        display.lcd_display_string("terminating process...",line=2,pos=0)
if (stage==2): # books collection
    display.backlight(1)
    display.lcd_display_string("Books collection",line=1,pos=0)
    display.lcd_display_string("function selected... ",line=2,pos=0)

    while(stage2==0):
        if text_printed == False:
            display.lcd_clear()
            display.lcd_display_string("Books collection", line=1,pos=0)
            display.lcd_display_string("function processing...",line=2,pos=0)
            text_printed = True
    if(stage2==1): #This function will be changed to display the reason for terminating(eg. the user has borrowed too many books)
        display.lcd_clear()
        display.lcd_display_string("Error with process",line=1,pos=0)
        display.lcd_display_string("terminating function",line=2,pos=1) 
    elif(stage2==2):
        display.lcd.clear()
        display.lcd_display_string("Operation successful",line=1,pos=0)
        display.lcd_display_string("collect yr books",line=2,pos=0)
    else:
        display.lcd_display_string("An error occured",line=1,pos=0)
        display.lcd_display_string("terminating process...",line=2,pos=0)
if (stage==3): #book extension
    display.backlight(1)
    display.lcd_display_string("Returning books ",line=1,pos=0)
    display.lcd_display_string("function selected... ",line=2,pos=0)

    while(stage2==0):
        if text_printed == False:
            display.lcd_clear()
            display.lcd_display_string("Book extension", line=1,pos=0)
            display.lcd_display_string("function processing...",line=2,pos=0)
            text_printed = True
    if(stage2==1): #This function will be changed to display the reason for terminating(eg. the user has borrowed too many books)
        display.lcd_clear()
        display.lcd_display_string("Error with process",line=1,pos=0)
        display.lcd_display_string("terminating return function",line=2,pos=1) 
    elif(stage2==2):
        display.lcd.clear()
        display.lcd_display_string("Book deadline",line=1,pos=0)
        display.lcd_display_string("has been extended",line=2,pos=0)
    else:
        display.lcd_display_string("An error occured",line=1,pos=0)
        display.lcd_display_string("terminating process...",line=2,pos=0)



from hal import hal_keypad as keypad
MATRIX=[ [1,2,3],
         [4,5,6],
         [7,8,9],
         ['*',0,'#']] 
return_books = MATRIX[0][0] #This is for the return of books when 1 is pressed
collect_books = MATRIX[0][1]#This is for the collection of books when 2 is pressed
extend_return_period = MATRIX[0][2] #This is to extend the period when books is returned when 3 is pressed
result = 0
keypad.init()
key_press = keypad.get_key()
def process_detection():
    if key_press == return_books:
        result = 1
        return result
    elif key_press == collect_books:
        result = 2
        return result
    elif key_press == extend_return_period:
        result = 3
        return result
    else:
        return 0

process_detection()
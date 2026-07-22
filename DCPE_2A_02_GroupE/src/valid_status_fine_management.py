from src import config
import time 

def book_loan_extension(book_index):
    if config.user_id not in config.library_database:
        config.user_na = 1
        return "User not found"
    current_user = config.user_id
    user_record = config.library_database[config.user_id]
    books_list = user_record["books_borrowed"]
    if book_index>=len(books_list) or book_index<0:
        return "Invalid choice"
    selected_book= books_list[book_index]
    if selected_book["extension_allowed"] is True:
        selected_book["expiry_timestamp"]+=(14*config.SECONDS_IN_A_DAY)
        selected_book["extension_allowed"] = False
        return "Success"
    else:
        return "Already Done"
def calculate_fine(expiry_timestamp): # This should be ran after the user has scanned their id
    current_time = time.time()
    if current_time> expiry_timestamp:
        seconds_overdue = current_time - expiry_timestamp
        days_overdue = seconds_overdue / config.SECONDS_IN_A_DAY
        if seconds_overdue % config.SECONDS_IN_A_DAY != 0:
            days_overdue += 1
        FINE_RATE_PER_DAY = 0.15
        total_fine = days_overdue * FINE_RATE_PER_DAY
        return days_overdue, total_fine #RFID payment should be made after this function has ran, with the LCD prompting the user to pay
    return 0, 0.0

def book_limit(): #This function should be run when users select what books they would like to borrow online
    books_borrowed = len(config.library_database[config.user_id]["books_borrowed"])
    if books_borrowed>10:
        config.books_limit_exceeded = 1
        return
def book_return(student_id, book_id): # Book return, implemented when barcode scan is finished
    if config.user_id not in config.library_database:
        config.user_na = 1
        return False
    student_record = config.library_database[student_id]
    for book in student_record["books_borrowed"]:
        if book["Book_id"]==book_id:
            student_record["books_borrowed"].remove(book) #This removes all the values associated like expiry_timestamp associated with the id
            return True
    config.book_not_checked_out_by_user=1
    return False
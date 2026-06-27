from hal import config
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

    


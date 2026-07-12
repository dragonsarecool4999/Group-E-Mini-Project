import time
return_books = 0

collect_books = 0
extend_return_period =0 
outside_range=0
SECONDS_IN_A_DAY=86400
user_id =0 #updates based on barcode scanned on the user's nric or SP card
user_na = 0
extension_step=0
chosen_book_key= None
book_limit_exceeded = 0
timeout_payment = 0
library_database ={
    "P2519863":
    {
        "Name":"Jovan",
        "books_borrowed":[
        {
            "Book_id":"ABC101",
            "expiry_timestamp":time.time()+(14*SECONDS_IN_A_DAY),
            "extension_allowed":True
        },
        {
            "Book_id":"DCPE55",
            "expiry_timestamp":time.time()+(14*SECONDS_IN_A_DAY),
            "extension_allowed":False
        }
        ],
    },
    "P4321727":
    {
        "Name":"Navoj",
        "books_borrowed":[
        {
            "Book_id":"FAGO21",
            "expiry_timestamp":time.time()+(14*SECONDS_IN_A_DAY),
            "extension_allowed":False
        },
        {
            "Book_id":"HH2710",
            "expiry_timestamp":time.time()+(14*SECONDS_IN_A_DAY),
            "extension_allowed":True
        }

        ],
    },
                
}
RFID_CARD_DATABASE= {
    711535355173:50.00
}
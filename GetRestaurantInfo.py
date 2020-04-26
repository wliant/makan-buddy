from pydialogflow_fulfillment import DialogflowResponse
from pydialogflow_fulfillment import SimpleResponse, Confirmation, OutputContexts, Suggestions
import json
import intelligence
import MakeReservation

CONTEXT_ASK_PROGRAMME = "GetRestaurantInfo-followup"

RESTAURANT_NAME = ""

reservation_date = "16/05/2020"
reservation_time = "1730"
party_size = "2"
restaurant_name ='Yujin Izakaya'
first_name = 'John'
last_name='Tan'
email_address = 'test@gmail.com'
phone_number = '98769876'

def process(req):
    i = intelligence.Intel()
    for j in range(0, 10):
        id,path = i.get_query()
        i.update_response(id, 3, 0, 0)
    RESTAURANT_NAME = i.get_result();
    
    print("here is the restaurant name" + RESTAURANT_NAME)
    res = DialogflowResponse("We are recommanding " + RESTAURANT_NAME + ", do you want to make a reservation?")
     
    return res.get_final_response()    
    #if isConfirmed == "yes":
    #    print("here proceed to make reservation")
    #    MakeReservation.make_reservation("16/05/2020","1730","2",'Yujin Izakaya','John','Tan','test@gmail.com','98769876')
    # fdreturn DialogflowResponse("We recommand the restaurant "+restaurant_name +", do you want to book a table?").get_final_response()
    
def makeReservation(req):
    
    print("make reservation for " + RESTAURANT_NAME)
    
    MakeReservation.make_reservation(reservation_date,reservation_time,party_size,RESTAURANT_NAME,first_name,last_name,email_address,phone_number)
    res = DialogflowResponse("finish making reservation for  " + RESTAURANT_NAME )
     
    return res.get_final_response()  
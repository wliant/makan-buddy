from pydialogflow_fulfillment import DialogflowResponse
from pydialogflow_fulfillment import SimpleResponse, Confirmation, OutputContexts, Suggestions
import json
import intelligence
import MakeReservation

CONTEXT_ASK_PROGRAMME = "getrestaurantinfo-followup"

reservation_date = "16/07/2020"
reservation_time = "1730"
party_size = "2"
first_name = 'John'
last_name='Tan'
email_address = 'test@gmail.com'
phone_number = '98769876'

def process(req):
    i = intelligence.Intel()
    for j in range(0, 10):
        id,path = i.get_query()
        i.update_response(id, 3, 0, 0)
    restaurant_name = i.get_result();
    
    res = DialogflowResponse("We are recommanding " + restaurant_name + ", do you want to make a reservation?")
    res.add(SimpleResponse("We are recommanding " + restaurant_name + ", do you want to make a reservation?","We are recommanding " + restaurant_name + ", do you want to make a reservation?"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME,5,{"restaurantName": restaurant_name}))
    return res.get_final_response()    
    #if isConfirmed == "yes":
    #    print("here proceed to make reservation")
    #    MakeReservation.make_reservation("16/05/2020","1730","2",'Yujin Izakaya','John','Tan','test@gmail.com','98769876')
    # fdreturn DialogflowResponse("We recommand the restaurant "+restaurant_name +", do you want to book a table?").get_final_response()
    
def makeReservation(req):
    outputcontext = req.get_single_ouputcontext(CONTEXT_ASK_PROGRAMME)
    restaurant_name = outputcontext["parameters"]["restaurantName"]
    print(restaurant_name)
    #MakeReservation.make_reservation(reservation_date,reservation_time,party_size,restaurant_name,first_name,last_name,email_address,phone_number)
    res = DialogflowResponse("finish making reservation for  " + restaurant_name )
     
    return res.get_final_response()  


from pydialogflow_fulfillment import DialogflowResponse
from pydialogflow_fulfillment import SimpleResponse, Confirmation, OutputContexts, Suggestions
import json
import intelligence
import MakeReservation

CONTEXT_ASK_PROGRAMME = "GetRestaurantInfo-followup"

def askReservation(req,name):
    print("here to ask for reservation")
    res = DialogflowResponse("We are recommanding " + name + ", do you want to make a reservation?")
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME,5,req.get_paramters()))
    return res.get_final_response()


def process(req):
    i = intelligence.Intel()
    for j in range(0, 10):
        id,path = i.get_query()
        i.update_response(id, 3, 0, 0)
    restaurant_name = i.get_result();
    
   # askReservation(req)
    
    #if isConfirmed == "yes":
    #    print("here proceed to make reservation")
    #    MakeReservation.make_reservation("16/05/2020","1730","2",'Yujin Izakaya','John','Tan','test@gmail.com','98769876')
    return DialogflowResponse("We recommand the restaurant "+restaurant_name +", do you want to book a table?").get_final_response()
    

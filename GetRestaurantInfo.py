from pydialogflow_fulfillment import DialogflowResponse
from pydialogflow_fulfillment import SimpleResponse, Confirmation, OutputContexts, Suggestions
import json
import intelligence
import MakeReservation



CONTEXT_ASK_PROGRAMME = "getrestaurantinfo-followup"

CONTEXT_ASK_PROGRAMME_YES = "getrestaurantinfo-yes-followup"

reservation_date = "16/07/2020"
reservation_time = "1730"
party_size = "2"
first_name = 'John'
last_name='Tan'
email_address = 'test@gmail.com'
phone_number = '98769876'

def has_params(theKey, params):
    return theKey in params and params[theKey] != ""

def askDate(req):
    res = DialogflowResponse("What is the date you are looking at?(e.g Date:dd/mm/yyyy)")
    print(req.get_parameters())
    res.add(SimpleResponse("What is the date you are looking at?(e.g Date:dd/mm/yyyy)","What is the date you are looking at?(e.g Date:dd/mm/yyyy)"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def askTime(req):
    res = DialogflowResponse("How about the time?(e.g Time:1730)")
    res.add(SimpleResponse("How about the time?(e.g Time:1730)","How about the time?(e.g Time:1730)"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def askPartySize(req):
    res = DialogflowResponse("How many people?")
    res.add(SimpleResponse("How many people?","How many people?"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def askfirstName(req):
    res = DialogflowResponse("May I know your first name?(e.g First Name:Sam)")
    res.add(SimpleResponse("May I know your first name?(e.g First Name:Sam)","May I know your first name?e.g First Name:Sam"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def askLastName(req):
    res = DialogflowResponse("May I know your last name?(e.g Last Name:Lee)")
    res.add(SimpleResponse("May I know your last name?(e.g Last Name:Lee)","May I know your last name?(e.g Last Name:Lee)"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def askEmail(req):
    res = DialogflowResponse("What is your email address?(e.g Email:test@gmail.com)")
    res.add(SimpleResponse("What is your email address?(e.g Email:test@gmail.com)","What is your email address?(e.g Email:test@gmail.com)"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def askPhone(req):
    res = DialogflowResponse("May I know your mobile number?(e.g Phone:83927594)")
    res.add(SimpleResponse("May I know your mobile number?(e.g Phone:83927594)","May I know your mobile number?(e.g Phone:83927594)"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def process(req):
    i = intelligence.Intel()
    for j in range(0, 10):
        id,path = i.get_query()
        i.update_response(id, 3, 0, 0)
    restaurant_name = i.get_result()[0];
    image_url = i.get_result()[1][0]
    res = DialogflowResponse("We are recommanding " + restaurant_name + ", do you want to make a reservation?")
    res.add(SimpleResponse("We are recommanding " + restaurant_name + ", do you want to make a reservation?","We are recommanding " + restaurant_name + ", do you want to make a reservation?"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME,5,{"restaurantName": restaurant_name}))
 
    res.fulfillment_messages.append({
        "card": {
          "title": "We are recommanding " + restaurant_name + ", do you want to make a reservation?", 
          "imageUri": "https://4c547015.ngrok.io/image?path="+image_url, 
          "buttons": [ 
            {
              "text": "yes",
              "postback": "yes" 

            }
          ]
        },
        "platform": "SLACK"
      })
 
    print(res.get_final_response()) 
    return res.get_final_response()     
    #if isConfirmed == "yes":
    #    print("here proceed to make reservation")
    #    MakeReservation.make_reservation("16/05/2020","1730","2",'Yujin Izakaya','John','Tan','test@gmail.com','98769876')
    # fdreturn DialogflowResponse("We recommand the restaurant "+restaurant_name +", do you want to book a table?").get_final_response()
    
def makeReservation(req): 
    print(req.get_ouputcontext_list())
    params = req.get_parameters()
    try:  
        for con in req.get_ouputcontext_list():
            o_params = con["parameters"]
            for x in o_params: 
                params[x] = o_params[x] 
    except: 
        None

    print("print params during init "+ str(params)) 
     
    if not has_params("date", params):
        print("here is not have date")
        return askDate(req)
    if not has_params("time", params):
        return askTime(req)    
    if not has_params("partySize", params):
        return askPartySize(req)
    if not has_params("firstName", params):
        return askfirstName(req)    
    if not has_params("lastName", params):
        return askLastName(req)
    if not has_params("email", params):
        return askEmail(req) 
    if not has_params("phoneNumber", params):
        return askPhone(req) 


    print(params)
    restaurant_name = "" if "restaurantName" not in params else params["restaurantName"]     
    reservation_date = "" if "date" not in params else params["date.original"] 
    reservation_time = "" if "time" not in params else params["time.original"]
    party_size = "" if "partySize" not in params else params["partySize.original"] 
    first_name = "" if "firstName" not in params else params["firstName"]
    last_name = "" if "lastName" not in params else params["lastName"] 
    email_address = "" if "email" not in params else params["email"]
    phone_number = "" if "phone" not in params else params["phone"] 
    
    
    MakeReservation.make_reservation(reservation_date,reservation_time,party_size,restaurant_name,first_name,last_name,email_address,phone_number)
    res = DialogflowResponse("finish making reservation for  " + restaurant_name )
       
    return res.get_final_response()


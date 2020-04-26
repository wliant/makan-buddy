import requests
from flask import Flask, request, make_response, jsonify
from pydialogflow_fulfillment import DialogflowRequest
from pydialogflow_fulfillment import DialogflowResponse
from pydialogflow_fulfillment import SimpleResponse, Confirmation, OutputContexts, Suggestions
import GetRestaurantInfo


app = Flask(__name__)

def getjson(url):
    resp = requests.get(url)
    print(url)
    return resp.json() 

# *****************************
# WEBHOOK MAIN ENDPOINT : START
# *****************************
PROJECT_ID = 'issipa-lsekbm'

@app.route('/', methods=['POST'])
def webhook():
    req = DialogflowRequest(request.data)
    intent_name = req.get_intent_displayName()
    print("here to print intent_name "+ intent_name)

    if intent_name == "GetRestaurantInfo" or intent_name == "GetRestaurantInfo-yes":
        return make_response(GetRestaurantInfo.process(req))
   
    # TODO: STEP 2
    # Write your code here..
    # write some if/else to check for the correct intent name.
    # Write code to call the getWeatherIntentHandler function with appropriate input

    if intent_name == "Weather Intent":
        respose_text = "weather"

    else:
        respose_text = "No intent matched from fullfilment code."
    # Branching ends here

    # Finally sending this response to Dialogflow.
    return make_response(jsonify({"fulfillmentText": respose_text}))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

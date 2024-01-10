import requests
from flask import Flask, request
import json

app = Flask(__name__)



@app.route('/receive_sms', methods=['POST'])
def receive_sms():
    sms_data = request.json
    print("Received SMS:", json.dumps(sms_data, indent=4))
    # Further processing here
    return 'SMS Received'

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    user_id = request.args.get('id')
    # Process the unsubscription here using the user_id
    # E.g., mark the user's number as 'remove from list'
    message = 'You\'ve been removed from the list. UserID: ' + user_id
    send_sms_via_server(number='7708626316', message=message, isRaw=True)
    return 'You have been removed from the list.'

def send_sms_via_server(number, message, isRaw = False):
    url = 'http://192.168.39.150:5000/send_sms'
    data = {'number': number, 'message': message, 'isRaw': isRaw}
    response = requests.post(url, data=data)
    print(response.text)


# Example usage
# send_sms_via_server('7708426732', 'Would you like to talk? Choose a time: https://calendly.com/sheldonbakergroup/benefitsconversation!')
def main():

    send_sms_via_server('7708626316', 'Would you like to talk? http://192.168.39.134:5000/unsubscribe?id=5klajskdlf29', isRaw=True)

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=5000)
import requests
from flask import Flask, request
import json
import PySimpleGUI as ui
from pathlib import Path

app = Flask(__name__)


def choose_file(text: str = "File: ") -> str:
    select_file = [
        [ui.Text(text), ui.InputText(key='-file1-'), ui.FileBrowse()],
        [ui.Button("Start")],
    ]
    window = ui.Window('SteveConnections', select_file)
    file_exists = False
    while not file_exists:
        event, values = window.read()
        if event == ui.WINDOW_CLOSED:
            break
        elif event == "Start":
            filename = values['-file1-']
            while True:
                if not Path(filename).is_file():
                    if filename == '':
                        ui.popup_ok('Please select a file!')
                    else:
                        ui.popup_ok("That file doesn't exist!")
                    filename = ui.popup_get_file("", no_window=True)
                    if filename == '':
                        break
                    window['-file1-'].update(filename)
                else:
                    print('File is ready !')
                    file_exists = True
                    break
    window.close()
    return str(values['-file1-'])


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
    send_sms_via_server(number='+522227084870', message=message, isRaw=True)
    return 'You have been removed from the list.'

def send_sms_via_server(number, message, isRaw = False):
    url = 'http://192.168.39.150:5000/send_sms'
    if isinstance(number, str):
        number_final = number
        numbers_final = None
    if isinstance(number, list):
        number_final = None
        numbers_final = number 
    data = {'number': number_final, 'numbers': numbers_final, 'message': message, 'isRaw': isRaw}
    response = requests.post(url, data=data)
    print(response.text)


# Example usage
# send_sms_via_server('7708426732', 'Would you like to talk? Choose a time: https://calendly.com/sheldonbakergroup/benefitsconversation!')
def main():
    import openpyxl
    file = choose_file("Text Messages")
    print(file)
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        phone_number, test_message = row
        personalized_message = f"{test_message}"
        print(f"Phone: {phone_number} -- Message: {test_message}")
        send_sms_via_server(str(round(7624001194)), "To join the video meeting, click this link: https://meet.google.com/jge-iiab-sxo")
        send_sms_via_server(str(round(7708626316)), personalized_message)


    # send_sms_via_server('7708626316', 'Would you like to talk? http://192.168.39.134:5000/unsubscribe?id=5klajskdlf29', isRaw=True)
    # send_sms_via_server('+522227084870', 'Would you like to talk? http://192.168.39.134:5000/unsubscribe?id=5klajskdlf29', isRaw=True)

if __name__ == '__main__':
    main()
    # app.run(host='0.0.0.0', port=5000)
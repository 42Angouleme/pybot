import PySimpleGUI as sg


def run():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('Change the webapp password'), sg.InputText('hello')],
              [sg.Text('Enter the openai token'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Robot Python Options', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        print('You entered ', values[0])
        print('You entered ', values[1])
        f = open(".env", "w")
        f.write("WEPAPP_PASSWORD=" +
                values[0] + "\n" + "OPENAI_TOKEN=" + values[1])
        f.close()

    window.close()

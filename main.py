import PySimpleGUI as sg
from file_loader import load_file
from keyboard import is_pressed as isp
import os
import string


def themes(theme):
    sg.theme(theme)

themes('LightGrey1')


layout = [
    [sg.Input(key='-IN-', size=70, border_width=0),
     sg.Button("Browse", pad=(13, 1), size=(6, 1), border_width=0, font=('Arial', 12)),
     sg.Button("Ok", border_width=0, size=(6, 1), font=('Arial', 12))
    ],
    [sg.Multiline(size=(95, 26), key="text", border_width=0, no_scrollbar=True)],
    [sg.Column([[  # Coluna com botões na parte superior
        sg.Button("New File", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
        sg.Button("Save", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
        sg.Button("Save As", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
        sg.Button('Theme', key='-TOGGLE-', size=(7, 1), pad=(10, 1), border_width=0, font=('Arial', 12)),
        sg.Button("Exit", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12))
    ]], justification='left')]
]

window = sg.Window('Tnotes', layout, size=(680, 500), finalize=True, return_keyboard_events=True, icon=r'img\ico\favicon.ico')
toggle_state = False
current_file_path = None  

while True:
    event, values = window.read(timeout=100) 

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    elif event == "Ok" or isp('enter'):
        new_file_path = values['-IN-']  
        if new_file_path and new_file_path != current_file_path:
            current_file_path = new_file_path  
            text = load_file(current_file_path) 
            window['text'].update(text)

    elif event == "Browse" or isp('ctrl+w'):
        file_path = sg.popup_get_file('Select a file', file_types=(("Text Files", "*.txt"),), no_window=True)
        if file_path:
            window['-IN-'].update(file_path)

    elif event == "Save" or isp('ctrl+s'):
        if current_file_path:
            try:
                with open(current_file_path, 'w') as file:
                    file.write(values['text']) 
                sg.popup("File saved successfully!")
            except Exception as e:
                sg.popup_error(f"Error to save the file: {e}")
        else:
            sg.popup("No files to save.")

    elif event == "Save As" or isp('ctrl+x'):
        save_path = sg.popup_get_file("File", save_as=True, file_types=(("Text Files", "*.txt"),), no_window=True)
        if save_path:
            try:
                with open(save_path, 'w') as file:
                    file.write(values['text'])
                sg.popup("File saved successfully!")
                current_file_path = save_path
            except Exception as e:
                sg.popup_error(f"Error to save the file: {e}")

    elif event == "-TOGGLE-":
        toggle_state = not toggle_state
        window.close()
        if toggle_state:
            themes('DarkGrey14')
        else:
            themes('LightGrey1')

        layout = [
            [sg.Input(key='-IN-', size=70, border_width=0),
            sg.Button("Browse", pad=(13, 1), size=(6, 1), border_width=0, font=('Arial', 12)),
            sg.Button("Ok", border_width=0, size=(6, 1), font=('Arial', 12))
            ],
            [sg.Multiline(size=(95, 26), key="text", border_width=0, no_scrollbar=True)],
            [sg.Column([[  # Coluna com botões na parte superior
                sg.Button("New File", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
                sg.Button("Save", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
                sg.Button("Save As", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
                sg.Button('Theme', key='-TOGGLE-', size=(7, 1), pad=(10, 1), border_width=0, font=('Arial', 12)),
                sg.Button("Exit", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
            ]], justification='left')]
        ]
        window = sg.Window('Tnotes', layout, size=(680, 500), finalize=True, return_keyboard_events=True)

    elif event == "New File":
        newfile_window = sg.popup_get_text("Text Name", title="New File")
        archivenm = newfile_window
        if newfile_window is None or newfile_window == '':
            sg.popup("File creation cancelled or no name provided.")
            continue
        if archivenm and all(char not in string.punctuation for char in archivenm):
            current_file_path = os.path.join(os.getcwd(), f"{archivenm}.txt")
            with open(current_file_path, 'w') as file:
                file.write("")
            sg.popup("New file created successfully!")
            window['-IN-'].update(current_file_path)
        else:
            sg.popup("Invalid file name. Please use only alphanumeric characters and underscores.")

window.close()
import PySimpleGUI as sg
from file_loader import load_file
import keyboard as k

def themes(theme):
    sg.theme(theme)

themes('LightGrey1')

layout = [
    [sg.Input(key='-IN-', size=70, border_width=0),
     sg.Button("Browse", pad=(10, 1), size=(6, 1), border_width=0, font=('Arial', 12)),
     sg.Button("Ok", border_width=0, size=(6, 1), font=('Arial', 12))
    ],
    [sg.Multiline(size=(90, 20), key="text", border_width=0)],
    [
        sg.Column([
            [sg.Button("Save", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
             sg.Button("Save As", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
             sg.Button('Theme', key='-TOGGLE-', size=(7, 1), pad=(10, 1), border_width=0, font=('Arial', 12)),
             sg.Button("Exit", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12))]
        ], justification='left'),
        sg.Column([
            [sg.Text("Words: ", key='-WORDS-', pad=(50, 1)),  
             sg.Text("Chars: ", key='-CHARS-')]
        ])
    ]
]

window = sg.Window('Tnotes', layout, size=(680, 400))
toggle_state = False
current_file_path = None  

while True:
    event, values = window.read(timeout=100) 

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    elif event == "Ok":
        new_file_path = values['-IN-']  
        if new_file_path and new_file_path != current_file_path:
            current_file_path = new_file_path  
            text = load_file(current_file_path) 
            window['text'].update(text)

    elif event == "Browse":
        file_path = sg.popup_get_file('Select a file', file_types=(("Text Files", "*.txt"),), no_window=True)
        if file_path:
            window['-IN-'].update(file_path)

    elif event == "Save":
        if current_file_path:
            try:
                with open(current_file_path, 'w') as file:
                    file.write(values['text']) 
                sg.popup("File saved successfully!")
            except Exception as e:
                sg.popup_error(f"Error to save the file: {e}")
        else:
            sg.popup("No files to save")

    elif event == "Save As":
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
             sg.Button("Browse", pad=(10, 1), border_width=0, font=('Arial', 12)),
             sg.Button("Ok", border_width=0, font=('Arial', 12))],
            [sg.Multiline(size=(90, 20), key="text", border_width=0)],
            [sg.Text("Words: ", key='-WORDS-', size=(10, 1)), sg.Text("Chars: ", key='-CHARS-', size=(10, 1))],
            [sg.Column([
                [
                    sg.Button("Save", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
                    sg.Button("Save As", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
                    sg.Button('Theme', key='-TOGGLE-', pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12)),
                    sg.Button("Exit", pad=(10, 1), size=(7, 1), border_width=0, font=('Arial', 12))
                ]
            ])]
        ]
        window = sg.Window('Tnotes', layout, size=(800, 400))

    text_content = values['text']
    word_count = len(text_content.split())
    char_count = len(text_content)

    window['-WORDS-'].update(f"Words: {word_count}")
    window['-CHARS-'].update(f"Chars: {char_count}")

    # Hotkeys
    if k.is_pressed('ctrl+s'):
        if current_file_path:
            try:
                with open(current_file_path, 'w') as file:
                    file.write(values['text']) 
                sg.popup("File saved successfully!")
            except Exception as e:
                sg.popup_error(f"Error to save the file: {e}")
        else:
            sg.popup("No files to save")

    elif k.is_pressed('ctrl+x'):
        save_path = sg.popup_get_file("File", save_as=True, file_types=(("Text Files", "*.txt"),), no_window=True)
        if save_path:
            try:
                with open(save_path, 'w') as file:
                    file.write(values['text'])
                sg.popup("File saved successfully!")
                current_file_path = save_path
            except Exception as e:
                sg.popup_error(f"Error to save the file: {e}")

    elif k.is_pressed('ctrl+w'):
        file_path = sg.popup_get_file('Select a file', file_types=(("Text Files", "*.txt"),), no_window=True)
        if file_path:
            window['-IN-'].update(file_path)

    elif k.is_pressed('enter'):
        new_file_path = values['-IN-']  
        if new_file_path and new_file_path != current_file_path:
            current_file_path = new_file_path  
            text = load_file(current_file_path) 
            window['text'].update(text)

window.close()
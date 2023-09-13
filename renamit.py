import glob, os, unicodedata
import time
from PySimpleGUI import PySimpleGUI as gui

# Theme
gui.theme('Reddit')

# Layout
separators = [
    '-',
    '_'
]

text_size = (15, 1)
input_size = (70, 1)
text_size_max = (25, 1)
input_size_max = (100, 1)
radio_size_max = (100, 1)
select_size = (100, 1)
button_size = (100, 1)
progressbar_size = (100, 25)

layout = [
    [
        gui.Text('Caminho da pasta: ', size=text_size),  
        gui.Input(key='folder_path', size=input_size), 
        gui.Listbox(key='separator', default_values=separators[0], values=separators, size=select_size)
    ],
    [
        gui.Text('Nome complementar do arquivo: ', size=text_size_max),
        gui.Input(key='aux_file_name', size=input_size_max), 
    ],
    [
        gui.Radio('Index no começo do nome', 'INDEXRADIO', default=True),
        gui.Radio('Index no final do nome', 'INDEXRADIO', key="index_radio_button", default=False),
    ],
    [
        gui.Button('Confirmar', size=button_size)
    ],
    [
        gui.ProgressBar(key='ProgressBar', max_value=100, orientation='h', expand_x=True, visible=True, size=progressbar_size),
    ],
    [
        gui.Text(key='OUT', enable_events=True, expand_x=True, size=text_size)
    ]
]

# Window
window = gui.Window(title='Renamit', layout=layout, size=(800, 600))

# Events
while True:
    events, values = window.read()
    
    if events == gui.WINDOW_CLOSED:
        break
    if events == 'Confirmar':
        window['Confirmar'].update(disabled=True)
           
        def response_message(path='', message='') -> None:
            if not path:
                gui.popup_ok(f'{message}')
            else:
                gui.popup_ok(f'{message} - {path}')
                
        def validate_sep(sep=str) -> bool:
            if sep == "-" or sep == "_":
                return True
            
            return False 

        def normalize(path=str, sep=str) -> str:
            text = path.split('\\')[-1]
            nfkd = unicodedata.normalize('NFKD', text)
            no_esp_char_lower = u"".join([c for c in nfkd if not unicodedata.combining(c)]).lower()
            
            return no_esp_char_lower.replace(' ', sep)

        def rename(path=str, formatted_folder_name=str, aux_file_name=str, sep=str):
            index = 0
            messages = 'Arquivos renomeados: \n\n'
            len_files = len(glob.glob(path + '\\*'))
            
            index_position = values['index_radio_button']
            
            for file in glob.glob(path + '\\*'):
                _, extension = os.path.splitext(file)
                        
                if index_position:        
                    new_file = f'{path}\\{formatted_folder_name}{sep}{aux_file_name}{sep}0{index}{extension}'
                else:
                    new_file = f'{path}\\0{index}{sep}{formatted_folder_name}{sep}{aux_file_name}{extension}'
                    
                if (os.path.isfile(file) and file == new_file) : break
                        
                os.rename(file, new_file)
                    
                old_name = file.split('\\')[-1]
                new_name = new_file.split('\\')[-1]
                
                message = f'{old_name}\tpara\t{new_name}'
                messages += message + '\n'
                
                window['OUT'].update(f'Renomeando {old_name}...') 
                window['ProgressBar'].update(current_count=(index + 1) * (100 / len_files))
                
                time.sleep(0.5)
                    
                index += 1
                
            window['Confirmar'].update(disabled=False)   
            gui.popup_ok(f'{messages}', title='Mensagem')
                
        path = values['folder_path']
        aux_file_name = values['aux_file_name']
        sep = values['separator'][0]
        
        if (path and path != ''): 
            valid_sep = validate_sep(sep)
            formatted_folder_name = normalize(path, sep)
            formatted_aux_file_name = normalize(aux_file_name, sep)
            
            if valid_sep:
                rename(path, formatted_folder_name, formatted_aux_file_name, sep)
            else:
                response_message(message='O separador deve ser apenas - ou _')  
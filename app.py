import dash
import json
from dash import dcc, html
from dash.dependencies import Input, Output, State

from slownik import Diki
diki = Diki()

translation = {
    'polish_words': [],
    'english_word': None,
    'popularity': None,
    'pronunciation': None,
    'examples': {},
    'synonyms':{},
    'other_words': []
}

app = dash.Dash(__name__, assets_folder='assets')

app.layout = html.Div(style={'color': 'white', 'padding': '20px'}, children=[
    html.Header([
        dcc.Input(
            id='input-box',
            type='text',
            value='',
            placeholder='Wpisz coś...',
            style={
                'font-size': '20px',
                'width': '300px',
                'height': '30px',
                'backgroundColor': '#444444',
                'color': 'white',
                'border': '1px solid #666666',
                'border-radius': '5px',
                'padding': '5px'
            }
        ),
        html.Button(
            'Dodaj', 
            id='button-1', 
            n_clicks=0,
            style={
                'font-size': '20px',
                'vertical-align': 'top',
                'margin-left': '10px',
                'backgroundColor': '#666666',
                'color': 'white',
                'border': 'none',
                'border-radius': '5px',
                'padding': '5px'
            }
        ),
        html.Div(
            id='popularity',
            style={
                'font-size': '30px',
                'font-weight': 'bold',
                'color': '#66B2FF',
                'margin-left': '10px',
                'display': 'inline-block',
                'vertical-align': 'top'
            }
        )
    ],
    style={
        'display': 'flex',
        'flex-direction': 'row',
        'align-items': 'center'
    }),
    html.Div(
        dcc.Checklist(
            id='checkboxes',
            value=[],
            labelStyle={
                'display': 'block', 
                'font-size': '20px',
                'color': 'white',
            }
        ),
        style={
            'margin-top': '10px',
            'padding': '10px',
            'min-height': '50px',
            'background-color': '#444444',
            'border': '1px solid #666666',
            'color': 'white',
            'border-radius': '5px'
        }
    ),
    html.P(
        id='output-1',
        style={
            'margin-top': '10px',  # Przerwa nad output-1
            'margin-bottom': '5px',  # Przerwa między output-1 a output-2
            'font-size': '20px',
            'padding': '10px',
            'min-height': '50px',
            'background-color': '#444444',
            'border': '1px solid #666666',
            'color': 'white',
            'border-radius': '5px'
        }
    ),
    html.P(
        id='output-2',
        style={
            'margin-top': '10px',  # Większa przerwa między output-2 a output-1
            'font-size': '20px',
            'padding': '10px',
            'min-height': '50px',
            'background-color': '#444444',
            'border': '1px solid #666666',
            'color': 'white',
            'border-radius': '5px'
        }
    ),
    html.P(
        id='output-3',
        style={
            'font-size': '20px',
            'color': '#66B2FF',
            'padding': '10px',
            'margin-top': '10px'
        }
    )
])

@app.callback(
    [Output('checkboxes', 'options'),
    Output('checkboxes', 'value'),
    Output('popularity', 'children'),
    Output('output-3', 'children')],
    Input('input-box', 'value')
)
def update_output(input_value):

    global translation
    translation = diki.translation(input_value)

    polish_words = [i[0] for i in translation['polish_words']]
    parts_of_speach = [i[1] for i in translation['polish_words']]
    other_words = translation['other_words']
    popularity = translation['popularity']
    examples = translation['examples']

    checkboxy = [{
        'label': f"{word[1]} [{parts_of_speach[word[0]]}] 📝" 
        if word[1] in examples.keys() else f"{word[1]} [{parts_of_speach[word[0]]}]", 
        'value': word[0]
        } for word in enumerate(polish_words)]

    lista_3 = ' | '.join(other_words)
    
    return checkboxy, [0], popularity, lista_3 

@app.callback(
    [Output('output-1', 'children'),
     Output('output-2', 'children')],
    [Input('checkboxes', 'value')]
)
def update_checkboxes(selected_values):
    if not selected_values:
        return None, None

    global translation

    polish_words = [i[0] for i in translation['polish_words']]
    english_word = translation['english_word']
    pronunciation = translation['pronunciation']
    examples = translation['examples']

    if not english_word:
        return None, None

    selected_words = [polish_words[i] for i in selected_values if i < len(polish_words)]

    if len(selected_words) == 1:
        lista_1 = selected_words[0]
    else:
        lista_1 = ', '.join(selected_words)

    lista_2 = [english_word, html.Br(), pronunciation, html.Br(), html.Br()]

    try:
        for i in selected_values:
            if polish_words[i] in examples.keys():
                lista_2.extend([examples[polish_words[i]], html.Br()])
    except:
        pass

    def usun_koncowe_br(lista):
        while lista and isinstance(lista[-1], html.Br):
            lista.pop()
        return lista

    return usun_koncowe_br(lista_1), usun_koncowe_br(lista_2)

@app.callback(
    [Output('input-box', 'value')],
    Input('button-1', 'n_clicks'),
    [State('output-1', 'children'),
     State('output-2', 'children')]
)
def handle_button_click(n_clicks, output_1, output_2):
    if n_clicks > 0 and output_1 and output_2:
        html_content = []

        for item in output_2:
            if isinstance(item, str):
                html_content.append(item)
            elif isinstance(item, dict) and item.get('type') == 'Br':
                html_content.append('<br>')
        
        html_string = ''.join(html_content)

        with open('new_flashcards.txt', 'a', encoding='utf-8') as plik:
            plik.write(f'{output_1};{html_string}' + '\n')

    return ['']

if __name__ == '__main__':
    app.run_server(debug=True)

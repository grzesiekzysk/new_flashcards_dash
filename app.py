import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from datetime import datetime
import eng_to_ipa

from slownik import Diki
diki = Diki()

app = dash.Dash(
    __name__, 
    title='Generator fiszek',
    assets_folder='assets', 
    prevent_initial_callbacks=True
)

app.layout = html.Div(style={'color': 'white', 'padding': '20px'}, children=[
    dcc.Store(id='translation-store', data={}),
    dcc.Store(id='accumulated-records', data=[]),
    html.H1(
        'Generator fiszek do aplikacji Anki',
        style={
            'text-align': 'center',
            'font-size': '26px',
            'margin-top': '0px',
            'padding': '5px',
            'border-bottom': '4px double #666666',
            'box-shadow': '0 4px 2px -2px rgba(0, 0, 0, 0.3)'
        }
    ),
    html.Header([
        html.Button(
            'Dodaj', 
            id='button-1', 
            n_clicks=0,
            style={
                'font-size': '16px',
                'width': '75px',
                'vertical-align': 'left',
                # 'margin-left': '10px',
                'background-color': '#666666',
                'color': 'white',
                'border': 'none',
                'border-radius': '5px',
                'padding': '5px',
                'cursor': 'pointer',
                'display': 'block',
            }
        ),
        dcc.Input(
            id='input-box',
            type='text',
            value='',
            placeholder='Wpisz angielskie słowo...',
            style={
                'font-size': '16px',
                'text-align': 'left',
                'text-indent': '5px',
                'width': 'calc(100% - 190px)',
                # 'max-width': '250px',
                'height': '20px',
                'margin-left': '10px',
                'backgroundColor': 'rgba(163, 203, 255, 0.1)',
                'color': 'white',
                'border': '1px solid #666666',
                'border-radius': '5px',
                'padding': '5px'
            }
        ),
        html.Div(
            id='popularity',
            children='OTHER',
            style={
                'font-size': '16px',
                'text-align': 'center',
                'width': '95px',
                'font-weight': 'bold',
                'color': '#ffffff',
                'margin-left': '10px',
                'display': 'inline-block',
                'vertical-align': 'top',
                'border-radius': '5px',
                'padding': '5px',
                'background-color': 'rgba(25, 165, 111, 0.5)',
                'border': '1px solid #19a56f'
            }
        )
    ],
    style={
        'display': 'flex',
        'flex-direction': 'row',
        'align-items': 'center'
    }),
    html.Div(
        dcc.RadioItems(
            id='checkboxes',
            labelStyle={
                'display': 'block', 
                # 'font-size': '16px',
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
            'margin-top': '10px',
            'margin-bottom': '5px',
            # 'font-size': '16px',
            'padding': '10px',
            'min-height': '20px',
            'background-color': '#444444',
            'border': '1px solid #666666',
            'color': 'white',
            'border-radius': '5px'
        }
    ),
    html.P(
        id='output-2',
        style={
            'margin-top': '10px',
            # 'font-size': '16px',
            'padding': '10px',
            'min-height': '20px',
            'background-color': '#444444',
            'border': '1px solid #666666',
            'color': 'white',
            'border-radius': '5px'
        }
    ),
    html.P(
        id='output-3',
        style={
            # 'font-size': '16px',
            'color': '#66B2FF',
            'padding': '10px',
            'margin-top': '10px',
            # 'border': '1px solid #666666',
            # 'border-radius': '5px'
        }
    ),
    html.Div(
        id='output-4',
        style={
            'margin-top': '10px',
            'font-size': '16px',
            'padding': '5px',
            'width': '225px',
            'min-height': '20px',
            'background-color': 'rgba(222, 49, 99, 0.25)',
            'border': '1px solid #D70040',
            'color': 'white',
            'border-radius': '5px',
            'display': 'flex',
            'align-items': 'center'
        },
        children=[
            html.Button(
                'Pobierz',
                id='download-button',
                n_clicks=0,
                style={
                    'font-size': '16px',
                    'margin-right': '10px',
                    'backgroundColor': '#D70040',
                    'color': 'white',
                    'border': 'none',
                    'border-radius': '5px',
                    'padding': '5px',
                    'cursor': 'pointer'
                }
            ),
            html.Span(id='record-count', children='Liczba rekordów: 0')
        ]
    ),
    dcc.Download(id="download-text"),
    html.Div(id='dummy-output', style={'display': 'none'})
])

@app.callback(
    [Output('checkboxes', 'options', allow_duplicate=True),
     Output('checkboxes', 'value', allow_duplicate=True),
     Output('popularity', 'children'),
     Output('output-3', 'children'),
     Output('translation-store', 'data', allow_duplicate=True)],
    Input('input-box', 'value')
)
def update_output(input_value):
    translation = diki.translation(input_value)
    if not translation:
        return [], None, '', '', {}
    
    polish_words = [i[0] for i in translation['polish_words']]
    parts_of_speech = [i[1] for i in translation['polish_words']]
    other_words = translation['other_words']
    popularity = translation['popularity']
    examples = translation['examples']
    opposites = translation['opposites']

    checkboxes = [{
        'label': f"{word[1]} [{parts_of_speech[word[0]]}] 📝"
        if word[1] in examples.keys() else f"{word[1]} [{parts_of_speech[word[0]]}]",
        'value': word[0]
    } for word in enumerate(polish_words)]

    lista_3_elements = []

    for idx, word in enumerate(opposites):
        lista_3_elements.append(html.Span(word, style={'color': 'red'}))
        lista_3_elements.append(' 🔗 ')

    other_words_set = set(other_words) - set(opposites)

    for idx, word in enumerate(other_words_set):
        lista_3_elements.append(html.Span(word))
        lista_3_elements.append(' 🔗 ')

    if lista_3_elements and lista_3_elements[-1] == ' 🔗 ':
        lista_3_elements.pop()

    return checkboxes, 0, popularity, lista_3_elements, translation

@app.callback(
    [Output('output-1', 'children'),
     Output('output-2', 'children')],
    [Input('checkboxes', 'value'),
     State('translation-store', 'data')]
)
def update_checkboxes(selected_value, translation):
    if selected_value is None or not translation:
        return None, None

    polish_words = [i[0] for i in translation['polish_words']]
    english_word = translation['english_word']
    examples = translation['examples']

    if not polish_words:
        return '', None

    if not english_word:
        return None, None

    selected_index = int(selected_value)

    if selected_index < 0 or selected_index >= len(polish_words):
        return "Błąd: nieprawidłowy indeks", None

    selected_word = polish_words[selected_index]

    try:
        synonyms = ' (' + translation['synonyms'][selected_word] + ')'
        pronunciation_syn = ' /' + eng_to_ipa.convert(translation['synonyms'][selected_word]) + '/'
    except:
        synonyms = ''
        pronunciation_syn = ''

    pronunciation_eng = '/' + eng_to_ipa.convert(english_word) + '/'

    output_1 = selected_word
    output_2 = [english_word + synonyms, html.Br(), pronunciation_eng + pronunciation_syn, html.Br(), html.Br()]

    if selected_word in examples.keys():
        output_2.extend([examples[selected_word], html.Br()])

    def usun_koncowe_br(lista):
        while lista and isinstance(lista[-1], html.Br):
            lista.pop()
        return lista

    return usun_koncowe_br([output_1]), usun_koncowe_br(output_2)

@app.callback(
    [Output('checkboxes', 'options', allow_duplicate=True),
     Output('checkboxes', 'value', allow_duplicate=True),
     Output('accumulated-records', 'data'),
     Output('translation-store', 'data', allow_duplicate=True)],
    Input('button-1', 'n_clicks'),
    [State('output-1', 'children'),
     State('output-2', 'children'),
     State('checkboxes', 'value'),
     State('accumulated-records', 'data'),
     State('translation-store', 'data')]
)
def handle_button_click(n_clicks, output_1, output_2, selected_value, accumulated_records, translation):
    if n_clicks and n_clicks > 0 and output_1 and output_2:
        html_content = []

        for item in output_2:
            if isinstance(item, str):
                html_content.append(item)
            elif isinstance(item, dict) and item.get('type') == 'Br':
                html_content.append('<br>')
            elif isinstance(item, html.Br):
                html_content.append('<br>')
        
        html_string = ''.join(html_content)

        accumulated_records.append(f'{output_1[0]};{html_string}')

    try:
        translation['polish_words'].pop(int(selected_value))
    except Exception as e:
        print(e)
        print(selected_value, '\n')
        print(translation['polish_words'], '\n')

    # Aktualizujemy checkboxes po usunięciu wybranego słowa
    polish_words = [i[0] for i in translation['polish_words']]
    parts_of_speech = [i[1] for i in translation['polish_words']]
    examples = translation['examples']  

    checkboxes = [{
        'label': f"{word[1]} [{parts_of_speech[word[0]]}] 📝"
        if word[1] in examples.keys() else f"{word[1]} [{parts_of_speech[word[0]]}]",
        'value': word[0]
    } for word in enumerate(polish_words)]

    return checkboxes, 0, accumulated_records, translation

@app.callback(
    [Output('download-text', 'data'),
     Output('accumulated-records', 'data', allow_duplicate=True)],
    Input('download-button', 'n_clicks'),
    State('accumulated-records', 'data'),
    prevent_initial_call=True
)
def download_file(n_clicks, accumulated_records):
    if n_clicks and accumulated_records:
        content = '\n'.join(accumulated_records)
        return dict(content=content, filename='new_flashcards.txt'), []
    return None, accumulated_records

@app.callback(
    Output('record-count', 'children'),
    Input('accumulated-records', 'data')
)
def update_record_count(accumulated_records):
    return f'Liczba rekordów: {len(accumulated_records)}'

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(host='0.0.0.0', port=8080)

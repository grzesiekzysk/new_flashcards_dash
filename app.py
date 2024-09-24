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
    'other_words': []
}

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(
        id='input-box',
        type='text',
        value='',
        placeholder='Wpisz coś...',
        style={
            'font-size': '18px',
            'width': '200px'
        }
    ),
    html.Button(
        'Dodaj fiszkę', 
        id='button-1', 
        n_clicks=0,
        style={
            'font-size': '18px',
            'vertical-align': 'top'
        }
    ),
    html.Div(
        id='popularity',
        style={
            'font-size': '25px',
            'font-weight': 'bold',
            'color': '#3333FF',
            'margin-left': '20px',
            'display': 'inline-block',
            'vertical-align': 'top'
        }
    ),
    html.Br(),
    html.Br(),
    dcc.Checklist(
        id='checkboxes',
        value=[],
        labelStyle={
            #'display': 'grid', 
            #'grid-template-columns': '50% 50%',
            'display': 'block', 
            'font-size': '20px'}
    ),
    html.Br(),
    html.Br(),
    html.P(
        id='output-1',
        style={
            'margin-top': '10px', 
            'font-size': '20px', 
            'border': '1px solid #000', 
            'padding': '10px'}
    ),
    dcc.Clipboard(
        target_id="output-1"
    ),
    html.P(
        id='output-2',
        style={
            'margin-top': '10px', 
            'font-size': '20px', 
            'border': '1px solid #000', 
            'padding': '10px'}
    ),
    dcc.Clipboard(
        target_id="output-2"
    ),
    html.P(
        id='output-3',
        style={
            'margin-top': '10px', 
            'font-size': '20px',
            'color': '#66B2FF',
            # 'border': '1px solid #000', 
            'padding': '10px'}
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

    checkboxy = [{'label': word[1] + f' [{parts_of_speach[word[0]]}]', 'value': word[0]} for word in enumerate(polish_words)]

    # lista_3 = []

    # for w in other_words:
    #     lista_3.append(w)
    #     lista_3.append(' | ')

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

    # polish_words = translation['polish_words']
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
    Input('button-1', 'n_clicks'),
    [State('output-1', 'children'),
     State('output-2', 'children')]
)
def handle_button_click(n_clicks, output_1, output_2):
    if n_clicks > 0:

        html_content = []
        
        for item in output_2:
            if isinstance(item, str):  # Jeśli element jest tekstem
                html_content.append(item)  # Dodaj tekst
            elif isinstance(item, dict) and item.get('type') == 'Br':
                html_content.append('<br>')  # Dodaj <br> jako tekst
        
        html_string = ''.join(html_content)

        print(f"Output 1: {output_1}")
        print(f"Output 2: {html_string}")

    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)

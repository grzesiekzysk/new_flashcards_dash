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
            'width': '50%'
        }
    ),
    html.Div(
        id='popularity',
        style={
            'font-size': '25px',
            'color': 'red',
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
            'font-size': '15px'}
    ),
    html.P(
        id='output-1',
        style={
            'margin-top': '10px', 
            'font-size': '15px', 
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
            'font-size': '15px', 
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
            'font-size': '15px', 
            'border': '1px solid #000', 
            'padding': '10px'}
    ),
    html.Script(src="/assets/copy.js")
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

    lista_3 = []

    for w in other_words:
        # lista_3.append(w)
        # lista_3.append(' | ')
        lista_3.append(html.A(w, href='#', id={'type': 'dynamic-link', 'index': w}, **{'data-copy': w}))
        lista_3.append(' | ')
    
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

    return lista_1, lista_2

if __name__ == '__main__':
    app.run_server(debug=True)

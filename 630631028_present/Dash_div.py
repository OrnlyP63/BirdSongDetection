import dash  
import dash_core_components as dcc 
import dash_html_components as html  
from dash.dependencies import Input, Output, State
import pandas as pd 
import base64


def encode_img(image_file):
  encode = base64.b64encode(open(image_file,'rb').read())
  return f'data:image/png;base64,{encode.decode()}'

def encode_audio(sound_filename):
  encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())
  return f'data:audio/mpeg;base64,{encoded_sound.decode()}'

meta = pd.read_csv('selected_bird.csv')
ID = meta['Recording_ID']
Bird = sorted(meta['Species'].unique())
app = dash.Dash()

all_options = {i:meta[meta['Species']==i]['Recording_ID'].to_list() for i in Bird}

sound_filename = 'cat_1.wav'  # replace with your own .mp3 file
encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())

app.layout = html.Div(children=[
  html.H2(
    'Bird song Application',
    style={
      'textAlign':'center'
    }
  ),

  html.Div([
    html.Label('Bird Species :'),
    html.Br(),
    dcc.Dropdown(
      id='Species',
      options=[{'label': k, 'value': k} for k in all_options.keys()]
    ),
    html.Label('ID Record :'),
    html.Br(),
    dcc.Dropdown(id='ID')
  ],
    style={"width": "30%"},
  ),
  

  html.Div([
    html.Label('Short Time Fourier Transform'),
    html.Br(),
    html.Img(id='img',height=300),
    html.Br(),
    html.Label('Describe :'),
    html.Div(id='describe')
  ],
    style={'text-align': 'center'}
  ),

  html.Div([html.Audio(id='sound', controls=True, style={"width": "30%"})],style={'text-align': 'center'}),
])

@app.callback(
  Output('ID','options'),
  [Input('Species','value')]
)
def set_species_options(selected_species):
    return [{'label': i, 'value': i} for i in all_options[selected_species]]

@app.callback(
  Output('img','src'),
  [Input('ID','value')]
)
def set_img_ID(img_ID):
  path = 'Image/'
  return encode_img(f'Image/{img_ID}.png')

@app.callback(
  Output('describe','children'),
  [Input('ID','value')]
)
def set_img_describe(des_ID):
  return meta.loc[meta['Recording_ID']==des_ID]['Vocalization_type'].to_list()

@app.callback(
  Output('sound','src'),
  [Input('ID','value')]
)
def set_sound(sound_ID):
  path = 'sound/'
  return encode_audio(path+f'{sound_ID}'+'.wav')

if __name__ == "__main__":
  app.run_server()
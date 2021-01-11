import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from tensorflow.keras.models import load_model
import base64
import librosa
import scipy.io.wavfile
import numpy as np
import noisereduce as nr
import io
import plotly.graph_objs as go
import pandas as pd
import plotly.offline as pyo 

#Creating dash application
app = dash.Dash()
Model = load_model('my_model_weights.h5')

# Creating body
body =  [
    html.H2(
    'Bird song predict',
    style={
      'textAlign':'center'
    }
  ),
    html.Div(id='output-box'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        })

  #  dcc.Graph(
  #       id='graph',
  #       figure={
  #           'data': [
  #               {'x': ['Fringilla', 'Parus', 'Turdus', 'Sylvia', 'Emberiza'], 'y': [0, 0, 0, 0, 0], 'type': 'bar', 'name': 'Percent'},
  #           ],
  #           'layout': {
  #               'title': 'Dash Data Visualization'
  #           }
  #       }
  #   )

]

# Setting layout for the application
app.layout = html.Div(body)

def process_content(contents):
    type, data  = contents.split(',')
    decoded = base64.b64decode(data)
    return decoded

def STFT(x):
    #read byte array
    rate, data = scipy.io.wavfile.read(io.BytesIO(x))
    sound = librosa.util.buf_to_float(data)
    
    # noise reduction
    reduced_noise = nr.reduce_noise(audio_clip=sound, noise_clip=sound ,verbose=False)
    
    #trimming
    trimmed, index = librosa.effects.trim(reduced_noise, top_db=20,frame_length=512, hop_length=64)
    
    # extract features
    stft = np.abs(librosa.stft(trimmed, n_fft=512, hop_length=256,win_length=512))
    a = np.mean(stft,axis=1)
    a = a.reshape(1,257)
    return a

# Definfing callback with input and Output
# You need to specify id of Input and Output components along with their attribute name which you want to process
@app.callback(Output('output-box','children'),[Input('upload-data','contents')])
def update(value):
    if value is not None:
        bytes_data = process_content(value)
        vector = STFT(bytes_data)
        Predict = Model.predict(vector)*100
        return f'Sonus : {np.round(Predict[0][0],4)},\n Fringilla : {np.round(Predict[0][1],4)},\n Parus : {np.round(Predict[0][2],4)},\n Turdus : {np.round(Predict[0][3],4)},\n Sylvia : {np.round(Predict[0][4],4)}'

# @app.callback(Output('graph', 'figure'),[Input('upload-data','contents')])
# def update_graph(value):
  
#   if value is not None:
#     bytes_data = process_content(value)
#     vector = STFT(bytes_data)
#     Predict = Model.predict(vector)*100
#     fig={
#             'data': [
#                 {'x': ['Fringilla', 'Parus', 'Turdus', 'Sylvia', 'Emberiza'], 'y': Predict.tolist()[0], 'type': 'bar', 'name': 'Percent'},
#             ],
#             'layout': {'title': 'Dash Data Visualization'}
#           }
#     return fig


# Starting the server
if __name__ == "__main__":
    app.run_server(debug=True)

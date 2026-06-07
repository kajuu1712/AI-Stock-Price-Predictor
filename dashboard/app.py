# ============================================
# app.py — Entry point only
# Creates app, sets layout, registers callbacks
# ============================================

import dash
from dash import dcc, html
from callbacks import register_all_callbacks

app    = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.title = "AI Stock Predictor"

# Two stores — username and current page
# Keeping them separate prevents navigation bugs
app.layout = html.Div([
    dcc.Store(id='store-user', storage_type='session', data=''),
    dcc.Store(id='store-page', storage_type='session', data='dashboard'),
    html.Div(id='page-content')
], style={'backgroundColor': '#0f0f1a',
          'minHeight': '100vh',
          'fontFamily': 'Arial, sans-serif'})

register_all_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
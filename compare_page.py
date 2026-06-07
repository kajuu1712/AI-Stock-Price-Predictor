# ============================================
# compare_page.py
# Layout for the Stock Comparison page
# ============================================

from dash import html, dcc
from data import STOCKS


def compare_page(username):
    return html.Div([

        # ── Header ───────────────────────────
        html.Div([
            html.Div([
                html.H1("📊 Stock Comparison",
                        style={'color': 'white', 'margin': '0',
                               'fontSize': '28px'}),
                html.P("Compare two stocks side by side",
                       style={'color': '#aaa', 'margin': '0'})
            ], style={'flex': '1'}),

            html.Div([
                html.Span(f"👤 {username}",
                          style={'color': '#00ff88', 'marginRight': '20px',
                                 'fontSize': '16px', 'fontWeight': 'bold'}),
                html.Button("📈 Dashboard", id='btn-to-dashboard',
                            n_clicks=0,
                            style={'backgroundColor': '#00d4ff',
                                   'color': '#0f0f1a', 'border': 'none',
                                   'padding': '9px 20px', 'borderRadius': '6px',
                                   'cursor': 'pointer', 'fontWeight': 'bold',
                                   'marginRight': '10px', 'fontSize': '14px'}),
                html.Button("💼 Portfolio", id='btn-to-portfolio',
                            n_clicks=0,
                            style={'backgroundColor': '#ffaa00',
                                   'color': '#0f0f1a', 'border': 'none',
                                   'padding': '9px 20px', 'borderRadius': '6px',
                                   'cursor': 'pointer', 'fontWeight': 'bold',
                                   'marginRight': '10px', 'fontSize': '14px'}),
                html.Button("Logout", id='btn-logout',
                            n_clicks=0,
                            style={'backgroundColor': '#ff6b6b',
                                   'color': 'white', 'border': 'none',
                                   'padding': '9px 20px', 'borderRadius': '6px',
                                   'cursor': 'pointer', 'fontWeight': 'bold',
                                   'fontSize': '14px'})
            ], style={'display': 'flex', 'alignItems': 'center'})

        ], style={'backgroundColor': '#1a1a2e', 'padding': '20px 30px',
                  'display': 'flex', 'alignItems': 'center'}),

        # ── Stock Selectors ───────────────────
        html.Div([

            html.Label("Stock 1:",
                       style={'color': 'white', 'fontWeight': 'bold',
                              'marginRight': '10px', 'fontSize': '15px'}),
            dcc.Dropdown(
                id='compare-stock1',
                options=[{'label': f"{v}  ({k})", 'value': k}
                         for k, v in STOCKS.items()],
                value='AAPL',
                clearable=False,
                style={'width': '280px', 'display': 'inline-block',
                       'verticalAlign': 'middle', 'marginRight': '30px'}
            ),

            html.Label("Stock 2:",
                       style={'color': 'white', 'fontWeight': 'bold',
                              'marginRight': '10px', 'fontSize': '15px'}),
            dcc.Dropdown(
                id='compare-stock2',
                options=[{'label': f"{v}  ({k})", 'value': k}
                         for k, v in STOCKS.items()],
                value='MSFT',
                clearable=False,
                style={'width': '280px', 'display': 'inline-block',
                       'verticalAlign': 'middle', 'marginRight': '30px'}
            ),

            html.Button("🔄 Compare", id='btn-compare',
                        n_clicks=0,
                        style={'backgroundColor': '#cc44ff',
                               'color': 'white', 'border': 'none',
                               'padding': '10px 28px', 'borderRadius': '6px',
                               'cursor': 'pointer', 'fontWeight': 'bold',
                               'fontSize': '15px', 'marginRight': '15px'}),

            html.Span(id='compare-status',
                      children="Select two stocks and click Compare →",
                      style={'color': '#555', 'fontSize': '14px'})

        ], style={'backgroundColor': '#1a1a2e',
                  'padding': '15px 30px 20px 30px',
                  'display': 'flex', 'alignItems': 'center',
                  'flexWrap': 'wrap', 'gap': '8px'}),

        # ── Summary Cards ─────────────────────
        html.Div(id='compare-summary',
                 style={'display': 'flex', 'flexWrap': 'wrap',
                        'backgroundColor': '#1a1a2e',
                        'padding': '0 20px 15px 20px'}),

        # ── Chart 1: Normalized Price ─────────
        html.Div([
            html.H3("📈 Normalized Price Growth (Base = 100)",
                    style={'color': 'white', 'padding': '15px 20px 0',
                           'margin': '0'}),
            html.P("Both stocks start at 100 — fairly compares % growth regardless of actual price",
                   style={'color': '#888', 'padding': '0 20px',
                          'margin': '0', 'fontSize': '13px'}),
            dcc.Graph(id='chart-normalized')
        ], style={'backgroundColor': '#16213e', 'margin': '20px',
                  'borderRadius': '10px'}),

        # ── Chart 2: RSI Comparison ───────────
        html.Div([
            html.H3("⚡ RSI Comparison",
                    style={'color': 'white', 'padding': '15px 20px 0',
                           'margin': '0'}),
            html.P("Which stock is more overbought or oversold right now?",
                   style={'color': '#888', 'padding': '0 20px',
                          'margin': '0', 'fontSize': '13px'}),
            dcc.Graph(id='chart-rsi-compare')
        ], style={'backgroundColor': '#16213e', 'margin': '20px',
                  'borderRadius': '10px'}),

        # ── Chart 3: MACD Comparison ──────────
        html.Div([
            html.H3("📉 MACD Comparison",
                    style={'color': 'white', 'padding': '15px 20px 0',
                           'margin': '0'}),
            html.P("Which stock has stronger momentum right now?",
                   style={'color': '#888', 'padding': '0 20px',
                          'margin': '0', 'fontSize': '13px'}),
            dcc.Graph(id='chart-macd-compare')
        ], style={'backgroundColor': '#16213e', 'margin': '20px',
                  'borderRadius': '10px'}),

        # ── Chart 4: Volume Comparison ────────
        html.Div([
            html.H3("📊 Volume Comparison",
                    style={'color': 'white', 'padding': '15px 20px 0',
                           'margin': '0'}),
            html.P("Which stock has more trading activity?",
                   style={'color': '#888', 'padding': '0 20px',
                          'margin': '0', 'fontSize': '13px'}),
            dcc.Graph(id='chart-volume-compare')
        ], style={'backgroundColor': '#16213e', 'margin': '20px',
                  'borderRadius': '10px'}),

        # ── Chart 5: Correlation ──────────────
        html.Div([
            html.H3("🔗 Price Correlation",
                    style={'color': 'white', 'padding': '15px 20px 0',
                           'margin': '0'}),
            html.P("Each dot = one trading day. Straight line = stocks move together. Scattered = independent.",
                   style={'color': '#888', 'padding': '0 20px',
                          'margin': '0', 'fontSize': '13px'}),
            dcc.Graph(id='chart-correlation')
        ], style={'backgroundColor': '#16213e', 'margin': '20px',
                  'borderRadius': '10px'}),

        # ── Footer ────────────────────────────
        html.Div([
            html.P("AI Stock Price Predictor  |  Stock Comparison  |  Internship 2026",
                   style={'color': '#444', 'textAlign': 'center', 'margin': '0'})
        ], style={'backgroundColor': '#1a1a2e', 'padding': '20px'})

    ], style={'backgroundColor': '#0f0f1a', 'minHeight': '100vh',
              'fontFamily': 'Arial, sans-serif'})
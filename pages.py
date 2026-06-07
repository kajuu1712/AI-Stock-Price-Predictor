# ============================================
# pages.py
# All page layouts: Login, Dashboard, Portfolio
# ============================================

from dash import html, dcc
from data import STOCKS, get_latest_price, get_trade_signal
from portfolio import get_holdings, get_history
from charts import make_card


# ════════════════════════════════════════════
# LOGIN PAGE
# ════════════════════════════════════════════
def login_page(message="", msg_type="warn"):
    # Message box color based on type
    msg_colors = {
        "error":   "#ff6b6b",
        "success": "#00ff88",
        "warn":    "#ffaa00"
    }
    msg_bgs = {
        "error":   "rgba(255,107,107,0.15)",
        "success": "rgba(0,255,136,0.1)",
        "warn":    "rgba(255,170,0,0.1)"
    }
    msg_borders = {
        "error":   "1px solid rgba(255,107,107,0.3)",
        "success": "1px solid rgba(0,255,136,0.3)",
        "warn":    "1px solid rgba(255,170,0,0.3)"
    }

    msg_style = {
        'color':           msg_colors.get(msg_type, "#ffaa00"),
        'textAlign':       'center',
        'fontSize':        '14px',
        'padding':         '10px' if message else '0',
        'borderRadius':    '5px',
        'marginBottom':    '15px',
        'minHeight':       '20px',
        'backgroundColor': msg_bgs.get(msg_type, "transparent") if message else "transparent",
        'border':          msg_borders.get(msg_type, "none") if message else "none"
    }

    return html.Div([

        # Top header
        html.Div([
            html.H1("📈 AI Stock Price Predictor",
                    style={'color':'white','textAlign':'center',
                           'marginBottom':'5px','fontSize':'32px'}),
            html.H3("Multi-Stock ML Dashboard with Technical Indicators",
                    style={'color':'#aaa','textAlign':'center','marginTop':'0'})
        ], style={'backgroundColor':'#1a1a2e','padding':'30px'}),

        # Login card
        html.Div([
            html.Div([

                html.H2("🔐 Login / Register",
                        style={'color':'white','textAlign':'center',
                               'marginBottom':'25px'}),

                # Tab buttons — Login | Register
                html.Div([
                    html.Button("Login", id='tab-login', n_clicks=0,
                                style={'backgroundColor':'#00d4ff',
                                       'color':'#0f0f1a','border':'none',
                                       'padding':'10px 0','flex':'1',
                                       'borderRadius':'6px 0 0 6px',
                                       'cursor':'pointer','fontWeight':'bold',
                                       'fontSize':'15px'}),
                    html.Button("Register", id='tab-register', n_clicks=0,
                                style={'backgroundColor':'#16213e',
                                       'color':'#aaa',
                                       'border':'1px solid #333',
                                       'padding':'10px 0','flex':'1',
                                       'borderRadius':'0 6px 6px 0',
                                       'cursor':'pointer','fontWeight':'bold',
                                       'fontSize':'15px'})
                ], style={'display':'flex','marginBottom':'25px'}),

                # Stores the current mode: 'login' or 'register'
                dcc.Store(id='auth-mode', data='login'),

                # Username
                html.Label("Username",
                           style={'color':'#aaa','display':'block',
                                  'marginBottom':'5px'}),
                dcc.Input(id='input-username', type='text',
                          placeholder='Enter your username...',
                          n_submit=0,
                          style={'width':'100%','padding':'10px',
                                 'backgroundColor':'#0f3460','color':'white',
                                 'border':'1px solid #444','borderRadius':'5px',
                                 'marginBottom':'15px','boxSizing':'border-box',
                                 'fontSize':'14px'}),

                # Password label (changes for register mode)
                html.Label(id='label-password', children="Password",
                           style={'color':'#aaa','display':'block',
                                  'marginBottom':'5px'}),
                dcc.Input(id='input-password', type='password',
                          placeholder='Enter your password...',
                          n_submit=0,
                          style={'width':'100%','padding':'10px',
                                 'backgroundColor':'#0f3460','color':'white',
                                 'border':'1px solid #444','borderRadius':'5px',
                                 'marginBottom':'15px','boxSizing':'border-box',
                                 'fontSize':'14px'}),

                # Confirm password — only shown in register mode
                html.Div([
                    html.Label("Confirm Password",
                               style={'color':'#aaa','display':'block',
                                      'marginBottom':'5px'}),
                    dcc.Input(id='input-confirm', type='password',
                              placeholder='Re-enter your password...',
                              n_submit=0,
                              style={'width':'100%','padding':'10px',
                                     'backgroundColor':'#0f3460','color':'white',
                                     'border':'1px solid #444','borderRadius':'5px',
                                     'marginBottom':'15px','boxSizing':'border-box',
                                     'fontSize':'14px'})
                ], id='div-confirm', style={'display':'none'}),

                # Message area — always rendered, text changes
                html.Div(id='auth-message',
                         children=message,
                         style=msg_style),

                # Submit button
                html.Button(id='btn-submit',
                            children="Login",
                            n_clicks=0,
                            style={'width':'100%','padding':'12px',
                                   'backgroundColor':'#00d4ff',
                                   'color':'#0f0f1a','border':'none',
                                   'borderRadius':'6px','cursor':'pointer',
                                   'fontWeight':'bold','fontSize':'16px'}),

                # Hint text below button
                html.P(id='hint-text',
                       children="Don't have an account? Click Register above",
                       style={'color':'#555','textAlign':'center',
                              'marginTop':'15px','fontSize':'13px'})

            ], style={
                'backgroundColor':'#16213e',
                'padding':         '40px',
                'borderRadius':    '15px',
                'width':           '420px',
                'margin':          '60px auto',
                'boxShadow':       '0 0 40px rgba(0,212,255,0.1)'
            })
        ])

    ], style={'backgroundColor':'#0f0f1a','minHeight':'100vh'})


# ════════════════════════════════════════════
# DASHBOARD PAGE
# ════════════════════════════════════════════
def dashboard_page(username):
    return html.Div([

        # Header
        html.Div([
            html.Div([
                html.H1("📈 AI Stock Price Predictor",
                        style={'color':'white','margin':'0','fontSize':'28px'}),
                html.P("Multi-Stock ML Dashboard with Technical Indicators",
                       style={'color':'#aaa','margin':'0'})
            ], style={'flex':'1'}),
            html.Div([
                html.Span(f"👤 {username}",
                          style={'color':'#00ff88','marginRight':'20px',
                                 'fontSize':'16px','fontWeight':'bold'}),
                html.Button("💼 Portfolio", id='btn-to-portfolio',
                            n_clicks=0,
                            style={'backgroundColor':'#ffaa00','color':'#0f0f1a',
                                   'border':'none','padding':'9px 20px',
                                   'borderRadius':'6px','cursor':'pointer',
                                   'fontWeight':'bold','marginRight':'10px',
                                   'fontSize':'14px'}),
                html.Button("📊 Compare", id='btn-to-compare',
                            n_clicks=0,
                            style={'backgroundColor':'#cc44ff','color':'white',
                                   'border':'none','padding':'9px 20px',
                                   'borderRadius':'6px','cursor':'pointer',
                                   'fontWeight':'bold','marginRight':'10px',
                                   'fontSize':'14px'}),
                html.Button("Logout", id='btn-logout',
                            n_clicks=0,
                            style={'backgroundColor':'#ff6b6b','color':'white',
                                   'border':'none','padding':'9px 20px',
                                   'borderRadius':'6px','cursor':'pointer',
                                   'fontWeight':'bold','fontSize':'14px'})
            ], style={'display':'flex','alignItems':'center'})
        ], style={'backgroundColor':'#1a1a2e','padding':'20px 30px',
                  'display':'flex','alignItems':'center'}),

        # Stock Selector
        html.Div([
            html.Label("Select Stock: ",
                       style={'color':'white','marginRight':'10px',
                              'fontSize':'16px'}),
            dcc.Dropdown(
                id='stock-dropdown',
                options=[{'label':f"{v}  ({k})",'value':k}
                         for k,v in STOCKS.items()],
                value='AAPL', clearable=False,
                style={'width':'380px','display':'inline-block',
                       'verticalAlign':'middle'}
            ),
            html.Span(id='loading-msg',
                      style={'color':'#ffaa00','marginLeft':'15px',
                             'fontSize':'14px'})
        ], style={'backgroundColor':'#1a1a2e','padding':'10px 30px 20px'}),

        # Stat Cards
        html.Div(id='stats-cards',
                 style={'display':'flex','backgroundColor':'#1a1a2e',
                        'padding':'0 20px 15px 20px'}),

        # Chart 1 — Price + Moving Averages
        html.Div([
            html.H3(id='chart1-title',
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            dcc.Graph(id='price-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Chart 2 — Actual vs Predicted
        html.Div([
            html.H3("🤖 Actual vs Predicted Price",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            dcc.Graph(id='prediction-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Chart 3 — RSI
        html.Div([
            html.H3("⚡ RSI — Relative Strength Index",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            html.P("Above 70 = Overbought (might drop) | Below 30 = Oversold (might rise) | 14-day period",
                   style={'color':'#888','padding':'0 20px','margin':'0',
                          'fontSize':'13px'}),
            dcc.Graph(id='rsi-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Chart 4 — MACD
        html.Div([
            html.H3("📉 MACD — Moving Average Convergence Divergence",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            html.P("MACD above Signal = Bullish 📈 | MACD below Signal = Bearish 📉",
                   style={'color':'#888','padding':'0 20px','margin':'0',
                          'fontSize':'13px'}),
            dcc.Graph(id='macd-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Chart 5 — Volume
        html.Div([
            html.H3("📊 Trading Volume Over Time",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            dcc.Graph(id='volume-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Chart 6 — Daily Range
        html.Div([
            html.H3("📏 Daily Price Range — Volatility",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            dcc.Graph(id='range-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Chart 7 — Yearly Box Plot
        html.Div([
            html.H3("📅 Yearly Price Distribution",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            dcc.Graph(id='yearly-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Prediction Tool
        html.Div([
            html.H3("🔮 Predict Price for a Date",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            html.Div([
                html.P("Select a date from the last 100 trading days:",
                       style={'color':'#aaa','marginBottom':'8px'}),
                dcc.Dropdown(id='date-dropdown', clearable=False,
                             style={'width':'300px'}),
                html.Div(id='prediction-output',
                         style={'marginTop':'15px','fontSize':'18px',
                                'color':'#00ff88','fontWeight':'bold'})
            ], style={'padding':'10px 20px 25px'})
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Footer
        html.Div([
            html.P("AI Stock Price Predictor  |  Linear Regression + RSI + MACD  |  Internship 2026",
                   style={'color':'#444','textAlign':'center','margin':'0'})
        ], style={'backgroundColor':'#1a1a2e','padding':'20px'})

    ], style={'backgroundColor':'#0f0f1a','minHeight':'100vh',
              'fontFamily':'Arial, sans-serif'})


# ════════════════════════════════════════════
# PORTFOLIO PAGE
# ════════════════════════════════════════════
def portfolio_page(username):
    holdings = get_holdings(username)
    history  = get_history(username)

    # ── Build holdings table rows ─────────────
    holding_rows   = []
    total_invested = 0
    total_current  = 0

    for item in holdings:
        current_price          = get_latest_price(item['stock']) or item['buy_price']
        rsi_val, rsi_sig, macd_sig = get_trade_signal(item['stock'])
        invested               = item['buy_price'] * item['shares']
        current                = current_price * item['shares']
        profit                 = current - invested
        pct                    = (profit / invested * 100) if invested > 0 else 0
        total_invested        += invested
        total_current         += current
        color                  = '#00ff88' if profit >= 0 else '#ff6b6b'

        holding_rows.append(
            html.Tr([
                html.Td(item['stock'],
                        style={'color':'#00d4ff','fontWeight':'bold','padding':'12px'}),
                html.Td(f"{item['shares']:.0f}",
                        style={'color':'white','padding':'12px'}),
                html.Td(f"${item['buy_price']:.2f}",
                        style={'color':'white','padding':'12px'}),
                html.Td(f"${current_price:.2f}",
                        style={'color':'white','padding':'12px'}),
                html.Td(f"${profit:+.2f} ({pct:+.1f}%)",
                        style={'color':color,'padding':'12px','fontWeight':'bold'}),
                html.Td(rsi_sig,
                        style={'color':'#cc44ff','padding':'12px','fontSize':'13px'}),
                html.Td(macd_sig,
                        style={'color':'#ffaa00','padding':'12px','fontSize':'13px'}),
                html.Td(
                    html.Button("Sell",
                                id={'type':'btn-sell','index':item['id']},
                                n_clicks=0,
                                style={'backgroundColor':'#ff6b6b',
                                       'color':'white','border':'none',
                                       'padding':'6px 16px','borderRadius':'5px',
                                       'cursor':'pointer','fontWeight':'bold'}),
                    style={'padding':'12px'}
                )
            ], style={'borderBottom':'1px solid #1a1a2e'})
        )

    # ── Build history table rows ──────────────
    history_rows = []
    for item in reversed(history[-15:]):
        if item['type'] == 'SELL':
            color = '#00ff88' if item['profit'] >= 0 else '#ff6b6b'
            history_rows.append(html.Tr([
                html.Td("SELL", style={'color':'#ff6b6b','padding':'10px',
                                       'fontWeight':'bold'}),
                html.Td(item['stock'],                style={'color':'#00d4ff','padding':'10px'}),
                html.Td(f"{item['shares']:.0f}",      style={'color':'white','padding':'10px'}),
                html.Td(f"${item['buy_price']:.2f}",  style={'color':'white','padding':'10px'}),
                html.Td(f"${item['sell_price']:.2f}", style={'color':'white','padding':'10px'}),
                html.Td(f"${item['profit']:+.2f}",
                        style={'color':color,'padding':'10px','fontWeight':'bold'}),
                html.Td(item['date'], style={'color':'#aaa','padding':'10px'})
            ], style={'borderBottom':'1px solid #1a1a2e'}))
        else:
            history_rows.append(html.Tr([
                html.Td("BUY",  style={'color':'#00ff88','padding':'10px',
                                       'fontWeight':'bold'}),
                html.Td(item['stock'],           style={'color':'#00d4ff','padding':'10px'}),
                html.Td(f"{item['shares']:.0f}", style={'color':'white','padding':'10px'}),
                html.Td(f"${item['buy_price']:.2f}", style={'color':'white','padding':'10px'}),
                html.Td("—", style={'color':'#aaa','padding':'10px'}),
                html.Td("—", style={'color':'#aaa','padding':'10px'}),
                html.Td(item['date'], style={'color':'#aaa','padding':'10px'})
            ], style={'borderBottom':'1px solid #1a1a2e'}))

    # ── Summary numbers ───────────────────────
    total_profit = total_current - total_invested
    total_pct    = (total_profit / total_invested * 100) if total_invested > 0 else 0
    pnl_color    = '#00ff88' if total_profit >= 0 else '#ff6b6b'

    return html.Div([

        # Header
        html.Div([
            html.Div([
                html.H1("💼 My Portfolio",
                        style={'color':'white','margin':'0','fontSize':'28px'}),
                html.P(f"Welcome, {username}!",
                       style={'color':'#aaa','margin':'0'})
            ], style={'flex':'1'}),
            html.Div([
                html.Button("📈 Dashboard", id='btn-to-dashboard',
                            n_clicks=0,
                            style={'backgroundColor':'#00d4ff','color':'#0f0f1a',
                                   'border':'none','padding':'9px 20px',
                                   'borderRadius':'6px','cursor':'pointer',
                                   'fontWeight':'bold','marginRight':'10px',
                                   'fontSize':'14px'}),
                html.Button("Logout", id='btn-logout',
                            n_clicks=0,
                            style={'backgroundColor':'#ff6b6b','color':'white',
                                   'border':'none','padding':'9px 20px',
                                   'borderRadius':'6px','cursor':'pointer',
                                   'fontWeight':'bold','fontSize':'14px'})
            ], style={'display':'flex','alignItems':'center'})
        ], style={'backgroundColor':'#1a1a2e','padding':'20px 30px',
                  'display':'flex','alignItems':'center'}),

        # Summary Cards
        html.Div([
            make_card("Total Invested",  f"${total_invested:.2f}",                       '#00d4ff'),
            make_card("Current Value",   f"${total_current:.2f}",                        '#00ff88'),
            make_card("Total P&L",       f"${total_profit:+.2f} ({total_pct:+.1f}%)",   pnl_color),
            make_card("Holdings",        str(len(holdings)),                              '#ffaa00'),
        ], style={'display':'flex','backgroundColor':'#1a1a2e',
                  'padding':'10px 20px 20px'}),

        # Buy Form
        html.Div([
            html.H3("➕ Buy Stock",
                    style={'color':'white','padding':'15px 20px 10px','margin':'0'}),
            html.Div([
                dcc.Dropdown(id='buy-ticker',
                             options=[{'label':f"{v} ({k})",'value':k}
                                      for k,v in STOCKS.items()],
                             placeholder="Select stock...",
                             style={'width':'220px','display':'inline-block',
                                    'marginRight':'10px','verticalAlign':'middle'}),
                dcc.Input(id='buy-shares', type='number', placeholder='Shares',
                          min=1,
                          style={'width':'120px','padding':'8px',
                                 'backgroundColor':'#0f3460','color':'white',
                                 'border':'1px solid #444','borderRadius':'5px',
                                 'marginRight':'10px','fontSize':'14px'}),
                dcc.Input(id='buy-price', type='number', placeholder='Price ($)',
                          min=0.01,
                          style={'width':'140px','padding':'8px',
                                 'backgroundColor':'#0f3460','color':'white',
                                 'border':'1px solid #444','borderRadius':'5px',
                                 'marginRight':'10px','fontSize':'14px'}),
                html.Button("Buy Now", id='btn-buy', n_clicks=0,
                            style={'backgroundColor':'#00ff88','color':'#0f0f1a',
                                   'border':'none','padding':'9px 22px',
                                   'borderRadius':'6px','cursor':'pointer',
                                   'fontWeight':'bold','fontSize':'14px'}),
                html.Span(id='buy-message',
                          style={'marginLeft':'15px','fontSize':'14px',
                                 'color':'#ffaa00'})
            ], style={'padding':'0 20px 20px','display':'flex',
                      'alignItems':'center','flexWrap':'wrap','gap':'8px'})
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Holdings Table
        html.Div([
            html.H3("📊 Current Holdings",
                    style={'color':'white','padding':'15px 20px 10px','margin':'0'}),
            html.Div([
                html.Table([
                    html.Thead(html.Tr([
                        html.Th(h, style={'color':'#aaa','padding':'12px',
                                          'textAlign':'left','whiteSpace':'nowrap'})
                        for h in ["Stock","Shares","Buy Price","Current Price",
                                  "Profit / Loss","RSI Signal","MACD Signal","Action"]
                    ], style={'backgroundColor':'#0f3460'})),
                    html.Tbody(
                        holding_rows if holding_rows else [
                            html.Tr([html.Td(
                                "No holdings yet — buy your first stock above! 👆",
                                colSpan=8,
                                style={'color':'#555','padding':'30px',
                                       'textAlign':'center','fontSize':'15px'}
                            )])
                        ]
                    )
                ], style={'width':'100%','borderCollapse':'collapse','color':'white'})
            ], style={'padding':'0 20px 20px','overflowX':'auto'}),
            html.Div(id='sell-message',
                     style={'color':'#ffaa00','padding':'0 20px 15px','fontSize':'14px'})
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # History Table
        html.Div([
            html.H3("📋 Transaction History (Last 15)",
                    style={'color':'white','padding':'15px 20px 10px','margin':'0'}),
            html.Div([
                html.Table([
                    html.Thead(html.Tr([
                        html.Th(h, style={'color':'#aaa','padding':'10px',
                                          'textAlign':'left','whiteSpace':'nowrap'})
                        for h in ["Type","Stock","Shares","Buy Price",
                                  "Sell Price","Profit/Loss","Date"]
                    ], style={'backgroundColor':'#0f3460'})),
                    html.Tbody(
                        history_rows if history_rows else [
                            html.Tr([html.Td(
                                "No transactions yet.",
                                colSpan=7,
                                style={'color':'#555','padding':'20px',
                                       'textAlign':'center'}
                            )])
                        ]
                    )
                ], style={'width':'100%','borderCollapse':'collapse','color':'white'})
            ], style={'padding':'0 20px 20px','overflowX':'auto'})
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Footer
        html.Div([
            html.P("AI Stock Price Predictor  |  Portfolio Tracker  |  Internship 2026",
                   style={'color':'#444','textAlign':'center','margin':'0'})
        ], style={'backgroundColor':'#1a1a2e','padding':'20px'})

    ], style={'backgroundColor':'#0f0f1a','minHeight':'100vh',
              'fontFamily':'Arial, sans-serif'})


# ════════════════════════════════════════════
# COMPARE PAGE (Priority 2)
# ════════════════════════════════════════════
def compare_page(username):
    from data import STOCKS
    return html.Div([

        # Header
        html.Div([
            html.Div([
                html.H1("📊 Stock Comparison",
                        style={'color':'white','margin':'0','fontSize':'28px'}),
                html.P("Compare two stocks side by side",
                       style={'color':'#aaa','margin':'0'})
            ], style={'flex':'1'}),
            html.Div([
                html.Span(f"👤 {username}",
                          style={'color':'#00ff88','marginRight':'20px',
                                 'fontSize':'16px','fontWeight':'bold'}),
                html.Button("📈 Dashboard", id='btn-to-dashboard',
                            n_clicks=0,
                            style={'backgroundColor':'#00d4ff','color':'#0f0f1a',
                                   'border':'none','padding':'9px 20px',
                                   'borderRadius':'6px','cursor':'pointer',
                                   'fontWeight':'bold','marginRight':'10px',
                                   'fontSize':'14px'}),
                html.Button("💼 Portfolio", id='btn-to-portfolio',
                            n_clicks=0,
                            style={'backgroundColor':'#ffaa00','color':'#0f0f1a',
                                   'border':'none','padding':'9px 20px',
                                   'borderRadius':'6px','cursor':'pointer',
                                   'fontWeight':'bold','marginRight':'10px',
                                   'fontSize':'14px'}),
                html.Button("📊 Compare", id='btn-to-compare',
                            n_clicks=1,
                            style={'backgroundColor':'#cc44ff','color':'white',
                                   'border':'none','padding':'9px 20px',
                                   'borderRadius':'6px','cursor':'pointer',
                                   'fontWeight':'bold','marginRight':'10px',
                                   'fontSize':'14px'}),
                html.Button("Logout", id='btn-logout',
                            n_clicks=0,
                            style={'backgroundColor':'#ff6b6b','color':'white',
                                   'border':'none','padding':'9px 20px',
                                   'borderRadius':'6px','cursor':'pointer',
                                   'fontWeight':'bold','fontSize':'14px'})
            ], style={'display':'flex','alignItems':'center'})
        ], style={'backgroundColor':'#1a1a2e','padding':'20px 30px',
                  'display':'flex','alignItems':'center'}),

        # Stock selectors
        html.Div([
            html.Div([
                html.Label("Stock 1:",
                           style={'color':'white','marginRight':'10px',
                                  'fontSize':'15px','fontWeight':'bold'}),
                dcc.Dropdown(
                    id='compare-stock1',
                    options=[{'label':f"{v} ({k})",'value':k}
                             for k,v in STOCKS.items()],
                    value='AAPL', clearable=False,
                    style={'width':'280px','display':'inline-block',
                           'verticalAlign':'middle'}
                )
            ], style={'display':'flex','alignItems':'center',
                      'marginRight':'30px'}),

            html.Div([
                html.Label("Stock 2:",
                           style={'color':'white','marginRight':'10px',
                                  'fontSize':'15px','fontWeight':'bold'}),
                dcc.Dropdown(
                    id='compare-stock2',
                    options=[{'label':f"{v} ({k})",'value':k}
                             for k,v in STOCKS.items()],
                    value='MSFT', clearable=False,
                    style={'width':'280px','display':'inline-block',
                           'verticalAlign':'middle'}
                )
            ], style={'display':'flex','alignItems':'center'}),

            html.Button("🔄 Compare Now", id='btn-compare', n_clicks=0,
                        style={'backgroundColor':'#00ff88','color':'#0f0f1a',
                               'border':'none','padding':'10px 25px',
                               'borderRadius':'6px','cursor':'pointer',
                               'fontWeight':'bold','fontSize':'15px',
                               'marginLeft':'30px'}),

            html.Span(id='compare-loading',
                      style={'color':'#ffaa00','marginLeft':'15px',
                             'fontSize':'14px'})

        ], style={'backgroundColor':'#1a1a2e','padding':'15px 30px 20px',
                  'display':'flex','alignItems':'center','flexWrap':'wrap',
                  'gap':'10px'}),

        # Comparison stat cards
        html.Div(id='compare-cards',
                 style={'display':'flex','backgroundColor':'#1a1a2e',
                        'padding':'0 20px 15px 20px'}),

        # Chart 1 — Normalized Price
        html.Div([
            html.H3("📈 Normalized Price Comparison (Base = 100)",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            html.P("Both stocks start at 100 — shows % growth fairly regardless of actual price",
                   style={'color':'#888','padding':'0 20px','margin':'0',
                          'fontSize':'13px'}),
            dcc.Graph(id='compare-price-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Chart 2 — RSI Comparison
        html.Div([
            html.H3("⚡ RSI Comparison",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            html.P("Which stock is more overbought or oversold right now?",
                   style={'color':'#888','padding':'0 20px','margin':'0',
                          'fontSize':'13px'}),
            dcc.Graph(id='compare-rsi-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Chart 3 — MACD Comparison
        html.Div([
            html.H3("📉 MACD Comparison",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            html.P("Which stock has stronger momentum right now?",
                   style={'color':'#888','padding':'0 20px','margin':'0',
                          'fontSize':'13px'}),
            dcc.Graph(id='compare-macd-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Chart 4 — Volume Comparison
        html.Div([
            html.H3("📊 Volume Comparison",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            html.P("Which stock has more trading activity?",
                   style={'color':'#888','padding':'0 20px','margin':'0',
                          'fontSize':'13px'}),
            dcc.Graph(id='compare-volume-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Chart 5 — Correlation
        html.Div([
            html.H3("🔗 Price Correlation",
                    style={'color':'white','padding':'15px 20px 0','margin':'0'}),
            html.P("Do these stocks move together? Points forming a line = high correlation",
                   style={'color':'#888','padding':'0 20px','margin':'0',
                          'fontSize':'13px'}),
            dcc.Graph(id='compare-corr-chart')
        ], style={'backgroundColor':'#16213e','margin':'20px','borderRadius':'10px'}),

        # Footer
        html.Div([
            html.P("AI Stock Price Predictor  |  Stock Comparison  |  Internship 2026",
                   style={'color':'#444','textAlign':'center','margin':'0'})
        ], style={'backgroundColor':'#1a1a2e','padding':'20px'})

    ], style={'backgroundColor':'#0f0f1a','minHeight':'100vh',
              'fontFamily':'Arial, sans-serif'})
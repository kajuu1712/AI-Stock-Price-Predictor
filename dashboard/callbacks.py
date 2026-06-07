# ============================================
# callbacks.py
# ALL callbacks for the entire app
# Cleanly separated by feature section
# ============================================

from dash import Input, Output, State, no_update, ALL, html
from data import get_stock_data, STOCKS, get_latest_price, get_trade_signal
from pages import login_page, dashboard_page, portfolio_page
from compare_page import compare_page
from auth import login_user, register_user
from portfolio import buy_stock, sell_stock, get_holdings
from charts import (make_card,
                    build_price_chart, build_prediction_chart,
                    build_rsi_chart, build_macd_chart,
                    build_volume_chart, build_range_chart,
                    build_yearly_chart, empty_figure)
from compare_charts import (build_normalized_chart, build_rsi_comparison,
                             build_macd_comparison, build_volume_comparison,
                             build_correlation_chart, empty_compare_figure)


def register_all_callbacks(app):

    # ══════════════════════════════════════════
    # SECTION 1 — PAGE ROUTING
    # ══════════════════════════════════════════

    @app.callback(
        Output('page-content', 'children'),
        Input('store-user',    'data'),
        Input('store-page',    'data')
    )
    def render_page(username, page):
        if not username:
            return login_page()
        if page == 'portfolio':
            return portfolio_page(username)
        if page == 'compare':
            return compare_page(username)
        return dashboard_page(username)

    # ══════════════════════════════════════════
    # SECTION 2 — AUTH (Login / Register)
    # ══════════════════════════════════════════

    @app.callback(
        Output('auth-mode',      'data'),
        Output('tab-login',      'style'),
        Output('tab-register',   'style'),
        Output('div-confirm',    'style'),
        Output('btn-submit',     'children'),
        Output('label-password', 'children'),
        Output('hint-text',      'children'),
        Output('auth-message',   'children'),
        Output('auth-message',   'style'),
        Input('tab-login',       'n_clicks'),
        Input('tab-register',    'n_clicks'),
        prevent_initial_call=True
    )
    def toggle_auth_tab(l, r):
        from dash import ctx
        clicked = ctx.triggered_id

        ACTIVE   = {'border': 'none', 'padding': '10px 0', 'flex': '1',
                    'cursor': 'pointer', 'fontWeight': 'bold', 'fontSize': '15px',
                    'backgroundColor': '#00d4ff', 'color': '#0f0f1a'}
        INACTIVE = {'border': '1px solid #333', 'padding': '10px 0', 'flex': '1',
                    'cursor': 'pointer', 'fontWeight': 'bold', 'fontSize': '15px',
                    'backgroundColor': '#16213e', 'color': '#aaa'}
        CLEAR    = {'color': '#ffaa00', 'textAlign': 'center', 'fontSize': '14px',
                    'padding': '0', 'minHeight': '20px', 'marginBottom': '15px',
                    'backgroundColor': 'transparent', 'border': 'none'}

        if clicked == 'tab-register':
            return (
                'register',
                {**INACTIVE, 'borderRadius': '6px 0 0 6px'},
                {**ACTIVE,   'borderRadius': '0 6px 6px 0'},
                {'display': 'block'},
                "Register",
                "Create Password",
                "Already have an account? Click Login above",
                "", CLEAR
            )
        return (
            'login',
            {**ACTIVE,   'borderRadius': '6px 0 0 6px'},
            {**INACTIVE, 'borderRadius': '0 6px 6px 0'},
            {'display': 'none'},
            "Login",
            "Password",
            "Don't have an account? Click Register above",
            "", CLEAR
        )

    @app.callback(
        Output('store-user',   'data',     allow_duplicate=True),
        Output('store-page',   'data',     allow_duplicate=True),
        Output('auth-message', 'children', allow_duplicate=True),
        Output('auth-message', 'style',    allow_duplicate=True),
        Input('btn-submit',    'n_clicks'),
        State('auth-mode',     'data'),
        State('input-username','value'),
        State('input-password','value'),
        State('input-confirm', 'value'),
        prevent_initial_call=True
    )
    def handle_auth(n, mode, username, password, confirm):
        if not n:
            return no_update, no_update, "", {}

        ERR  = {'color':'#ff6b6b','textAlign':'center','fontSize':'14px',
                'padding':'10px','minHeight':'20px','marginBottom':'15px',
                'borderRadius':'5px','backgroundColor':'rgba(255,107,107,0.15)',
                'border':'1px solid rgba(255,107,107,0.3)'}
        OK   = {'color':'#00ff88','textAlign':'center','fontSize':'14px',
                'padding':'10px','minHeight':'20px','marginBottom':'15px',
                'borderRadius':'5px','backgroundColor':'rgba(0,255,136,0.1)',
                'border':'1px solid rgba(0,255,136,0.3)'}
        WARN = {'color':'#ffaa00','textAlign':'center','fontSize':'14px',
                'padding':'10px','minHeight':'20px','marginBottom':'15px',
                'borderRadius':'5px','backgroundColor':'rgba(255,170,0,0.1)',
                'border':'1px solid rgba(255,170,0,0.3)'}

        if not username or not username.strip():
            return no_update, no_update, "⚠️ Please enter a username!", WARN
        if not password:
            return no_update, no_update, "⚠️ Please enter a password!", WARN

        u = username.strip()

        if mode == 'register':
            if not confirm:
                return no_update, no_update, "⚠️ Please confirm your password!", WARN
            if password != confirm:
                return no_update, no_update, "❌ Passwords do not match!", ERR
            if len(password) < 4:
                return no_update, no_update, "❌ Password must be at least 4 characters!", ERR
            ok, msg = register_user(u, password)
            if ok:
                return u, 'dashboard', f"✅ {msg}", OK
            return no_update, no_update, f"❌ {msg}", ERR
        else:
            ok, msg = login_user(u, password)
            if ok:
                return u, 'dashboard', f"✅ {msg}", OK
            return no_update, no_update, f"❌ {msg}", ERR

    # ══════════════════════════════════════════
    # SECTION 3 — NAVIGATION
    # ══════════════════════════════════════════

    @app.callback(
        Output('store-user', 'data',      allow_duplicate=True),
        Output('store-page', 'data',      allow_duplicate=True),
        Input('btn-logout',  'n_clicks'),
        prevent_initial_call=True
    )
    def handle_logout(n):
        if not n:
            return no_update, no_update
        return '', 'dashboard'

    @app.callback(
        Output('store-page',       'data', allow_duplicate=True),
        Input('btn-to-portfolio',  'n_clicks'),
        prevent_initial_call=True
    )
    def go_portfolio(n):
        if not n:
            return no_update
        return 'portfolio'

    @app.callback(
        Output('store-page',      'data',  allow_duplicate=True),
        Input('btn-to-dashboard', 'n_clicks'),
        prevent_initial_call=True
    )
    def go_dashboard(n):
        if not n:
            return no_update
        return 'dashboard'

    @app.callback(
        Output('store-page',     'data',   allow_duplicate=True),
        Input('btn-to-compare',  'n_clicks'),
        prevent_initial_call=True
    )
    def go_compare(n):
        if not n:
            return no_update
        return 'compare'

    # ══════════════════════════════════════════
    # SECTION 4 — PORTFOLIO (Buy / Sell)
    # ══════════════════════════════════════════

    @app.callback(
        Output('buy-message', 'children'),
        Output('store-page',  'data',      allow_duplicate=True),
        Input('btn-buy',      'n_clicks'),
        State('buy-ticker',   'value'),
        State('buy-shares',   'value'),
        State('buy-price',    'value'),
        State('store-user',   'data'),
        prevent_initial_call=True
    )
    def handle_buy(n, ticker, shares, price, username):
        if not n:
            return "", no_update
        if not ticker:
            return "⚠️ Please select a stock!", no_update
        if not shares or float(shares) <= 0:
            return "⚠️ Please enter a valid number of shares!", no_update
        if not price or float(price) <= 0:
            return "⚠️ Please enter a valid price!", no_update
        ok, msg = buy_stock(username, ticker, shares, price)
        if ok:
            return f"✅ {msg}", 'portfolio'
        return f"❌ {msg}", no_update

    @app.callback(
        Output('sell-message', 'children'),
        Output('store-page',   'data',     allow_duplicate=True),
        Input({'type': 'btn-sell', 'index': ALL}, 'n_clicks'),
        State('store-user',    'data'),
        prevent_initial_call=True
    )
    def handle_sell(n_clicks_list, username):
        from dash import ctx
        if not any(n_clicks_list):
            return "", no_update
        triggered = ctx.triggered_id
        if not triggered:
            return "", no_update
        record_id     = triggered['index']
        holdings      = get_holdings(username)
        current_price = None
        for h in holdings:
            if h['id'] == record_id:
                current_price = get_latest_price(h['stock']) or h['buy_price']
                break
        if current_price is None:
            return "❌ Could not find holding!", no_update
        ok, msg = sell_stock(username, record_id, current_price)
        if ok:
            return f"✅ {msg}", 'portfolio'
        return f"❌ {msg}", no_update

    # ══════════════════════════════════════════
    # SECTION 5 — DASHBOARD CHARTS
    # ══════════════════════════════════════════

    @app.callback(
        Output('stats-cards',      'children'),
        Output('price-chart',      'figure'),
        Output('prediction-chart', 'figure'),
        Output('rsi-chart',        'figure'),
        Output('macd-chart',       'figure'),
        Output('volume-chart',     'figure'),
        Output('range-chart',      'figure'),
        Output('yearly-chart',     'figure'),
        Output('date-dropdown',    'options'),
        Output('date-dropdown',    'value'),
        Output('chart1-title',     'children'),
        Output('loading-msg',      'children'),
        Input('stock-dropdown',    'value')
    )
    def update_dashboard_charts(ticker):
        name = STOCKS.get(ticker, ticker)
        try:
            df, r2, mae = get_stock_data(ticker)
        except Exception as e:
            ef = empty_figure()
            return ([], ef, ef, ef, ef, ef, ef, ef,
                    [], None, "Error", f"❌ {str(e)}")

        rsi_now    = round(float(df['RSI'].iloc[-1]), 1)
        rsi_status = ("🔴 Overbought" if rsi_now > 70
                      else ("🟢 Oversold" if rsi_now < 30 else "🟡 Neutral"))

        cards = [
            make_card("Total Days",          str(len(df)),                    '#00d4ff'),
            make_card("R² Accuracy",         f"{r2}%",                       '#00ff88'),
            make_card("Avg Error MAE",        f"${mae}",                      '#ffaa00'),
            make_card("Latest Price",        f"${df['Close'].iloc[-1]:.2f}", '#ff6b6b'),
            make_card(f"RSI ({rsi_status})", str(rsi_now),                   '#cc44ff'),
        ]

        dates  = [{'label': str(d)[:10], 'value': str(d)[:10]}
                  for d in df.index[-100:]]
        latest = str(df.index[-1])[:10]
        title  = f"📊 {name} ({ticker}) — Price History with Moving Averages"

        return (cards,
                build_price_chart(df),
                build_prediction_chart(df),
                build_rsi_chart(df),
                build_macd_chart(df),
                build_volume_chart(df),
                build_range_chart(df),
                build_yearly_chart(df),
                dates, latest, title, "")

    @app.callback(
        Output('prediction-output', 'children'),
        Input('date-dropdown',      'value'),
        Input('stock-dropdown',     'value')
    )
    def show_prediction(date, ticker):
        if not date:
            return ""
        try:
            df, _, _ = get_stock_data(ticker)
            row    = df.loc[date]
            actual = float(row['Close'])
            pred   = float(row['Predicted'])
            rsi    = float(row['RSI'])
            error  = abs(actual - pred)
            sig    = ("🔴 Overbought" if rsi > 70
                      else ("🟢 Oversold" if rsi < 30 else "🟡 Neutral"))
            return [
                html.Span(f"📅 {date}   "),
                html.Span(f"✅ Actual: ${actual:.2f}   "),
                html.Span(f"🤖 Predicted: ${pred:.2f}   "),
                html.Span(f"📏 Error: ${error:.2f}   ",
                          style={'color': '#ffaa00'}),
                html.Span(f"⚡ RSI: {rsi:.1f} ({sig})",
                          style={'color': '#cc44ff'})
            ]
        except Exception as e:
            return f"Date not available: {str(e)}"

    # ══════════════════════════════════════════
    # SECTION 6 — COMPARISON CHARTS
    # ══════════════════════════════════════════

    @app.callback(
        Output('compare-summary',      'children'),
        Output('chart-normalized',     'figure'),
        Output('chart-rsi-compare',    'figure'),
        Output('chart-macd-compare',   'figure'),
        Output('chart-volume-compare', 'figure'),
        Output('chart-correlation',    'figure'),
        Output('compare-status',       'children'),
        Input('btn-compare',           'n_clicks'),
        State('compare-stock1',        'value'),
        State('compare-stock2',        'value'),
        prevent_initial_call=True
    )
    def run_comparison(n, t1, t2):
        ef = empty_compare_figure()

        if not n:
            return [], ef, ef, ef, ef, ef, "Select two stocks and click Compare →"

        if not t1 or not t2:
            return [], ef, ef, ef, ef, ef, "⚠️ Please select both stocks!"

        if t1 == t2:
            return [], ef, ef, ef, ef, ef, "⚠️ Please select two different stocks!"

        try:
            # Download both stocks
            df1, r2_1, mae1 = get_stock_data(t1)
            df2, r2_2, mae2 = get_stock_data(t2)

            name1 = STOCKS.get(t1, t1)
            name2 = STOCKS.get(t2, t2)

            # ── Calculate metrics ─────────────
            # Total return %
            ret1 = round((df1['Close'].iloc[-1] / df1['Close'].iloc[0] - 1) * 100, 1)
            ret2 = round((df2['Close'].iloc[-1] / df2['Close'].iloc[0] - 1) * 100, 1)

            # Daily volatility (std dev of daily % change)
            vol1 = round(float(df1['Close'].pct_change().std() * 100), 2)
            vol2 = round(float(df2['Close'].pct_change().std() * 100), 2)

            # Current RSI
            rsi1 = round(float(df1['RSI'].iloc[-1]), 1)
            rsi2 = round(float(df2['RSI'].iloc[-1]), 1)

            # Current MACD signal
            macd1_bull = float(df1['MACD'].iloc[-1]) > float(df1['MACD_Signal'].iloc[-1])
            macd2_bull = float(df2['MACD'].iloc[-1]) > float(df2['MACD_Signal'].iloc[-1])

            # Correlation
            common = df1.index.intersection(df2.index)
            corr   = round(float(df1.loc[common, 'Close'].corr(
                                  df2.loc[common, 'Close'])), 3)

            # ── Helper: RSI label ─────────────
            def rsi_label(rsi):
                if rsi > 70: return f"{rsi} 🔴"
                if rsi < 30: return f"{rsi} 🟢"
                return f"{rsi} 🟡"

            # ── Correlation strength label ────
            a = abs(corr)
            if a > 0.8:   corr_strength = "Very High"
            elif a > 0.6: corr_strength = "High"
            elif a > 0.4: corr_strength = "Moderate"
            else:         corr_strength = "Low"

            # ── Summary Cards ─────────────────
            def versus_card(title, v1, v2, c1, c2):
                return html.Div([
                    html.P(title,
                           style={'color': '#aaa', 'margin': '0 0 8px 0',
                                  'fontSize': '12px', 'textAlign': 'center'}),
                    html.Div([
                        html.Div([
                            html.P(name1, style={'color': '#00d4ff',
                                                  'margin': '0', 'fontSize': '11px'}),
                            html.H3(str(v1), style={'color': c1,
                                                     'margin': '0', 'fontSize': '17px'})
                        ], style={'flex': '1', 'textAlign': 'center'}),
                        html.Span("vs", style={'color': '#555',
                                               'padding': '0 8px',
                                               'alignSelf': 'center'}),
                        html.Div([
                            html.P(name2, style={'color': '#ffaa00',
                                                  'margin': '0', 'fontSize': '11px'}),
                            html.H3(str(v2), style={'color': c2,
                                                     'margin': '0', 'fontSize': '17px'})
                        ], style={'flex': '1', 'textAlign': 'center'})
                    ], style={'display': 'flex', 'alignItems': 'center'})
                ], style={'backgroundColor': '#16213e', 'padding': '15px',
                          'borderRadius': '10px', 'flex': '1', 'margin': '8px',
                          'minWidth': '180px'})

            rc1 = '#00ff88' if ret1 >= 0 else '#ff6b6b'
            rc2 = '#00ff88' if ret2 >= 0 else '#ff6b6b'

            cards = [
                versus_card("Total Return",
                            f"{ret1:+.1f}%", f"{ret2:+.1f}%", rc1, rc2),
                versus_card("Model R² Accuracy",
                            f"{r2_1}%", f"{r2_2}%",
                            '#00ff88', '#00ff88'),
                versus_card("Daily Volatility",
                            f"{vol1}%", f"{vol2}%",
                            '#ffaa00', '#ffaa00'),
                versus_card("Current RSI",
                            rsi_label(rsi1), rsi_label(rsi2),
                            '#cc44ff', '#cc44ff'),
                versus_card("MACD Momentum",
                            "📈 Bullish" if macd1_bull else "📉 Bearish",
                            "📈 Bullish" if macd2_bull else "📉 Bearish",
                            '#00d4ff', '#00d4ff'),
                versus_card(f"Correlation ({corr_strength})",
                            str(corr), "r-value",
                            '#00ff88', '#aaa'),
            ]

            # ── Build all 5 charts ────────────
            fig_norm  = build_normalized_chart(df1, df2, t1, t2)
            fig_rsi   = build_rsi_comparison(df1, df2, t1, t2)
            fig_macd  = build_macd_comparison(df1, df2, t1, t2)
            fig_vol   = build_volume_comparison(df1, df2, t1, t2)
            fig_corr, _ = build_correlation_chart(df1, df2, t1, t2)

            status = f"✅ Comparing {name1} vs {name2} — {len(common)} common trading days"

            return cards, fig_norm, fig_rsi, fig_macd, fig_vol, fig_corr, status

        except Exception as e:
            ef = empty_compare_figure()
            return [], ef, ef, ef, ef, ef, f"❌ Error: {str(e)}"
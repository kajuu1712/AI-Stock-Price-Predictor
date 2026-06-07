# ============================================
# compare_charts.py
# All chart functions for stock comparison page
# ============================================

import numpy as np
import plotly.graph_objects as go


# ── Chart 1: Normalized Price ─────────────────
# Both stocks start at 100 so we compare % growth
# This is FAIR comparison regardless of actual price
# Example: AAPL at $300 vs TCS at $3000 — normalized shows who grew more %
def build_normalized_chart(df1, df2, t1, t2):
    norm1 = (df1['Close'] / df1['Close'].iloc[0]) * 100
    norm2 = (df2['Close'] / df2['Close'].iloc[0]) * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df1.index, y=norm1, name=t1,
        line=dict(color='#00d4ff', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df2.index, y=norm2, name=t2,
        line=dict(color='#ffaa00', width=2)
    ))
    # Baseline at 100 (starting point)
    fig.add_hline(y=100, line_dash='dot',
                  line_color='#555', line_width=1)
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#16213e',
        plot_bgcolor='#16213e',
        height=420,
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        yaxis_title='Growth Index (Start = 100)',
        margin=dict(l=40, r=40, t=20, b=40)
    )
    return fig


# ── Chart 2: RSI Comparison ───────────────────
# Both RSI lines on same chart
# Shows which stock is more overbought/oversold
def build_rsi_comparison(df1, df2, t1, t2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df1.index, y=df1['RSI'], name=f'{t1} RSI',
        line=dict(color='#00d4ff', width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=df2.index, y=df2['RSI'], name=f'{t2} RSI',
        line=dict(color='#ffaa00', width=1.5)
    ))
    # Overbought line
    fig.add_hline(y=70, line_dash='dash',
                  line_color='#ff6b6b', line_width=1,
                  annotation_text='Overbought (70)',
                  annotation_position='top right',
                  annotation_font_color='#ff6b6b')
    # Oversold line
    fig.add_hline(y=30, line_dash='dash',
                  line_color='#00ff88', line_width=1,
                  annotation_text='Oversold (30)',
                  annotation_position='bottom right',
                  annotation_font_color='#00ff88')
    # Shaded zones
    fig.add_hrect(y0=70, y1=100,
                  fillcolor='rgba(255,107,107,0.05)', line_width=0)
    fig.add_hrect(y0=0, y1=30,
                  fillcolor='rgba(0,255,136,0.05)', line_width=0)
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#16213e',
        plot_bgcolor='#16213e',
        height=380,
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        yaxis=dict(range=[0, 100], title='RSI Value'),
        margin=dict(l=40, r=40, t=20, b=40)
    )
    return fig


# ── Chart 3: MACD Comparison ──────────────────
# Both MACD lines on same chart
# Shows which stock has stronger/better momentum
def build_macd_comparison(df1, df2, t1, t2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df1.index, y=df1['MACD'], name=f'{t1} MACD',
        line=dict(color='#00d4ff', width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=df2.index, y=df2['MACD'], name=f'{t2} MACD',
        line=dict(color='#ffaa00', width=1.5)
    ))
    # Zero line reference
    fig.add_hline(y=0, line_color='#555', line_width=1)
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#16213e',
        plot_bgcolor='#16213e',
        height=380,
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        yaxis_title='MACD Value',
        margin=dict(l=40, r=40, t=20, b=40)
    )
    return fig


# ── Chart 4: Volume Comparison ────────────────
# Both volumes overlaid as bars
# Shows which stock has more trading activity/interest
def build_volume_comparison(df1, df2, t1, t2):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df1.index, y=df1['Volume'], name=t1,
        marker_color='#00d4ff', opacity=0.6,
        marker_line_width=0
    ))
    fig.add_trace(go.Bar(
        x=df2.index, y=df2['Volume'], name=t2,
        marker_color='#ffaa00', opacity=0.6,
        marker_line_width=0
    ))
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#16213e',
        plot_bgcolor='#16213e',
        height=350,
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        barmode='overlay',
        yaxis_title='Volume (shares traded)',
        margin=dict(l=40, r=40, t=20, b=40)
    )
    return fig


# ── Chart 5: Correlation Scatter ──────────────
# Each dot = one trading day
# X = stock1 price, Y = stock2 price
# Dots forming a straight line = high correlation
# Returns (figure, correlation_value)
def build_correlation_chart(df1, df2, t1, t2):
    # Only use dates that exist in BOTH stocks
    common_dates = df1.index.intersection(df2.index)
    s1 = df1.loc[common_dates, 'Close']
    s2 = df2.loc[common_dates, 'Close']

    # Correlation coefficient (-1 to +1)
    corr = round(float(s1.corr(s2)), 3)

    # Trend line using linear regression
    z      = np.polyfit(s1, s2, 1)
    p      = np.poly1d(z)
    x_line = np.linspace(float(s1.min()), float(s1.max()), 100)

    fig = go.Figure()
    # Scatter dots
    fig.add_trace(go.Scatter(
        x=s1, y=s2,
        mode='markers',
        name='Daily prices',
        marker=dict(color='#cc44ff', size=3, opacity=0.4)
    ))
    # Trend line
    fig.add_trace(go.Scatter(
        x=x_line, y=p(x_line),
        mode='lines',
        name=f'Trend line (r = {corr})',
        line=dict(color='#00ff88', width=2.5)
    ))
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#16213e',
        plot_bgcolor='#16213e',
        height=400,
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        xaxis_title=f'{t1} Price ($)',
        yaxis_title=f'{t2} Price ($)',
        margin=dict(l=40, r=40, t=20, b=40)
    )
    return fig, corr


# ── Empty figure (shown before comparison runs) ──
def empty_compare_figure():
    fig = go.Figure()
    fig.add_annotation(
        text="Select two stocks and click Compare",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color='#555')
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#16213e',
        plot_bgcolor='#16213e',
        height=380
    )
    return fig
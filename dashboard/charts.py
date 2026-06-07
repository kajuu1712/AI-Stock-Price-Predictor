# ============================================
# charts.py
# All 7 chart building functions
# ============================================

import plotly.graph_objects as go

def make_card(title, value, color):
    from dash import html
    return html.Div([
        html.H4(title, style={'color':'#aaa','margin':'0','fontSize':'14px'}),
        html.H2(value, style={'color':color, 'margin':'0'})
    ], style={
        'backgroundColor':'#16213e','padding':'20px',
        'borderRadius':'10px','textAlign':'center',
        'flex':'1','margin':'10px'
    })

def build_price_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'],
                             name='Close Price',
                             line=dict(color='#00d4ff', width=1.5)))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA_50'],
                             name='50-Day MA',
                             line=dict(color='#ffaa00', width=2)))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA_200'],
                             name='200-Day MA',
                             line=dict(color='#ff6b6b', width=2)))
    fig.update_layout(template='plotly_dark', paper_bgcolor='#16213e',
                      plot_bgcolor='#16213e', height=420,
                      legend=dict(bgcolor='rgba(0,0,0,0)'),
                      margin=dict(l=40,r=40,t=20,b=40))
    return fig

def build_prediction_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'],
                             name='Actual Price',
                             line=dict(color='#00d4ff', width=1.5)))
    fig.add_trace(go.Scatter(x=df.index, y=df['Predicted'],
                             name='Predicted Price',
                             line=dict(color='#ff6b6b', width=1.5, dash='dash')))
    fig.update_layout(template='plotly_dark', paper_bgcolor='#16213e',
                      plot_bgcolor='#16213e', height=420,
                      legend=dict(bgcolor='rgba(0,0,0,0)'),
                      margin=dict(l=40,r=40,t=20,b=40))
    return fig

def build_rsi_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'],
                             name='RSI',
                             line=dict(color='#cc44ff', width=1.5)))
    fig.add_hline(y=70, line_dash='dash', line_color='#ff6b6b', line_width=1.5,
                  annotation_text='Overbought (70)',
                  annotation_position='top right',
                  annotation_font_color='#ff6b6b')
    fig.add_hline(y=30, line_dash='dash', line_color='#00ff88', line_width=1.5,
                  annotation_text='Oversold (30)',
                  annotation_position='bottom right',
                  annotation_font_color='#00ff88')
    fig.add_hline(y=50, line_dash='dot', line_color='#555555', line_width=1)
    fig.add_hrect(y0=70, y1=100, fillcolor='rgba(255,107,107,0.08)', line_width=0)
    fig.add_hrect(y0=0,  y1=30,  fillcolor='rgba(0,255,136,0.08)',   line_width=0)
    fig.update_layout(template='plotly_dark', paper_bgcolor='#16213e',
                      plot_bgcolor='#16213e', height=350,
                      yaxis=dict(range=[0,100], title='RSI Value'),
                      margin=dict(l=40,r=40,t=20,b=40))
    return fig

def build_macd_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD'],
                             name='MACD Line',
                             line=dict(color='#00d4ff', width=1.5)))
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'],
                             name='Signal Line',
                             line=dict(color='#ffaa00', width=1.5)))
    colors = ['#00ff88' if v >= 0 else '#ff6b6b' for v in df['MACD_Hist']]
    fig.add_trace(go.Bar(x=df.index, y=df['MACD_Hist'],
                         name='Histogram',
                         marker_color=colors,
                         opacity=0.6, marker_line_width=0))
    fig.add_hline(y=0, line_color='#555', line_width=1)
    fig.update_layout(template='plotly_dark', paper_bgcolor='#16213e',
                      plot_bgcolor='#16213e', height=380,
                      legend=dict(bgcolor='rgba(0,0,0,0)'),
                      barmode='relative',
                      margin=dict(l=40,r=40,t=20,b=40))
    return fig

def build_volume_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'],
                         name='Volume',
                         marker_color='#00d4ff',
                         opacity=0.8, marker_line_width=0))
    fig.update_layout(template='plotly_dark', paper_bgcolor='#16213e',
                      plot_bgcolor='#16213e', height=350,
                      margin=dict(l=40,r=40,t=20,b=40))
    return fig

def build_range_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Daily_Range'],
                             name='Daily Range',
                             line=dict(color='#cc44ff', width=1),
                             fill='tozeroy',
                             fillcolor='rgba(204,68,255,0.1)'))
    fig.update_layout(template='plotly_dark', paper_bgcolor='#16213e',
                      plot_bgcolor='#16213e', height=350,
                      margin=dict(l=40,r=40,t=20,b=40))
    return fig

def build_yearly_chart(df):
    fig = go.Figure()
    for year in sorted(df['Year'].unique()):
        yd = df[df['Year'] == year]['Close']
        fig.add_trace(go.Box(y=yd, name=str(year),
                             marker_color='#00d4ff',
                             line_color='#00d4ff',
                             fillcolor='rgba(0,212,255,0.15)'))
    fig.update_layout(template='plotly_dark', paper_bgcolor='#16213e',
                      plot_bgcolor='#16213e', height=420,
                      showlegend=False,
                      margin=dict(l=40,r=40,t=20,b=40))
    return fig

def empty_figure():
    fig = go.Figure()
    fig.update_layout(template='plotly_dark',
                      paper_bgcolor='#16213e',
                      plot_bgcolor='#16213e')
    return fig


# ════════════════════════════════════════════
# COMPARISON CHARTS (Priority 2)
# ════════════════════════════════════════════

def build_normalized_price_chart(df1, df2, ticker1, ticker2):
    """
    Normalized price chart — both stocks on 0-100 scale
    so they can be compared fairly regardless of price difference
    AAPL at $300 vs RELIANCE at $1200 — normalized shows % growth
    """
    import numpy as np

    # Normalize: start both at 100 so we compare % growth not raw price
    norm1 = (df1['Close'] / df1['Close'].iloc[0]) * 100
    norm2 = (df2['Close'] / df2['Close'].iloc[0]) * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df1.index, y=norm1,
        name=ticker1,
        line=dict(color='#00d4ff', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df2.index, y=norm2,
        name=ticker2,
        line=dict(color='#ffaa00', width=2)
    ))
    fig.add_hline(y=100, line_dash='dot', line_color='#555', line_width=1)
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e',
        plot_bgcolor='#16213e', height=420,
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        yaxis_title='Growth (Base = 100)',
        margin=dict(l=40,r=40,t=20,b=40)
    )
    return fig


def build_rsi_comparison_chart(df1, df2, ticker1, ticker2):
    """
    RSI of both stocks on same chart
    Shows which stock is more overbought/oversold
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df1.index, y=df1['RSI'],
        name=f'{ticker1} RSI',
        line=dict(color='#00d4ff', width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=df2.index, y=df2['RSI'],
        name=f'{ticker2} RSI',
        line=dict(color='#ffaa00', width=1.5)
    ))
    fig.add_hline(y=70, line_dash='dash', line_color='#ff6b6b', line_width=1,
                  annotation_text='Overbought (70)',
                  annotation_position='top right',
                  annotation_font_color='#ff6b6b')
    fig.add_hline(y=30, line_dash='dash', line_color='#00ff88', line_width=1,
                  annotation_text='Oversold (30)',
                  annotation_position='bottom right',
                  annotation_font_color='#00ff88')
    fig.add_hrect(y0=70, y1=100, fillcolor='rgba(255,107,107,0.05)', line_width=0)
    fig.add_hrect(y0=0,  y1=30,  fillcolor='rgba(0,255,136,0.05)',   line_width=0)
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e',
        plot_bgcolor='#16213e', height=380,
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        yaxis=dict(range=[0,100], title='RSI Value'),
        margin=dict(l=40,r=40,t=20,b=40)
    )
    return fig


def build_macd_comparison_chart(df1, df2, ticker1, ticker2):
    """
    MACD lines of both stocks overlaid
    Shows which has stronger momentum
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df1.index, y=df1['MACD'],
        name=f'{ticker1} MACD',
        line=dict(color='#00d4ff', width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=df2.index, y=df2['MACD'],
        name=f'{ticker2} MACD',
        line=dict(color='#ffaa00', width=1.5)
    ))
    fig.add_hline(y=0, line_color='#555', line_width=1)
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e',
        plot_bgcolor='#16213e', height=380,
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        yaxis_title='MACD Value',
        margin=dict(l=40,r=40,t=20,b=40)
    )
    return fig


def build_volume_comparison_chart(df1, df2, ticker1, ticker2):
    """
    Volume of both stocks side by side
    Shows which stock has more trading interest
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df1.index, y=df1['Volume'],
        name=ticker1,
        marker_color='#00d4ff',
        opacity=0.7
    ))
    fig.add_trace(go.Bar(
        x=df2.index, y=df2['Volume'],
        name=ticker2,
        marker_color='#ffaa00',
        opacity=0.7
    ))
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e',
        plot_bgcolor='#16213e', height=350,
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        barmode='overlay',
        margin=dict(l=40,r=40,t=20,b=40)
    )
    return fig


def build_correlation_chart(df1, df2, ticker1, ticker2):
    """
    Scatter plot showing correlation between two stocks
    Each point = one trading day
    X axis = stock1 price, Y axis = stock2 price
    If points form a straight line = high correlation
    """
    import numpy as np

    # Align both dataframes on common dates
    common = df1.index.intersection(df2.index)
    s1 = df1.loc[common, 'Close']
    s2 = df2.loc[common, 'Close']

    # Calculate correlation coefficient
    corr = round(float(s1.corr(s2)), 3)

    # Trend line
    z    = np.polyfit(s1, s2, 1)
    p    = np.poly1d(z)
    x_line = np.linspace(s1.min(), s1.max(), 100)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=s1, y=s2,
        mode='markers',
        name='Daily prices',
        marker=dict(color='#cc44ff', size=3, opacity=0.5)
    ))
    fig.add_trace(go.Scatter(
        x=x_line, y=p(x_line),
        mode='lines',
        name=f'Trend (r={corr})',
        line=dict(color='#00ff88', width=2)
    ))
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e',
        plot_bgcolor='#16213e', height=400,
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        xaxis_title=f'{ticker1} Price ($)',
        yaxis_title=f'{ticker2} Price ($)',
        margin=dict(l=40,r=40,t=20,b=40)
    )
    return fig, corr
import dash
import dash_table
import pandas as pd
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table.FormatTemplate as ft
from dash_table.Format import Sign
import dash_core_components as dcc
# from Database.data_puller.Data import Factor, Data

import numpy as np

FILE_BASE = '/home/cso/Downloads/'

# file_name='Dashboard_template.xlsx'
file_name = 'dashboard.csv'

# df = pd.read_excel('%s%s' %(FILE_BASE,file_name),sheet_name='Sheet1')
df = pd.read_csv('%s%s' % (FILE_BASE, file_name))
unique_bse_code = df['BSE Code'].unique().tolist()

# todo to be resolved in next commit
# db = Data()
# close_df = db.get_stocks_v2(by=Factor.BSE_CODE, factor=Factor.CLOSE, table=Factor.DATA_ADJUSTED_QUANT, stocks=unique_bse_code, frequency=Factor.DAILY, start=dt.date(2018, 1, 1))
close_df = pd.DataFrame()

for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='ignore')

col_order = ['BSE Code']

col_mapping = {'3Return': '3M Returns',
               '3Rank': '3M Rank',
               '9Return': '9M Returns',
               '9Rank': '9M Rank',
               '18Return': '18M Returns',
               '18Rank': '18M Rank',
               '12 Beta': 'Beta',
               '12 Beta rank': 'Beta Rank',
               'universe': 'Universe',
               'catagory': 'Catagory'
               }

# df.rename(columns=col_mapping,inplace=True)

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        # id='datatable-filtering-fe',
        id='datatable-interactivity',
        style_header={'backgroungColor': 'white', 'fontWeight': 'bold', 'border': '1px solid black', 'width': 'auto', 'whiteSpace': 'normal', 'textAlign': 'center'},
        style_data={'whiteSpace': 'normal', 'height': 'auto'},
        style_cell={'textAlign': 'left'},
        # style_data={'whiteSpace':'normal'},
        columns=[
            {"name": 'Stock Name', "id": 'stock_name', "deletable": True},
            {"name": 'My Picks', "id": 'Strategy', "deletable": True},
            {"name": 'Universe', "id": 'universe', "deletable": True},
            {"name": 'Catagory', "id": 'catagory', "deletable": True},
            {"name": 'Sector', "id": 'Sector', "deletable": True},
            {"name": 'My Rank', "id": 'My Rank', "deletable": True},
            {"name": 'Intrinsic rank', "id": 'Intrinsic_rank', "deletable": True},

            {"name": 'Std. Above 150 DMA', "id": 'STD', "deletable": True, 'type': 'numeric', 'format': ft.Format(precision=2)},

            {"name": 'Beta', "id": '12 Beta', "deletable": True, 'type': 'numeric', 'format': ft.Format(precision=2)},
            {"name": 'Beta Rank', "id": '12 Beta Rank', "deletable": True},

            {"name": '3M Returns', "id": '3Return', "deletable": True, 'type': 'numeric', 'format': ft.percentage(1).sign(Sign.positive)},
            {"name": '3M Rank', "id": '3Rank', "deletable": True},

            {"name": '9M Returns', "id": '9Return', "deletable": True, 'type': 'numeric', 'format': ft.percentage(1).sign(Sign.positive)},
            {"name": '9M Rank', "id": '9Rank', "deletable": True},

            {"name": '18M Returns', "id": '18Return', "deletable": True, 'type': 'numeric', 'format': ft.percentage(1).sign(Sign.positive)},
            {"name": '18M Rank', "id": '18Rank', "deletable": True},

        ],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        page_action="native",
        selected_rows=[],
        style_data_conditional=[
            {
                'if': {
                    'column_id': '3Return',
                    'filter_query': '{3Return} gt 0'
                },
                'backgroundColor': '#03d376',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': '3Return',
                    'filter_query': '{3Return} lt 0'
                },
                'backgroundColor': '#ff5500',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': 'STD',
                    'filter_query': '{STD} gt 0'
                },
                'backgroundColor': '#03d376',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': 'STD',
                    'filter_query': '{STD} lt 0'
                },
                'backgroundColor': '#ff5500',
                'color': 'white',
            },
        ]
    ),

    dcc.Graph(
        id='graph',
        config={
            'showSendToCloud': True,
            'plotlyServerURL': 'https://plot.ly'
        }
    ),

    # html.Div(id='datatable-filter-container')
    html.Div(id='datatable-interactivity-container'),

])

'''
@app.callback(
    Output('datatable-filter-container', "children"),
    [Input('datatable-filtering-fe', "data")])
def update_graph(rows):
    if rows is None:
        dff = df
    else:
        dff = pd.DataFrame(rows)

    return html.Div()
'''


@app.callback(
    # Output('datatable-interactivity-container', "children"),
    Output('graph', 'figure'),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_output(rows, derived_virtual_selected_rows):
    if rows is not None and len(rows) > 0:
        title = rows[0]['stock_name']
        bse_code = rows[0]['BSE Code']
        buy_date = rows[0]['Buy_date']
        # print('here')
        # print(rows)
    else:
        title = 'title'
        bse_code = ''
        buy_date = None
        trade_data = None

    if bse_code:
        price_data = close_df[bse_code].values.tolist()
        MA1 = close_df[bse_code].rolling(70).mean().values.tolist()
        MA2 = close_df[bse_code].rolling(150).mean().values.tolist()
        date_list = close_df.index.tolist()
        if buy_date is not None:
            trade_data = close_df[bse_code].loc[buy_date:].values.tolist()
            trade_data = [np.nan] * (len(price_data) - len(trade_data)) + trade_data
    else:
        price_data = list(range(10))
        date_list = list(range(10))
        MA1 = list(range(10))
        MA2 = list(range(10))
        # print('b')
        # print(price_data)
        # print(date_list)
        # print(rows)

    # print('price data')
    # print(price_data)
    if buy_date is not None:
        return {
            'data': [{
                'type': 'scatter',
                'name': 'Close Price',
                'x': date_list,
                'y': price_data
            },
                {
                    'type': 'scatter',
                    'name': '70 DMA',
                    'x': date_list,
                    'y': MA1
                },
                {
                    'type': 'scatter',
                    'name': '150 DMA',
                    'x': date_list,
                    'y': MA2
                },
                {
                    'type': 'scatter',
                    'name': 'Trade',
                    'x': date_list,
                    'y': trade_data
                },

            ],
            'layout': {
                'title': title
            }
        }

    else:
        return {
            'data': [{
                'type': 'scatter',
                'name': 'Close Price',
                'x': date_list,
                'y': price_data
            },
                {
                    'type': 'scatter',
                    'name': '70 DMA',
                    'x': date_list,
                    'y': MA1
                },
                {
                    'type': 'scatter',
                    'name': '150 DMA',
                    'x': date_list,
                    'y': MA2
                },

            ],
            'layout': {
                'title': title
            }
        }


'''
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize

    print('Code')
    if rows is not None:
        print(rows[0]['BSE Code'])

    print('ROWS')
    print(rows)
    print('V ROWS')
    print(derived_virtual_selected_rows)

    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    print('here')
    print(dff)
    print(dff.columns)

    if rows is not None:
        colors = ['#7FDBFF' if i in rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id='graph',
            figure={
                "data": [
                    {
                        "x": 'X',
                        "y": 100,
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": 'Test'}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )

        for column in ["pop", "lifeExp", "gdpPercap"] if column in dff
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        # for column in ["Stock_name"] if column in dff
        # for column in ["Stock_name"] if True
    ]
'''

# app.layout = dash_table.DataTable(
#     id='table',
#     columns=[{"name": i, "id": i} for i in df.columns],
#     data=df.to_dict('records'),
#     style_data_conditional=[
#         {
#             'if': {
#                 'column_id': 'Moving Averages',
#                 'filter_query': '{Moving Averages} eq "Bullish"'
#             },
#             'backgroundColor': '#3D9970',
#             'color': 'white',
#         },]
#
# )


if __name__ == '__main__':
    # app.run_server(debug=False)
    app.run_server(debug=True, host='0.0.0.0', port=8080)

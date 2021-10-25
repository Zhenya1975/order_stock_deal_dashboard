import datetime

import dash_bootstrap_components as dbc
import dash
from dash import html, dcc
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import csv
import os

app = dash.Dash(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])

makers = [{'label': "John Deere", 'value': "John Deere"},
           {'label': "JCB", 'value': "JCB"},
           {'label': "Kuhn", 'value': "KUHN"},]

product_groups = [{'label': " Тракторы", 'value': "TR"},
                  {'label': " З/У комбайны", 'value': "HARV"},
                  {'label': " Прицепное оборудование", 'value': "TL"},
                  {'label': " Опрыскиватели", 'value': "SPR"},
                  {'label': " Погрузчики", 'value': "LDR"},]



# df_calendar = pd.read_csv('data/calendar.csv')
# df_calendar['date'] =  pd.to_datetime(df_calendar['date'], infer_datetime_format=True)
# format = "%Y-%m-%d"
#print("типа даты в календаре ", type(df_calendar['date'][0]))
#print(df_calendar['date'][0])

card_content1 = [
    dbc.CardHeader("Факт заказов, ед  *"),
    dbc.CardBody([html.P("1 438 ед", className="card-title"),
                  #html.P("План: 1 653 ед"),
                  html.P("По состоянию на 18.10.2021",className="card-text"),]
                 ),]


body = html.Div([
    dbc.Container([

        # Заголовок Дашшборда
        html.Div(style={'padding-left': '15px', 'padding-right': '20px', 'padding-top': '5px', 'padding-bottom': '5px', 'color': 'white'},
                 children=[
                     html.H2('ЗАКАЗЫ У ПОСТАВЩИКА - СКЛАД ДИЛЕРА - СДЕЛКИ')
                 ]
                 ),
        dbc.Row([
            dbc.Col(width=3,
                children=[
                    html.Div(style={'padding-left': '30px', 'padding-right': '20px', 'margin-top': '10px', 'color': 'white'},
                             children=[
                                 html.P(),
                                 html.B('Бренды'),
                                 html.P(),
                                 dcc.Checklist(
                                        id="all-or-none-brands",
                                        options=[{"label": " Выбрать все", "value": "All"}],
                                        value=["All"],
                                        labelStyle={"display": "inline-block"},
                                    ),
                                 dcc.Checklist(id='maker_selector',
                                               options=makers,
                                               labelStyle = dict(display='block')),

                                 html.P(),
                                 html.B('Товарные группы'),
                                 html.P(),
                                 dcc.Checklist(
                                        id="all-or-none",
                                        options=[{"label": " Выбрать все", "value": "All"}],
                                        value=["All"],
                                        labelStyle={"display": "inline-block"},
                                    ),
                                 dcc.Checklist(id='product_group_selector_checklist',
                                               options=product_groups,
                                               labelStyle = dict(display='block')),

                                 # dcc.Dropdown(id='product_group_selector',
                                 #              options= product_groups,
                                 #                      #options=get_options(df_order_fact_2021['product_group_Top_Code'].unique()),
                                 #                      multi=True,
                                 #                      value=df_order_fact_2021['product_group_Top_Code'].unique()
                                 #                      ),
                                html.Hr(),
                             ]
                             ),
                ]),
            dbc.Col(width=9,
                children=[
                    html.P(),
                    html.Div(style={'padding-left': '30px', 'padding-right': '20px', 'padding-top': '10px'},
                                 children=[
                                    dbc.Row([
                                            dbc.Col(dbc.Card(card_content1, color="dark", inverse=True)),
                                            dbc.Col(dbc.Card(card_content1, color="dark", inverse=True)),
                                            dbc.Col(dbc.Card(card_content1, color="dark", inverse=True)),
                                                ],
                                                className="mb-4",
                                            ),

                                     dcc.Graph(id='orders_stock_deals', config={'displayModeBar': False}),
                                     html.P(),
                                     #dcc.Graph(id='orders_stock_deals_bars', config={'displayModeBar': False}),

                                 ]),
                    # html.Div(style={'padding-left': '30px', 'padding-right': '20px', 'padding-top': '10px'},
                    #              children=[
                    #                  html.Div(style={'color': 'white', 'textAlign': 'center'},
                    #                           children=[
                    #                               html.P('План-факт заказов по кварталам 2021')
                    #                           ]),
                    #                  dbc.Row([
                    #                      dbc.Col(width=3, children=[html.Div(dcc.Graph(id = "orders_q4"))]),
                    #                      dbc.Col(width=3, children=[html.Div(dcc.Graph(id = "orders_q3"))]),
                    #                      dbc.Col(width=3, children=[html.Div(dcc.Graph(id = "orders_q2"))]),
                    #                      dbc.Col(width=3, children=[html.Div(dcc.Graph(id = "orders_q1"))]),
                    # ],
                    # justify="between",)
                    #
                    #              ]),


                    ])

        ])

    ], fluid=True, style={'background-color': '#19202A',"height": "150vh"},)
])


# передаем разметку страницы в приложение
app.layout = html.Div([body])

@app.callback(Output("maker_selector", "value"),
              [Input("all-or-none-brands", "value")],
              [State("maker_selector", "options")],
)
def select_all_none(all_selected, options):
    #all_or_none = []
    all_or_none = [option["value"] for option in options if all_selected]
    return all_or_none

@app.callback(Output("product_group_selector_checklist", "value"),
              [Input("all-or-none", "value")],
              [State("product_group_selector_checklist", "options")],
)
def select_all_none(all_selected, options):
    #all_or_none = []
    all_or_none = [option["value"] for option in options if all_selected]
    return all_or_none

orders_delivery_df = pd.read_csv('data/orders_delivery_df.csv')
dealer_stockin_stockout_df = pd.read_csv('data/dealer_stockin_stockout.csv')
@app.callback(Output('orders_stock_deals', 'figure'),
              [Input('maker_selector', 'value'),
               Input('product_group_selector_checklist', 'value'),
               ])
def order_plan_fact(selected_maker, selected_product_groups):
    df_orders_filtered_by_inputs = orders_delivery_df[orders_delivery_df['product_group_code'].isin(selected_product_groups) &
                                                    orders_delivery_df['action_type'].isin(['order', 'delivery']) &
                                                    orders_delivery_df['manufacturer'].isin(selected_maker) |
                                                    orders_delivery_df['action_type'].isin(['empty'])]

    df_orders_filtered_by_inputs.to_csv('data/temp1.csv')
    df_graph_orders = pd.read_csv('data/temp1.csv')
    os.remove('data/temp1.csv')
    #df_graph_orders['date'] = pd.to_datetime(df_graph_orders['date'], infer_datetime_format=True).date()
    #df_graph_orders.to_csv('data/temp_df_graph_orders.csv')
    #df_graph_orders = df_graph_orders[df_graph_orders['date'] <= datetime.datetime.now()]

    df_graph_orders['cumsum'] = df_graph_orders['qty'].cumsum()
    df_graph_orders_data = df_graph_orders[['date', 'cumsum']]
    df_graph_orders_groupped = df_graph_orders_data.groupby('date').tail(1)
    df_graph_orders_groupped.to_csv('data/temp.csv')
    df_graph_orders_groupped = pd.read_csv('data/temp.csv')
    os.remove('data/temp.csv')
    print("df_graph_orders_groupped['date'][0]", df_graph_orders_groupped['date'][0], type(df_graph_orders_groupped['date'][0]))
    exists = '2020-01-01' in df_graph_orders_groupped['date']
    print(exists)
    calendar_df = pd.read_csv('data/calendar.csv')
    # for index_cal, row_cal in calendar_df.iterrows():
    #     print(row_cal['date'])



    #df_graph_orders_groupped['date'] = pd.to_datetime(df_graph_orders_groupped.loc[:, 'date']).dt.date
    #print(df_graph_orders_groupped['date'])
    #df_graph_orders_groupped_2021 = df_graph_orders_groupped[df_graph_orders_groupped['date'] >= datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")]
    #df_graph_orders_groupped_2021 = df_graph_orders_groupped.loc[:, df_graph_orders_groupped['date'] >= datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")]
    #df_graph_orders_groupped.to_csv('data/df_graph_orders_data_groupped.csv')
    # теперь надо заполнять пустые даты.

    #calendar_df['date'] = pd.to_datetime(calendar_df['date'], infer_datetime_format=True)
    #calendar_df['date'] = pd.to_datetime(calendar_df['date']).dt.date

    #print('calendar_df', calendar_df['date'][0], type(calendar_df['date'][0]))
    # надо получить лист уникальных дат в датафрейме действий


    start_date_orders = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    end_date_orders = datetime.datetime.now()
    after_start_date_orders = df_graph_orders_groupped["date"] >= start_date_orders
    before_end_date_orders = df_graph_orders_groupped["date"] <= end_date_orders
    between_two_dates = after_start_date_orders & before_end_date_orders
    df_graph_orders_groupped_2021 = df_graph_orders_groupped.loc[between_two_dates]

    ########## готовим данные для ряда Ожидаемые поставки
    df_expected_orders = df_graph_orders_groupped
    start_date_orders = datetime.datetime.now()
    end_date_orders = df_expected_orders['date'].max()
    after_start_date_orders = df_expected_orders["date"] >= start_date_orders
    before_end_date_orders = df_expected_orders["date"] <= end_date_orders
    between_two_dates = after_start_date_orders & before_end_date_orders
    df_expected_orders_2021 = df_expected_orders.loc[between_two_dates]

    # Данные для ряда STOCK
    df_stock_filtered_by_inputs = dealer_stockin_stockout_df[dealer_stockin_stockout_df['product_group_code'].isin(selected_product_groups) &
        dealer_stockin_stockout_df['action_type'].isin(['stock_in', 'stock_out']) &
        dealer_stockin_stockout_df['manufacturer'].isin(selected_maker) |
        dealer_stockin_stockout_df['action_type'].isin(['empty'])]
    #df_stock_filtered_by_inputs.to_csv('data/temp_df_stock_filtered_by_inputs.csv')
    #df_graph_dealer_stock = pd.read_csv('data/temp_df_stock_filtered_by_inputs.csv', parse_dates=['date'])
    #os.remove('data/temp_df_stock_filtered_by_inputs.csv')
    #df_graph_dealer_stock['date'] = pd.to_datetime(df_graph_dealer_stock['date'], infer_datetime_format=True)



    #df_graph_dealer_stock.to_csv('data/temp_df_graph_dealer_stock.csv')
    #df_graph_dealer_stock['cumsum'] = df_graph_dealer_stock['qty'].cumsum()
    #df_graph_dealer_stock.to_csv('data/temp_df_graph_dealer_stock_cumsum.csv')

    #df_graph_dealer_stock_groupped = df_graph_dealer_stock.groupby('date').tail(1)
    #df_graph_dealer_stock_groupped.to_csv('data/temp_df_graph_dealer_stock_groupped.csv')
    #df_graph_dealer_stock_groupped_2021 = df_graph_dealer_stock_groupped[df_graph_dealer_stock_groupped['date'] >= datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")]
    # start_date = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    # end_date = datetime.datetime.now()
    # after_start_date = df_graph_dealer_stock_groupped["date"] >= start_date
    # before_end_date = df_graph_dealer_stock_groupped["date"] <= end_date
    # between_two_dates = after_start_date & before_end_date
    # df_graph_dealer_stock_groupped_2021 = df_graph_dealer_stock_groupped.loc[between_two_dates]
    #df_graph_dealer_stock_groupped_2021.to_csv('data/df_graph_dealer_stock_groupped_2021.csv')

    ########## готовим данные для ряда Ожидаемые поставки




    # df_graph_expected_delivery['date'] = pd.to_datetime(df_graph_expected_delivery['date'], infer_datetime_format=True)
    # df_graph_expected_delivery = df_graph_expected_delivery[df_graph_expected_delivery['date'] >= datetime.datetime.now()]
    # #df_graph_expected_delivery.to_csv('data/df_graph_expected_delivery_raw.csv')
    # df_graph_expected_delivery['qty'] = df_graph_expected_delivery['qty'] * -1
    # df_graph_expected_delivery_groupped = df_graph_expected_delivery.groupby('date').agg(qty = ('qty', pd.Series.sum)).sort_values('date').reset_index()

    #df_graph_expected_delivery_groupped.to_csv('data/df_graph_expected_delivery_groupped.csv')

    #  Считаем максимальную высоту по Y
    #df_graph_dealer_stock_groupped_2021_maxY = df_graph_dealer_stock_groupped_2021['cumsum'].max()
    #df_graph_orders_groupped_2021_maxY = df_graph_orders_groupped_2021['cumsum'].max()
    #maxY = df_graph_dealer_stock_groupped_2021_maxY + df_graph_orders_groupped_2021_maxY
    #print('df_graph_dealer_stock_groupped_2021_maxY', df_graph_dealer_stock_groupped_2021_maxY, 'df_graph_orders_groupped_2021_maxY', df_graph_orders_groupped_2021_maxY, "maxY", maxY)

    fig = go.Figure()
    # Ожидаемые поставки у поставщика
    # fig.add_trace(go.Bar(
    #     x=df_expected_orders_2021['date'],
    #     y=df_expected_orders_2021['cumsum'],
    #     # fill='tozeroy',
    #     name='Ожидаемые поставки',
    # ))
    # Заказы у поставщика
    fig.add_trace(go.Scatter(
        x=df_graph_orders_groupped_2021['date'],
        y = df_graph_orders_groupped_2021['cumsum'],
        #fill='tozeroy',
        name='В заказах у поставщика',
        hoverinfo='x+y',
        stackgroup='one',
    ))



    # Склад ДИЛЕРА
    # fig.add_trace(go.Scatter(
    #     x=df_graph_dealer_stock_groupped_2021['date'],
    #     y=df_graph_dealer_stock_groupped_2021['cumsum'],
    #     # fill='tozeroy',
    #     name='Склад дилера',
    #     hoverinfo='x+y',
    #     stackgroup='one'
    # ))

    # fig.add_trace(go.Scatter(
    #     x=df_graph_expected_delivery_groupped['date'],
    #     y=df_graph_expected_delivery_groupped['qty'],
    #     # fill='tozeroy',
    #     name='Ожидаемые поставки',
    #     # hoverinfo='x+y',
    #
    # ))

    date_range_min = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    date_range_max = df_graph_orders['date'].max()

    fig.update_xaxes(rangeslider_visible=True,)

    fig.update_layout(template='plotly_dark',
                      xaxis={'range': [date_range_min, date_range_max]},
                      #yaxis_range=[0, int(order_plan_2021 * 1.5)],
                      #yaxis_range=[0, maxY*1.3],
                      hovermode = "closest",
                      yaxis_title="Кол-во единиц",

                      #xaxis_title='Дата заказа',
                      # legend_title="Legend Title",
                      title={'text': 'Техника в заказах, на складах и сделках, ед', 'font': {'color': 'white'}, 'x': 0.5},
                      )

    return fig

if __name__ == "__main__":
    app.run_server(debug = True)
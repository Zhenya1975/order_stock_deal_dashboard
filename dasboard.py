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


card_orders_ = [
    dbc.CardHeader("Оборудование в заказах, ед  *"),
    dbc.CardBody([html.P(className="card-title", id = 'card_orders_today_value'),
                  #html.P("План: 1 653 ед"),
                  #html.P(className="card-text", id = 'card_orders_today_date'),
                  ]
                 ),]

card_stock = [
    dbc.CardHeader("Оборудование на складах, ед  *"),
    dbc.CardBody([html.P(className="card-title", id = 'card_stock_today_value'),
                  ]
                 ),]
card_deals = [
    dbc.CardHeader("Оборудование в сделках, ед  *"),
    dbc.CardBody([html.P(className="card-title", id = 'card_deals_today_value'),
                  ]
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
                                            dbc.Col(dbc.Card(card_orders_, color="dark", inverse=True)),
                                            dbc.Col(dbc.Card(card_stock, color="dark", inverse=True)),
                                            dbc.Col(dbc.Card(card_deals, color="dark", inverse=True)),
                                                ],
                                                #className="mb-4",
                                            ),
                                     html.P(className="card-text", id = 'card_orders_today_date'),
                                     html.P(),
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
@app.callback([Output('orders_stock_deals', 'figure'),
               Output('card_orders_today_value', 'children'),
               Output('card_orders_today_date', 'children'),
               Output('card_stock_today_value', 'children'),
               Output('card_deals_today_value', 'children'),
               ],
              [Input('maker_selector', 'value'),
               Input('product_group_selector_checklist', 'value'),
               ])
def orders_stock(selected_maker, selected_product_groups):
    df_orders_filtered_by_inputs = orders_delivery_df[orders_delivery_df['product_group_code'].isin(selected_product_groups) &
                                                    orders_delivery_df['action_type'].isin(['order', 'delivery']) &
                                                    orders_delivery_df['manufacturer'].isin(selected_maker) |
                                                    orders_delivery_df['action_type'].isin(['empty'])]

    df_orders_filtered_by_inputs.to_csv('data/temp1.csv')
    df_graph_orders = pd.read_csv('data/temp1.csv')
    #os.remove('data/temp1.csv')
    #df_graph_orders['date'] = pd.to_datetime(df_graph_orders['date'], infer_datetime_format=True).date()
    #df_graph_orders.to_csv('data/temp_df_graph_orders.csv')
    #df_graph_orders = df_graph_orders[df_graph_orders['date'] <= datetime.datetime.now()]

    df_graph_orders['cumsum'] = df_graph_orders['qty'].cumsum()
    df_graph_orders_data = df_graph_orders[['date', 'cumsum']]
    df_graph_orders_groupped = df_graph_orders_data.groupby('date').tail(1)
    df_graph_orders_groupped.to_csv('data/temp.csv')
    df_graph_orders_groupped = pd.read_csv('data/temp.csv')
    df_graph_orders_groupped['date'] = pd.to_datetime(df_graph_orders_groupped['date'], infer_datetime_format=True)
    os.remove('data/temp.csv')
    start_date_orders = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    end_date_orders = datetime.datetime.now()
    after_start_date_orders = df_graph_orders_groupped["date"] >= start_date_orders
    before_end_date_orders = df_graph_orders_groupped["date"] <= end_date_orders
    between_two_dates = after_start_date_orders & before_end_date_orders
    df_graph_orders_groupped_2021 = df_graph_orders_groupped.loc[between_two_dates]
    today = datetime.datetime.now()
    today_str = today.strftime("%Y-%m-%d")

    today_df = df_graph_orders_groupped_2021[df_graph_orders_groupped_2021['date'] == today_str]
    orders_qty_today = today_df.iloc[0]['cumsum']
    #df_graph_orders_groupped_2021.to_csv('data/temp_df_graph_orders_groupped_2021_to_delete.csv')


    # данные для ряда Сделки
    df_deals = pd.read_csv('data/df_deals.csv')
    df_deals_filtered_by_inputs = df_deals[
        df_deals['product_group_code'].isin(selected_product_groups) &
        df_deals['manufacturer'].isin(selected_maker)
        ]
    df_deals_filtered_by_inputs = df_deals_filtered_by_inputs[['date', 'qty']]
    df_deals_groupped = df_deals_filtered_by_inputs.groupby('date', as_index=False)["qty"].sum()
    df_deals_groupped.to_csv('data/df_deals_groupped.csv')

    ########## готовим данные для ряда Ожидаемые поставки
    df_expected_orders = df_graph_orders_groupped
    start_date_orders = datetime.datetime.now()
    end_date_orders = df_expected_orders['date'].max()
    after_start_date_orders = df_expected_orders["date"] >= start_date_orders
    before_end_date_orders = df_expected_orders["date"] <= end_date_orders
    between_two_dates = after_start_date_orders & before_end_date_orders
    df_expected_orders_2021 = df_expected_orders.loc[between_two_dates]
    df_expected_orders_2021 = df_expected_orders_2021[df_expected_orders_2021['cumsum']>0]


    # Данные для ряда STOCK
    df_stock_filtered_by_inputs = dealer_stockin_stockout_df[dealer_stockin_stockout_df['product_group_code'].isin(selected_product_groups) &
        dealer_stockin_stockout_df['action_type'].isin(['stockin', 'stockout']) &
        dealer_stockin_stockout_df['manufacturer'].isin(selected_maker) |
        dealer_stockin_stockout_df['action_type'].isin(['empty'])]

    df_stock_filtered_by_inputs.to_csv('data/temp2.csv')
    df_graph_stock = pd.read_csv('data/temp2.csv')
    os.remove('data/temp2.csv')

    df_graph_stock['cumsum'] = df_graph_stock['qty'].cumsum()
    #df_graph_stock.to_csv('data/df_graph_stock_with_cumsum_delete.csv')
    df_graph_stock_data_groupped = df_graph_stock.groupby('date').tail(1)
    #df_graph_stock_data_groupped.to_csv('data/df_graph_stock_data_groupped_to_delete.csv')
    df_graph_stock_data_groupped_date_and_cumsum = df_graph_stock_data_groupped[['date', 'cumsum']]

    df_graph_stock_data_groupped_date_and_cumsum.to_csv('data/df_graph_stock_data_groupped.csv')
    df_graph_stock_data_groupped_date_and_cumsum = pd.read_csv('data/df_graph_stock_data_groupped.csv')
    os.remove('data/df_graph_stock_data_groupped.csv')
    df_graph_stock_data_groupped_date_and_cumsum['date'] = pd.to_datetime(df_graph_stock_data_groupped_date_and_cumsum['date'], infer_datetime_format=True)
    #os.remove('data/df_graph_stock_data_groupped.csv')
    start_date_stock = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    end_date_stock = datetime.datetime.now()
    after_start_date_stock = df_graph_stock_data_groupped_date_and_cumsum["date"] >= start_date_stock
    before_end_date_stock = df_graph_stock_data_groupped_date_and_cumsum["date"] <= end_date_stock
    between_two_dates = after_start_date_stock & before_end_date_stock
    df_graph_stock_data_groupped_2021 = df_graph_stock_data_groupped_date_and_cumsum.loc[between_two_dates]
    #df_graph_stock_data_groupped_2021.to_csv('data/df_graph_stock_data_groupped_2101.csv')
    today_df_stock = df_graph_stock_data_groupped_2021[df_graph_stock_data_groupped_2021['date'] == today_str]
    stock_qty_today = today_df_stock.iloc[0]['cumsum']



    fig = go.Figure()
    #Ожидаемые поставки у поставщика
    fig.add_trace(go.Bar(
        x=df_expected_orders_2021['date'],
        y=df_expected_orders_2021['cumsum'],
        # fill='tozeroy',
        name='В заказах у поставщика. По ожидаемой дате поставки',
    ))
    # Заказы у поставщика
    fig.add_trace(go.Scatter(
        x=df_graph_orders_groupped_2021['date'],
        y = df_graph_orders_groupped_2021['cumsum'],
        #fill='tozeroy',
        name='В заказах у поставщика. История',
        hoverinfo='x+y',
        stackgroup='one',
    ))

    # Склад ДИЛЕРА
    fig.add_trace(go.Scatter(
        x=df_graph_stock_data_groupped_2021['date'],
        y=df_graph_stock_data_groupped_2021['cumsum'],
        # fill='tozeroy',
        name='Склад дилера',
        hoverinfo='x+y',
        stackgroup='one'
    ))

    # сделки
    fig.add_trace(go.Scatter(
        x=df_deals_groupped['date'],
        y=df_deals_groupped['qty'],
        # fill='tozeroy',
        name='Сделки',
    ))


    date_range_min = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    date_range_max = df_expected_orders_2021['date'].max()

    fig.update_xaxes(rangeslider_visible=True,)

    fig.update_layout(template='plotly_dark',
                      xaxis={'range': [date_range_min, date_range_max]},
                      #yaxis_range=[0, int(order_plan_2021 * 1.5)],
                      #yaxis_range=[0, maxY*1.3],
                      hovermode = "closest",
                      yaxis_title="Кол-во единиц",
                      legend_orientation="h",

                      #xaxis_title='Дата заказа',
                      #legend_title="Legend Title",
                      #title={'text': 'Техника в заказах, на складах и сделках, ед', 'font': {'color': 'white'}, 'x': 0.5},
                      )

    today_df_deals = df_deals_groupped[df_deals_groupped['date'] == today_str]
    #print(today_df_deals)
    #deals_qty_today = today_df_deals.iloc[0]['qty']




    today_to_card = datetime.datetime.now()
    today_to_card = today_to_card.strftime("%d.%m.%Y")
    return fig, '{}'.format(orders_qty_today), '* По состоянию на {}'.format(today_to_card), format(stock_qty_today), format("-")

if __name__ == "__main__":
    app.run_server(debug = True)
import datetime
import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context, Input, Output, State
import dash
import pandas as pd
# import numpy as np
# import plotly.express as px
#from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
# import csv
# import os
import tab_deal
import tab_order
import tab_plan_fact
import initial_values
import plan_prep
import base64
import io

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Demo dashboard"
server = app.server

makers = initial_values.makers
makers_list = initial_values.makers_list
product_groups = initial_values.product_groups
product_groups_list = initial_values.product_groups_list
deal_stages = initial_values.deal_stages

body = html.Div([
    dbc.Container(
        [html.Div(style={'paddingLeft': '15px', 'paddingRight': '20px', 'paddingTop': '5px', 'paddingBottom': '5px',
                            'color': 'white'},
                  children=[
                      dbc.Row([
                          dbc.Col(width=3, children=[html.Img(src="static/logo RB.png", width=300),]),
                          dbc.Col(width=9, children=[html.H3('БИЗНЕС АНАЛИТИКА'),]),
                         ]),
                         html.P(),
                         html.P('Бизнес-показатели отдела продаж техники'),
                     ]),
         html.Div([
             dcc.Tabs(
                 id="tabs-with-classes",
                 value='tab_plan_fact',
                 parent_className='custom-tabs',
                 className='custom-tabs-container',
                 children=[
                     tab_plan_fact.plan_fact_tab(),
                     tab_deal.deal_tab(),
                     tab_order.order_tab(),

                 ]),
         ]),
         ], fluid=True, className='custom_container')
], style={"height": "100vh"}, )

# передаем разметку страницы в приложение
app.layout = html.Div([body])


@app.callback(
    Output("deal_stage_selector_checklist", "value"),
    [Input('select_all_deals_stage_button', 'n_clicks'),
     Input('release_all_deals_stage_button', 'n_clicks')],
    [State("deal_stage_selector_checklist", "options")],
)
def button_productgroup_callback_func(select_all_product_groups_button, release_all_product_groups_button, options):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    full_list = [option["value"] for option in options]
    if 'select_all_deals_stage_button' in changed_id:
        selected_values = [option["value"] for option in options]
        return selected_values
    elif 'release_all_deals_stage_button' in changed_id:
        selected_values = []
        return selected_values
    return full_list


@app.callback(
    Output("maker_selector", "value"),
    [Input('select_all_makers_button', 'n_clicks'),
     Input('release_all_makers_button', 'n_clicks')],
    [State("maker_selector", "options")],
)
def button_callback_func(select_all_makers_button, release_all_makers_button, options):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    full_list = [option["value"] for option in options]
    if 'select_all_makers_button' in changed_id:
        selected_values = [option["value"] for option in options]
        return selected_values
    elif 'release_all_makers_button' in changed_id:
        selected_values = []
        return selected_values
    return full_list


@app.callback(
    Output("product_group_selector_checklist", "value"),
    [Input('select_all_product_groups_button', 'n_clicks'),
     Input('release_all_product_groups_button', 'n_clicks')],
    [State("product_group_selector_checklist", "options")],
)
def button_productgroup_callback_func(select_all_product_groups_button, release_all_product_groups_button, options):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    full_list = [option["value"] for option in options]
    if 'select_all_product_groups_button' in changed_id:
        selected_values = [option["value"] for option in options]
        return selected_values
    elif 'release_all_product_groups_button' in changed_id:
        selected_values = []
        return selected_values
    return full_list


@app.callback(
    Output("product_group_selector_checklist_tab_deals", "value"),
    [Input('select_all_product_groups_button_tab_deals', 'n_clicks'),
     Input('release_all_product_groups_button_tab_deals', 'n_clicks')],
    [State("product_group_selector_checklist_tab_deals", "options")],
)
def button_productgroup_callback_func(select_all_product_groups_button, release_all_product_groups_button, options):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    full_list = [option["value"] for option in options]
    if 'select_all_product_groups_button_tab_deals' in changed_id:
        selected_values = [option["value"] for option in options]
        return selected_values
    elif 'release_all_product_groups_button_tab_deals' in changed_id:
        selected_values = []
        return selected_values
    return full_list


@app.callback(
    Output("maker_selector_tab_deals", "value"),
    [Input('select_all_makers_button_tab_deals', 'n_clicks'),
     Input('release_all_makers_button_tab_deals', 'n_clicks')],
    [State("maker_selector_tab_deals", "options")],
)
def button_callback_func(select_all_makers_button, release_all_makers_button, options):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    full_list = [option["value"] for option in options]
    if 'select_all_makers_button_tab_deals' in changed_id:
        selected_values = [option["value"] for option in options]
        return selected_values
    elif 'release_all_makers_button_tab_deals' in changed_id:
        selected_values = []
        return selected_values
    return full_list


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
               Input('deal_stage_selector_checklist', 'value'),
               ])
def orders_stock(selected_maker, selected_product_groups, selected_deal_stages):
    df_orders_filtered_by_inputs = orders_delivery_df.loc[
        orders_delivery_df['product_group_code'].isin(selected_product_groups) &
        orders_delivery_df['action_type'].isin(['order', 'delivery']) &
        orders_delivery_df['manufacturer'].isin(selected_maker) |
        orders_delivery_df['action_type'].isin(['empty'])]

    df_orders_filtered_by_inputs.loc[:, 'cumsum'] = df_orders_filtered_by_inputs['qty'].cumsum()

    df_graph_orders_groupped = df_orders_filtered_by_inputs.groupby('date').tail(1)

    df_graph_orders_groupped.loc[:, 'date'] = pd.to_datetime(df_graph_orders_groupped['date'],
                                                             infer_datetime_format=True)

    start_date_orders = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    end_date_orders = datetime.datetime.now()
    after_start_date_orders = df_graph_orders_groupped.loc[:, "date"] >= start_date_orders
    before_end_date_orders = df_graph_orders_groupped.loc[:, "date"] <= end_date_orders
    between_two_dates = after_start_date_orders & before_end_date_orders
    df_graph_orders_groupped_2021 = df_graph_orders_groupped.loc[between_two_dates]
    today = datetime.datetime.now()
    today_str = today.strftime("%Y-%m-%d")

    today_df = df_graph_orders_groupped_2021.loc[df_graph_orders_groupped_2021['date'] == today_str]
    orders_qty_today = today_df.iloc[0]['cumsum']

    # данные для ряда Сделки
    df_deals = pd.read_csv('data/df_deals.csv')
    df_deals_filtered_by_inputs = df_deals.loc[
        df_deals['product_group_code'].isin(selected_product_groups) &
        df_deals['deal_stage_code'].isin(selected_deal_stages) &
        df_deals['manufacturer'].isin(selected_maker) |
        df_deals['deal_status'].isin(['empty'])
        ]

    df_deals_groupped = df_deals_filtered_by_inputs.groupby('date', as_index=False)["qty"].sum()

    df_deals_groupped.loc[:, 'date'] = pd.to_datetime(df_deals_groupped['date'], infer_datetime_format=True)
    start_date_deal = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    end_date_deal = datetime.datetime.now()
    after_start_date_deal = df_deals_groupped.loc[:, "date"] >= start_date_deal
    before_end_date_deal = df_deals_groupped.loc[:, "date"] <= end_date_deal
    between_two_dates_deals = after_start_date_deal & before_end_date_deal
    # between_two_dates = after_start_date_deal
    df_deals_groupped_2021 = df_deals_groupped.loc[between_two_dates_deals]

    # данные для ряда Ожидаемые сделки.
    expected_deals_start_date = datetime.datetime.now()
    expected_deals_end_date = df_deals_groupped.loc[:, 'date'].max()
    after_start_date_expected_deals = df_deals_groupped.loc[:, "date"] >= expected_deals_start_date
    before_end_date_expected_deals = df_deals_groupped.loc[:, "date"] <= expected_deals_end_date
    between_two_dates_expected_deals = after_start_date_expected_deals & before_end_date_expected_deals
    df_expected_deals_groupped_2021 = df_deals_groupped.loc[between_two_dates_expected_deals]

    # готовим данные для ряда Ожидаемые поставки
    # df_expected_orders = df_graph_orders_groupped
    start_date_expected_orders = datetime.datetime.now()
    end_date_expected_orders = df_graph_orders_groupped.loc[:, 'date'].max()
    after_start_date_expected_orders = df_graph_orders_groupped.loc[:, "date"] >= start_date_expected_orders
    before_end_date_expected_orders = df_graph_orders_groupped.loc[:, "date"] <= end_date_expected_orders
    between_two_dates = after_start_date_expected_orders & before_end_date_expected_orders
    df_expected_orders_2021 = df_graph_orders_groupped.loc[between_two_dates]
    df_expected_orders_2021_ = df_expected_orders_2021.loc[df_expected_orders_2021['cumsum'] > 0]

    # Данные для ряда STOCK
    df_stock_filtered_by_inputs = dealer_stockin_stockout_df.loc[
        dealer_stockin_stockout_df['product_group_code'].isin(selected_product_groups) &
        dealer_stockin_stockout_df['action_type'].isin(['stockin', 'stockout']) &
        dealer_stockin_stockout_df['manufacturer'].isin(selected_maker) |
        dealer_stockin_stockout_df['action_type'].isin(['empty'])]

    # df_graph_stock = df_stock_filtered_by_inputs

    df_stock_filtered_by_inputs.loc[:, 'cumsum'] = df_stock_filtered_by_inputs['qty'].cumsum()
    # df_graph_stock.to_csv('data/df_graph_stock_with_cumsum_delete.csv')
    df_graph_stock_data_groupped = df_stock_filtered_by_inputs.groupby('date').tail(1)
    # df_graph_stock_data_groupped.to_csv('data/df_graph_stock_data_groupped_to_delete.csv')
    df_graph_stock_data_groupped_date_and_cumsum = df_graph_stock_data_groupped.loc[:, ['date', 'cumsum']]

    df_graph_stock_data_groupped_date_and_cumsum.loc[:, 'date'] = pd.to_datetime(
        df_graph_stock_data_groupped_date_and_cumsum['date'], infer_datetime_format=True)

    start_date_stock = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    end_date_stock = datetime.datetime.now()
    after_start_date_stock = df_graph_stock_data_groupped_date_and_cumsum.loc[:, "date"] >= start_date_stock
    before_end_date_stock = df_graph_stock_data_groupped_date_and_cumsum.loc[:, "date"] <= end_date_stock
    between_two_dates = after_start_date_stock & before_end_date_stock
    df_graph_stock_data_groupped_2021 = df_graph_stock_data_groupped_date_and_cumsum.loc[between_two_dates]
    # df_graph_stock_data_groupped_2021.to_csv('data/df_graph_stock_data_groupped_2101.csv')
    today_df_stock = df_graph_stock_data_groupped_2021.loc[df_graph_stock_data_groupped_2021['date'] == today_str]
    stock_qty_today = today_df_stock.iloc[0]['cumsum']

    fig = go.Figure()
    # Ожидаемые поставки у поставщика
    fig.add_trace(go.Bar(
        x=df_expected_orders_2021_['date'],
        y=df_expected_orders_2021_['cumsum'],
        # fill='tozeroy',
        name='В заказах у поставщика, ед',
    ))
    # Заказы у поставщика
    fig.add_trace(go.Scatter(
        x=df_graph_orders_groupped_2021['date'],
        y=df_graph_orders_groupped_2021['cumsum'],
        # fill='tozeroy',
        name='В заказах у поставщика. История, ед',
        hoverinfo='x+y',
        stackgroup='one',
    ))

    # Склад ДИЛЕРА
    fig.add_trace(go.Scatter(
        x=df_graph_stock_data_groupped_2021['date'],
        y=df_graph_stock_data_groupped_2021['cumsum'],
        # fill='tozeroy',
        name='Склад дилера, ед',
        hoverinfo='x+y',
        stackgroup='one'
    ))

    # сделки до сегодняшнего дня в прошлом
    fig.add_trace(go.Scatter(
        x=df_expected_deals_groupped_2021['date'],
        y=df_expected_deals_groupped_2021['qty'],
        # fill='tozeroy',
        mode='markers',
        name='Зарегистрированный спрос, ед',
    ))
    # ожидаемые сделки
    fig.add_trace(go.Scatter(
        x=df_deals_groupped_2021['date'],
        y=df_deals_groupped_2021['qty'],
        # fill='tozeroy',
        name='Товары в активных сделках, ед',
    ))

    date_range_min = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    date_range_max = df_deals_groupped.loc[:, 'date'].max()

    fig.update_xaxes(rangeslider_visible=True, )

    fig.update_layout(template='plotly_dark',
                      xaxis={'range': [date_range_min, date_range_max]},
                      # yaxis_range=[0, int(order_plan_2021 * 1.5)],
                      # yaxis_range=[0, maxY*1.3],
                      hovermode="closest",
                      yaxis_title="Кол-во единиц",
                      legend_orientation="h",

                      # xaxis_title='Дата заказа',
                      # legend_title="Legend Title",
                      # title={'text': 'Техника в заказах, на складах и сделках, ед', 'font': {'color': 'white'}, 'x': 0.5},
                      )

    today_df_deals = df_deals_groupped.loc[df_deals_groupped['date'] == today_str]
    deals_qty_today = today_df_deals.iloc[0]['qty']

    today_to_card = datetime.datetime.now()
    today_to_card = today_to_card.strftime("%d.%m.%Y")
    return fig, '{}'.format(orders_qty_today), '* По состоянию на {}'.format(today_to_card), format(
        stock_qty_today), format(deals_qty_today)


df_deals = pd.read_csv('data/df_deals.csv')


# callback Воронка продаж
@app.callback([Output('funnel_graph', 'figure'),
               Output('card_deals_tab_deals_today_value', 'children'),
               Output('card_deals_tab_deals_won_in_2021', 'children'),
               Output('card_deals_tab_deals_lost_in_2021', 'children'),
               Output('card_deals_today_date', 'children'),
               ],
              [Input('maker_selector_tab_deals', 'value'),
               Input('product_group_selector_checklist_tab_deals', 'value'),
               # Input('deal_stage_selector_checklist', 'value'),
               ])
def deals_tab(selected_maker, selected_product_groups):
    df_deals_filtered_by_inputs = df_deals.loc[
        df_deals['product_group_code'].isin(selected_product_groups) &
        df_deals['manufacturer'].isin(selected_maker) |
        df_deals['deal_status'].isin(['empty'])
        ]

    today = datetime.datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_funnel_df = df_deals_filtered_by_inputs.loc[df_deals_filtered_by_inputs['date'] == today_str]
    df_deals_groupped = today_funnel_df.groupby('deal_stage_name', as_index=False)["qty"].sum()

    ##### Готовим списки X и Y для построения графика
    # сначала готовим словарь с нулевыми значеними
    deal_stages_zeros = {}
    deal_stages_zeros['1. Выявление потребности'] = 0
    deal_stages_zeros['2. Презентационная работа'] = 0
    deal_stages_zeros['3. Переговоры'] = 0
    deal_stages_zeros['4. Заключение договора'] = 0
    deal_stages_zeros['5. Отгрузка и закрытие сделки'] = 0
    # затем переписываем строки в словаре значеними. Нули должны остаться
    for index, row in df_deals_groupped.iterrows():
        deal_stage_name_in_selection = row['deal_stage_name']
        deal_stage_qty_in_selection = row['qty']
        deal_stages_zeros[deal_stage_name_in_selection] = deal_stage_qty_in_selection

    y_graph = []
    for key, val in deal_stages_zeros.items():
        y_graph.append([key][0])
    x_graph = []
    for key, val in deal_stages_zeros.items():
        x_graph.append([val][0])

    # deals_qty_today - для карточки Количество товаров в сделках на сегодняшний день
    deals_qty_today = df_deals_groupped.loc[:, 'qty'].sum()

    # считаем сколько машин мы продали
    deal_won = df_deals_filtered_by_inputs.loc[df_deals_filtered_by_inputs['milestone_event'] == 'deal_won']
    # переводим поле "Дата" в формат времени
    deal_won.loc[:, 'date'] = pd.to_datetime(deal_won['date'], infer_datetime_format=True)
    # начало года - формат времени
    start_date_deal_won = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    end_date_deal_won = datetime.datetime.now()
    after_start_date_won = deal_won.loc[:, "date"] >= start_date_deal_won
    before_end_date_won = deal_won.loc[:, "date"] <= end_date_deal_won
    between_two_dates = after_start_date_won & before_end_date_won
    deal_won_groupped_2021 = deal_won.loc[between_two_dates]
    won_qty_2021 = deal_won_groupped_2021.loc[:, 'qty'].sum()

    # считаем сколько машин мы проиграли
    deal_lost = df_deals_filtered_by_inputs.loc[df_deals_filtered_by_inputs['milestone_event'] == 'deal_lost']
    # переводим поле "Дата" в формат времени
    deal_lost.loc[:, 'date'] = pd.to_datetime(deal_lost['date'], infer_datetime_format=True)
    # начало года - формат времени
    start_date_deal_lost = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    end_date_deal_lost = datetime.datetime.now()
    after_start_date_lost = deal_lost.loc[:, "date"] >= start_date_deal_lost
    before_end_date_lost = deal_lost.loc[:, "date"] <= end_date_deal_lost
    between_two_dates = after_start_date_lost & before_end_date_lost
    deal_lost_groupped_2021 = deal_lost.loc[between_two_dates]
    lost_qty_2021 = deal_lost_groupped_2021.loc[:, 'qty'].sum()

    trace = go.Funnel(
        # y=["Website visit", "Downloads", "Potential customers", "Requested price", "Finalized"],
        y=y_graph,
        x=x_graph,
        textposition="inside",
        textinfo="value",
        opacity=0.65,
        # marker={"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
        #         "line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
        # connector={"line": {"color": "royalblue", "dash": "dot", "width": 3}}
    )
    today_to_card = datetime.datetime.now()
    today_to_card = today_to_card.strftime("%d.%m.%Y")

    layout = {'template': 'plotly_dark', 'title': {'text': 'Товары в сделках по этапам, ед'}}
    return go.Figure(data=trace, layout=layout), '{}'.format(deals_qty_today), '{}'.format(won_qty_2021), '{}'.format(
        lost_qty_2021), '* По состоянию на {}'.format(today_to_card)


df_won_fact = df_deals.loc[df_deals['milestone_event'] == 'deal_won']


# обработчик чек-боксов Производитель во вкладке План-факт
@app.callback(
    Output("maker_selector_plan_fact", "value"),
    [Input('select_all_makers_button_tab_plan_fact', 'n_clicks'),
     Input('release_all_makers_button_plan_fact', 'n_clicks')],
    [State("maker_selector_plan_fact", "options")],
)
def button_callback_func(select_all_makers_button, release_all_makers_button, options):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    full_list = [option["value"] for option in options]
    if 'select_all_makers_button_tab_plan_fact' in changed_id:
        selected_values = [option["value"] for option in options]
        return selected_values
    elif 'release_all_makers_button_plan_fact' in changed_id:
        selected_values = []
        return selected_values
    return full_list


@app.callback(
    Output("product_group_selector_checklist_tab_plan_fact", "value"),
    [Input('select_all_product_groups_button_tab_plan_fact', 'n_clicks'),
     Input('release_all_product_groups_button_tab_plan_fact', 'n_clicks')],
    [State("product_group_selector_checklist_tab_plan_fact", "options")],
)
def button_productgroup_callback_func(select_all_product_groups_button, release_all_product_groups_button, options):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    full_list = [option["value"] for option in options]
    if 'select_all_product_groups_button_tab_plan_fact' in changed_id:
        selected_values = [option["value"] for option in options]
        return selected_values
    elif 'release_all_product_groups_button_tab_plan_fact' in changed_id:
        selected_values = []
        return selected_values
    return full_list


# Обработчик Вкладки План факт
@app.callback(Output('contracts_plan_fact_graph', 'figure'),
              Output('card_plan_fact_tab_contract_value', 'children'),
              Output('card_plan_fact_today_date', 'children'),
              Output("output-data-table", "children"),
              [Input('maker_selector_plan_fact', 'value'),
               Input('product_group_selector_checklist_tab_plan_fact', 'value'),
               Input('finish_date_slider', 'value'),
               Input('upload_plan', 'contents')],
               [State('upload_plan', 'filename')])
def deals_tab(selected_maker, selected_product_groups, finish_date_slider_value, contents, filename):
    df_plan_fact_filtered_by_inputs = df_won_fact.loc[
        df_won_fact['product_group_code'].isin(selected_product_groups) &
        df_won_fact['manufacturer'].isin(selected_maker)
        ]
    df_plan_fact_filtered_by_inputs.loc[:, 'date'] = pd.to_datetime(df_won_fact['date'], infer_datetime_format=True)

    start_date_plan_fact = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    #end_date_plan_fact = datetime.datetime.now()
    end_date_plan_fact = datetime.datetime.fromtimestamp(finish_date_slider_value)
    after_start_date_plan_fact = df_plan_fact_filtered_by_inputs.loc[:, "date"] >= start_date_plan_fact
    before_end_date_plan_fact = df_plan_fact_filtered_by_inputs.loc[:, "date"] <= end_date_plan_fact
    between_two_dates = after_start_date_plan_fact & before_end_date_plan_fact
    df_won_fact_groupped_2021 = df_plan_fact_filtered_by_inputs.loc[between_two_dates]

    df_won_fact_groupped_2021.loc[:, 'cumsum'] = df_won_fact_groupped_2021['qty'].cumsum()

    x = df_won_fact_groupped_2021.loc[:, 'date']
    y = df_won_fact_groupped_2021.loc[:, 'cumsum']
    fact_at_current_date = df_won_fact_groupped_2021.iloc[-1]['cumsum']

    #table_plan_output = html.Div()
    plan_value_for_selected_inputs = 0
    annotation_text = ""

    # создаем линию плана по умолчанию
    plan_df = plan_prep.plan_prep()

    # если с кнопки Загрузить что-то к нам заехало, то:
    if contents is not None:
        # парсим то, что мы получили
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        # делаем попытку прочитать эксель
        try:
            if 'xlsx' in filename:
                # если к нам загружен эксель, то делаем из него датафрейм plan_df
                plan_df = pd.read_excel(io.BytesIO(decoded))
                # здесь надо сделать проверку загруженных из эксель данных
                print('эксель успешно загружен')
                # если файл не ексель, то пока просто ничего не делаем
        # если попытка загрузить не прошла по каким-то причинам, то пока ничего не далем. Выводим в принт
        except Exception as e:
            print('при попытке загрузить excal файл возникло исключение', e)



    plan_df_filtered_by_inputs = plan_df.loc[plan_df['product_group_code'].isin(selected_product_groups) &
                                                            plan_df['maker'].isin(selected_maker)
                                                            ]
    plan_df_filtered_by_inputs_value = plan_df_filtered_by_inputs['plan_qty'].sum()
    annotation_text = "    План продаж: " + str(plan_df_filtered_by_inputs_value) + " ед."

    # результирующую таблицу с планом мы получаем в html.Div(id='output-data-table') На него ссылается в колбэке, ожидая от него children, то есть html
    output_table = dbc.Table().from_dataframe(plan_df_filtered_by_inputs, style={'color': 'white'})
    # переменная table_plan_output нужна для того, чтобы передаеть ее в return
    table_plan_output = html.Div([output_table])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        fill='tozeroy',
        name='Факт продаж, ед',
    ))

    fig.add_hline(y=plan_df_filtered_by_inputs_value, line_width=3, line_color="red", annotation_text=annotation_text,
                  annotation_position="top left",
                  annotation_font_size=15,
                  annotation_font_color="white"
                  )


    fig.update_layout(template='plotly_dark',
                      xaxis={'range': ['2021-01-01', '2022-01-01']},
                      yaxis_title="Проданное кол-во, ед",
                      xaxis_title='Дата продажи',
                      # legend_title="Legend Title",
                      title={'text': 'План-факт продаж в 2021 году', 'font': {'color': 'white'}, 'x': 0.5}, )
    value_to_fact_qty = fact_at_current_date
    #today_to_card = datetime.datetime.now()
    today_to_card = end_date_plan_fact

    today_to_card = today_to_card.strftime("%d.%m.%Y")
    current_date_output = '* По состоянию на {}'.format(today_to_card)



    return fig, value_to_fact_qty, current_date_output, table_plan_output


# обработчик кнопки выгрузки наружу файла "plan_template.xlsx"
@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    if n_clicks:
        df = plan_prep.plan_prep()
        return dcc.send_data_frame(df.to_excel, "plan_template.xlsx",index=False, sheet_name="plan_template")


if __name__ == "__main__":
    app.run_server(debug=True)

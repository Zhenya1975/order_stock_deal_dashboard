from dash import dcc, html
import dash_bootstrap_components as dbc

makers = [{'label': " John Deere", 'value': "John Deere"},
          {'label': " JCB", 'value': "JCB"},
          {'label': " Kuhn", 'value': "KUHN"}, ]

makers_list = ["John Deere", "JCB", "KUHN"]

product_groups = [{'label': " Тракторы", 'value': "TR"},
                  {'label': " З/У комбайны", 'value': "HARV"},
                  {'label': " Прицепное оборудование", 'value': "TL"},
                  {'label': " Опрыскиватели", 'value': "SPR"},
                  {'label': " Погрузчики", 'value': "LDR"}, ]

product_groups_list = ["TR", "HARV", "TL", "SPR", "LDR"]

deal_stages = [
    {'label': ' 1. Выявление потребности', 'value': 'phase_1'},
    {'label': ' 2. Презентационная работа', 'value': 'phase_2'},
    {'label': ' 3. Переговоры', 'value': 'phase_3'},
    {'label': ' 4. Заключение договора', 'value': 'phase_4'},
    {'label': ' 5. Отгрузка и закрытие сделки', 'value': 'phase_5'}, ]

deal_stages_list = ['phase_1', 'phase_2', 'phase_3', 'phase_4', 'phase_5']

card_orders_ = [
    dbc.CardHeader("В заказах, ед *"),
    dbc.CardBody([html.P(className="card-title", id='card_orders_today_value'),
                  ]
                 ), ]

card_stock = [
    dbc.CardHeader("На складах, ед *"),
    dbc.CardBody([html.P(className="card-title", id='card_stock_today_value'),
                  ]
                 ), ]
card_deals = [
    dbc.CardHeader("В сделках, ед *"),
    dbc.CardBody([html.P(className="card-title", id='card_deals_today_value'),
                  ]
                 ), ]


def order_tab():
    order_tab = dcc.Tab(
                            label='ЗАКАЗЫ-СКЛАДЫ-СДЕЛКИ',
                            value='tab-orders',
                            className='custom-tab',
                            selected_className='custom-tab--selected',
                            children=[
                                dbc.Row([
                                    dbc.Col(width=3,
                                            children=[
                                                html.Div(style={'paddingReft': '30px', 'paddingRight': '20px',
                                                                'marginTop': '10px', 'color': 'white'},
                                                         children=[
                                                             html.P(),
                                                             html.B('Бренды'),
                                                             html.P(),
                                                             html.Div(style={'marginLeft': '3px'},
                                                                      children=[
                                                                          dbc.Button("Выбрать все", size="sm",
                                                                                     id="select_all_makers_button",
                                                                                     style={'marginBottom': '3px',
                                                                                            'marginTop': '3px',
                                                                                            'backgroundColor': '#232632'}),
                                                                          dbc.Button("Снять выбор", color="secondary",
                                                                                     size="sm",
                                                                                     style={'marginBottom': '3px',
                                                                                            'marginTop': '3px',
                                                                                            'backgroundColor': '#232632'},
                                                                                     id="release_all_makers_button"),
                                                                      ]
                                                                      ),

                                                             dcc.Checklist(id='maker_selector',
                                                                           options=makers,
                                                                           value=makers_list,
                                                                           labelStyle=dict(display='block')),

                                                             html.Hr(className="hr"),

                                                             html.B('Товарные группы'),
                                                             html.P(),
                                                             html.Div(style={'marginLeft': '3px'},
                                                                      children=[
                                                                          dbc.Button("Выбрать все", color="secondary",
                                                                                     size="sm",
                                                                                     id="select_all_product_groups_button",
                                                                                     style={'marginBottom': '3px',
                                                                                            'marginTop': '3px',
                                                                                            'backgroundColor': '#232632'}),
                                                                          dbc.Button("Снять выбор", color="secondary",
                                                                                     size="sm",
                                                                                     style={'marginBottom': '3px',
                                                                                            'marginTop': '3px',
                                                                                            'backgroundColor': '#232632'},
                                                                                     id="release_all_product_groups_button"),
                                                                      ]
                                                                      ),

                                                             dcc.Checklist(id='product_group_selector_checklist',
                                                                           options=product_groups,
                                                                           value=product_groups_list,
                                                                           labelStyle=dict(display='block')),
                                                             html.Hr(className="hr"),
                                                             ##### Выбор этапа сделки
                                                             html.P(),
                                                             html.B('Этапы сделки'),
                                                             html.P(),
                                                             html.Div(style={'marginLeft': '3px'},
                                                                      children=[
                                                                          dbc.Button("Выбрать все", color="secondary",
                                                                                     size="sm",
                                                                                     id="select_all_deals_stage_button",
                                                                                     style={'marginBottom': '3px',
                                                                                            'marginTop': '3px',
                                                                                            'backgroundColor': '#232632'}),
                                                                          dbc.Button("Снять выбор", color="secondary",
                                                                                     size="sm",
                                                                                     style={'marginBottom': '3px',
                                                                                            'marginTop': '3px',
                                                                                            'backgroundColor': '#232632'},
                                                                                     id="release_all_deals_stage_button"),
                                                                      ]
                                                                      ),

                                                             dcc.Checklist(id='deal_stage_selector_checklist',
                                                                           options=deal_stages,
                                                                           value=deal_stages_list,
                                                                           labelStyle=dict(display='block')),
                                                             html.Hr(),
                                                         ]
                                                         ),
                                            ]),
                                    dbc.Col(width=9,
                                            children=[
                                                html.P(),
                                                html.Div(style={'paddingLeft': '30px', 'paddingRight': '20px',
                                                                'paddingTop': '10px', 'color': 'white'},
                                                         children=[
                                                             html.P(
                                                                 'Динамика изменения запасов (в заказах + на складах) и спроса (в сделках)'),
                                                             dbc.Row([
                                                                 dbc.Col(dbc.Card(card_orders_, color="dark",
                                                                                  inverse=True)),
                                                                 dbc.Col(
                                                                     dbc.Card(card_stock, color="dark", inverse=True)),
                                                                 dbc.Col(
                                                                     dbc.Card(card_deals, color="dark", inverse=True)),
                                                             ],

                                                             ),
                                                             html.P(className="card-text", id='card_orders_today_date'),
                                                             html.P(),
                                                             dcc.Graph(id='orders_stock_deals',
                                                                       config={'displayModeBar': False}),
                                                             html.P(),

                                                         ]),
                                            ])

                                ])
                            ]

                        )
    return order_tab
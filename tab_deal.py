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


def deal_tab():
    card_tab_deals_qty_in_deals = [
        dbc.CardHeader("Товары в сделках, ед *"),
        dbc.CardBody([html.P(className="card-title", id='card_deals_tab_deals_today_value'),
                      ]
                     ), ]
    card_tab_deals_won_deals = [
        dbc.CardHeader("Продано в 2021г., ед *"),
        dbc.CardBody([html.P(className="card-title", id='card_deals_tab_deals_won_in_2021'),
                      ]
                     ), ]

    card_tab_deals_lost_deals = [
        dbc.CardHeader("Проиграно d 2021г., ед *"),
        dbc.CardBody([html.P(className="card-title", id='card_deals_tab_deals_lost_in_2021'),
                      ]
                     ), ]
    deal_tab_block = dcc.Tab(
        label='СДЕЛКИ',
        value='tab-deals',
        className='custom-tab',
        selected_className='custom-tab--selected',
        children=[
            dbc.Row([
                dbc.Col(width=3,
                        children=[
                            html.Div(style={'paddingLeft': '30px', 'paddingRight': '20px',
                                            'marginTop': '10px', 'color': 'white'},
                                     children=[
                                         html.P(),
                                         html.B('Бренды'),
                                         html.P(),
                                         html.Div(style={'marginLeft': '3px'},
                                                  children=[
                                                      dbc.Button("Выбрать все", size="sm",
                                                                 id="select_all_makers_button_tab_deals",
                                                                 style={'marginBottom': '3px',
                                                                        'marginTop': '3px',
                                                                        'backgroundColor': '#232632'}),
                                                      dbc.Button("Снять выбор", color="secondary",
                                                                 size="sm",
                                                                 style={'marginBottom': '3px',
                                                                        'marginTop': '3px',
                                                                        'backgroundColor': '#232632'},
                                                                 id="release_all_makers_button_tab_deals"),
                                                  ]
                                                  ),

                                         dcc.Checklist(id='maker_selector_tab_deals',
                                                       options=makers,
                                                       value=makers_list,
                                                       labelStyle=dict(display='block')),
                                         html.Hr(className="hr"),

                                         html.P(),
                                         html.B('Товарные группы'),
                                         html.P(),
                                         html.Div(style={'marginLeft': '3px'},
                                                  children=[
                                                      dbc.Button("Выбрать все", color="secondary",
                                                                 size="sm",
                                                                 id="select_all_product_groups_button_tab_deals",
                                                                 style={'marginBottom': '3px',
                                                                        'marginTop': '3px',
                                                                        'backgroundColor': '#232632'}),
                                                      dbc.Button("Снять выбор", color="secondary",
                                                                 size="sm",
                                                                 style={'marginBottom': '3px',
                                                                        'marginTop': '3px',
                                                                        'backgroundColor': '#232632'},
                                                                 id="release_all_product_groups_button_tab_deals"),
                                                  ]
                                                  ),

                                         dcc.Checklist(id='product_group_selector_checklist_tab_deals',
                                                       options=product_groups,
                                                       value=product_groups_list,
                                                       labelStyle=dict(display='block')),

                                     ]
                                     ),
                        ]),
                dbc.Col(width=9,
                        children=[
                            html.P(),
                            html.Div(style={'paddingLeft': '30px', 'paddingRight': '20px',
                                            'paddingTop': '10px', 'color': 'white'},
                                     children=[
                                         dbc.Row([
                                             dbc.Col(dbc.Card(card_tab_deals_qty_in_deals, color="dark", inverse=True)),
                                             dbc.Col(dbc.Card(card_tab_deals_won_deals, color="dark", inverse=True)),
                                             dbc.Col(dbc.Card(card_tab_deals_lost_deals, color="dark", inverse=True)),
                                         ],
                                         ),
                                         html.P(className="card-text", id='card_deals_today_date'),

                                         html.P(),
                                         dcc.Graph(id='funnel_graph', config={'displayModeBar': False}),
                                         html.P(),

                                     ]),
                        ])

            ])
        ]
    )
    return deal_tab_block

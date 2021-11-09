from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import initial_values
import base64
import datetime
import io
import pandas as pd

makers = initial_values.makers
makers_list = initial_values.makers_list
product_groups = initial_values.product_groups
product_groups_list = initial_values.product_groups_list
deal_stages = initial_values.deal_stages

def plan_fact_tab():
    card_tab_deals_qty_in_deals = [
        dbc.CardHeader("Факт продаж в 2021, ед *"),
        dbc.CardBody([
            html.P(className="card-title", id='card_plan_fact_tab_contract_value'),
            html.P(className="card-text", id='card_plan_fact_tab_plan_value'),
                      ]
                     ), ]

    plan_fact_tab_block = dcc.Tab(
        label='ПЛАН ФАКТ',
        value='tab_plan_fact',
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
                                                                 id="select_all_makers_button_tab_plan_fact",
                                                                 style={'marginBottom': '3px',
                                                                        'marginTop': '3px',
                                                                        'backgroundColor': '#232632'}),
                                                      dbc.Button("Снять выбор", color="secondary",
                                                                 size="sm",
                                                                 style={'marginBottom': '3px',
                                                                        'marginTop': '3px',
                                                                        'backgroundColor': '#232632'},
                                                                 id="release_all_makers_button_plan_fact"),
                                                  ]
                                                  ),

                                         dcc.Checklist(id='maker_selector_plan_fact',
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
                                                                 id="select_all_product_groups_button_tab_plan_fact",
                                                                 style={'marginBottom': '3px',
                                                                        'marginTop': '3px',
                                                                        'backgroundColor': '#232632'}),
                                                      dbc.Button("Снять выбор", color="secondary",
                                                                 size="sm",
                                                                 style={'marginBottom': '3px',
                                                                        'marginTop': '3px',
                                                                        'backgroundColor': '#232632'},
                                                                 id="release_all_product_groups_button_tab_plan_fact"),
                                                  ]
                                                  ),

                                         dcc.Checklist(id='product_group_selector_checklist_tab_plan_fact',
                                                       options=product_groups,
                                                       value=product_groups_list,
                                                       labelStyle=dict(display='block')),
                                         html.Hr(className="hr"),
                                         #dcc.Upload(html.Button('Upload File'), id="upload_plan"),
                                         html.P(),
                                         html.B('План продаж'),
                                         html.P(),
                                         dcc.Upload(dbc.Button("Загрузить план", color="secondary",
                                                    size="md",
                                                    style={'marginBottom': '3px',
                                                           'marginTop': '3px',
                                                           'backgroundColor': '#232632'},
                                                    ),
                                                    id="upload_plan"
                                                    ),
                                         html.Div([
                                             html.A("Выгрузить Excel шаблон", id="btn_xlsx"),
                                             dcc.Download(id="download-dataframe-xlsx"),
                                         ]),
                                         # html.Hr(className="hr"),
                                         # html.P(),
                                         # html.B('Ожидания'),
                                         # html.P(),
                                         # dcc.Checklist(id='expectations_deals',
                                         #               options=[{'label': " Текущие сделки", 'value': "expected_deals"},
                                         #                               #{'label': " Статистический тренд", 'value': "trend"},
                                         #                        ],
                                         #
                                         #               value=[],
                                         #               labelStyle=dict(display='block')),

                                     ]
                                     ),
                        ]),
                dbc.Col(width=9,
                        children=[
                            html.P(),
                            html.Div(style={'paddingLeft': '30px', 'paddingRight': '20px',
                                            'paddingTop': '10px', 'color': 'white'},
                                     children=[
                                         dbc.Row([ # card_tab_deals_qty_in_deals - это название карточки
                                             dbc.Col(width = 4, children=[dbc.Card(card_tab_deals_qty_in_deals, color="dark", inverse=True)]),

                                             #dbc.Col(dbc.Card(card_tab_deals_won_deals, color="dark", inverse=True)),
                                             #dbc.Col(dbc.Card(card_tab_deals_lost_deals, color="dark", inverse=True)),
                                         ],
                                         ),
                                         html.P(className="card-text", id='card_plan_fact_today_date'),

                                         html.P(),
                                         dcc.Graph(id='contracts_plan_fact_graph', config={'displayModeBar': False}),
                                         html.P(),
                                         dcc.Slider(
                                             id='finish_date_slider',
                                             min=1609459200, # 1 января 2021
                                             max=datetime.datetime.timestamp(datetime.datetime.now()),  # сегодня
                                             step=86400,

                                             value=datetime.datetime.timestamp(datetime.datetime.now()),
                                         ),
                                         html.Div(
                                                  children=[
                                                      html.P("План продаж"),
                                                      html.Div(id='output-data-table')
                                                  ]
                                                  ),


                                     ]),
                        ])

            ])
        ]
    )



    return plan_fact_tab_block

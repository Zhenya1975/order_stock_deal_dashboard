import pandas as pd
import datetime
def plan_fact_graph_date_range():
    graph_start_date = '2021-01-01'
    graph_end_date = '2022-01-01'
    return graph_start_date, graph_end_date

def cut_df_by_dates_interval(df, start_date, end_date):
    start_date = start_date
    end_date = end_date
    after_start_date = df.loc[:, "date"] >= start_date
    before_end_date = df.loc[:, "date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    result_df = df.loc[between_two_dates]
    return result_df

# для построения линии ожидания от сделок. Надо взять все сделки. Отобрать строки won и их отложить на графике
def expected_deals(df, fact_at_current_date, start_date):
    """expected_deals"""
    #deals = pd.read_csv('data/df_deals.csv', parse_dates=['date'])
    won_deals = df.loc[df['milestone_event']=='deal_won']
    start_date = start_date
    end_date = datetime.datetime.strptime("31.12.2021", "%d.%m.%Y")
    expected_sales_df = cut_df_by_dates_interval(won_deals, start_date, end_date)
    result_list = []
    result_list.append({'date': start_date, 'value': fact_at_current_date})
    for index, row in expected_sales_df.iterrows():
        dict_temp = {}
        dict_temp['date'] = row['date']
        dict_temp['value'] = row['qty']
        result_list.append(dict_temp)
    result_df = pd.DataFrame(result_list)
    result_df.loc[:, 'cumsum'] = result_df['value'].cumsum()

    return (result_df)

# def funnel - получение данных для построения вопронки продаж
def funnel_data(df_deals_filtered_by_inputs):
    # получаем df_deals
    #df_deals = pd.read_csv('data/df_deals.csv', parse_dates=['date'])
    # колонку date переводим в формат даты
    df_deals_filtered_by_inputs['date'] = df_deals_filtered_by_inputs['date'].apply(lambda x: datetime.date(x.year,x.month,x.day))
    # получаем сегодняшнюю дату и переводим ее в формат даты
    today = datetime.datetime.now().date()
    # получаем датафрейм с данными за сегодняшний день
    today_funnel_df = df_deals_filtered_by_inputs.loc[df_deals_filtered_by_inputs['date'] == today]
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
    # deals_qty_today сколько товаров сейчас в сделках всего
    deals_qty_today = df_deals_groupped.loc[:, 'qty'].sum()

    # считаем сколько машин мы продали
    deal_won = df_deals_filtered_by_inputs.loc[df_deals_filtered_by_inputs['milestone_event'] == 'deal_won']

    start_date_deal_won = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y").date()
    finish_date_deal_won = today
    deal_won_period_2021 = cut_df_by_dates_interval(deal_won, start_date_deal_won, finish_date_deal_won)
    won_qty_2021 = deal_won_period_2021.loc[:, 'qty'].sum()

    # считаем сколько машин мы проиграли
    deal_lost = df_deals_filtered_by_inputs.loc[df_deals_filtered_by_inputs['milestone_event'] == 'deal_lost']
    start_date_deal_lost = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y").date()
    finish_date_deal_lost = today
    deal_lost_period_2021 = cut_df_by_dates_interval(deal_lost, start_date_deal_lost, finish_date_deal_lost)

    lost_qty_2021 = deal_lost_period_2021.loc[:, 'qty'].sum()

    return x_graph, y_graph, deals_qty_today, won_qty_2021, lost_qty_2021


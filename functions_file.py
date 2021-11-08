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
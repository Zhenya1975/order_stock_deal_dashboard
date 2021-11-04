import pandas as pd
import initial_values
import random
import datetime

def plan_prep():
    deals = pd.read_csv('data/df_deals.csv', parse_dates=['date'])
    #print(deals.memory_usage(index=False, deep=True))
    won_deals = deals.loc[deals['milestone_event']=='deal_won']
    #won_deals.loc[:, 'date'] = pd.to_datetime(won_deals['date'], infer_datetime_format=True)

    start_date_plan = datetime.datetime.strptime("01.01.2021", "%d.%m.%Y")
    end_date_plan = datetime.datetime.strptime("31.12.2021", "%d.%m.%Y")
    after_start_date_plan = won_deals.loc[:, "date"] >= start_date_plan
    before_end_date_plan = won_deals.loc[:, "date"] <= end_date_plan
    between_two_dates = after_start_date_plan & before_end_date_plan
    df_won_plan_groupped_2021 = won_deals.loc[between_two_dates]

    quarter_list = [1,2,3,4]
    makers_list = initial_values.makers_list
    product_groups_list = initial_values.product_groups_list

    # итерируемся по кварталам, по производителям и по товарным группам
    # результат пишем в лист
    plan_result_list = []
    for quarter in quarter_list:
        for maker in makers_list:
            for product_group_code in product_groups_list:
                dict_temp = {}
                dict_temp['quarter'] = quarter
                dict_temp['maker'] = maker
                dict_temp['product_group_code'] = product_group_code
                temp_df = df_won_plan_groupped_2021.loc[(df_won_plan_groupped_2021['deal_finish_quarter']==quarter) & (df_won_plan_groupped_2021['manufacturer']==maker) & (df_won_plan_groupped_2021['product_group_code']==product_group_code)]
                fact_sold_qty = temp_df['qty'].sum()
                dict_temp['fact'] = fact_sold_qty
                if fact_sold_qty !=0:
                    plan_qty = random.randint(int(fact_sold_qty - fact_sold_qty*0.1), int(fact_sold_qty + fact_sold_qty*0.3))
                    dict_temp['plan_qty']=plan_qty
                    plan_result_list.append(dict_temp)

    plan_df = pd.DataFrame(plan_result_list)
    plan_df.to_excel('data/plan1.xlsx', index=False)
    return plan_df
#plan_prep()
import pandas as pd
import random
# import os
import datetime
import secrets
# погнали делать график сделок
# это вообще просто. Бежим по календарю Для каждой даты случайным образом определяем количество товаров в сделках. и это все.

df_calendar = pd.read_csv('data/calendar.csv')
df_calendar['date'] = pd.to_datetime(df_calendar['date'], infer_datetime_format=True)
df_master_product_catalogue = pd.read_csv('data/manufacturer_catalogue.csv', index_col='product_id')

deal_stage = [
{'deal_stage_id': 1, 'deal_stage_name': '1. Выявление потребности', 'deal_phase_code': 'phase_1'},
{'deal_stage_id': 2, 'deal_stage_name': '2. Презентационная работа', 'deal_phase_code': 'phase_2'},
{'deal_stage_id': 3, 'deal_stage_name': '3. Переговоры', 'deal_phase_code': 'phase_3'},
{'deal_stage_id': 4, 'deal_stage_name': '4. Заключение договора', 'deal_phase_code': 'phase_4'},
{'deal_stage_id': 5, 'deal_stage_name': '5. Отгрузка и закрытие сделки', 'deal_phase_code': 'phase_5'},
]
df_deal_stages = pd.DataFrame(deal_stage).set_index('deal_stage_id')


df_calendar_deals = df_calendar[df_calendar['date'] < (datetime.datetime.now() + datetime.timedelta(days=120))]
df_calendar_deals = df_calendar_deals[df_calendar_deals['date']>=datetime.datetime.strptime('2020-01-01', "%Y-%m-%d")]
result_deals_list_of_dicts = []
for index, row_calendar in df_calendar_deals.iterrows():
    dict_temp_zero = {}
    date_calendar = row_calendar['date']
    qty = 0

    dict_temp_zero['date'] = date_calendar
    dict_temp_zero['deal_status'] = 'empty'
    dict_temp_zero['qty'] = 0
    result_deals_list_of_dicts.append(dict_temp_zero)

# будем итерироваться по всему календарю с 20-го года.

for index, row_calendar in df_calendar_deals.iterrows():

    #date_calendar = datetime.datetime.strptime(row_calendar['date'], "%Y-%m-%d")
    date_calendar = row_calendar['date']
    # случайно выбираем из товарной номенклатуры товар
    product_id = random.randint(1, 232)
    product_name = df_master_product_catalogue.loc[product_id, 'product_name']
    manufacturer = df_master_product_catalogue.loc[product_id, 'Manufacturer']
    product_group_code = df_master_product_catalogue.loc[product_id, 'Product_group_code']
    product_group_name = df_master_product_catalogue.loc[product_id, 'Product_group_name']
    model_name = df_master_product_catalogue.loc[product_id, 'model_name']
    # в количество в сделке вставляем случайное число
    deal_qty = random.randint(3, 10)
    deal_id = secrets.token_hex(nbytes=16)
    # в переменную current_record_date положим текущую дату, которую будем обновлять
    current_record_date = date_calendar
    # определяем сколько будет этапов в сделке.
    number_of_deal_stages = random.randint(1, 5)
    for i in range(number_of_deal_stages):
        deal_stage_code = df_deal_stages.loc[i+1,'deal_phase_code']
        deal_stage_name = df_deal_stages.loc[i+1,'deal_stage_name']
        # определяем сколько дней сделка будет существовать на каждом из своих этапов
        number_of_days_on_deal_stage = random.randint(2, 15)
        for i in range(number_of_days_on_deal_stage):
            dict_temp = {}
            dict_temp['date'] = current_record_date
            delta = datetime.timedelta(days=1)
            current_record_date = current_record_date + delta
            dict_temp['deal_id'] = deal_id
            dict_temp['deal_status'] = 'active'
            dict_temp['qty'] = deal_qty
            dict_temp['product_id'] = product_id
            dict_temp['product_name'] = product_name
            dict_temp['manufacturer'] = manufacturer
            dict_temp['product_group_code'] = product_group_code
            dict_temp['product_group_name'] = product_group_name
            dict_temp['model_name'] = model_name
            dict_temp['deal_stage_code'] = deal_stage_code
            dict_temp['deal_stage_name'] = deal_stage_name

            result_deals_list_of_dicts.append(dict_temp)




df_deals = pd.DataFrame(result_deals_list_of_dicts).sort_values('date')
df_deals.reset_index()
df_deals.to_csv('data/df_deals.csv')

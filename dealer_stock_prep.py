import pandas as pd
import random
import datetime
import secrets

df_master_product_catalogue = pd.read_csv('data/manufacturer_catalogue.csv', index_col='product_id')
df_calendar = pd.read_csv('data/calendar.csv')

# создаем поступления на склад.
result_list_of_dicts = []
for index, row in df_calendar.iterrows():
    dict_temp_zero = {}
    date_calendar = datetime.datetime.strptime(row['date'], "%Y-%m-%d").date()
    if date_calendar <= datetime.datetime.now().date():
        dict_temp_zero['date'] = date_calendar
        dict_temp_zero['qty'] = 0
        dict_temp_zero['action_type'] = 'empty'
        dict_temp_zero['stock_balance'] = 0
        result_list_of_dicts.append(dict_temp_zero)

# мтерируемся по отгрузкам с завода и создаем строки наших поступлений
orders_delivery_df = pd.read_csv('data/orders_delivery_df.csv')

orders_delivery_df_delivery = orders_delivery_df[orders_delivery_df['action_type']=='delivery']
for index, row in orders_delivery_df_delivery.iterrows():
    dict_temp = {}
    date_row = datetime.datetime.strptime(row['date'], "%Y-%m-%d").date()
    stock_in_qty = -1 * row['qty']
    stock_balance = stock_in_qty
    doc_id = secrets.token_hex(nbytes=16)
    dict_temp['date'] = date_row
    dict_temp['qty'] = stock_in_qty
    dict_temp['action_type'] = 'stock_in'
    dict_temp['stock_balance'] = stock_balance
    dict_temp['doc_id'] = doc_id
    dict_temp['product_id'] = row['product_id']
    dict_temp['product_name'] = row['product_name']
    dict_temp['manufacturer'] = row['manufacturer']
    dict_temp['product_group_code'] = row['product_group_code']
    dict_temp['product_group_name'] = row['product_group_name']
    dict_temp['model_name'] = row['model_name']
    result_list_of_dicts.append(dict_temp)

    # есть строка поставки, значит надо сразу делать и строки расхода
    temp_date = date_row
    while stock_balance > 0:
        delta = datetime.timedelta(days=random.randint(15, 100))
        temp_date = temp_date + delta
        sold_qty = random.randint(1, stock_balance)
        updated_stock_balance = stock_balance - sold_qty
        dict_temp['date'] = temp_date
        dict_temp['qty'] = -1 * sold_qty
        dict_temp['action_type'] = 'stock_out'
        dict_temp['stock_balance'] = stock_balance
        dict_temp['doc_id'] = doc_id
        dict_temp['product_id'] = row['product_id']
        dict_temp['product_name'] = row['product_name']
        dict_temp['manufacturer'] = row['manufacturer']
        dict_temp['product_group_code'] = row['product_group_code']
        dict_temp['product_group_name'] = row['product_group_name']
        dict_temp['model_name'] = row['model_name']
        result_list_of_dicts.append(dict_temp)
        stock_balance = updated_stock_balance
        dict_temp = {}

df_dealer_stock_income_outcome = pd.DataFrame(result_list_of_dicts).sort_values('date').reset_index()
df_dealer_stock_income_outcome.to_csv('data/dealer_stockin_stockout.csv')



#print(dealer_stock_income_outcome)
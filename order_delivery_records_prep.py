import pandas as pd
import random
# import os
import datetime
import secrets

df_master_product_catalogue = pd.read_csv('data/manufacturer_catalogue.csv', index_col='product_id')

# Загужаем календарь
df_calendar = pd.read_csv('data/calendar.csv')
# df_calendar['date'] = pd.to_datetime(df_calendar['date'], infer_datetime_format=True)
# df_calendar = df_calendar['date'] <= datetime.datetime.now()

# Сначала проходим по всем дням календаря и заполняем их empty строками
result_list_of_dicts = []
for index, row in df_calendar.iterrows():
    dict_temp_zero = {}
    date = datetime.datetime.strptime(row['date'], "%Y-%m-%d")
    dict_temp_zero['date'] = date
    dict_temp_zero['qty'] = 0
    dict_temp_zero['action_type'] = 'empty'
    dict_temp_zero['order_balance'] = 0
    result_list_of_dicts.append(dict_temp_zero)
# в результате цикла выше мы должны добавить строки календаря

# запускаем еще раз этот же цикл. По средам будем создавать заказы. И переписывать ранее созданные записи
for index, row in df_calendar.iterrows():
    if row['weekday'] == 3:
        # Мы случайным образом определяем кол-во строк из номенклатуры, которые выйдут в заказ в выбранном дне.
        # Случайное число от 3 до 15.
        number_of_product_lines_in_order = random.randint(1, 5)
        # в result_list_of_dicts  будем записывать дикты, которые будут строками результирующего датафрейма
        # внутри среды мы выбираем количество строк и по каждому из них итерируемся.
        for i in range(number_of_product_lines_in_order):
            # dict_temp - это словарь с данными о заказах
            # dict_temp1 -  это словарь с данными об отгрузках с завода
            # dict_temp_stock_income - это словарь с поступлениями на склад дилера
            dict_order_temp = {}
            # случайно выбираем из товарной номенклатуры товар
            product_id = random.randint(1, 232)
            product_name = df_master_product_catalogue.loc[product_id, 'product_name']
            manufacturer = df_master_product_catalogue.loc[product_id, 'Manufacturer']
            product_group_code = df_master_product_catalogue.loc[product_id, 'Product_group_code']
            product_group_name = df_master_product_catalogue.loc[product_id, 'Product_group_name']
            model_name = df_master_product_catalogue.loc[product_id, 'model_name']
            # в количество вставляем случайное число от 1 до 4
            ordered_qty = random.randint(1, 10)
            # date - это дата из календаря
            order_date = datetime.datetime.strptime(row['date'], "%Y-%m-%d")
            if order_date <= datetime.datetime.now():
                order_id = secrets.token_hex(nbytes=16)
                dict_order_temp['date'] = order_date
                dict_order_temp['order_id'] = order_id
                dict_order_temp['product_id'] = product_id
                dict_order_temp['product_name'] = product_name
                dict_order_temp['manufacturer'] = manufacturer
                dict_order_temp['product_group_code'] = product_group_code
                dict_order_temp['product_group_name'] = product_group_name
                dict_order_temp['model_name'] = model_name
                dict_order_temp['qty'] = ordered_qty
                dict_order_temp['order_balance'] = ordered_qty
                dict_order_temp['action_type'] = 'order'
                result_list_of_dicts.append(dict_order_temp)
                # Добавили строку с заказом по средам
df_orders = pd.DataFrame(result_list_of_dicts).sort_values('date').reset_index()
df_orders.to_csv('data/df_orders.csv')
df_orders_delivery = pd.read_csv('data/df_orders.csv')

result_order_delivery_list_of_dicts = []
for index, row in df_orders_delivery.iterrows():
    temp_date = datetime.datetime.strptime(row['date'], "%Y-%m-%d")
    action_type = row['action_type']
    if action_type == 'empty':
        dict_temp_zero = {}
        dict_temp_zero['date'] = temp_date
        dict_temp_zero['qty'] = 0
        dict_temp_zero['action_type'] = 'empty'
        dict_temp_zero['order_balance'] = 0
        result_order_delivery_list_of_dicts.append(dict_temp_zero)
        continue

    # если action_type не равен empty, значит это order.
    # добавляем исходную строку order
    dict_temp_order = {}
    dict_temp_order['date'] = temp_date
    dict_temp_order['qty'] = row['qty']
    dict_temp_order['action_type'] = 'order'
    dict_temp_order['order_balance'] = row['order_balance']
    dict_temp_order['order_id'] = row['order_id']
    dict_temp_order['product_id'] = row['product_id']
    dict_temp_order['product_name'] = row['product_name']
    dict_temp_order['manufacturer'] = row['manufacturer']
    dict_temp_order['product_group_code'] = row['product_group_code']
    dict_temp_order['product_group_name'] = row['product_group_name']
    dict_temp_order['model_name'] = row['model_name']
    result_order_delivery_list_of_dicts.append(dict_temp_order)

    order_balance = row['order_balance']
    while order_balance > 0:
        dict_temp1 = {}
        # delta - количество дней, которые будем прибавлять к дате заказа для получения даты отгрузки
        delta = datetime.timedelta(days=random.randint(10, 60))
        temp_date = temp_date + delta
        delivery_qty = random.randint(1, order_balance)
        updated_order_balance = order_balance - delivery_qty
        dict_temp1['date'] = temp_date
        dict_temp1['qty'] = -1 * delivery_qty
        dict_temp1['action_type'] = 'delivery'
        dict_temp1['order_id'] = row['order_id']
        dict_temp1['product_id'] = row['product_id']
        dict_temp1['product_name'] = row['product_name']
        dict_temp1['manufacturer'] = row['manufacturer']
        dict_temp1['product_group_code'] = row['product_group_code']
        dict_temp1['product_group_name'] = row['product_group_name']
        dict_temp1['model_name'] = row['model_name']
        dict_temp1['order_balance'] = updated_order_balance
        result_order_delivery_list_of_dicts.append(dict_temp1)
        order_balance = updated_order_balance

df_order_delivery = pd.DataFrame(result_order_delivery_list_of_dicts).sort_values('date').reset_index()
df_order_delivery.to_csv('data/orders_delivery_df.csv')

df_order_delivery_for_stock = pd.read_csv('data/orders_delivery_df.csv')

result_stockin_stockout_list_of_dicts = []
for index, row in df_calendar.iterrows():
    dict_temp_zero = {}
    date = datetime.datetime.strptime(row['date'], "%Y-%m-%d")
    dict_temp_zero['date'] = date
    dict_temp_zero['qty'] = 0
    dict_temp_zero['action_type'] = 'empty'
    dict_temp_zero['order_balance'] = 0
    result_stockin_stockout_list_of_dicts.append(dict_temp_zero)

# итерируемся по датафрему, загруженного заказов - отгрузок из csv
for index, row_df_order_delivery in df_order_delivery_for_stock.iterrows():
    action_type = row_df_order_delivery['action_type']
    if action_type == 'delivery':

        dict_temp_stockin = {}
        stock_in_qty = -1 * row_df_order_delivery['qty']
        temp_date_stockin = datetime.datetime.strptime(row_df_order_delivery['date'], "%Y-%m-%d")
        dict_temp_stockin['date'] = temp_date_stockin
        dict_temp_stockin['order_id'] = row_df_order_delivery['order_id']
        dict_temp_stockin['action_type'] = 'stockin'
        dict_temp_stockin['product_id'] = row_df_order_delivery['product_id']
        dict_temp_stockin['product_name'] = row_df_order_delivery['product_name']
        dict_temp_stockin['manufacturer'] = row_df_order_delivery['manufacturer']
        dict_temp_stockin['product_group_code'] = row_df_order_delivery['product_group_code']
        dict_temp_stockin['product_group_name'] = row_df_order_delivery['product_group_name']
        dict_temp_stockin['model_name'] = row_df_order_delivery['model_name']
        dict_temp_stockin['qty'] = stock_in_qty
        stock_balance = stock_in_qty
        dict_temp_stockin['stock_balance'] = stock_balance
        result_stockin_stockout_list_of_dicts.append(dict_temp_stockin)

        temp_date_stockout = temp_date_stockin
        while stock_balance > 0:
            dict_temp_stockout = {}
            # delta - количество дней, которые будем прибавлять к дате заказа для получения даты отгрузки
            delta = datetime.timedelta(days=random.randint(60, 70))
            temp_date_stockout = temp_date_stockout + delta
            sold_qty = random.randint(1, stock_balance)
            updated_stock_balance = stock_balance - sold_qty
            dict_temp_stockout['date'] = temp_date_stockout
            dict_temp_stockout['qty'] = -1 * sold_qty
            dict_temp_stockout['action_type'] = 'stockout'
            dict_temp_stockout['order_id'] = row_df_order_delivery['order_id']
            dict_temp_stockout['product_id'] = row_df_order_delivery['product_id']
            dict_temp_stockout['product_name'] = row_df_order_delivery['product_name']
            dict_temp_stockout['manufacturer'] = row_df_order_delivery['manufacturer']
            dict_temp_stockout['product_group_code'] = row_df_order_delivery['product_group_code']
            dict_temp_stockout['product_group_name'] = row_df_order_delivery['product_group_name']
            dict_temp_stockout['model_name'] = row_df_order_delivery['model_name']
            dict_temp_stockout['stock_balance'] = updated_stock_balance
            result_stockin_stockout_list_of_dicts.append(dict_temp_stockout)
            stock_balance = updated_stock_balance

df_stockin_stockout = pd.DataFrame(result_stockin_stockout_list_of_dicts).sort_values('date').reset_index()
df_stockin_stockout.to_csv('data/dealer_stockin_stockout.csv')

# погнали делать график сделок
# это вообще просто. Бежим по календарю Для каждой даты случайным образом определяем количество товаров в сделках. и это все.
df_calendar['date'] = pd.to_datetime(df_calendar['date'], infer_datetime_format=True)

df_calendar_deals = df_calendar[df_calendar['date'] < (datetime.datetime.now() + datetime.timedelta(days=120))]
df_calendar_deals = df_calendar_deals[df_calendar_deals['date']>=datetime.datetime.strptime('2021-01-01', "%Y-%m-%d")]
result_deals_list_of_dicts = []
for index, row_calendar in df_calendar_deals.iterrows():
    dict_temp_zero = {}
    date_calendar = row_calendar['date']
    qty = 0

    dict_temp_zero['date'] = date_calendar
    dict_temp_zero['qty'] = 0
    result_deals_list_of_dicts.append(dict_temp_zero)


for index, row_calendar in df_calendar_deals.iterrows():

    #date_calendar = datetime.datetime.strptime(row_calendar['date'], "%Y-%m-%d")
    date_calendar = row_calendar['date']
    # выбираем сколько товаров будет в сделках в этот день.
    number_of_product_lines_in_deals = random.randint(30, 70)
    for i in range(number_of_product_lines_in_deals):
        # случайно выбираем из товарной номенклатуры товар
        product_id = random.randint(1, 232)
        product_name = df_master_product_catalogue.loc[product_id, 'product_name']
        manufacturer = df_master_product_catalogue.loc[product_id, 'Manufacturer']
        product_group_code = df_master_product_catalogue.loc[product_id, 'Product_group_code']
        product_group_name = df_master_product_catalogue.loc[product_id, 'Product_group_name']
        model_name = df_master_product_catalogue.loc[product_id, 'model_name']
        # в количество вставляем случайное число
        deal_qty = random.randint(2, 5)
        deal_row_id = secrets.token_hex(nbytes=16)
        dict_temp_deal = {}
        dict_temp_deal['date'] = date_calendar # deal_snapshot_date - дата сохраненного снапшота
        dict_temp_deal['product_id'] = product_id
        dict_temp_deal['product_name'] = product_name
        dict_temp_deal['manufacturer'] = manufacturer
        dict_temp_deal['product_group_code'] = product_group_code
        dict_temp_deal['product_group_name'] = product_group_name
        dict_temp_deal['model_name'] = model_name
        dict_temp_deal['qty'] = deal_qty
        result_deals_list_of_dicts.append(dict_temp_deal)
df_deals = pd.DataFrame(result_deals_list_of_dicts).sort_values('date')
df_deals.to_csv('data/df_deals.csv')

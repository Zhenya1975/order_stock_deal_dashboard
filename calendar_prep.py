import datetime
import pandas as pd
temp_date = '2020-01-01'
temp_date = datetime.datetime.strptime(temp_date, "%Y-%m-%d")

result_list_of_dict = []
for i in range(2000):
    temp_dict = {}
    temp_dict['date'] = temp_date
    temp_dict['weekday'] = temp_date.weekday()+1
    temp_dict['quarter'] = (temp_date.month -1)//3+1
    result_list_of_dict.append(temp_dict)
    delta = datetime.timedelta(days=1)
    temp_date = temp_date + delta

calendar_df = pd.DataFrame(result_list_of_dict).sort_values('date')
calendar_df.to_csv('data/calendar.csv')




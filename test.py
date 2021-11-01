import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randint(0,11,(10,3)), columns = ['num1','num2','num3'])
df['category'] = ['a','a','a','b','b','b','b','c','c','c']
df = df[['category','num1','num2','num3']]
print(df)

# создали группу
gb = df.groupby('category')

print('группа gb: ', gb) #  распечатать его нельзя ибо это просто объект

gb.apply(lambda grp: grp.sum()) # к этой группе применяется метод lambda

# Grp" - это первый аргумент в лямбда-функции. Мне не нужно ничего указывать для него, поскольку он уже есть, автоматически принимается за каждую группу объекта groupby.
print(gb.groups)
# интересно. В результате я получил словарь. В котором ключ -группа, а в значение передались id-шники строк этой группы
print('1st GROUP:\n', df.loc[gb.groups['a']])
print('SUM of 1st group:\n', df.loc[gb.groups['a']].sum())
print("last row\n", gb.apply(lambda df,a,b: sum(df[a] * df[b]), 'num1', 'num2'))
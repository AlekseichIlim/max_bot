from function import read_repot_file, get_str_stat, get_str_total, get_str_month
from function import get_name_month_old
from utils import file_path_report, file_path_month
import pandas as pd

# df = pd.read_excel(file_path_month)
# print(df)
# print(file_path)
# df = pd.read_excel(file_path, sheet_name='СВОД')

# df.columns = df.iloc[3]
# df.drop(0).reset_index(drop=True)
# df['Эффективное время'] = pd.to_numeric(df['Эффективное время, час'], errors='coerce', downcast=None)
# df['Объем производства'] = pd.to_numeric(df['Объем производства без коры, м3'], errors='coerce',
#                              downcast=None)

# valka = df[(df['"Бирка"'].str.startswith('ВАЛ', na=False)) & (df['Объем производства'] > 0)]
# process = df[(df['"Бирка"'].str.startswith('ПРО', na=False)) & (df['Объем производства'] > 0)]
# ford = df[(df['"Бирка"'].str.startswith('ФОР', na=False)) & (df['Объем производства'] > 0)]
# scid = df[(df['"Бирка"'].str.startswith('СКИ', na=False)) & (df['Объем производства'] > 0)]
#
# valka_gr = (valka.groupby('Оператор\nФИО').agg({'Эффективное время': 'sum',
#                                                  'Объем производства': 'sum'}).reset_index()
#             .rename(columns={'Оператор\nФИО': 'Оператор'}))
# valka_gr['Выработка'] = (valka_gr['Объем производства'] / valka_gr['Эффективное время']).round(1)
# valka_gr['Доля'] = (valka_gr['Объем производства'] / valka_gr['Объем производства'].sum() * 100).round().astype(int)
# valka_gr['Объем производства'] = valka_gr['Объем производства'].round().astype(int)
#
# mask_valka = valka_gr['Оператор'].astype(str).apply(lambda x: not any(char.isdigit() for char in x))
# valka_clean = valka_gr[mask_valka].sort_values('Доля', ascending=False)
#
# valka_dict = valka_clean.to_dict(orient='records')
#
# process_gr = process.groupby('Оператор\nФИО').agg(
# {'Эффективное время': 'sum', 'Объем производства': 'sum'}).reset_index().rename(
# columns={'Оператор\nФИО': 'Оператор'})
# process_gr['Выработка'] = (process_gr['Объем производства'] / process_gr['Эффективное время']).round(1)
# process_gr['Доля'] = (process_gr['Объем производства'] / process_gr['Объем производства'].sum() * 100).round().astype(int)
# process_gr['Объем производства'] = process_gr['Объем производства'].round().astype(int)
#
# mask_process = process_gr['Оператор'].astype(str).apply(lambda x: not any(char.isdigit() for char in x))
# process_clean = process_gr[mask_process].sort_values('Доля', ascending=False)
# process_dict = process_clean.to_dict(orient='records')
# total_process = process_gr['Объем производства'].sum()
#
# ford_gr = (ford.groupby('Оператор\nФИО').agg({'Эффективное время': 'sum',
#                                              'Объем производства': 'sum'}).reset_index()
#            .rename(columns={'Оператор\nФИО': 'Оператор'}))
# ford_gr['Выработка'] = (ford_gr['Объем производства'] / ford_gr['Эффективное время']).round(1)
# ford_gr['Доля'] = (
# ford_gr['Объем производства'] / ford_gr['Объем производства'].sum() * 100).round().astype(int)
# ford_gr['Объем производства'] = ford_gr['Объем производства'].round().astype(int)
#
# mask_ford = ford_gr['Оператор'].astype(str).apply(lambda x: not any(char.isdigit() for char in x))
# ford_clean = ford_gr[mask_ford].sort_values('Доля', ascending=False)
# ford_dict = ford_clean.to_dict(orient='records')
# total_ford = ford_gr['Объем производства'].sum()
#
# if len(scid) > 0:
#     scid_gr = process.groupby('Оператор\nФИО').agg(
#     {'Эффективное время': 'sum', 'Объем производства': 'sum'}).reset_index().rename(
#     columns={'Оператор\nФИО': 'Оператор'})
#     total_scid = scid_gr['Объем производства'].sum()
# else:
#     total_scid = 0
#
# stat_dict = {'Валка': valka_dict, 'Процессоры': process_dict, 'Форвардеры': ford_dict,
#  'Процесс объем': total_process, 'Форд объем': total_ford, 'Скидер объем': total_scid}

# total = read_month_file(file_path_month)
# stat = read_repot_file(file_path_report)
#
# if stat['Скидер объем'] > 0:
#     a = f'Стрелевано: {total['Стрелевано']}(из них скидером {stat['Скидер объем']})'
# else:
#     a = f'Стрелевано: {total['Стрелевано']}'
#
# if total['Пиловочник'] > 0:
#     b = f'(из них пиловочник {total['Пиловочник']}) м3'
# else:
#     b = ' м3'
#
# if total['Напилено харвестер'] > 0:
#     c = f'Напилено: {stat['Процесс объем']}(из них харвестерами {total['Напилено харвестер']}) м3'
# else:
#     c = f'Напилено: {stat['Процесс объем']} м3'
#
#

# name_month = get_name_month_old()
mes_test_oper = """СТАТИСТИКА РАБОТЫ ОПЕРАТОРОВ\nФ.И.О - объем производства,м³ // процент выполненного объема от общего,% //\
 выработка в эффективный час,м³/час\n\nВПМ\nВальщик #1 - 7500 // 25 // 75\nВальщик #2 - 7500 // 25 // 75\n\
Вальщик #3 - 7500 // 25 // 75\nВальщик #4 - 7500 // 25 // 75\n\nПРОЦЕССОРЫ\nОператор #1 - 3750 // 12,5 // 40\n\
Оператор #2 - 3750 // 12,5 // 40\nОператор #3 - 3750 // 12,5 // 40\nОператор #4 - 3750 // 12,5 // 40\nОператор #5 - \
3750 // 12,5 // 40\nОператор #6 - 3750 // 12,5 // 40\nОператор #7 - 3750 // 12,5 // 40\nОператор #8 - 3750 // 12,5 //\
 40\n\nФОРВАРДЕРЫ\nФордист #1 - 3750 // 12,5 // 35\nФордист #2 - 3750 // 12,5 // 35\nФордист #3 - 3750 // 12,5 //\
 35\nФордист #4 - 3750 // 12,5 // 35\nФордист #5 - 3750 // 12,5 // 35\nФордист #6 - 3750 // 12,5 // 35\nФордист #7 -\
 3750 // 12,5 // 35\nФордист #8 - 3750 // 12,5 // 35\n"""

# mes_test_month= f"""{a}{b}\n{c}\n\nВыполнение плана: \
# {total['Выполнение плана']} %\nКоличество сдельных часов: {total['Количество часов']} ч\n\
# Премия: {total['Премия']} %\n\nКоэффициент на ср.объем хлыста: {total['коэфф ср объем']}\nКоэффициент на ср.запас на гектар: \
# {total['коэфф на запас']}\nКоэффициент на выполнение плана: {total['коэфф на план']}\n\
# ОБЩИЙ КОЭФФИЦИЕНТ НА РАСЦЕНКУ: {total['общ коэфф']}\n\nСтоимость сдельного часа: ~{total['стоимость часа']} р."""

# a = get_str_month()
# b = get_str_total(total, stat)
# c = get_str_stat(stat)
# print(a)
# print()
# print(b)
# print()
# print(c)
# print(mes_test)
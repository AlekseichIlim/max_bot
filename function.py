import pandas as pd
from config import dict_months
from datetime import datetime


def get_name_month_old():
    """
    Возвращает название предыдущего месяца
    :return: Строка, название месяца на русском
    """
    num_month = datetime.now().month - 1

    if num_month == 0:
        return dict_months[12]
    else:
        return dict_months[num_month]


def read_repot_file(file_path_report, file_path_month):

    try:
        df = pd.read_excel(file_path_report, sheet_name='СВОД')
        df_month = pd.read_excel(file_path_month)

        df.columns = df.iloc[3]
        df.drop(0).reset_index(drop=True)
        df = df.copy()
        df['Эффективное время'] = pd.to_numeric(df['Эффективное время, час'], errors='coerce', downcast=None)
        df['Объем производства'] = pd.to_numeric(df['Объем производства без коры, м3'], errors='coerce',
                                     downcast=None)

        valka = df[(df['"Бирка"'].str.startswith('ВАЛ', na=False)) & (df['Объем производства'] > 0)]
        process = df[(df['"Бирка"'].str.startswith('ПРО', na=False)) & (df['Объем производства'] > 0)]
        ford = df[(df['"Бирка"'].str.startswith('ФОР', na=False))]
        scid = df[(df['"Бирка"'].str.startswith('СКИ', na=False)) & (df['Объем производства'] > 0)]

        if len(scid) > 0:
            scid_gr = scid.groupby('Оператор\nФИО').agg(
                {'Эффективное время': 'sum', 'Объем производства': 'sum'}).reset_index().rename(
                columns={'Оператор\nФИО': 'Оператор'})
            total_scid = scid_gr['Объем производства'].sum().round().astype(int)
        else:
            total_scid = 0

        valka_gr = (valka.groupby('Оператор\nФИО').agg({'Эффективное время': 'sum',
                                                         'Объем производства': 'sum'}).reset_index()
                    .rename(columns={'Оператор\nФИО': 'Оператор'}))
        valka_gr['Выработка'] = (valka_gr['Объем производства'] / valka_gr['Эффективное время']).round(1)
        valka_gr['Доля'] = (valka_gr['Объем производства'] / valka_gr['Объем производства'].sum() * 100).round().astype(int)
        valka_gr['Объем производства'] = valka_gr['Объем производства'].round().astype(int)

        mask_valka = valka_gr['Оператор'].astype(str).apply(lambda x: not any(char.isdigit() for char in x))
        valka_clean = valka_gr[mask_valka].sort_values('Объем производства', ascending=False)

        valka_dict = valka_clean.to_dict(orient='records')

        process_gr = process.groupby('Оператор\nФИО').agg(
        {'Эффективное время': 'sum', 'Объем производства': 'sum'}).reset_index().rename(
        columns={'Оператор\nФИО': 'Оператор'})
        process_gr['Выработка'] = (process_gr['Объем производства'] / process_gr['Эффективное время']).round(1)
        process_gr['Доля'] = (process_gr['Объем производства'] / process_gr['Объем производства'].sum() * 100).round().astype(int)
        process_gr['Объем производства'] = process_gr['Объем производства'].round().astype(int)

        mask_process = process_gr['Оператор'].astype(str).apply(lambda x: not any(char.isdigit() for char in x))
        process_clean = process_gr[mask_process].sort_values('Объем производства', ascending=False)
        process_dict = process_clean.to_dict(orient='records')
        total_process = process_gr['Объем производства'].sum()

        # ford_gr = (ford.groupby('Оператор\nФИО').agg({'Эффективное время': 'sum',
        #                                              'Объем производства': 'sum'}).reset_index()
        #            .rename(columns={'Оператор\nФИО': 'Оператор'}))
        # ford_gr['Выработка'] = (ford_gr['Объем производства'] / ford_gr['Эффективное время']).round(1)
        # ford_gr['Доля'] = (
        # ford_gr['Объем производства'] / ford_gr['Объем производства'].sum() * 100).round().astype(int)
        # ford_gr['Объем производства'] = ford_gr['Объем производства'].round().astype(int)
        #
        # mask_ford = ford_gr['Оператор'].astype(str).apply(lambda x: not any(char.isdigit() for char in x))
        # ford_clean = ford_gr[mask_ford].sort_values('Объем производства', ascending=False)
        # ford_dict = ford_clean.to_dict(orient='records')
        # total_ford = ford_gr['Объем производства'].sum()

        sum_teleg = int(ford['Объем с корой для ПРОЦ, м3/ Кол-во телег для ФОР, шт'].sum())
        volume_ford = (df_month['Стрелевано'] - total_scid).iloc[0]
        volume_one_teleg = (volume_ford / sum_teleg)
        ford_gr = (ford.groupby('Оператор\nФИО').agg({'Эффективное время': 'sum',
                                                      'Объем с корой для ПРОЦ, м3/ Кол-во телег для ФОР, шт': 'sum'}).reset_index()
                   .rename(columns={'Оператор\nФИО': 'Оператор',
                                    'Объем с корой для ПРОЦ, м3/ Кол-во телег для ФОР, шт': 'Количество телег'}))
        ford_gr['Количество телег'] = ford_gr['Количество телег'].astype(float)
        ford_gr['Объем производства'] = (ford_gr['Количество телег'] * volume_one_teleg).round().astype(int)
        ford_gr['Выработка'] = (ford_gr['Объем производства'] / ford_gr['Эффективное время']).round(1)
        ford_gr['Доля'] = (ford_gr['Объем производства'] * 100 / volume_ford).round().astype(int)
        mask_ford = ford_gr['Оператор'].astype(str).apply(lambda x: not any(char.isdigit() for char in x))
        ford_clean = ford_gr[mask_ford].sort_values('Объем производства', ascending=False)
        ford_dict = ford_clean.to_dict(orient='records')

        stat_dict = {'stat': {'ВПМ': valka_dict, 'Процессоры': process_dict, 'Форвардеры': ford_dict},
         'Процесс объем': total_process, 'Форд объем': volume_ford, 'Скидер объем': total_scid}

        # stat_dict = {'stat': {'Процессоры': process_dict},
        #              'Процесс объем': total_process, 'Форд объем': total_ford, 'Скидер объем': total_scid}

        df_month['общ коэфф'] = df_month['общ коэфф'].round(2)
        month = df_month.to_dict(orient='records')
        month_dict = month[0]

        return stat_dict, month_dict

    except Exception as e:
        print('Ошибка')
    return []


# def read_month_file(file_path):
#
#     df_month = pd.read_excel(file_path)
#     df_month['общ коэфф'] = df_month['общ коэфф'].round(2)
#     month = df_month.to_dict(orient='records')
#     month_dict = month[0]
#     return month_dict


def get_str_month():
    name_month = get_name_month_old()
    mes_month = f'Итоги работы за {name_month.upper()} месяц!'
    return mes_month


def get_str_total(stat_total, stat_oper):

    total = stat_total
    stat = stat_oper

    if stat['Скидер объем'] > 0:
        a = f'Стрелевано: {total['Стрелевано']} из них скидером {stat['Скидер объем']}'
    else:
        a = f'Стрелевано: {total['Стрелевано']}'

    if total['Пиловочник'] > 0:
        b = f', из них пиловочник {total['Пиловочник']} м³'
    else:
        b = ' м³'

    if total['Напилено харвестер'] > 0:
        c = f'Напилено: {stat['Процесс объем']} из них харвестерами {total['Напилено харвестер']} м³'
    else:
        c = f'Напилено: {stat['Процесс объем']} м³'

    mes_total = f"""{a}{b}\n{c}\n\nВыполнение плана: {total['Выполнение плана']} %\nКоличество сдельных часов: \
{total['Количество часов']} ч\nПремия: {total['Премия']} %\n\nКоэффициент на ср.объем хлыста: \
{total['коэфф ср объем']}\nКоэффициент на ср.запас на гектар: {total['коэфф на запас']}\n\
Коэффициент на выполнение плана: {total['коэфф на план']}\nОБЩИЙ КОЭФФИЦИЕНТ НА РАСЦЕНКУ: \
{total['общ коэфф']}\n\nСтоимость сдельного часа: ~{total['стоимость часа']} р."""

    return mes_total


def get_str_stat(stat):

    stat_str = f"СТАТИСТИКА РАБОТЫ ОПЕРАТОРОВ\nФ.И.О - объем\
 производства,м³ // процент выполненного объема от общего,% // выработка в эффективный час,м³/час"
    for k, v in stat['stat'].items():
        stat_str += f'\n\n{k.upper()}'
        for i in v:
            stat_str += f'\n{i['Оператор']} - {i['Объем производства']} // {i['Доля']} // {i['Выработка']}'
    return stat_str

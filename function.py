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
        ######
        EXCLUDE = 'Плотников'

        valka_gr['Фамилия'] = valka_gr['Оператор'].astype(str).str.strip().str.split().str[0]

        valka_gr['_skip'] = valka_gr['Фамилия'].astype(str).str.strip() == EXCLUDE
        df_skip = valka_gr[valka_gr['_skip']]
        df_work = valka_gr[~valka_gr['_skip']]

        def agg_group(g):
            if len(g) == 1:
                return g.iloc[0]
            main = g.loc[g['Объем производства'].idxmax()].copy()
            main['Объем производства'] = g['Объем производства'].sum()
            main['Эффективное время'] = g['Эффективное время'].sum()
            return main

        df_work = (df_work.groupby('Фамилия', group_keys=False).apply(agg_group))

        process_gr = (
            pd.concat([df_work, df_skip]).drop(columns=['_skip']).sort_values('Фамилия').reset_index(drop=True))
        ######
        valka_gr['Выработка'] = (valka_gr['Объем производства'] / valka_gr['Эффективное время']).round(1)
        valka_gr['Доля'] = (valka_gr['Объем производства'] / valka_gr['Объем производства'].sum() * 100).round().astype(int)
        valka_gr['Объем производства'] = valka_gr['Объем производства'].round().astype(int)

        mask_valka = valka_gr['Оператор'].astype(str).apply(lambda x: not any(char.isdigit() for char in x))
        valka_clean = valka_gr[mask_valka].sort_values('Объем производства', ascending=False)

        valka_dict = valka_clean.to_dict(orient='records')

        process_gr = process.groupby('Оператор\nФИО').agg(
        {'Эффективное время': 'sum', 'Объем производства': 'sum'}).reset_index().rename(
        columns={'Оператор\nФИО': 'Оператор'})
        ####
        EXCLUDE = 'Плотников'

        process_gr['Фамилия'] = process_gr['Оператор'].astype(str).str.strip().str.split().str[0]

        process_gr['_skip'] = process_gr['Фамилия'].astype(str).str.strip() == EXCLUDE
        df_skip = process_gr[process_gr['_skip']]
        df_work = process_gr[~process_gr['_skip']]

        def agg_group(g):
            if len(g) == 1:
                return g.iloc[0]
            main = g.loc[g['Объем производства'].idxmax()].copy()
            main['Объем производства'] = g['Объем производства'].sum()
            main['Эффективное время'] = g['Эффективное время'].sum()
            return main

        df_work = (df_work.groupby('Фамилия', group_keys=False).apply(agg_group))

        process_gr = (
            pd.concat([df_work, df_skip]).drop(columns=['_skip']).sort_values('Фамилия').reset_index(drop=True))
        ####
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
        ford_gr = ford_gr[(ford_gr['Объем производства'] > 0)]
        ###
        EXCLUDE = 'Плотников'

        ford_gr['Фамилия'] = ford_gr['Оператор'].astype(str).str.strip().str.split().str[0]

        ford_gr['_skip'] = ford_gr['Фамилия'].astype(str).str.strip() == EXCLUDE
        df_skip = ford_gr[ford_gr['_skip']]
        df_work = ford_gr[~ford_gr['_skip']]

        def agg_group(g):
            if len(g) == 1:
                return g.iloc[0]
            main = g.loc[g['Объем производства'].idxmax()].copy()
            main['Объем производства'] = g['Объем производства'].sum()
            main['Эффективное время'] = g['Эффективное время'].sum()
            return main

        df_work = (df_work.groupby('Фамилия', group_keys=False).apply(agg_group))

        ford_gr = (
            pd.concat([df_work, df_skip]).drop(columns=['_skip']).sort_values('Фамилия').reset_index(drop=True))
        ###
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

    mes_total = f"""{a}{b}\n{c}\nОбъем сухостоя свыше 3%: {total['сухостой']} м³\n\nВыполнение плана: {total['Выполнение плана']} %\nКоличество сдельных часов: \
{total['Количество часов']} ч\nПремия: {total['Премия']} %\n\nКоэффициент на ср.объем хлыста: \
{total['коэфф ср объем']}\nКоэффициент на ср.запас на гектар: {total['коэфф на запас']}\n\
Коэффициент на выполнение плана: {total['коэфф на план']}\nОБЩИЙ КОЭФФИЦИЕНТ НА РАСЦЕНКУ: \
{total['общ коэфф']}\n\nСтоимость сдельного часа\nВПМ: ~{total['стоимость ВПМ']} р.\nПроцессоры: \
~{total['стоимость проц']} р.\nФорвардеры: ~{total['стоимость форд']} р."""

    return mes_total


def get_str_stat(stat):

    stat_str = f"СТАТИСТИКА РАБОТЫ ОПЕРАТОРОВ\nФ.И.О - объем\
 производства,м³ // процент выполненного объема от общего,% // выработка в эффективный час,м³/час"
    for k, v in stat['stat'].items():
        stat_str += f'\n\n{k.upper()}'
        for i in v:
            stat_str += f'\n{i['Оператор']} - {i['Объем производства']} // {i['Доля']} // {i['Выработка']}'
    return stat_str

def get_message_new():

    message = f"""Бот обновлен до версии 1.2\n\nСписок изменений:\n\n1. Добавлена информация об объеме заготовленного \
    сухостоя свыше 3% от общего объема(все что свыше 3% оплачивается на 50% меньше)\n2. Стоимость сдельного часа \
    "разбита" по фазам \n3. В статистике по операторам, исправлено "дублирование" операторов в следствии некорректных \
    данных в рапортах"""

    return message

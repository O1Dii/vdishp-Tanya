import matplotlib

matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt

from patterns import *


def set_input_file(extension, vehicle):
    dfs = DataFrameSingleton()

    if extension == 'csv':
        factory = CsvFactory()
    else:
        factory = JsonFactory()

    if vehicle == 'автобус':
        bus = factory.create_bus()
        dfs.df = bus.get_df()
    else:
        train = factory.create_train()
        dfs.df = train.get_df()

    dfs.df['дата отправления'] = pd.to_datetime(dfs.df['дата отправления'])
    dfs.df['время отправления'] = dfs.df['время отправления'].astype('string')


def get_filtered_df(
        leave,
        arrival,
        leave_date,
        weekend_setting,
        time_start,
        time_end,
        approximation_amount,
        show_plots=True
):
    res_df = DataFrameSingleton().df.copy()

    res_df['hour'] = pd.to_numeric(
        res_df['время отправления'].str.split(n=1, pat=':').str[0]
    )

    res_df = res_df[
        (res_df['hour'] >= time_start) & (res_df['hour'] <= time_end)
    ]
    res_df = res_df.drop(columns='hour')

    if weekend_setting == 'только выходные':
        res_df = res_df[res_df['дата отправления'].dt.dayofweek > 4]

    if weekend_setting == 'только будние':
        res_df = res_df[res_df['дата отправления'].dt.dayofweek < 5]

    if leave:
        res_df = res_df[res_df['вокзал отправления'].str.startswith(leave)]

    if arrival:
        res_df = res_df[res_df['вокзал прибытия'].str.startswith(arrival)]

    if leave_date:
        res_df = res_df[
            res_df['дата отправления'].dt.date <= leave_date
        ].sort_values(
            ['дата отправления', 'время отправления']
        ).tail(approximation_amount)

    if show_plots:
        fig, (ax1, ax2) = plt.subplots(1, 2)

        res_df.groupby('вокзал прибытия').size().plot(ax=ax1,
                                                      kind='pie',
                                                      title='отображение вокзалов')
        ax1.axis(False)

        sorted_df = res_df.sort_values(['дата отправления', 'время отправления'])

        sorted_df['стоимость билетов'].plot(ax=ax2,
                                            title='изменение цен на билеты',
                                            rot=70)
        labels = DataFrameSingleton().df['дата отправления'].dt.strftime('%d:%m')\
                 + \
                 ' ' + \
                 DataFrameSingleton().df['время отправления']
        ax2.set_xticks(range(1, labels.nunique()))
        ax2.set_xticklabels(labels)
        ax2.grid()
        plt.tight_layout()
        plt.show()

    res_df['дата отправления'] = res_df['дата отправления'].astype('string')

    return res_df

# использование паттерна Итератор)
# my_list = MyCollection(DataFrameSingleton().df['стоимость билетов'])
# my_list.sort_items()
#
# for each in my_list:
#     print(each)

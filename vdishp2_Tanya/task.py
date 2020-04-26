import matplotlib
import pandas as pd

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from datetime import date as dd

from patterns import *
from utils import df_not_empty

df = pd.read_csv('data.csv')
publisher = Publisher()


def load_file(format):
    global df

    if format == 'csv':
        df = pd.read_csv('data.csv')
    else:
        df = pd.read_json('data.json')


def run_statistics_module(
        project_name,
        task_name,
        task_id,
        hour_effort,
        executor,
        allow_unassigned_tasks,
        column,
        order_type,
        show_plots=False
):
    global df

    project_name_filter = df['название проекта'].str.startswith(project_name)
    task_name_filter = df['название задачи'].str.startswith(task_name)
    task_id_filter = (df['id задачи'] == task_id) if (task_id != 0) else True
    hour_effort_filter = df['трудоёмкость'] == hour_effort if hour_effort != 0 else True
    executor_filter_values = [executor, '-'] if allow_unassigned_tasks else [executor] if executor else ['[^-]']
    executor_filter = df['исполнитель'].str.match('|'.join(executor_filter_values))

    filtered_df = df[
        project_name_filter &
        task_name_filter &
        task_id_filter &
        hour_effort_filter &
        executor_filter
        ]

    if filtered_df.empty:
        return filtered_df

    if show_plots:
        fig, (ax1, ax2) = plt.subplots(2, 1)

        pie_labels = filtered_df['название проекта'].str.cat(filtered_df['название задачи'], sep=" ")
        pie_plot = filtered_df['трудоёмкость'].plot.pie(
            ax=ax1,
            autopct='%1.1f%%',
            radius=2,
            pctdistance=0.8,
            labeldistance=1.1,
            labels=pie_labels
        )
        pie_plot.set_ylabel('')
        pie_plot.set_title('Отношение трудоёмкости задач', pad=100)

        executors = filtered_df \
            .groupby('исполнитель')['исполнитель'] \
            .count() \
            .reset_index(name='кол-во исполнителей')

        hist_plot = filtered_df.merge(executors, left_on='исполнитель', right_on='исполнитель') \
            .plot.hist(
            ax=ax2,
            x='кол-во исполнителей',
            y='трудоёмкость',
            title='Изменение трудоёмкости к кол-ву исполнителей',
            bins=8
        )
        hist_plot.set_xlabel('трудоёмкость')
        hist_plot.set_ylabel('кол-во исполнителей')
        hist_plot.set_yticks(list(executors['кол-во исполнителей']) + [
            executors['кол-во исполнителей'].max() + 1
        ])

        plt.tight_layout()
        plt.show()

    return filtered_df.sort_values(
        by=column,
        ascending=(order_type == '<')
    ) if column else filtered_df


@df_not_empty(df)
def run_creating_report_module(
        project_name,
        task_name,
        task_id,
        date,
        active_time,
        report_name,
        report_file_type
):
    r_df = df[df['исполнитель'] != '-'].copy()
    r_df['дата'] = date or dd.today()
    r_df['временные затраты'] = active_time
    r_df['остаток трудозатрат'] = r_df['трудоёмкость'].astype(float)

    def create_report(r_df, project_name, task_name, task_id, date, active_time):
        condition = (r_df['название проекта'] == project_name) & \
                    (r_df['название задачи'] == task_name) & \
                    (r_df['id задачи'] == task_id)
        columns = ['дата', 'временные затраты', 'остаток трудозатрат']

        r_df.loc[condition, columns] = [date, active_time, r_df.loc[condition, 'трудоёмкость'] - active_time]

        return r_df[condition]

    def generate_file(df):
        if report_file_type == 'csv':
            df.to_csv(report_name + '.' + report_file_type)
        else:
            df.to_json(report_name + '.' + report_file_type)

    report = create_report(r_df, project_name, task_name, task_id, date, active_time)

    if len(report) != 0:
        generate_file(report)
        return True

    return False

"""Modul with all functions

"""

import requests

from prettytable import PrettyTable

import pygal

from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

import settings as st


def get_stat_from_github(language):
    """Function does request to GitHub for one language(format 'str')

    """
    url = "https://api.github.com/search/repositories?q=language:{}&sort=stars".format(language)
    r = requests.get(url)
    print ("")
    print("Request: ", url)
    if r.status_code == 200:
        print("Status request: OK")
    else:
        print("Status request: not OK")
    lang_stat_dict = r.json()
    return lang_stat_dict

def create_total_dict():
    """Function does requests for list language in settings.py

    """
    total_dict = {}
    print ("")
    print ("------------------")
    print ("Progress requests")
    print ("------------------")
    for language in st.list_languages:
        total_dict [language] = get_stat_from_github(language)
        print (len(total_dict.keys()))
    return total_dict

def process_total_dict(total_dict):
    """Function make list for tables and charts

    """
    counts = []
    langs = list(total_dict.keys())
    for lang in langs:
        counts.append(total_dict[lang]['total_count'])
    x = zip(langs,counts)
    xs = sorted(x, key=lambda tup: tup[1], reverse=True)
    langs = [x[0] for x in xs]
    counts = [x[1] for x in xs]
    return langs,counts

def create_total_count_table(data_count_sorted):
    """Function make table with number of repos on GitHub all languages
    for list from settings.py

    """
    Nn = list(range(len(data_count_sorted[0])))
    Nn = [i + 1 for i in Nn]
    table = PrettyTable()
    column_names = ["Nn", "Language", "Repositories"]

    table.add_column(column_names[0], Nn)
    table.add_column(column_names[1], data_count_sorted[0])
    table.add_column(column_names[2], data_count_sorted[1])

    print ("""
          """)
    print("-----------------------------------------")
    print ("Popularity rating of languages on GitHub")
    print("-----------------------------------------")
    print ("")
    print (table)

def create_total_count_chart(data_count_sorted):
    """Function make chart with number of repos on GitHub for all languges
    for list from settings.py

    """
    my_style = LS('#333366', base_style=LCS)
    chart = pygal.Bar(style=my_style,x_label_rotation=45, show_legend=False)
    chart.title = "Popularity rating of languages on GitHub"
    chart.x_labels = data_count_sorted[0]
    chart.add('',data_count_sorted[1])
    chart.render_to_file('pop_langs.svg')


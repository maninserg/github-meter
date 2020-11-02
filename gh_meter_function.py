"""Modul with all funct:wqions

"""

import requests

import os

import datetime

from prettytable import PrettyTable

import pygal

from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

import time

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
    if len(st.list_languages) <= 10:
        t_sleep = 0
    elif len(st.list_languages) > 10 and len(st.list_languages) <= 20:
        t_sleep = 5

    total_dict = {}
    print ("\n" * 100)
    print ("------------------")
    print ("Progress requests")
    print ("------------------")
    for language in st.list_languages:
        total_dict [language] = get_stat_from_github(language)
        print (len(total_dict.keys()))
        time.sleep(t_sleep)
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
    table.add_column(column_names[2], ['{:,}'.format(int(x)) for x in data_count_sorted[1]])

    print ("""
          """)
    print(table.get_string(title="Numbers of repositories by languages on GitHub"))


def create_total_count_chart(data_count_sorted):
    """Function make chart with number of repos on GitHub for all languges
    for list from settings.py

    """
    create_folder_svg()
    my_style = LS('#333366', base_style=LCS)
    chart = pygal.Bar(style=my_style,x_label_rotation=45, show_legend=False)
    chart.title = "Numbers of repositories by languages on GitHub"
    chart.x_labels = data_count_sorted[0]
    chart.value_formatter = lambda x: '{:,}'.format(int(x))
    chart.add('',data_count_sorted[1])
    chart.render_to_file('./tmp_svg/pop_langs.svg')
    print ("")
    print ("Look bar chart in file './tmp_svg/pop_langs.svg'")
    print ("!!!Attention!!! Open this chart by internt browser for good display")


def print_main_menu():
    """Print main menu to stdout

    """
    print ("\n" * 100)
    print ("--------------------------------")
    print ("Main menu program github-meter")
    print ("--------------------------------")
    print ("")
    print ("1.Show Numbers of Repositories by Language on GitHub")
    print ("2.Show Most-Starred Language Projects on GitHub")
    print("3.Show list 'The 100 most interesting users on GitHub")
    print ("0.Exit")
    print ("")

def print_back_menu():
    """Print menu for come back to main menu

    """
    print ("")
    print ("-----------")
    print ("Navigation")
    print ("-----------")
    print ("1.Back to Main menu")
    print ("0.Exit")
    print ("")

def process_depos_lang(lang_dict):
    """Function processes information about Most-Starred Repos

    """
    repo_dicts = lang_dict['items']
    print ("Repositories returned: ", len(repo_dicts))
    list_name = []
    list_owner = []
    list_stars = []
    list_repo_html = []
    list_descrip = []
    list_created = []
    list_updated = []
    list_forks = []
    for repo_dict in repo_dicts:
        list_name.append(repo_dict['name'])
        list_owner.append(repo_dict['owner']['login'])
        list_stars.append(repo_dict['stargazers_count'])
        list_repo_html.append(repo_dict['html_url'])
        list_descrip.append(repo_dict['description'])
        list_created.append(repo_dict['created_at'])
        list_updated.append(repo_dict['updated_at'])
        list_forks.append(repo_dict['forks_count'])

        list_created = list_date_format(list_created)
        list_updated = list_date_format(list_updated)

    list_repos = [list_name, list_owner, list_stars, list_repo_html,
                  list_descrip, list_created, list_updated, list_forks]
    return list_repos



def output_info_depos(list_repos):
    """Fucnction print information about Most-Starred Pepositories
    of language

    """

    print ("""
         """)
    print("----------------------------------------------")
    print ("Selected information about each repository:")
    print("----------------------------------------------")
    print ("")
    for i in range(len(list_repos[0])):
        print ("Nn: ", i + 1)
        print ("Name: ", list_repos[0][i])
        print ("Owner: ", list_repos[1][i])
        print ("Stars: ", list_repos[2][i])
        print ("Repository: ", list_repos[3][i])
        print ("Description: ", list_repos[4][i])
        print ("Created: ", list_repos[5][i])
        print ("Updated: ", list_repos[6][i])
        print ("Forks count: ", list_repos[7][i])
        print("")

def create_sum_repos_table(list_repos, lang):
    """Function make summary table with info about repositories

    """
    Nn = list(range(len(list_repos[0])))
    Nn = [i + 1 for i in Nn]
    table = PrettyTable()
    column_names = ["Nn", "Name", "Owner", "Stars", "Forks count", "Created", "Updated"]
    table.add_column(column_names[0], Nn)
    table.add_column(column_names[1], list_repos[0])
    table.add_column(column_names[2], list_repos[1])
    table.add_column(column_names[3], ['{:,}'.format(int(x)) for x in list_repos[2]])
    table.add_column(column_names[4], ['{:,}'.format (int(x)) for x in list_repos[7]])
    table.add_column(column_names[5], list_repos[5])
    table.add_column(column_names[6], list_repos[6])

    table.align["Name"] = "l"
    table.align["Owner"] = "l"
    print ("""
          """)
    print(table.get_string(title="Summary table of Most-Starred {} Projects".format(lang.capitalize())))

def create_repos_lang_chart(list_repos, lang):
    """Function make chart with  Most-Starred Repositories

    """
    create_folder_svg()
    my_style = LS('#333366', base_style=LCS)
    chart = pygal.Bar(style=my_style,x_label_rotation=45, show_legend=False)
    chart.title = ("Most-Starred {} Projects on GitHub".format(lang.capitalize()))
    chart.x_labels = list_repos[0]
    plot_dicts = []

    desks = []
    for desk in list_repos[4]:
        if not desk:
            desk = "No description provided"
        desks.append(desk)

    for i in range(len(list_repos[2])):
        plot_dict = {'value' : list_repos[2][i],
                     'label' : desks[i],
                     'xlink' : list_repos[3][i]}
        plot_dicts.append(plot_dict)

    chart.value_formatter = lambda x: '{:,}'.format(int(x))
    chart.add('',plot_dicts)
    chart.render_to_file('./tmp_svg/repos_{}.svg'.format(lang.lower()))
    print ("")
    print ("Look bar chart in file './tmp_svg/repos_{}.svg'".format(lang.lower()))
    print ("!!!Attention!!! Open this chart by internt browser for good display")

def list_date_format(list_date):
    """ Format date, delete information about time

    """
    list_form = []
    for item in list_date:
        ls_split = item.split('T')
        list_form.append(ls_split[0])
    return list_form

def create_folder_svg():
    """Create foder for save svg files

    """
    list_dir = os.listdir(path=".")
    if not "tmp_svg" in list_dir:
        os.mkdir(path="./tmp_svg")

def create_html_report():
    now = datetime.datetime.now()
    print(str(now.year), str(now.month), str(now.day))
    file_report = open("report_langs_{}-{:02d}-{:02d}.html".format(now.year,now.month,now.day), "w")
    file_report.write("<center>")
    file_report.write('<object type="image/svg+xml" data="./tmp_svg/pop_langs.svg"  width="800" height="600" >')
    file_report.write('</object>')
    for lang in st.list_languages:
        file_report.write('<object type="image/svg+xml" data="./tmp_svg/repos_{}.svg"  width="800" height="600" >'.format(lang))
        file_report.write('</object>')
    file_report.write('</center>')
    file_report.close

def get_stat_users():
    """Function does request the 100 most interesting users

    """
    url = "https://api.github.com/search/users?q=followers:>1000&per_page=100&sort=followers"
    r = requests.get(url)
    print ("\n" * 100)
    print("Request: ", url)
    if r.status_code == 200:
        print("Status request: OK")
    else:
        print("Status request: not OK")
    users_dict = r.json()
    return users_dict

def process_users(users_tot_dict):
    """Function processes information about the 100 most interesting users

    """
    users_dicts = users_tot_dict['items']
    print ("Repositories returned: ", len(users_dicts))
    list_login = []
    list_html = []
    for user in users_dicts:
        list_login.append(user['login'])
        list_html.append(user['html_url'])

    list_users = [list_login, list_html]
    return list_users

def create_users_table(list_users):
    """Function make table with the 100 most interesting users on GitHub

    """
    Nn = list(range(len(list_users[0])))
    Nn = [i + 1 for i in Nn]
    table = PrettyTable()
    column_names = ["Nn", "Name", "Link"]
    table.add_column(column_names[0], Nn)
    table.add_column(column_names[1], list_users[0])
    table.add_column(column_names[2], list_users[1])


    table.align["Name"] = "l"
    table.align["Link"] = "l"
    print ("""
          """)
    print(table.get_string(title="The 100 most interesting users on GitHub"))

if __name__ == "__main__":
    users_tot_dict = get_stat_users()
    list_users = process_users(users_tot_dict)
    create_users_table(list_users)


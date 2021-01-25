"""Modul with all funct:wqions

"""

import requests

import os

import datetime

import sqlite3 as sq

from prettytable import PrettyTable

from prettytable import from_db_cursor

import pygal

from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

import time

import settings as st


def get_stat_from_github(language):
    """Function does request to GitHub for one language(format 'str')

    """
    url = ("https://api.github.com/search/repositories?q=language:{}&sort=stars"
           .format(language))
    r = requests.get(url)
    print ("")
    print("Request: ", url)
    if r.status_code == 200:
        print("Status request: " +'\033[92m'+ "OK"+'\033[0m')
    else:
        print("Status request: "+'\033[91m'+"not OK"+'\033[0m')
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
    print ("-----------------")
    print ("Progress requests")
    print ("-----------------")
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


def get_stat_from_database():

    if not "github.db" in os.listdir("./"):
        last_update = "NEVER!!! The database will be created in file './github.db'"
        avl_dates = 0
        avl_langs = 0
    else:
        conn = sq.connect('github.db')
        cursor = conn.execute("SELECT Date FROM languages ORDER BY Date DESC LIMIT 1")
        for row in cursor:
            last_update = row[0]
        cursor = conn.execute("SELECT COUNT(*) FROM dates")
        for row in cursor:
            avl_dates = str(row[0])
        cursor = conn.execute("SELECT COUNT(*) FROM ls_langs")
        for row in cursor:
            avl_langs = str(row[0])
        conn.close()
    return last_update, avl_dates, avl_langs

def print_main_menu():
    """Print main menu to stdout

    """
    stat_database = get_stat_from_database()
    last_update = stat_database[0]
    avl_dates = stat_database[1]
    if last_update == "NEVER!!! The database will be created in file './github.db'":
        ab = "\033[91m"
    else:
        ab = "\033[92m"
    print ("\n" * 100)
    print ("------------------------------")
    print ("Main menu program github-meter")
    print ("------------------------------")
    print ("")
    print("1.Update database")
    print("     The last update of database:", "\033[4m" + ab + last_update +"\033[0m")
    print("     The availible numbers of dates:", "\033[4m" + ab + str(avl_dates) +"\033[0m")
    print("")
    print ("2.Create and show tables and bar charts")
    print("")
    print ("0.Exit")
    print ("")

def print_show_menu():
    stat_database = get_stat_from_database()
    last_update = stat_database[0]
    avl_langs = stat_database[2]
    if last_update == "NEVER!!! The database will be created in file './github.db'":
        ab = "\033[91m"
    else:
        ab = "\033[92m"
    print("\n" * 100)
    print("-------------------------------------")
    print("Create and show tables and bar charts")
    print("-------------------------------------")
    print("")
    print("1. For the last date update:", "\033[4m" + ab + last_update +"\033[0m")
    print("")
    print("2. For the one language from", "\033[4m" + ab + str(avl_langs),"languages" +"\033[0m", "for all dates")
    print("")
    print("3.Main menu")
    print("")
    print("0.Exit")
    print("")

def print_back_menu():
    """Print menu for come back to main menu

    """
    print ("")
    print ("---------------")
    print ("Navigation menu")
    print ("---------------")
    print ("1.Back to Main Menu")
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


def list_date_format(list_date):
    """ Format date, delete information about time

    """
    list_form = []
    for item in list_date:
        ls_split = item.split('T')
        list_form.append(ls_split[0])
    return list_form

def create_database():
    """Create file github.db with tables

    """
    list_dir = os.listdir(".")
    if not "github.db" in list_dir:

        conn = sq.connect("github.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE languages
                       (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       Language TEXT, Repositories INTEGER, Date TEXT)""")
        cursor.execute("""CREATE TABLE repos
                       (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       Name TEXT, Owner TEXT, Stars INTEGER,
                       Forks_count INTEGER, Created TEXT,
                       Updated TEXT, Link_html TEXT,
                       Description TEXT,
                       Language TEXT, Date TEXT)""")
        cursor.execute("""CREATE TABLE dates
                       (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       Date TEXT)""")
        cursor.execute("""CREATE TABLE ls_langs
                       (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       Language TEXT)""")


        conn.commit()

def update_langs_database(dict_langs):
    """Update datebase languages

    """
    conn = sq.connect("github.db")
    cursor = conn.cursor()

    now = datetime.datetime.now()
    date_now = "{}-{:02d}-{:02d}".format(now.year,now.month,now.day)
    date_list = []
    for i in range(len(dict_langs[0])):
        date_list.append(date_now)

    list1 = list(zip(dict_langs[0], dict_langs[1],date_list))
    cursor.executemany("""INSERT INTO languages (Language, Repositories, Date)
                    VALUES (?, ?, ?)""",list1)
    conn.commit()

def update_repos_database(list_repos, lang):
    """Update database repositories

    """
    conn = sq.connect("github.db")
    cursor = conn.cursor()

    now = datetime.datetime.now()
    date_now = "{}-{:02d}-{:02d}".format(now.year,now.month,now.day)
    date_list = []
    for i in range(len(list_repos[0])):
        date_list.append(date_now)
    list_lang = []
    for i in range(len(list_repos[0])):
        list_lang.append(lang)
    list1 =list(zip(list_repos[0], list_repos[1], list_repos[2],
                    list_repos[7], list_repos[5], list_repos[6],
                    list_repos[3], list_repos[4],
                    list_lang, date_list))

    cursor.executemany("""INSERT INTO repos (Name, Owner, Stars, Forks_count,
                       Created, Updated, Link_html, Description, Language, Date)
                    VALUES (?,?,?,?,?,?,?,?,?,?)""",list1)
    conn.commit()

def refresh_table_dates_database():
    conn = sq.connect("github.db")
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE dates""")
    cursor.execute("""CREATE TABLE dates
                   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   Date TEXT)""")
    cursor.execute("""INSERT INTO dates (Date) SELECT DISTINCT Date FROM languages""")
    conn.commit()

def refresh_table_langs_database():
    conn = sq.connect("github.db")
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE ls_langs""")
    cursor.execute("""CREATE TABLE ls_langs
                   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   Language TEXT)""")
    cursor.execute("""INSERT INTO ls_langs (Language) SELECT DISTINCT Language
                   FROM languages""")
    conn.commit()

def create_table_langs():
    """Create and print table with Numbers of Repos all languages

    """
    conn = sq.connect('github.db')
    cursor = conn.execute("SELECT MAX(Date) FROM dates")
    for row in cursor:
        last_update = row[0]
    conn.commit()

    conn = sq.connect("github.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT Language, Repositories FROM languages
                WHERE Date=(SELECT MAX(Date) FROM languages)
                ORDER BY Repositories DESC""")
    my_table = from_db_cursor(cursor)
    my_table.add_column("Nn", [x + 1 for x in range(18)])
    my_table.align["Language"] = "l"
    my_table.align["Nn"] = "l"

    print(my_table.get_string(title="Numbers of Repos on GitHub for {}".format(last_update)))

    conn.commit()

def create_chart_langs():
    langs = []
    repos = []

    conn = sq.connect('github.db')
    cursor = conn.execute("""SELECT Language, Repositories FROM languages
                WHERE Date=(SELECT MAX(Date) FROM languages)
                ORDER BY Repositories DESC""")

    for row in cursor:
        langs.append(row[0])
        repos.append(row[1])
    conn.commit()

    chart = pygal.Bar(st.my_config, style=st.my_style)
    chart.title = "Numbers of Repos on GitHub"
    chart.x_labels = langs
    chart.value_formatter = lambda x: '{:,}'.format(int(x))
    chart.add("",repos)
    chart.render_in_browser()

def create_table_top_repos_all_langs():

    conn = sq.connect('github.db')
    cursor = conn.execute("SELECT MAX(Date) FROM dates")
    for row in cursor:
        last_update = row[0]
    conn.commit()

    conn = sq.connect("github.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT Name, Owner, Stars, Forks_count,
                   Language FROM repos
                WHERE Date=(SELECT MAX(Date) FROM repos)
                ORDER BY Stars DESC LIMIT 20""")
    my_table = from_db_cursor(cursor)
    my_table.add_column("Nn", [x + 1 for x in range(20)])
    my_table.align["Name"] = "l"
    my_table.align["Owner"] = "l"
    my_table.align["Language"] = "l"
    my_table.align["Nn"] = "l"

    print(my_table.get_string(title="TOP 20 Repositories on GitHub for {}".format(last_update)))

    conn.commit()

def create_chart_top_repos_all_langs():
    names= []
    stars = []
    lang  = []
    descrip = []
    link_html = []
    plot_dicts = []


    conn = sq.connect('github.db')
    cursor = conn.execute("""SELECT Name, Stars, Language, Description,
                          Link_html  FROM repos
                          WHERE Date=(SELECT MAX(Date) FROM repos)
                          ORDER BY Stars DESC LIMIT 20""")

    for row in cursor:
        names.append(row[0])
        stars.append(row[1])
        lang.append(row[2])
        descrip.append(row[3])
        link_html.append(row[4])
    conn.commit()

    chart = pygal.Bar(st.my_config, style=st.my_style)
    chart.title = "The TOP 20 Repos on GitHub"
    chart.x_labels = names
    chart.value_formatter = lambda x: '{:,}'.format(int(x))
    for i in range(len(names)):
        plot_dict = {
            'value' : stars[i],
            'label' : lang[i] + " : " + descrip[i],
            'xlink' : link_html[i],
            }
        plot_dicts.append(plot_dict)
    chart.add("",plot_dicts)
    chart.render_in_browser()

def create_table_numrepos_lang_alldates(lang):
    conn = sq.connect("github.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT Date, Repositories FROM languages
                   WHERE Language=:lang
                   ORDER BY Date DESC""", {"lang":lang})
    my_table = from_db_cursor(cursor)

    print(my_table.get_string(title="Numbers of {} Repos on GitHub".format(lang.capitalize())))

    conn.commit()

def create_chart_numrepos_lang_alldates(lang):
    dates = []
    repos = []
    conn = sq.connect('github.db')
    cursor = conn.execute("""SELECT Date, Repositories FROM languages
                   WHERE Language=:lang
                   ORDER BY Date""", {"lang":lang})
    for row in cursor:
        dates.append(row[0])
        repos.append(row[1])
    conn.commit()
    chart = pygal.StackedLine(st.my_config, fill=True)
    #chart = pygal.Bar(st.my_config, style=st.my_style)
    chart.title = ("Changing the number of repositories by date for {}".
                   format(lang.capitalize()))
    chart.x_labels = dates
    chart.value_formatter = lambda x: '{:,}'.format(int(x))
    chart.add("",repos)
    chart.render_in_browser()

def create_table_toprepos_lang_date(lang,date):
    conn = sq.connect("github.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT Name, Owner, Stars, Forks_count FROM repos
                   WHERE Date=:date AND Language=:lang
                   ORDER BY Stars DESC""", {"lang":lang, "date":date})
    my_table = from_db_cursor(cursor)
    my_table.align["Name"] = "l"
    my_table.align["Owner"] = "l"

    my_table.add_column("Nn", [x + 1 for x in range(30)])
    my_table.align["Nn"] = "l"
    print(my_table.get_string(title="TOP {} Repos on GitHub for {}".format(
        lang.capitalize(), date)))

    conn.commit()


def create_table_repo_all_dates(name):

    conn = sq.connect('github.db')
    cursor = conn.execute("""SELECT Name, Owner, Language, Description,
                          Link_html FROM repos
                WHERE Date=(SELECT MAX(Date) FROM repos) AND
                        Name=:name""", {"name" : name})
    for row in cursor:
        Name = row[0]
        Owner = row[1]
        Language = row[2]
        Description = row[3]
        Link_html = row[4]

    conn.commit()

    conn = sq.connect("github.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT Date, Stars, Forks_count FROM repos
                   WHERE Name=:name
                   ORDER BY Date DESC""", {"name": name})
    my_table = from_db_cursor(cursor)

    print("Name: ", Name)
    print("")
    print("Owner: ", Owner)
    print("")
    print("Language: ", Language)
    print("")
    print("Description: ", Description)
    print("")
    print("Link html: ", Link_html)
    print("")
    print("")
    print(my_table.get_string(title="Report {} Repositorie for all dates".format(name)))

    conn.commit()

def create_table_repo_lang_all_dates(lang, name):

    conn = sq.connect('github.db')
    cursor = conn.execute("""SELECT Name, Owner, Language, Description,
                          Link_html FROM repos
                WHERE Date=(SELECT MAX(Date) FROM repos) AND
                        Name=:name""", {"name" : name})
    for row in cursor:
        Name = row[0]
        Owner = row[1]
        Language = row[2]
        Description = row[3]
        Link_html = row[4]

    conn.commit()
    conn = sq.connect("github.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT Date, Stars, Forks_count FROM repos
                   WHERE Name=:name AND Language=:lang
                   ORDER BY Date DESC""", {"name": name, "lang": lang})
    my_table = from_db_cursor(cursor)
    print("Name: ", Name)
    print("")
    print("Owner: ", Owner)
    print("")
    print("Language: ", Language)
    print("")
    print("Description: ", Description)
    print("")
    print("Link html: ", Link_html)
    print("")
    print("")

    print(my_table.get_string(title="Report {} Repositorie for all dates".format(name)))

    conn.commit()

def get_ava_langs():
    langs = []
    conn = sq.connect('github.db')
    cursor = conn.execute("SELECT DISTINCT Language FROM languages")
    for row in cursor:
        langs.append(row[0].capitalize())
    conn.commit()
    return langs

def create_table_ava_langs():
    list_langs = get_ava_langs()
    list_count = [i + 1 for i in range(len(list_langs))]
    table_langs = PrettyTable()
    table_langs.add_column("Nn", list_count)
    table_langs.add_column("Language", list_langs)
    table_langs.align["Language"] = "l"
    print(table_langs.get_string(title="Available Languages"))
    return list_count

def choice_lang():
    list_langs = get_ava_langs()
    list_count = create_table_ava_langs()
    while True:
        nlang = int(input("Your choice(Nn): "))
        if nlang in list_count:
            lang = list_langs[nlang - 1]
            break
    return lang.lower()

def get_ava_dates(lang):
    dates = []
    conn = sq.connect('github.db')
    cursor = conn.execute("""SELECT DISTINCT Date FROM languages
                          WHERE Language =:lang""", {"lang": lang})
    for row in cursor:
        dates.append(row[0])
    conn.commit()
    return dates

def choice_date(lang):
    dates = get_ava_dates(lang)
    while True:
        date = input("Enter date: ")
        if date in dates:
            break
    return date


def get_ava_20repos_all_langs():
    repos = []
    conn = sq.connect('github.db')
    cursor = conn.execute("""SELECT Name, Owner, Stars, Forks_count,
                   Language FROM repos
                WHERE Date=(SELECT MAX(Date) FROM repos)
                ORDER BY Stars DESC LIMIT 20""")
    for row in cursor:
        repos.append(row[0])
    conn.commit()
    return repos

def choice_repo_20_all_langs():

    list_repos = get_ava_20repos_all_langs()
    list_count = [i + 1 for i in range(len(list_repos))]
    while True:
        nrepo = int(input("Your choice(Nn): "))
        if nrepo in list_count:
            repo = list_repos[nrepo - 1]
            break
    return repo

def get_ava_repos_lang_date(date,lang):
    repos = []
    conn = sq.connect('github.db')
    cursor = conn.execute("""SELECT Name, Owner, Stars, Forks_count FROM repos
                          WHERE Date=:date AND Language=:lang
                          ORDER BY Stars DESC""",{"date":date,"lang":lang})
    for row in cursor:
        repos.append(row[0])
    conn.commit()
    return repos

def choice_repo_lang(date, lang):

    list_repos = get_ava_repos_lang_date(date, lang)
    list_count = [i + 1 for i in range(len(list_repos))]
    while True:
        nrepo = int(input("Your choice(Nn): "))
        if nrepo in list_count:
            repo = list_repos[nrepo - 1]
            break
    return repo

if __name__ == "__main__":
    lang = 'java'
    create_chart_numrepos_lang_alldates(lang)


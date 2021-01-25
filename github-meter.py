"""Main module of program github-meter. For start program touch it.

"""
import time

import github_meter_func as fn

import settings as st


k = True
l = False
m = False

while k or l or m:
    fn.print_main_menu()
    key=input("Your choice: ")
    if key == '0':
        print("\n" * 100)
        k = False
    elif key =='1':
        fn.create_database()
        total_dict = fn.create_total_dict()
        data_count_sorted = fn.process_total_dict(total_dict)
        fn.update_langs_database(data_count_sorted)

        for language in st.list_languages:
            lang_dict = total_dict[language]
            list_repos = fn.process_depos_lang(lang_dict)
            fn.update_repos_database(list_repos, language)

        fn.refresh_table_dates_database()
        fn.refresh_table_langs_database()

    elif key == '2':
        fn.print_show_menu()
        l = True
        while l == True:
            key = input ("Your choice: ")

            if key == '0':
                l = False
                k = False
                print("\n" * 100)
            elif key == '3':
                l = False
            elif key == '2':
                print("\n" * 100)
                lang = fn.choice_lang()
                print("\n" * 100)
                fn.create_table_numrepos_lang_alldates(lang)
                date = fn.choice_date(lang)
                fn.create_table_toprepos_lang_date(lang, date)
                repo = fn.choice_repo_lang(date, lang)
                print("\n" * 100)
                fn.create_table_repo_lang_all_dates(lang,repo)

                fn.print_back_menu()
                m = True
                while m == True:
                    key=input("Your choice: ")
                    if key == '0':
                        m = False
                        l = False
                        k = False
                        print("\n" * 100)
                    elif key == '1':
                        l = False
                        m = False

            elif key == '1':
                print("\n" * 100)
                fn.create_table_langs()
                while True:
                    ch = input("Do you want to see bar chart?(y/n):")
                    if ch == 'y':
                        fn.create_chart_langs()
                        break
                    elif ch == 'n':
                        break
                fn.create_table_top_repos_all_langs()
                while True:
                    ch = input("Do you want to see bar chart?(y/n):")
                    if ch == 'y':
                        fn.create_chart_top_repos_all_langs()
                        break
                    elif ch == 'n':
                        break
                repo = fn.choice_repo_20_all_langs()
                print("\n" * 100)
                fn.create_table_repo_all_dates(repo)

                fn.print_back_menu()
                m = True
                while m == True:
                    key=input("Your choice: ")
                    if key == '0':
                        m = False
                        l = False
                        k = False
                        print("\n" * 100)
                    elif key == '1':
                        l = False
                        m = False

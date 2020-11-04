"""Main module of program github-meter. For start program touch it.

"""
import time

import gh_meter_function as fn

import settings as st


k = True
l = False

while k or l:
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
                fn.create_table_numrepos_lang_alldates()
                fn.create_table_top_depos_all_langs()
                fn.create_table_depo_all_dates()
                fn.print_back_menu()
            elif key == '1':
                print("\n" * 100)
                fn.create_table_langs()
                fn.create_table_top_depos_all_langs()
                fn.create_table_repo_all_dates()
                fn.print_back_menu()

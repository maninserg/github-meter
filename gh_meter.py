"""Main module of program github-meter. For start program touch it.

"""
import time

import gh_meter_function as fn

k = True
l = False

while k or l:
    fn.print_main_menu()
    key=input("Your choice: ")
    if key == '0':
        print("\n" * 100)
        k = False
    elif key == '1':
        print ("\n" * 100)
        total_dict = fn.create_total_dict()
        data_count_sorted = fn.process_total_dict(total_dict)
        print ("\n" * 100)
        fn.create_total_count_table(data_count_sorted)

        while True:
            print("")
            ch = input("Do you want to create bar chart? (y/n): ")
            if ch == 'y':
                time.sleep(2)
                fn.create_total_count_chart(data_count_sorted)
                break
            elif ch == 'n':
                time.sleep(1)
                break

        fn.print_back_menu()
        l = True
        while l == True:
            key = input("Your choice: ")
            if key == '0':
                k,l = False, False
                print("\n" * 100)
            elif key == '1':
                l = False

    elif key == '2':
        print ("\n" *100)
        lang = input("How language do you want to see?: " )
        lang.lower()
        fn.get_stat_from_github(lang)

        fn.print_back_menu()
        l = True
        while l == True:
            key = input("Your choice: ")
            if key == '0':
                k,l = False, False
                print("\n" * 100)
            elif key == '1':
                l = False

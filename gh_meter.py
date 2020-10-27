"""Main module of program github-meter. For start program touch it.

"""

import gh_meter_function as fn


while True:
    fn.print_main_menu()
    key=input("Your choice: ")
    if key == '0':
        print("\n" * 100)
        break
    elif key == '1':
        print ("\n" * 100)
        total_dict = fn.create_total_dict()
        data_count_sorted = fn.process_total_dict(total_dict)
        print ("\n" * 100)
        fn.create_total_count_table(data_count_sorted)
        fn.create_total_count_chart(data_count_sorted)
        fn.print_back_menu()
        key=input("Your choice: ")
        while True:
            if key == '1':
                break
            elif key == '0':
                continue
            else:
                key=input("Your choice: ")
            break

"""Main module of program github-meter. For start program touch it.

"""

import gh_meter_function as fn


while True:
    print ("\n" * 100)
    print ("--------------------------------")
    print ("Main menu program github-meter")
    print ("--------------------------------")
    print ("")
    print ("1.Show pop languages on GitHub")
    print ("0.Exit")
    print ("")
    key=input("Your choice: ")
    if key == '0':
        break
    elif key == '1':
        print ("\n" * 100)
        total_dict = fn.create_total_dict()
        data_count_sorted = fn.process_total_dict(total_dict)
        print ("\n" * 100)
        fn.create_total_count_table(data_count_sorted)
        fn.create_total_count_chart(data_count_sorted)
        print("")
        print("1.Back to Main menu")
        print("0.Exit")
        print("")
        key=input("Your choice: ")
        if key == '0':
            break
        elif key == '1':
            continue
        else:
            key=input("Your choice: ")

import gh_meter_function as fn

total_dict = fn.create_total_dict()

data_count_sorted = fn.process_total_dict(total_dict)

fn.create_total_count_table(data_count_sorted)

fn.create_total_count_chart(data_count_sorted)

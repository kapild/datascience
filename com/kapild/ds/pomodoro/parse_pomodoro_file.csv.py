

import csv
import time
delimiter  = ","
header_row_text = "Date,Pomodoro,Count"

def is_row_date(row):
    try:
        return True, time.strptime(row[0], "%Y-%m-%d")
    except ValueError:
        return False, row

def update_dict_with_tasks(prev_date, task_tokens):
    date_key = str(prev_date.tm_year) + "-" + str(prev_date.tm_mon) + "-" + str(prev_date.tm_mday)
    return date_key, task_tokens[1], task_tokens[2]


# this function will parse the csv file from flat pomodoro and output a csv friendly file.
def parse_flat_pomodoro_file(input_csv_file_path, output_file_path):
    with open(output_file_path, 'wb') as csv_write_file:
        csv_writer = csv.writer(csv_write_file, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        with open(input_csv_file_path, 'rb') as csvfile:
            flat_pomo_reader = csv.reader(csvfile, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL,
                                          skipinitialspace=True, quotechar='"')
            if csv_writer is not None and flat_pomo_reader is not None:
                prev_date = None
                for row in flat_pomo_reader:
                    if header_row_text in delimiter.join(row):
                        continue
                    is_date, row_date = is_row_date(row)
                    if is_date:
                        #process date
                        prev_date = row_date
                    else:
                        #process row associated with prev_date
                        out_tokens = update_dict_with_tasks(prev_date, row_date)
                        csv_writer.writerow(out_tokens)











if __name__ == "__main__":
    import sys
    f_path = sys.argv[0]
    f_path = "/Users/kdalwani/code/workspace/datascience/com/kapild/ds/pomodoro/input-flat-pomodoro.csv"
    f_path_out = "/Users/kdalwani/code/workspace/datascience/com/kapild/ds/pomodoro/input-flat-pomodoro_out.csv"

    parse_flat_pomodoro_file(f_path, f_path_out)


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
    return date_key + delimiter + "\"" + task_tokens[1] + "\"" + delimiter + task_tokens[2]


# this function will parse the csv file from flat pomodoro and output a csv friendly file.
def parse_flat_pomodoro_file(input_csv_file_path):
    with open(input_csv_file_path, 'rb') as csvfile:
        flat_pomo_reader = csv.reader(csvfile, delimiter=delimiter,
                                       quoting=csv.QUOTE_MINIMAL,
                                      skipinitialspace=True, quotechar='"')
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
                print str(update_dict_with_tasks(prev_date, row_date))











if __name__ == "__main__":
    import sys
    f_path = sys.argv[0]
    f_path = "/Users/kdalwani/code/workspace/datascience/com/kapild/ds/pomodoro/input-flat-pomodoro.csv"
    parse_flat_pomodoro_file(f_path)
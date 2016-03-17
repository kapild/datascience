

import csv
import time
from time import strftime
delimiter  = ","
header_row_text = "Date,Pomodoro,Count"

def is_row_date(row):
    try:
        return True, time.strptime(row[0], "%Y-%m-%d")
    except ValueError:
        return False, row

def get_date_task_count_csv_tokens(prev_date, task_tokens):
    date_key = strftime("%Y-%m-%d", prev_date)
    return {"Date" : date_key, "Pomodoro": task_tokens[1], "Count" :task_tokens[2]}


# this function will parse the csv file from flat pomodoro and output a csv friendly file.
def parse_flat_pomodoro_file(input_csv_file_path, output_file_path, ignore_tokens_sets):
    with open(output_file_path, 'wb') as csv_write_file:
        csv_writer = csv.DictWriter(csv_write_file, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                fieldnames = header_row_text.split(delimiter))
        with open(input_csv_file_path, 'rb') as csvfile:
            flat_pomo_reader = csv.reader(csvfile, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL,
                                          skipinitialspace=True, quotechar='"')
            if csv_writer is not None and flat_pomo_reader is not None:
                prev_date = None
                csv_writer.writeheader()
                for row in flat_pomo_reader:
                    if header_row_text in delimiter.join(row):
                        continue
                    is_date, row_date = is_row_date(row)
                    if is_date:
                        #process date
                        prev_date = row_date
                    else:
                        #process row associated with prev_date
                        out_tokens = get_date_task_count_csv_tokens(prev_date, row_date)
                        task_name = out_tokens["Pomodoro"].lower()
                        if is_task_ignored(task_name, ignore_tokens_sets):
                            print "Ignoring task and not adding to file:" + task_name
                        else:
                            csv_writer.writerow(out_tokens)



def is_task_ignored(task_name, ignore_token_sets):
    for ignore_token in ignore_token_sets:
        if ignore_token in task_name.lower():
            return True

    return False

def get_tokens_from_file(tokens_file_name):
    ignore_tokens_sets = set()
    f_open = open(tokens_file_name)
    for line in f_open.readlines():
        ignore_tokens_sets.add(line.lower().strip())
    return ignore_tokens_sets


if __name__ == "__main__":
    import sys
    f_path = sys.argv[1]
    ignore_tokens_sets = set()
    if len(sys.argv) > 2:
        ignore_tokens_sets = get_tokens_from_file(sys.argv[2])
    f_path_out = f_path + ".csv_out"

    print "Ignore token sets:" + str(ignore_tokens_sets)
    parse_flat_pomodoro_file(f_path, f_path_out, ignore_tokens_sets)
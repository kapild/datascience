#!/usr/bin/env bash

# this scripts takes in the csv from flatpomodoro app and converts into a format
# which this project can understand.

if [[ $#  < 1 ]] ; then
    echo 'Please provide an input file'
    echo 'usage: ./run_pomodoro_calendar.sh csv_input_file_name [comman_tokens_to_ignore]'
    exit 0
fi


csv_input_file=$1
work_task_remove_comma_file=$2


echo "Reading file:"  $csv_input_file
echo "Ignoring tasks from pomodoro:" work_task_remove_comma_file


echo "Running parse_pomodoro_csv_file: "
python ../../pomodoro/parse_pomodoro_csv_file.py $csv_input_file $work_task_remove_comma_file
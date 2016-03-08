#!/bin/bash
awk -F "," '{print $2}' $1 | sort | uniq -c | sort -rn
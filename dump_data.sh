#!/bin/bash

data_file="/tmp/data.txt"
bin_mysql="/usr/local/mariadb10/bin/mysql"

# python parser_by_csv.py > $data_file
# modify end of $data_file
$bin_mysql -e "drop table my_db.t1"
$bin_mysql -e "create table my_db.t1 (my_time DATE, my_value INT)"
$bin_mysql -e "insert into my_db.t1 (my_time, my_value) values `cat $data_file`"

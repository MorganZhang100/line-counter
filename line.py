#!/usr/bin/env python

import os
import glob
from optparse import OptionParser

def read_line_count(fname):
    count = 0
    for file_line in open(fname).xreadlines():
        count += 1
    return count

def search_current_path(path, r_flag):
    file_count = 0
    line_count = 0

    files = glob.glob(path + os.sep + '*')

    for file in files:
        if os.path.isfile(file):
            line_count += read_line_count(file)
            file_count += 1
        elif r_flag:
            (tem_file_count, tem_line_count) = search_current_path(file, r_flag)
            file_count += tem_file_count
            line_count += tem_line_count

    return (file_count, line_count)

def _main():
    command_parser = OptionParser(usage="%prog [options]", version="%prog 0.1.0", description="Analyze the amount of lines and files under current directory")
    command_parser.add_option("-r", "--recursive", action="store_true", dest="r_flag", default=False, help="make the command act on current directory and their contents recursively")
    (command_options, command_args) = command_parser.parse_args()
    r_flag = command_options.r_flag

    output = 'Search in ' + os.getcwd() + os.sep
    if r_flag:
        output += ' recursively'

    print output

    (file_count, line_count) = search_current_path(os.getcwd(), r_flag)

    print 'file count: %d' % file_count
    print 'line count: %d' % line_count

if __name__ == '__main__':
    _main()
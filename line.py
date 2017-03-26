#!/usr/bin/env python

import os
import glob
from optparse import OptionParser
import fnmatch

__version__ = '0.7.4'


class Line:
    def __init__(self, dir):
        self.raw_select_rule = set()
        self.raw_ignore_rule = set()

        self.final_file = set()
        self.final_file_dic = {}

        self.line_count = 0
        self.file_count = 0

        self.start_dir = dir

        self.rule_on_file = {}

    def get_line_select(self):
        if not os.path.exists('line.select'):
            self.raw_select_rule.add('*')
            return

        for line in open('line.select'):
            if line[0] == '#':
                continue

            if line[len(line) - 1] == '/':
                line = line[:len(line) - 1]

            if line[0] == '!':
                self.raw_ignore_rule.add(line[1:].strip())
            else:
                self.raw_select_rule.add(line.strip())

    def find_files(self, path, mode):
        path = path.replace('[',
                            '[[]')
        # "[" is a special character for Unix style file name matching pattern. If we want to match file name
        # with a "[" in it, we have to add this line.

        search_path = path + os.sep + '*'
        file_and_folder = glob.glob(search_path)

        folders = filter(self.folder_filter, file_and_folder)
        files = filter(self.file_filter, file_and_folder)

        if mode == 'filtrate':
            files = filter(self.select_filter, files)

        for file in files:
            self.add_file(file)

        for folder in folders:
            if mode == 'filtrate':
                if not self.select_filter(folder):
                    if not self.ignore_filter(folder):
                        self.find_files(folder, 'filtrate')
                else:
                    if not self.ignore_filter(folder):
                        self.find_files(folder, 'all')
            else:
                if not self.ignore_filter(folder):
                    self.find_files(folder, 'all')

    def select_filter(self, path):
        should_select = False

        for select_rule in self.raw_select_rule:
            if fnmatch.fnmatch(path, self.start_dir + os.sep + select_rule):
                should_select = True
                break

        return should_select

    def ignore_filter(self, path):
        should_ignore = False

        for ignore_rule in self.raw_ignore_rule:
            if fnmatch.fnmatch(path, self.start_dir + os.sep + ignore_rule):
                should_ignore = True
                break

        return should_ignore

    def file_filter(self, path):
        return os.path.isfile(path)

    def folder_filter(self, path):
        return os.path.isdir(path)

    def add_file(self, file):
        if not self.ignore_filter(file):
            self.final_file.add(os.path.abspath(file))
            self.final_file_dic[file] = self.analyze_file(file)

    def analyze_file(self, file):
        file_line_count = self.read_line_count(file)
        self.line_count += file_line_count
        self.file_count += 1

        return file_line_count

    def read_line_count(self, file_name):
        count = 0
        for file_line in open(file_name):
            count += 1
        return count

    def show_result(self):
        print('file count: %d' % self.file_count)
        print('line count: %d' % self.line_count)

    def show_detail_result(self):
        sorted_list = sorted(self.final_file_dic.items(), key=lambda d: d[0], reverse=False)
        for one_file in sorted_list:
            file_name, file_lines = one_file
            file_name = file_name[len(self.start_dir) + 1:]
            print('%-50s %10s' % (file_name, str(file_lines)))

        self.show_result()

    def get_rule_on_file(self):
        file_path = self.start_dir + os.sep + 'line.select'
        if not os.path.exists(file_path):
            return

        i = 0
        for line in open(file_path):
            self.rule_on_file[i] = line
            i += 1

    def show_rule_on_file(self):
        self.get_rule_on_file()

        if len(self.rule_on_file) == 0:
            print("Not found 'line.select' or no rules in it")
            return

        print("Here are the rules in 'line.select' under " + self.start_dir + os.sep + ":")
        for i in range(0, len(self.rule_on_file)):
            if i in self.rule_on_file:
                print(self.rule_on_file.get(i).strip())

    def add_rule_to_file(self, rule):
        file_path = self.start_dir + os.sep + 'line.select'
        if not os.path.exists(file_path):
            rule_file = open(file_path, "w")
            rule_file.write(rule)
            rule_file.close()
            print('Add successfully')
        else:
            exist = False
            self.get_rule_on_file()
            for r in self.rule_on_file:
                if self.rule_on_file.get(r) == rule:
                    print('This rule already exists')
                    exist = True
                    break

            if not exist:
                rule_file = open(file_path, "a")
                rule_file.write('\n' + rule)
                print('Add successfully')

    def delete_rule_from_file(self, rule):
        file_path = self.start_dir + os.sep + 'line.select'
        if not os.path.exists(file_path):
            print("'line.select' does not exist")
        else:
            exist = False
            about_to_delete_rule_index = -1
            self.get_rule_on_file()
            for r in self.rule_on_file:
                if self.rule_on_file.get(r) == rule:
                    about_to_delete_rule_index = r
                    exist = True
                    break

            if exist:
                del self.rule_on_file[about_to_delete_rule_index]
                rule_file = open(file_path, "w")

                for i in range(0, len(self.rule_on_file) + 1):
                    if self.rule_on_file.has_key(i):
                        rule_file.write(self.rule_on_file.get(i))

                rule_file.close()
                print('Delete successfully')

            if not exist:
                print("This rule doesn't exist")


def _main():
    command_parser = OptionParser(usage="%prog [options] [args]", version="%prog " + __version__,
                                  description="Analyze the amount of lines and files under current directory following the rules in 'line.select' or analyze all files if 'line.select' doesn't exist")
    command_parser.add_option("-d", "--detail", action="store_true", dest="d_flag", default=False,
                              help="show more detail in the result")
    command_parser.add_option("-s", "--show", action="store_true", dest="show_rule_flag", default=False,
                              help="show rules in 'line.select'")
    # command_parser.add_option("-a", "--add", action="store", dest="add_rule_content", type="string",
    #                           help="add a rule to the end of 'line.select'")
    # command_parser.add_option("-d", "--delete", action="store", dest="delete_rule_content", type="string",
    #                           help="delete a rule in 'line.select")

    command_options, command_args = command_parser.parse_args()
    d_flag = command_options.d_flag
    show_rule_flag = command_options.show_rule_flag
    # add_rule_arg = command_options.add_rule_content
    # delete_rule_arg = command_options.delete_rule_content

    a = Line(os.getcwd())

    if show_rule_flag:
        a.show_rule_on_file()
    # elif add_rule_arg is not None:
    #     a.add_rule_to_file(add_rule_arg)
    # elif delete_rule_arg is not None:
    #     a.delete_rule_from_file(delete_rule_arg)
    else:
        print('Search in ' + os.getcwd() + os.sep)

        a.get_line_select()
        a.find_files(os.getcwd(), 'filtrate')

        if d_flag:
            a.show_detail_result()
        else:
            a.show_result()


if __name__ == '__main__':
    _main()

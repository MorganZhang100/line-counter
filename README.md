# line-counter
A command line tool to analyze the amount of lines and files under current directory.   
It supports 'line.select' rules which works like '.gitignore'.

## Installation
You can install, upgrade, uninstall line-counter.py with these commands:
```
$ pip install line-counter  
$ pip install --upgrade line-counter  
$ pip uninstall line-counter  
```

## Usage
```
Usage: line [options] [args]

Analyze the amount of lines and files under current directory following the
rules in 'line.select' or analyze all files if 'line.select' doesn't exist

Options:
  --version     show program's version number and exit
  -h, --help    show this help message and exit
  -d, --detail  show more detail in the result
  -s, --show    show rules in 'line.select'
```

## Example usage and output
Analyze all files (when 'line.select' doesn't exist) or specific files (when 'line.select' exists) under current directory.
```
$ line
Search in /Users/Morgan/Documents/Example/
file count: 4
line count: 839
```
Analyze all files (when 'line.select' doesn't exist) or specific files (when 'line.select' exists) under current directory.  
And show results in detail.
```
$ line -d
Search in /Users/Morgan/Documents/Example/
Dir A/file C.c                                             72
Dir A/file D.py                                           268
file A.py                                                 467
file B.c                                                   32
file count: 4
line count: 839
```
Show the rules in 'line.select'
```
$ line -s
Here are the rules in 'line.select' under /Users/Morgan/Documents/Example/:
#Select rules:
*.c

#Ignore rules:
!Dir A
!*.py
```
Check current version
```
$ line --version
line 0.7.4
```

## line.select
This file works like '.gitignore'.
* Each line is a rule
* Each line starts with a '#' means that's a comment
* Each line starts with a '!' means it's a ignore rule
* Otherwise it's a select rule
* The order of rules is irrelevant and ignore rules can always override select rules
* The rules can find all the pathnames matching a specified pattern according to the rules used by the Unix shell. No tilde expansion is done, but *, ?, and character ranges expressed with [ ] will be correctly matched.

## Roadmap
* Add order output function
* Add option to only count file amount or line amount

## Change Log
* **0.7.4**  03/25/2017  
Fix distribution on PyPI.

* **0.7.3**  03/25/2017  
Fix the long description format on PyPI.

* **0.7.2**  03/25/2017  
Fix a bug that file cannot be matched when there is a '[' in the path.

## Author
I'm Morgan Zhang, a graduate computer science student in University of San Francisco.  

#### Why I made it
I always want to know how many lines of code that I have done, but there isn't a easy way to get it.  
So I decide to make a tool for this.

#### Contact Information
MorganZhang100@gmail.com

## License
The MIT license.

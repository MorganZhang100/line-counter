# line
A command line tool to analyze the amount of lines and files under current directory

## Usage
```
Usage: line [options]

Analyze the amount of lines and files under current directory

Options:
  --version        show program's version number and exit
  -h, --help       show this help message and exit
  -r, --recursive  make the command act on current directory and their
                   contents recursively
```

## Example output

```
$ line --version
line 0.1.0

$ line
Search in <Current Dir Name>
file count: 2
line count: 47

$ line -r
Search in <Current Dir Name> recursively
file count: 4
line count: 1008
```

## Roadmap
* lineignore support, which works like gitignore
* easy installation support

## Author
I'm Morgan Zhang, a graduate computer science student in University of San Francisco.  

#### Why I made it
I always want to know how many lines of code that I have done, but there isn't a easy way to get it.  
So I decide to make a tool for this.

#### Contact Information
MorganZhang100@gmail.com

## License
The MIT license.

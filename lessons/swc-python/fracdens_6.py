import sys
from optparse import OptionParser

def main():
    script, flags, filenames = handle_args(sys.argv)
    try:
        if flags.merge:
            process('all', filenames)
        elif not filenames:
            process('stdin', [])
        else:
            for f in filenames:
                process(f, [f])
    except IOError as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(1)
    except ValueError as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(1)

def handle_args(args):
    script, rest = args[0], args[1:]
    parser = OptionParser()
    parser.add_option('-m', '--merge', dest='merge', help='Merge data from all files', default=False, action='store_true')
    options, args = parser.parse_args(args=rest)
    return script, options, args

def process(name, filenames):
    if len(filenames) == 0:
        number = 1
        width, counts = count_cells(sys.stdin)
    else:
        number = len(filenames)
        with open(filenames[0], 'r') as source:
            width, counts = count_cells(source)
        for f in filenames[1:]:
            with open(f, 'r') as source:
                new_width, new_counts = count_cells(source)
                if new_width != width:
                    template = 'width of {0} is {1}, but width of {2} was {3}'
                    message = template.format(f, new_width, filenames[0], width)
                    raise ValueError(message)
            counts = combine(counts, new_counts)
    report(name, counts, number * width)

def count_cells(source):
    count = []
    for line in source:
        line = line.strip()
        width = len(line)
        count.append(line.count('1'))
    return width, count

def combine(left, right):
    result = []
    for i in range(len(left)):
        result.append(left[i] + right[i])
    return result

def report(name, totals, scale):
    print name
    for num in totals:
        print float(num) / scale

# Run the program.
main()
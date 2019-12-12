from aoc import day5_diagnostic as d5

if __name__ == '__main__':
    fp = './input/day9.txt'
    with open(fp) as f:
        code = [int(x) for x in f.read().strip().split(',')]
    
    # part 1
    input_val = 1 # test mode
    output = d5.intcode_helper(code, input_val)
    if len(output) != 1:
        print('Error codes! {}'.format(output[:-1]))
    else:
        print('No errors!')
        print('BOOST keycode: {}'.format(output[-1]))

        # part 2
        input_val = 2 # sensor boost mode
        output = d5.intcode_helper(code, input_val)
        print('Distress signal coordinates: {}'.format(output))

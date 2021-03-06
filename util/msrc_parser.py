import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

### Output format
# 1st row : request #
# 2nd row : max address
# 3rd row : duration distribution
# time, address, size, op
# op : WRITE (0), READ (1)

### MSRC format
# time, workload name, workload number, type, address, size, response time

TIMEColumn = 0
OPColumn = 3
ADDRESSColumn = 4
SIZEColumn = 5

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, type=str)

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print('[System] File does not exist! %s' % args.input)
        exit(1)

    if os.path.isfile(args.input) and args.input.split('.')[-1] != 'csv':
        print('[System] File is not csv file! %s' % args.input)
        exit(1)
    
    file_list = []
    if os.path.isfile(args.input):
        file_list.append(args.input)
    else:
        for file_name in os.listdir(args.input):
            if file_name.split('.')[-1] == 'csv':
                file_list.append(os.path.join(args.input, file_name))

    for (idx, file_name) in enumerate(file_list):
        max_address = 0
        initial_time = 0
        trace_list = []
        duration_list = []

        with open(file_name, 'r') as input_f:
            previous_time = 0
            for line in input_f.readlines():
                lineArr = line.split(',')
                if initial_time == 0:
                    initial_time = int(lineArr[TIMEColumn])
                time = int(lineArr[TIMEColumn]) - initial_time
                if time != previous_time:
                    duration_list.append(time - previous_time)
                    previous_time = time
                address = lineArr[ADDRESSColumn]
                if max_address < int(address):
                    max_address = int(address)
                size = lineArr[SIZEColumn]
                op = '0'
                if lineArr[OPColumn] == 'Read':
                    op = '1'
                trace_list.append((time, address, size, op))

        scale = [0] * 30
        for d in duration_list:
            tmp = 1
            index = 0
            while d > tmp:
                tmp *= 10
                index += 1
            scale[index] += 1

        with open(file_name.split('.')[0] + '.trace', 'w') as output_f:
            output_f.write('%d\n' % len(trace_list))
            output_f.write('%d\n' % max_address)
            for num in scale:
                output_f.write('%d ' % num)
            output_f.write('\n')
            for (time, address, size, op) in trace_list:
                output_f.write('%d %s %s %s\n' % (time, address, size, op))
        
        print('[System] (%d / %d) %s Finished' % (idx+1, len(file_list), os.path.basename(file_name)))
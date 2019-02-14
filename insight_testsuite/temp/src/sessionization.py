# script which reads log file and sessionize user HTTP requests

import os
import sys
import getopt
import csv
from datetime import datetime

def print_help():
    help_text = \
            """Sorry, help is not ready, yet."""
    print(help_text)

def get_args():
    """Function which gets arguments passed when the script is run at the command line."""

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                'l:p:o:h',
                ['log=', 'period-file=', 'output=', 'help'])

    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    if len(args) > 0:
        print("This function does not take arguments outside options.")
        sys.exit()

    log_file = None
    period_file = None
    output_file = None

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help()
            sys.exit()
        elif opt in ('-l', '--log'):
            log_file = arg
        elif opt in ('-p', '--period'):
            period_file = arg
        elif opt in ('-o', '--output'):
            output_file = arg
        else:
            print('Unhandled option')

    if log_file == None:
        print('Please provide a log file')
        sys.exit()

    if period_file == None:
        print('Please provide a period file')
        sys.exit()

    if output_file == None:
        print('Please provide an output file')
        sys.exit()

    return log_file, period_file, output_file

# the following function is actually not necessary
def get_fields(log):
    """Return tuple of strings corresponding to fields of log file."""
    with open(log, newline='') as logfile:
        reader = csv.reader(logfile)
        return tuple(next(reader))

def get_inactivity(fi):
    """Get inactivity duration from file."""
    with open(fi, 'r') as infile:
        inact_duration = int(infile.read().strip())
    return inact_duration

def time_diff(str1, str2):
    """Return time difference between two date and time strings."""
    fmt = '%Y-%m-%d %H:%M:%S'
    t1 = datetime.strptime(str1, fmt)
    t2 = datetime.strptime(str2, fmt)
    return abs(t1 - t2).seconds + 1

def line_to_dic(line):
    """Take a line from the log from csv.DictReader and return \
a dictionary formatted for output, i.e. a session. \
Use this if IP is not in sessions yet."""
    dic = {}
    dic['ip'] = line['ip']
    dic['first'] = line['date'] + ' ' + line['time']
    dic['last'] = dic['first']
    dic['duration'] = 1
    dic['count'] = 1
    return dic

def update_dic(dic, line):
    """Update dictionary corresponding to an IP from line of log."""
    dic['last'] = line['date'] + ' ' + line['time']
    dic['duration'] = time_diff(dic['first'], dic['last'])
    dic['count'] += 1
    return dic

def current_time(line):
    """Get current time from line of log."""
    current = line['date'] + ' ' + line['time']
    return current

def collect_inactive(line, sessions, current_time, threshold):
    """Collect inactive sessions from the sessions dictionary, then \
sort by increasing last time before returning as a list. Finally, \
remove the inactive keys from the sessions dictionary."""
    # list to append with inactive sessions
    inactive_sessions = []

    # iterate through sessions and append to list if inactive
    for k, v in sessions.items():
        last = v['last']
        if time_diff(last, current_time) > threshold + 1:
            inactive_sessions.append(v)

    # delete inactive sessions
    for i in inactive_sessions:
        del sessions[i['ip']]

    sorted_inactive_sessions = sorted(inactive_sessions, key=lambda k: k['first'])

    return sorted_inactive_sessions

def sessions_to_output(sessions_list):
    """Write list of inactive sessions to output csv file."""
    fields = ['ip', 'first', 'last', 'duration', 'count']
    with open(output_file, 'a', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fields)
        for session in sessions_list:
            writer.writerow(session)

if __name__ == '__main__':
    # get arguments of command line call
    log_file, period_file, output_file = get_args()

    # create output file to append into it later
    with open(output_file, 'w') as outfile:
        pass

    # get inactivaty duration threshold
    t = get_inactivity(period_file)

    # get fields of log file
    fields = get_fields(log_file)

    # dictionary of dictionaries containing sessions
    sessions = {}

    # iterate over lines of log file
    with open(log_file, newline='') as logfile:
        reader = csv.DictReader(logfile)
        for line in reader:
            curr_time = current_time(line)

            # collect inactive sessions and if any, write to output
            if sessions != {}:
                inactive = collect_inactive(line, sessions, curr_time, t)
                if inactive != []:
                    sessions_to_output(inactive)

            # check if current request's IP is in sessions
            # and update if it is
            if line['ip'] in sessions:
                temporary_dic = sessions[line['ip']]
                updated_dic = update_dic(temporary_dic, line)
                sessions[line['ip']] = updated_dic

            else:
                # create a session for this request
                sessions[line['ip']] = line_to_dic(line)

    # when log was processed sort them by increasing start time and write to output
    sorted_leftovers = sorted(sessions.values(), key=lambda k: k['first'])
    sessions_to_output(sorted_leftovers)

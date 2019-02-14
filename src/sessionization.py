from datetime import datetime
import sys
import time

start = time.time()
def edgar_analysis(f1, f2, f3):
    """
    main funtion to record each ip address
    for its access time and count the number
    of documents it downloaded per session.
    f1: filename of log csv
    f2: filename of inactivity txt
    f3: filename of output file
    """

    # First get the time for inactivity from file
    with open(f2, 'r') as f:
        time_lapsed = int(f.read()[0])

    # Open the connection to the output file
    output_file = open(f3, 'w')
    # Open input file
    with open(f1, 'r') as input_file:
        # Read header first
        headers = next(input_file).split(',')
        # Get indexes of the values we are interested in
        indexes_of_fields = {'ip': headers.index('ip'),
                             'date': headers.index('date'),
                             'time': headers.index('time')}
        # Initiate a dictionary to hold the data
        access_data = {}

        # Define some helper functions
        def write_to_file(ip, tf, tl, ts, ct):
            """
            This function writes to the output file
            """
            line = ','.join([ip, tf, tl, str(ts), str(ct)])
            output_file.write(line+'\n')

        def check_all_times():
            """
            This function will check to see if any ip has an
            inactivity of 2 seconds when a new line is read.
            If yes, then write those lines to the output and
            delete the entry from the dictionary
            """
            for key in list(access_data):
                if (timestamp - access_data[key]['time_last']).seconds>time_lapsed:
                    time_in_session = (access_data[key]['time_last']-access_data[key]['time_first']).seconds+1
                    write_to_file(key,
                                  datetime.strftime(access_data[key]['time_first'], '%Y-%m-%d %H:%M:%S'),
                                  datetime.strftime(access_data[key]['time_last'], '%Y-%m-%d %H:%M:%S'),
                                  time_in_session,
                                  access_data[key]['doc_count'])
                    del access_data[key]

        def initiate_dict(ip_address):
            """
            Initiate key values in the dictionary
            """
            access_data[ip_address] = {}
            access_data[ip_address]['time_first'] = timestamp
            access_data[ip_address]['time_last'] = timestamp
            access_data[ip_address]['doc_count'] = 1

        # Read in line by line
        for line in input_file:
            list_temp = line.split(',')
            ip_address = list_temp[indexes_of_fields['ip']]
            date = list_temp[indexes_of_fields['date']]
            time_ = list_temp[indexes_of_fields['time']]
            timestamp = datetime.strptime((date+' '+time_), '%Y-%m-%d %H:%M:%S')

            # First check to see if the ip address is already present
            if ip_address not in access_data.keys():
                initiate_dict(ip_address)
                check_all_times()
            # If ip address is already in the dictionary, check to see how much time has passed
            # If less than the specified inactivity time, then increment document count by 1
            elif (timestamp - access_data[ip_address]['time_last']).seconds <= time_lapsed:
                access_data[ip_address]['time_last'] = timestamp
                access_data[ip_address]['doc_count'] += 1
                check_all_times()
            # If time passed is longer than inactivity time, then terminate the session, write
            # to output and delete the original entry. Initiate a new entry with lastest times
            else:
                time_in_session = (access_data[ip_address]['time_last'] - \
                                   access_data[ip_address]['time_first']).seconds+1
                write_to_file(ip_address,
                              datetime.strftime(access_data[ip_address]['time_first'], '%Y-%m-%d %H:%M:%S'),
                              datetime.strftime(access_data[ip_address]['time_last'], '%Y-%m-%d %H:%M:%S'),
                              time_in_session,
                              access_data[ip_address]['doc_count'])
                del access_data[ip_address]
                check_all_times()
                initiate_dict(ip_address)
        # If reaching EOF, all sessions still in the dictionary will terminate
        # and be written to the output file
        for key, value in access_data.items():
            time_in_session = (value['time_last']-value['time_first']).seconds+1
            write_to_file(key,
                          datetime.strftime(value['time_first'], '%Y-%m-%d %H:%M:%S'),
                          datetime.strftime(value['time_last'], '%Y-%m-%d %H:%M:%S'),
                          time_in_session,
                          value['doc_count'])
    output_file.close()
    end = time.time()
    total_time = end-start
    # Print how many seconds are used to process the file
    print('Used ', total_time, ' seconds')

if __name__ == '__main__':
    edgar_analysis(sys.argv[1], sys.argv[2], sys.argv[3])

from datetime import datetime

def edgar_analysis(time_lapsed):
    with open('../output/sessionization1.txt', 'w') as output_file:
        with open('../input/log.csv', 'r') as input_file:
            headers = next(input_file).split(',')
            indexes_of_fields = {'ip': headers.index('ip'),
                                 'date': headers.index('date'),
                                 'time': headers.index('time')}
            access_data = {}
            for line in input_file:
                if line:
                    list_temp = line.split(',')
                    ip_address = list_temp[indexes_of_fields['ip']]
                    date = list_temp[indexes_of_fields['date']]
                    time = list_temp[indexes_of_fields['time']]
                    timestamp = datetime.strptime((date+''+time).strip(' '), '%Y-%m-%d%H:%M:%S')

                    if ip_address not in access_data.keys():
                        access_data[ip_address] = {}
                        access_data[ip_address]['time_first'] = timestamp
                        access_data[ip_address]['time_last'] = timestamp
                        access_data[ip_address]['doc_count'] = 1
                        for key, value in access_data.items():
                            if (timestamp - value['time_last']).seconds>2:
                                time_in_session = (value['time_last']-value['time_first']).seconds+1
                                output_file.write(','.join([key,
                                                        datetime.strftime(value['time_first'],
                                                                          '%Y-%m-%d%H:%M:%S'),
                                                        datetime.strftime(value['time_last'],
                                                                          '%Y-%m-%d%H:%M:%S'),
                                                        str(time_in_session),
                                                        str(value['doc_count'])])+'\n')
                                del access_data[key]
                    elif (timestamp - access_data[ip_address]['time_last']).seconds <= 2:
                        access_data[ip_address]['time_last'] = timestamp
                        access_data[ip_address]['doc_count'] += 1
                    else:
                        time_in_session = (access_data[ip_address]['time_last'] - \
                                           access_data[ip_address]['time_first']).seconds+1
                        output_file.write(','.join([ip_address,
                                                datetime.strftime(access_data[ip_address]['time_first'],
                                                                  '%Y-%m-%d%H:%M:%S'),
                                                datetime.strftime(access_data[ip_address]['time_last'],
                                                                  '%Y-%m-%d%H:%M:%S'),
                                                str(time_in_session),
                                                str(access_data[ip_address]['doc_count'])])+'\n')
                        access_data[ip_address]['time_first'] = timestamp
                        access_data[ip_address]['time_last'] = timestamp
                else:
                    for key, value in access_data.items():
                        time_in_session = (value['time_last']-value['time_first']).seconds+1
                        output_file.write(','.join([key,
                                                datetime.strftime(value['time_first'],
                                                                  '%Y-%m-%d%H:%M:%S'),
                                                datetime.strftime(value['time_last'],
                                                                  '%Y-%m-%d%H:%M:%S'),
                                                str(time_in_session),
                                                str(value['doc_count'])])+'\n')


if __name__ == '__main__':
    edgar_analysis(2)

import sys
from datetime import datetime, timedelta
import time
import config


def main():

    print("Welcome to PyLog: proudly developed by ClarityAI ")
    print("(Remember to set up your target log file in config.py)")
    print("------------------------------------------------------")
    print("Select type of parsing: ")
    print("   - Batch Log Parsing (1)")
    print("   - Real time Log Parsing (2)")

    while True:
        try:
            action = int(input())

            if action == 1:
                print("Batch Processing selected")
                parse_file()

                break

            elif action == 2:
                print("Real time processing selected")
                parse_file_real_time()

                break

            else:
                print("Not an option. Please enter a number (1 or 2) to choose your action")

        except:
            print("Invalid input. Please enter a number (1 or 2) to choose your action")


def parse_file():

    # Get data from config file
    log_file = config.batch_log_file
    init_datetime = datetime.strptime(config.batch_init_datetime, '%d/%m/%Y-%H:%M:%S')
    end_datetime = datetime.strptime(config.batch_end_datetime, '%d/%m/%Y-%H:%M:%S')
    target_host = config.batch_target_host

    # Read file and save in a list of triplets [timestamp, client, host]
    path_to_log = 'data/' + log_file

    connections = []

    with open(path_to_log, "r") as f:
        for line in f:
            el = line.split()
            try:
                connections.append([datetime.fromtimestamp(int(el[0]) / 1000), el[1], el[2]])
            except:
                print('Cannot append element:' + str(el) + '. Incorrect format')

    # Sort by timestamp. Not necessary due to being roughly sorted
    # connections = sorted(connections, key=lambda x: x[0])

    # Query the connections as configured in config.py
    client_list = [elem[1] for elem in connections
                   if elem[2] == target_host
                   and init_datetime < elem[0] < end_datetime]

    print("List of hosts connected to " + target_host + " between " + str(init_datetime) + " and " + str(end_datetime))
    print(client_list)


def parse_file_real_time():

    # Read the configured real-time file and save in a list of triplets [timestamp, client, host]
    # log_file = 'test.txt'
    log_file = config.rt_log_file
    path_to_log = 'data/' + log_file

    connections = []

    with open(path_to_log) as f:
        while True:

            start_computation_time = time.time()

            lines = f.readlines()
            for line in lines:
                el = line.split()
                try:
                    # Timestamp is in nanoseconds. It must be converted to seconds to make it work
                    connections.append([datetime.fromtimestamp(int(el[0]) / 1000), el[1], el[2]])
                except:
                    print('Cannot append element:' + str(el) + '. Incorrect format')

            # Compute and output the required information
            process_connections(connections)

            end_computation_time = time.time()

            # Sleep for an hour since reading
            total_computation_time = end_computation_time - start_computation_time
            time.sleep(3600 - total_computation_time)


def process_connections(conn):

    configured_host = config.rt_host
    configured_client = config.rt_client

    # Get current time to get last hour logs
    # current_date_time = datetime.now()
    # Since we are still in a testing environment so a dummy date of the test data is used
    current_date_time = datetime.fromtimestamp(int(1565647204351) / 1000 + 60 * 5)

    # Get subset of logs for the last hour
    last_hour_connections = [elem for elem in conn
                             if (current_date_time - timedelta(hours=1)) < elem[0] < current_date_time]
    # print(last_hour_connections)

    # Get user who connected to the configured host in the last hour
    incoming_connections = [elem[1] for elem in last_hour_connections if elem[2] == configured_host]

    print('---------------------------------------------------------------------------------')
    print('List of hostnames connected during the last hour to the configured host: ' + str(configured_host))
    print(incoming_connections)

    # Get hosts who received connection from the configured client in the last hour
    outgoing_connections = [elem[2] for elem in last_hour_connections if elem[1] == configured_client]

    print('---------------------------------------------------------------------------------')
    print('List of hostnames who received connections during the last hour from the configured client: '
          + str(configured_client))
    print(outgoing_connections)

    # Get the client who generated more connections in the last hour
    # First get the list of clients in the last hour
    last_clients = [elem[1] for elem in last_hour_connections]
    # Now get the top one
    top_client = max(last_clients, key=last_clients.count)

    print('---------------------------------------------------------------------------------')
    print('The hostname (CLIENT) that generated most connections in the last hour:')
    print(top_client)
    print('---------------------------------------------------------------------------------')


if __name__ == '__main__':
    # print(sys.argv)
    main()

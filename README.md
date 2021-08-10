# Log-Parser
Basic tool to parse and process connection log files both in batch and real time

## Usage:

- config.py: contains the parameters for the queries performed on the logs. Both for batch and real time options. It was also considered to skip this file and use sys args to specify such data. However this way seems cleaner to users who are not used to working with the terminal.

- main.py: includes the basic code to load, parse and query the log files. It extracts the query data from the config.py file. A simple UI menu is used to select the desired action. The results of the query are printed on the standard output.

- data/: folder containing the log files to process. It must be placed at the same level as the python files.

## Considerations and Assumptions:

The host connecting to another host is refered to as 'client' since it is the machine generating the connection to the second host. This nomenclature allows for easier comprehension. However, they are still hosts.

When listing host/client connections, some hosts/clienys might appear duplicted because they took part in more than one connection. I decided to keep the duplicated since they provide extra information which might be useful in a future. If they are not needed they can be easily deleted easily with user-level tools (Excel).

## Testing:

Some general format testing was carried out and the corresponding try-except clauses were added to handle them. 

In order to test the functionalities, a human readable subset of the data was used. After verifying the functionalities, the complete data set was used to verify no extra errors appeared.

Some extra steps were added to test the real time part. A hard coded date was used intead of the current date in order to test the functionalities. New records were copy/pasted to the test data and saved. Then it was verified that the program was able to read the new records and rerun the computations. The waiting time was reduced to 15 seconds instead of 1 hour. After testing, the code was set back to taking the current time and waiting 1 hour before processing new records as specified.

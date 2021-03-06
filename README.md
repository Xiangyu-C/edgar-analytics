# Edgar Analysis Solution
###  My approach to the problem
This coding challenge asks us to read the log file line by line and by using a
predefined inactivity time to determine how long a session is and how many
documents were accessed by the user (by their IP address) in that session.

Since we are not allowed to read the whole file at once, I read in one line at
a time. After getting the indexes of ip, date, time, I then used those indexes to
get the corresponding values from each line. I decided to use a dictionary to hold
all the information.

The algorithm is very simple:
1. Check if ip is already present in the dictionary, if not, add a new entry
2. In the meantime, check to see if the specified inactivity time has passed for all entries
3. If yes, write those to output and delete those entries
4. If ip is already present, then compare time difference to the length of inactivity time
5. If less or equal, then increment the document count by 1 since it's considered one session
6. If more, then write the previous entry to output, delete it, and enter the new session
7. When reaching EOF, simply write all remaining entries into the output as end of all sessions
---
###  Intructions to run
Simply execute run.sh at terminal and output file will be produced in the output folder.

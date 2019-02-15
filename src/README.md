# Table of contents

1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Improvements](README.md#improvements)

# Problem



# Approach

The general idea is to store sessions read from the log in an **ordered dictionary** to provide a [fast lookup](https://wiki.python.org/moin/TimeComplexity) when searching expired sessions. This ordered dictionary also preserves the order in which sessions start in the log the log. The input data is read line by line, each line is stored in another dictionary which is stored in the *sessions* dictionary. This is implemented with the *DictReader* class from the `csv` module in a `for` loop. For each item of the *sessions* dictionary, the key will be the IP, and the value will be itself a dictionary with keys corresponding to a subset of the requests read from the log (IP, date and time of first request, date and time of last request, duration of session, count of requests).

Since a dictionary can only store unique keys, we look for expired sessions in the *sessions* dictionary and we write them to the output. Since we are using an ordered dictionary and the log file contains data in chronological order, the condition of writing sessions in the same order as the user's first request is fulfilled.

We are then in front of two possibilities, either the current request is part of an ongoing session or it starts a new session. In the first case, there will be a session for this ID in the *sessions* dictionary and we update this session by changing the time of last request, the duration and increment the request count by 1. In the second case there will be no session and we add this session to the *sessions* dictionary.

When we reach the end of the log, we write the remaining sessions to the output.

# Improvements

This script runs with a time complexity of $O(n^2)$ since we iterate through the log elements then through the *sessions* elements to find expired sessions. If we could iterate through all sessions after they are added to the dictionary, this would decrease the time complexity to $O(n)$. To achieve this, using a unique *sessions* dictionary key for each session with the same IP may allow us to aggregate requests into sessions in a single loop after reading log data.

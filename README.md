Installation:
------------

Clone the repository or download the zip

Simple Python command line tool to count up the number of chat messages within interval time periods. 
Potential use cases are finding action clips based on volume of chat. 

Dependencies are requests, dateutil.parser, datetime, pandas, sys

Input:
-----------

Input: Python hello.py VodID ClientID Interval

Interval is time in seconds, (i.e. 5 minutes is 360 etc)

Output:
-----------
Output:file in downloads named 'Vod'+VodID+'chat'.csv

# PyPing_tool

This is a modified version of multithreaded ping that can be used to monitor monitor ping stats for multiple hosts during some testing.

To start pinging:  

1. Create a file with ip addresses/host names to ping. For example  
```
cat ./ip_to_ping.txt 
8.8.8.8
127.0.0.1
1.2.3.4
arista.com
google.com
```

2. Start the tool.  
```
./PyPing_tool.py -f ip_to_ping.txt
```

3. Select a ping command to use.
![](select-ping-mode.jpg)

4. Tool will create a log file with ping stats in the working directory.

5. Stats will be displayed in real time.
![](ping-running.jpg)

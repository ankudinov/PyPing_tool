# PyPing_tool

This is a modified version of multithreaded ping that can be used to monitor monitor ping stats for multiple hosts during some testing.

To start pinging:  


* Create a file with ip addresses/host names to ping. For example

```
cat ./ip_to_ping.txt 
8.8.8.8
127.0.0.1
1.2.3.4
arista.com
google.com
```

* Start the tool.
```
./PyPing_tool.py -f ip_to_ping.txt
```

* Select a ping command to use.
![](select-ping-mode.jpg)

* Tool will create a log file with ping stats in the working directory.
```
<etc.>
INFO:root:Entering cycle #7 at 2017-01-18::14:16:56.103454
INFO:root:                    arista.com : Received:               8, Loss:               0, Transmitted:               8
INFO:root:    some-non-existing-hostname : Received:               0, Loss:               8, Transmitted:               8
INFO:root:                       1.2.3.4 : Received:               0, Loss:               8, Transmitted:               8
INFO:root:                    google.com : Received:               8, Loss:               0, Transmitted:               8
INFO:root:                       8.8.8.8 : Received:               8, Loss:               0, Transmitted:               8
INFO:root:                     127.0.0.1 : Received:               8, Loss:               0, Transmitted:               8
INFO:root:Leaving cycle #7 at 2017-01-18::14:16:56.668228
INFO:root:Entering cycle #8 at 2017-01-18::14:16:56.668296
INFO:root:                    arista.com : Received:               9, Loss:               0, Transmitted:               9
INFO:root:    some-non-existing-hostname : Received:               0, Loss:               9, Transmitted:               9
INFO:root:                       1.2.3.4 : Received:               0, Loss:               9, Transmitted:               9
INFO:root:                    google.com : Received:               9, Loss:               0, Transmitted:               9
INFO:root:                       8.8.8.8 : Received:               9, Loss:               0, Transmitted:               9
INFO:root:                     127.0.0.1 : Received:               9, Loss:               0, Transmitted:               9
INFO:root:Leaving cycle #8 at 2017-01-18::14:16:57.235941
<etc.>
```

* Stats will be displayed in real time.
![](ping-running.jpg)

Exit by pressing Q at any time.

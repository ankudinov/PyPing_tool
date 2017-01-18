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
INFO:root:Entering cycle #70 at 2017-01-18::13:58:32.281629
INFO:root:     arista.com : Received:              71, Loss:               0, Transmitted:              71
INFO:root:some-non-existing-hostname : Received:               0, Loss:              71, Transmitted:              71
INFO:root:        1.2.3.4 : Received:               0, Loss:              71, Transmitted:              71
INFO:root:     google.com : Received:              71, Loss:               0, Transmitted:              71
INFO:root:        8.8.8.8 : Received:              71, Loss:               0, Transmitted:              71
INFO:root:      127.0.0.1 : Received:              71, Loss:               0, Transmitted:              71
INFO:root:Leaving cycle #70 at 2017-01-18::13:58:32.843859
INFO:root:Entering cycle #71 at 2017-01-18::13:58:32.843914
INFO:root:     arista.com : Received:              72, Loss:               0, Transmitted:              72
INFO:root:some-non-existing-hostname : Received:               0, Loss:              72, Transmitted:              72
INFO:root:        1.2.3.4 : Received:               0, Loss:              72, Transmitted:              72
INFO:root:     google.com : Received:              72, Loss:               0, Transmitted:              72
INFO:root:        8.8.8.8 : Received:              72, Loss:               0, Transmitted:              72
INFO:root:      127.0.0.1 : Received:              72, Loss:               0, Transmitted:              72
INFO:root:Leaving cycle #71 at 2017-01-18::13:58:33.410016
<etc.>
```

* Stats will be displayed in real time.
![](ping-running.jpg)

Exit by pressing Q at any time.

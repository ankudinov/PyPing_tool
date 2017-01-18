#!/usr/bin/env python

from threading import Thread
from Queue import Queue
import subprocess
from time import time as time                   # used in: time_stamp()
from datetime import datetime as datetime       # used in: time_stamp()
import os
import curses
import logging
import argparse


__author__ = 'Petr Ankudinov'


class Ping(Thread):
    """
    The class allows to ping an IP address in a thread using a command supported by OS.
    Output will be redirected from stdout, stderr to what is specified by stdin_out parameter.
    Usually stdin_out is os.devnull to hide any messages that can break terminal behaviour.
    """

    def __init__(self, queue_ip, queue_reachable, queue_unreachable, stdin_out, mode='mac_os_ping'):
        Thread.__init__(self)
        self.queue_ip = queue_ip  # queue of IP addresses to ping
        self.queue_reachable = queue_reachable  # queue of reachable IP addresses
        self.queue_unreachable = queue_unreachable  # queue of unreachable IP addresses
        self.inout = stdin_out  # to redirect stdin/stdout, used to hide any messages by redirecting to os.devnull
        self.mode = mode  # ping type to use, see cmd_dict below

    def run(self):

        try:
            ip = self.queue_ip.get(timeout=0.1)    # timeout is critical to avoid thread stuck due to empty queue
        except Exception as _:
            ip = None

        # OS specific ping command to use
        cmd_dict = {
            'mac_os_ping': 'ping -c 1 -i 0.25 -W 300 -t 1 %s',
            'linux_ping': 'ping -c 1 -W 1 -w 1 %s',
            'fping': 'fping -c 1 -t 250 -q %s',
        }

        cmd = cmd_dict[self.mode] % ip

        if ip:
            try:
                # if ping initiated by subprocess was successful, res should be > 0
                # any errors or massages will be redirected from stdout/stderr to os.devnull or something else
                res = subprocess.call(cmd.split(), stdout=self.inout, stderr=self.inout, close_fds=True)
            except Exception as _:
                self.queue_unreachable.put(ip)
            else:
                if res is not 0:
                    self.queue_unreachable.put(ip)
                else:
                    self.queue_reachable.put(ip)

            self.queue_ip.task_done()
        else:
            pass  # if there is no ip in the queue, do nothing


def check_if_pingable(ip_list, ping_type='mac_os_ping'):
    """
    Check what IP addresses from the list are reachable
    :param ip_list: list of IP addresses/host names to ping
    :param ping_type: switch between ping commands
    :return: list of reachable and unreachable hosts
    """

    queue_ip = Queue()
    queue_reachable = Queue()
    queue_unreachable = Queue()

    reachable = []
    unreachable = []

    for ip in ip_list:
        queue_ip.put(ip)  # build a queue to be used by threads

    dev_null = open(os.devnull, 'w')  # redirect any errors and messages from OS here

    while not queue_ip.empty():
        for x in range(50):  # max 50 threads will be initiated at once
            if not queue_ip.empty():
                worker = Ping(queue_ip, queue_reachable, queue_unreachable, dev_null, mode=ping_type)
                worker.daemon = True
                worker.start()

    worker.join(timeout=0.05)  # to prevent error due to daemon threads on interpreter exit
    queue_ip.join()

    while not queue_reachable.empty():
        reachable.append(queue_reachable.get())

    while not queue_unreachable.empty():
        unreachable.append(queue_unreachable.get())

    dev_null.close()

    return reachable, unreachable


def time_stamp():
    """
    time_stamp function can be used for debugging or to display timestamp for specific event to a user
    :return: returns current system time as a string in Y-M-D H-M-S format
    """
    """
    :return:
    """
    time_not_formatted = time()
    time_formatted = datetime.fromtimestamp(time_not_formatted).strftime('%Y-%m-%d::%H:%M:%S.%f')
    return time_formatted


def read_ip_from_file(filename):
    data = open(filename, mode='r')
    list_to_ping = [line.strip() for line in data]
    data.close()
    return list_to_ping


def get_addresses_to_ping():
    """
    Get file with IPs/host names to ping from a CLI argument and build a list.
    :return: list of hosts to ping
    """
    parser = argparse.ArgumentParser(description='J2parser tool.', epilog='Thank you for using help!')
    parser.add_argument('-f', '--filename', help='Name of a file with a list of IP addresses/names to ping.')
    args = parser.parse_args()
    ip_list = read_ip_from_file(args.filename)
    return ip_list


def ask_for_ping_type():
    # init curses
    scr = curses.initscr()
    scr.border(0)
    curses.noecho()
    curses.cbreak()
    scr.keypad(1)

    scr.addstr(3, 2, 'Select ping type:')
    scr.addstr(5, 3, '1. Mac OS ping: ping -c 1 -i 0.25 -W 300 -t 1 <IP/NAME>')
    scr.addstr(6, 3, '2. Linux ping: ping -c 1 -W 1 -w 1 <IP/NAME>    NOTE: No subsecond!')
    scr.addstr(7, 3, '3. fping: fping -c 1 -t 250 -q <IP/NAME>    NOTE: use apt-get or yum to install.')
    ch = scr.getch()

    scr.clear()

    # restore terminal state
    scr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

    if ch == ord('1'):
        ping_type = 'mac_os_ping'
    elif ch == ord('2'):
        ping_type = 'linux_ping'
    elif ch == ord('3'):
        ping_type = 'fping'
    else:
        ping_type = 'mac_os_ping'  # default mode to use
    # add exit here

    return ping_type


def main_loop():

    pt = ask_for_ping_type()  # ask user, what command should be used by script

    status = {}  # a dictionary to keep ping stats
    ip_list = get_addresses_to_ping()
    for ip in ip_list:
        status[ip] = {'reachable': 0, 'unreachable': 0, 'total': 0}  # initial stats

    # init curses
    scr = curses.initscr()
    scr.border(0)
    curses.noecho()
    curses.cbreak()
    scr.keypad(1)
    scr.nodelay(1)  # change getch to unblocking

    # open log file
    log_filename = 'PyPing-' + str(time_stamp()) + '.log'
    logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)

    cycle_number = 0

    while True:  # execute until user will press the button
        # log start of ping cycle
        logging.info('Entering cycle #' + str(cycle_number) + ' at ' + str(time_stamp()))
        ch = scr.getch()
        if (ch == ord('q')) or (ch == ord('Q')):  # break on q button press
            # restore terminal settings
            scr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            # log exit time
            logging.info('Breaking at cycle #' + str(cycle_number) + ' at ' + str(time_stamp()))
            break

        reachable, unreachable = check_if_pingable(ip_list, ping_type=pt)  # run ping threads

        string_number = 1  # used to position messages on curses terminal

        for ip in status.keys():  # update stats for every IP in status dictionary
            if ip in reachable:
                status[ip]['reachable'] += 1
            if ip in unreachable:
                status[ip]['unreachable'] += 1
            status[ip]['total'] += 1

            # display updated stats for every IP
            scr.addstr(string_number, 2, '%30s : Received: %15s, Loss: %15s, Transmitted: %15s' % (ip, status[ip]['reachable'], status[ip]['unreachable'], status[ip]['total']))
            # save stats in a log file
            logging.info('%30s : Received: %15s, Loss: %15s, Transmitted: %15s' % (ip, status[ip]['reachable'], status[ip]['unreachable'], status[ip]['total']))

            string_number += 1

        scr.addstr(string_number + 3, 2, 'Timestamp: ' + str(time_stamp()))
        scr.addstr(string_number + 5, 2, 'Use tail -f to monitor the log in real time.')
        scr.addstr(string_number + 6, 2, 'NOTE: if you see significant loss for many hosts, check ping mode.')
        scr.addstr(string_number + 7, 2, "PRESS 'Q' to exit.")

        scr.refresh()
        logging.info('Leaving cycle #' + str(cycle_number) + ' at ' + str(time_stamp()))

        cycle_number += 1


if __name__ == '__main__':
    # execute main loop
    main_loop()

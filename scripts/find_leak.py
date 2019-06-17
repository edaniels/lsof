import datetime
import subprocess
import sys
import time

fd_to_type = {}
while True:
        p = subprocess.Popen('lsof -P -p ' + sys.argv[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        num_dead = 0
        for line in iter(p.stdout.readline, ''):
                parts = line.split()
                fd = parts[3]
                sock_type = parts[4]
                if fd not in fd_to_type: #register
                        # fd_to_type[fd] = {'type': sock_type, 'name': parts[-2], 'dead': sock_type == 'sock', 'dead_since': datetime.datetime.now()}
                        fd_to_type[fd] = {'type': sock_type, 'name': parts[-2], 'dead': False}
                elif fd_to_type[fd]['dead'] and sock_type != 'sock': # no longer sock
                        fd_to_type[fd]['dead'] = False  
                elif fd_to_type[fd]['dead']:
                        now = datetime.datetime.now()
                        delta = (now-fd_to_type[fd]['dead_since']).total_seconds()
                        num_dead += 1
                        print 'leak', fd, fd_to_type[fd]['type'], '->', sock_type, '(', fd_to_type[fd]['name'], ') (DEAD) for', delta, 's'
                elif fd_to_type[fd]['type'] != sock_type and sock_type == 'sock':
                        fd_to_type[fd]['dead'] = True
                        fd_to_type[fd]['dead_since'] = datetime.datetime.now()
        retval = p.wait()
        print 'num_dead', num_dead
        time.sleep(5)

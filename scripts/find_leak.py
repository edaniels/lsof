import subprocess
import time
import sys

fd_to_type = {}
while True:
        p = subprocess.Popen('lsof -P -p ' + sys.argv[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, ''):
                parts = line.split()
                fd = parts[3]
                sock_type = parts[4]
                if fd not in fd_to_type: #register
                        fd_to_type[fd] = {'type': sock_type, 'name': parts[-2], 'dead': sock_type == 'sock'}
                elif fd_to_type[fd]['dead'] and sock_type != 'sock': # no longer sock
                        fd_to_type[fd]['dead'] = False  
                elif fd_to_type[fd]['dead']:
                        print 'leak', fd, fd_to_type[fd]['type'], '->', sock_type, '(', fd_to_type[fd]['name'], ') (DEAD)'      
                elif fd_to_type[fd]['type'] != sock_type and sock_type == 'sock':
                        fd_to_type[fd]['dead'] = True
        retval = p.wait()
        time.sleep(5)

"""
Move Ordering Spy

It is a python script that will attempt to measure the effects of move ordering
changes in a computer chess engine. It subjects the engine to a set of test
positions and record how many are solved and how fast.

"""

import getopt
import sys
import re
import os
import subprocess
import logging
import time


APP_NAME = "Move Ordering Spy"
APP_VER = "1.1"


def get_engine_id_name(engineName):
    """ Return engine id name """
    logging.info('Run engine to get its id name ...')
    p = subprocess.Popen(engineName, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.stdin.write("uci\n")
    logging.info('>> uci')
    for eline in iter(p.stdout.readline, ''):
        eline = eline.strip()
        logging.info('<< %s' % (eline))
        if 'id name' in eline:
            eng_name_id = ' '.join(eline.split()[2:])
        if "uciok" in eline:
            break
    # Quit the engine
    p.stdin.write("quit\n")
    logging.info('>> quit\n')
    p.communicate()

    return eng_name_id


def analyze_fen(engineName, fen, hashv, threadsv, sdepth = 8):
    """ Return bestmove and time elapsed """
    bestmove = None
    timev = None
    time_elapsed = 0
    logging.info('Running engine to analyze position ...')
    
    p = subprocess.Popen(engineName, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.stdin.write("uci\n")
    logging.info('>> uci')
    for eline in iter(p.stdout.readline, ''):
        eline = eline.strip()
        if "uciok" in eline:
            logging.info('<< uciok')
            break
    
    p.stdin.write("setoption name Hash value " + str(hashv) + "\n")
    p.stdin.write("setoption name Threads value " + str(threadsv) + "\n")

    logging.info('>> setoption name Hash value %d' % (hashv))
    logging.info('>> setoption name Threads value %d' % (threadsv))
    
    p.stdin.write("isready\n")
    logging.info('>> isready')
    
    for rline in iter(p.stdout.readline, ''):
        rline = rline.strip()
        logging.info('<< %s' % (rline))
        if "readyok" in rline:
            break
    p.stdin.write("ucinewgame\n")
    p.stdin.write("position fen " + fen + "\n")
    
    logging.info('>> ucinewgame')
    logging.info('>> position fen %s' % (fen))
    
    p.stdin.write("go depth %d\n" %(sdepth))
    logging.info('>> go depth %d' %(sdepth))

    # Record time for engines that do not sent time info
    time_start = time.clock()

    # Parse engine output
    for eline in iter(p.stdout.readline, ''):        
        eo = eline.strip()
        if "depth" in eo and "score" in eo and "time" in eo and "pv" in eo\
               and not "lowerbound" in eo and not "upperbound" in eo:
            logging.info('<< %s' %(eo))
            b = eo.split(' ')
            i = b.index("time")
            timev = int(b[i+1])
        # Also display line info even if there are no time info
        elif "depth" in eo and "score" in eo and "pv" in eo\
               and not "lowerbound" in eo and not "upperbound" in eo:
            logging.info('<< %s' %(eo))
            
        if "bestmove" in eo:
            logging.info('<< %s' %(eo))
            bestmove = ' '.join(eo.split()[1:2])
            time_elapsed = time.clock() - time_start
            break            

    # Quit the engine
    p.stdin.write("quit\n")
    logging.info('>> quit')
    p.communicate()

    # Use time_elapsed if engine does not send time info
    if timev is None:
        logging.warning('This engine does not send time info!!')
        logging.info('Wall clock elapsed time will be used.')
        if time_elapsed == 0:
            logging.warning('This engine searches faster, time elapsed is zero!!')
            logging.info('Perhaps consider increasing the search depth.')
        timev = time_elapsed * 1000  # Convert time_elapsed to ms

    logging.info('best time %d' %(timev))

    return bestmove, timev
           

def delete_file(fn):
    if os.path.isfile(fn):
        os.remove(fn)


def count_position(fn):
    """ Read epd file and returns number of lines """
    cnt = 0
    with open(fn, 'r') as f:
        for lines in f:
            cnt += 1

    return cnt


def usage():
    """ Sample command line and options """
    print('Usage:')
    print('app_name --engine sf8.exe --epd sts.epd --depth 12 --logging 1')
    print('Options:')
    print('--engine <engine file>')
    print('--epd <epd file>')
    print('--depth <search depth> default is 8')
    print('--logging <1 or 0> default is 0')
    print('--hash <value in mb> default is 64')
    print('--threads <number> default is 1')    
    

def main(argv):

    print('%s v%s\n' %(APP_NAME, APP_VER))

    sEngine = None
    epd_input_fn = None
    depth = 8
    islogging = 0
    summary_fn = 'mos_summary.txt'
    nHash = 64
    nThreads = 1
    total_pts = 0
    total_time = 0
    max_epd_points = 0

    # Read command line options
    try:
        opts, args = getopt.getopt(argv, "e:f:d:l:", ["engine=", "epd=", "depth=", "logging=", "hash=", "threads="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-e", "--engine"):
            sEngine = arg
        elif opt in ("-f", "--epd"):
            epd_input_fn = arg
        elif opt in ("-d", "--depth"):
            depth = int(arg)
            depth = max(1, depth)
        elif opt in ("-l", "--logging"):
            islogging = int(arg)
        elif opt in ("--hash"):
            nHash = int(arg)
        elif opt in ("--threads"):
            nThreads = int(arg)

    if islogging > 0:
        # Logging is in overwrite mode
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                            filename='mos_logs.txt',
                            filemode='w',
                            level=logging.INFO)
    logging.info('Started')

    # Check presence of engine and epd file
    if sEngine is None or not os.path.isfile(sEngine):
        print('Error, engine is not defined!!')
        usage()
        return

    if epd_input_fn is None or not os.path.isfile(epd_input_fn):
        print('Error, epd file is not defined!!')
        usage()
        return
    
    eng_name_id = get_engine_id_name(sEngine)
    total_epd_lines = count_position(epd_input_fn)

    # Show in console
    print('Test file    : %s' %(epd_input_fn))
    print('Positions    : %s' %(total_epd_lines))
    print('Engine       : %s' %(eng_name_id))
    print('Hash (mb)    : %d' %(nHash))
    print('Threads      : %d' %(nThreads))
    print('Search depth : %d\n' %(depth))

    logging.info('Test file : %s' %(epd_input_fn))
    logging.info('Engine    : %s\n' %(eng_name_id))

    # Open epd file for reading
    epd_cnt = 0
    evaluated_epd_cnt = 0
    with open(epd_input_fn, 'r') as epdfo:
        for epd_line in epdfo:
            epd_cnt += 1
            epd_line = epd_line.strip()
            logging.info('Test Pos %d: %s' %(epd_cnt, epd_line))
            epd = ' '.join(epd_line.split(' ')[0:4])

            # Search for hmvc opcode in input epd file
            if 'hmvc' in epd_line:
                hmvc = re.search('hmvc\s(.*?);', epd_line).group(1)
            else:
                hmvc = '0'                
            strFEN = epd + ' ' + hmvc + ' 1'

            # Print progress to console
            print('Pos %d/%d \r' %(epd_cnt, total_epd_lines)),
                
            # Analyze position
            bm, bt = analyze_fen(sEngine, strFEN, nHash, nThreads, depth)

            # Evaluate engine bestmove and time
            try:
                c8_pts = re.search('c8\s\"(.*?)\";', epd_line).group(1)
            except:
                logging.warning('Failed to read the c8 opcode on epd line %d\n' %(epd_cnt))
                continue
            try:
                c9_moves = re.search('c9\s\"(.*?)\";', epd_line).group(1)
            except:
                logging.warning('Failed to read the c9 opcode on epd line %d\n' %(epd_cnt))
                continue
            evaluated_epd_cnt += 1
            lst_pts = c8_pts.split()
            max_epd_points += int(lst_pts[0])
            lst_moves = c9_moves.split()
            logging.info('target moves: %s' %(lst_moves))
            logging.info('move points : %s' %(lst_pts))
            found = False
            best_i = None
            for i, n in enumerate(lst_moves):
                if n == bm:
                    best_i = i
                    found = True
                    break
            if found:
                logging.info('success!!')
                total_time += bt
                for j, n in enumerate(lst_pts):
                    if j == best_i:
                        pts = int(n)
                        total_pts += pts
                        logging.info('current pts %d\n' %(total_pts))
                        break
            else:
                logging.info('failure!!')
                logging.info('current pts %d\n' %(total_pts))

    rate = 0.0
    if max_epd_points:
        rate = float(100*total_pts)/max_epd_points
    
    # Write results summary to console
    print('Total Positions        : %d' %(total_epd_lines))
    print('Evaluated Positions    : %d' %(evaluated_epd_cnt))
    print('Max Points             : %d' %(max_epd_points))
    print('Points Gained          : %d' %(total_pts))
    print('Points Gained Rate (%s) : %0.2f' %('%', rate))
    print('Total Time (ms)        : %d\n' %(total_time))

    logging.info('Total Positions        : %d' %(total_epd_lines))
    logging.info('Evaluated Positions    : %d' %(evaluated_epd_cnt))
    logging.info('Max Points             : %d' %(max_epd_points))
    logging.info('Points Gained          : %d' %(total_pts))
    logging.info('Points Gained Rate (%s) : %0.2f' %('%', rate))
    logging.info('Total Time (ms)        : %d\n' %(total_time))

    # Write to summary file
    with open(summary_fn, "a") as f:            
        f.write('Test File           : %s\n' %(epd_input_fn))
        f.write('Total Positions     : %s\n' %(total_epd_lines))
        f.write('Evaluated Positions : %s\n' %(evaluated_epd_cnt))
        f.write('Search Depth        : %d\n' %(depth))
        f.write('Hash (mb)           : %s\n' %(nHash))
        f.write('Threads             : %s\n\n' %(nThreads))
        
        f.write('{:<32} {:>6} {:>8} {:>7} {:>9}\n'.format('Engine', 'Pts', 'MaxPts', 'Pts(%)', 'Time(ms)'))

        f.write('{:<32} {:>6} {:>8} {:>7.2f} {:>9}\n\n\n'.format(eng_name_id,
                                                                total_pts,
                                                                max_epd_points,
                                                                rate,
                                                                total_time))

    print('Done!!')


if __name__ == "__main__":
    main(sys.argv[1:])

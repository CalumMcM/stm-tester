import sys, os, getopt
import argparse
import subprocess
import signal
from subprocess import Popen, PIPE

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def usage(): #Output for flag '-h' and if no input given
    print('run_cpp.py -i -s [<fake_sensors>,<fake_motors>,<fake_embrakes>]\n')
    print('where \n\t-s\tIs your operating software -m (mac), -w (windows), -l (linux)\n\t<#-sensor>\tIs \'1\' (true) or a \'0\' (false) if you want that sensors data)')

def run(FakeSensor, FakeMotors, FakeEmbrakes):
    os.system('make')
    os.system('./hyped -v -d --fake_sensors=' + str(FakeSensor) + ' --fake_motors=' + str(FakeMotors) +' --fake_embrakes=' + str(FakeEmbrakes))

def noSensors():
    run_command = './hyped -v -d --fake_sensors=0 --fake_motors=0 --fake_embrakes=0'
    print (bcolors.BOLD + "\nRUNNING TEST" + bcolors.ENDC + "\n" + run_command)
    p = Popen([run_command], shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    error = False
    timer = 0
    while (timer < 3000 and not error):
        line = p.stdout.readline().strip()
        if "ERR[MOTOR]" in line:
            error = True
        timer += 1
    os.kill(p.pid, signal.SIGINT)
    if (error):
        print(bcolors.FAIL + "System failed with error:\n" + bcolors.ENDC + line)
    else:
        print(bcolors.OKGREEN + "System worked" + bcolors.ENDC)

def allSensors():
    run_command = './hyped -v -d --fake_sensors=1 --fake_motors=1 --fake_embrakes=1'
    print (bcolors.BOLD + "\nRUNNING TEST" + bcolors.ENDC + "\n" + run_command)
    p = Popen([run_command], shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    error = False
    timer = 0
    while (timer < 2 and not error):
        line = p.stdout.readline().strip()
        if "ERR[MOTOR]" in line:
            error = True
        timer += 1
    os.kill(p.pid, signal.SIGINT)
    if (error):
        print(bcolors.FAIL + "System failed with error:\n" + bcolors.ENDC + line)
    else:
        print(bcolors.OKGREEN + "System worked" + bcolors.ENDC)
    
#PARSER FLAGS
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inject", dest = 'inject', help="Run Hyped Machine", action = 'store_true')
parser.add_argument("-u", "--usage", dest = 'usage', help="Help for how to use the tester", action = 'store_true')
parser.add_argument("-a", "--all", dest = 'all', help="Run all combinations", action = 'store_true')
parser.add_argument("-fS", "--FakeSensors", dest = 'FakeSensors', type=int, default='1', metavar = 'FS', help = 'Use fake sensor data with a 1, else 0')
parser.add_argument("-fM", "--FakeMotors", dest = 'FakeMotors', type=int, default='1', metavar = 'FM', help = 'Use fake motor data with a 1, else 0')
parser.add_argument("-fE", "--FakeEmbrakes", dest = 'FakeEmbrakes', type=int, default='1', metavar = 'FE', help = 'Use fake embrakes data with a 1, else 0')
args = parser.parse_args()

if(args.usage):
    usage()
    sys.exit()
elif (args.all):
    noSensors()
    allSensors()
    """
    run(0,0,1)
    run(0,1,1)
    run(1,1,1)
    run(1,1,0)
    run(1,0,0)
    run(0,1,0)
    run(1,0,1)
    """
else:
    run(args.FakeSensors, args.FakeMotors, args.FakeEmbrakes)

   
#if __name__=='__main__':
#    main(sys.argv[1:])




""" OLD MAIN CONTENTS:
    hyped_machine = ''
    compiled_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:",["help",'ifile='])
    except getopt.GetoptError as err:
        # print help information and exit
        print(err)      
        usage()
        sys.exit(2)
    for o, a, array in opts:
        print(array)
        if o in ("-h", "--help"): 
            usage()
            sys.exit()
        elif o in ("-i", "--ifile"):
            hyped_machine = 'make'
            compiled_file = './hyped -v -d --fake_sensors=0 --fake_motors=0 --fake_embrakes=0'
            if a in ("-m", "-mac", "-l", "-linux"):
                runMac(hyped_machine, compiled_file)
                break
            elif a in ("-w", "-win"):
                runWin(hyped_machine, compiled_file)
                break
            else:
                usage()
                sys.exit()
    """
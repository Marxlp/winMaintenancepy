#coding:utf-8
import sys
import os
import time

def saf(argv,func):
    """ check the tasklist and proceed given action if the target task is/are finished """
    os.system('tasklist > temp.tsklst')
    f = open("temp.tsklst",'r')
    
    #get the task name in the tasklist file,while the first items are the processor names.
    tasklist = [taskitem.split(" ")[0] for taskitem in f]
    f.close()

    #remove the temporally created file
    os.remove('temp.tsklst')

    #create the condition list to record every monitor processor running condition.
    condition = [True] * len(argv)

    for iter,item  in enumerate(argv):
        if item not in tasklist:
            print "The process {0} is not in the list.".format(iter)
            condition[iter] = False 
        else:
            print "The process {0} is in the list !!!".format(iter)
    if True not in condition:
        func()
        print "The system will shutdown"

def shutdown():
    """Shutdown system"""
    os.system("shutdown -s -t 0")
    
while True:
    time.sleep(2)
    saf(sys.argv[1:],shutdown)

#!/usr/bin/env python
import signal
import time
import datetime
import os

#create a json data array
json_data = [
    {
    "folder_name" :"Useful", # a folder name which exists in the current dir, you can replace a folder name you have
    "parameter": "ls"
    },
    {
    "folder_name" :"Useful",
    "parameter": ""
    },
    {
    "folder_name" :"",
    "parameter": "ls"
    },
    {
    "folder_name" :"",
    "parameter": ""
    }
]


# define custom exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class errorhandler400(Error):
    """no rights to read it"""
    pass

class errorhandler404(Error):
    """the URL one tries to reach is not reachable"""
    pass

class errorhandler501(Error):
    """ not implemented """
    pass

# define shut down 
class shutdownhandler(object):
    """
        a gracefull shut down handler when it has "ctrl + c" registered
    """
    def __init__(self, sig=signal.SIGINT):
        self.sig = sig

    def __enter__(self):

        self.shutdown = False
        self.released = False

        self.original_handler = signal.getsignal(self.sig)

        def handler(signum, frame):
            self.release()
            self.shutdown = True

        signal.signal(self.sig, handler)

        return self

    def __exit__(self, type, value, tb):
        self.release()

    def release(self):

        if self.released:
            return False

        signal.signal(self.sig, self.original_handler)
        self.released = True

        return True

# define logging
def logErrorFile(errorstr):
    """
        log the error and timestamp into errorlogging txt file
    """
    f = open("errorlogging.txt", "a")
    ts = time.time()
    sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
    f.write(sttime + errorstr + '\n')    
    f.close() 

# define api 
def api(arg0, arg1):
    """
        try to list the folder's files if the folder exists in the current path.
        create an errorlog file in the current path if there is an exception.
    """
    try: 
        if os.path.exists(arg0) and (arg1 != ""):
            # a blocking call to list the folder's files
            originalPath = os.getcwd() 
            currentPath = originalPath + '\\' + arg0
            os.chdir(currentPath) # go the current folder and list all the files
            print(list(filter(os.path.isfile, os.listdir())))
            os.chdir(originalPath) #change it back to the orignal path
            time.sleep(5)
        elif (os.path.exists(arg0)) and (arg1 == ""):
            raise errorhandler400
        elif (not (os.path.exists(arg0))) and (arg1 != ""):
            raise errorhandler404

        else:
            raise errorhandler501
            
    except errorhandler400:
        errorstring = "no rights to read it"
        logErrorFile(errorstring)
        print(errorstring)
        print()

    except errorhandler404:
        errorstring = "the URL one tries to reach is not reachable"
        logErrorFile(errorstring)
        print(errorstring)
        print()

    except errorhandler501:
        errorstring = "not implemented"
        logErrorFile(errorstring)
        print(errorstring)
        print()


        

if __name__ == "__main__":
    with shutdownhandler() as s:
        for obj in json_data:
            api(obj["folder_name"],obj["parameter"])
            time.sleep(1)
            if s.shutdown:
                print("shutdown now")
                time.sleep(2)
                break

#!/usr/bin/env python

from __future__ import print_function

import os
import string
import sys
import argparse
import re
import time




def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def correctNames(name):
    newName = name
    changed = False

    if newName != name.strip():
        newName = name.strip()
        changed = True

    while newName.endswith('.'):
        newName = newName[:-1]
        changed = True

    if any(s in newName for s in badChars):
        for char in badChars:
            newName = newName.replace(char, '-')
        changed = True

    return (newName, changed)


def main():
    global start_time
    global badChars
    global corrections
    global checkedCount
    global errorCount
    global changeCount

    start_time = time.time()
    badChars = ['"', '*', ':', '<', '>', '?', '/', '\\', '|']
    corrections = {}
    checkedCount = 0
    errorCount = 0
    changeCount = 0

    if sys.argv[1]:
        path = sys.argv[1]
        for dirName, subdirName, fileList in os.walk(path):

            for filename in fileList:
                checkedCount += 1
                if checkedCount % 10 == 0:
                    print('%s items checked.' % checkedCount, end='\r')
                # print filename
                (newfilename, isChanged) = correctNames(filename)
                if isChanged:
                    corrections[dirName + "/" + filename] = dirName + "/" + newfilename
                    # print "File '%s/%s' needs to be renamed to '%s'" % (dirName, filename, newfilename)
            for subDir in subdirName:
                checkedCount += 1
                if checkedCount % 10 == 0:
                    print('%s items checked.' % checkedCount, end='\r')
                (newDir, isChanged) = correctNames(subDir)
                if isChanged:
                    corrections[dirName + "/" + subDir] = dirName + "/" + newDir
                    # print "SubDir '%s' need to be renamed to '%s'" % (subDir, newDir)

        print("--- %s seconds ---" % (time.time() - start_time))

        for old, new in corrections.items():
            print("'%s' needs to be renamed to '%s'" % (old, new))
            errorCount += 1

        if errorCount > 0:
            print("\r%s results found out of %s files checked." % (errorCount, checkedCount))
            if (query_yes_no("The following files need to be renamed as indicated. Proceed? y/N: ", "no")):
                for old, new in corrections.items():
                    os.rename(old, new)
                    print("renaming %s to %s" % (old, new))
                    changeCount += 1
                print("%s file(s) changed." % changeCount)
            else:
                print("Files not renamed - exiting.")
        else:
            print("You're all set! You may now move this folder to OneDrive.")

        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        print("Utility requires a path be sent - example use: './cleanFileNames.py /path/to/directory/'")


if __name__ == '__main__':
    main()
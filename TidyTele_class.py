#!/usr/bin/python

import os
import string
import shutil
from datetime import datetime
from datetime import timedelta
import time
import levensh
from sys import platform

class TeleBot(object):
    '''A Class to implement a cleaner, more organized TidyTele. It uses the same logic and functions as TidyTele, 
    but the logic is abstracted out into separate functions'''
    def __init__(self, top=os.path.expanduser('~'), flag='<<', dirs=['Downloads', 'Movies', 'Music', 'Documents', 'Pictures', 'Desktop', 'Scripts'], log='Tele_log.txt'):
    	self.SEARCH = dirs
    	self.FLAG = flag
    	self.TOP = os.path.expanduser('~')
        self.num = 0
        self.failed = 0
        self.details = []
        self.log = log
        self.title = '==TidyBot Called @ {:.19}=='.format(str(datetime.now()))

    def find_all_paths(self, target_dir):
        '''Find all folder paths to reach a directory with name target_dir'''
        paths = []
        autocorrect = []
        for sub in self.SEARCH:
            if sub.lower() == target_dir.lower():
                paths.append(os.path.join(self.TOP, sub))
            for root, dirs, files in os.walk(os.path.join(self.TOP, sub)):
                for a_dir in dirs:
                    lev = levensh.fastMemLev(a_dir.lower(), target_dir.lower())
                    if lev == 0:
                        paths.append(os.path.join(root, a_dir))
                    if lev <= 2 and lev > 0:
                        autocorrect.append(os.path.join(root, a_dir))
        if  len(paths) == 0 and len(autocorrect) > 0:
            ## Autocorrect opportunity?
            pass
        return paths

    def sudo_move(self, fname, name, dest):
        '''Returns 0 if file is moved successfully, 1 otherwise'''
        if self.no_dupes(name, dest): ## Okay to move file
            shutil.move(os.path.join(root,fname), os.path.join(dest, name))
            return 0
        return 1

    def no_dupes(self, name, target_dir):
        '''Checks if name already exists in target_dir,
        returns TRUE if the file can be moved there.'''
        return not (name in os.listdir(dirpath))

    def choose_paths(self, fname, paths):
        pass

    def process_file(self, f):
        '''Given a file name and the root folder it is in:
        - determine the paths to the appropriate destination
        - move the file if possible to the destination, and log it
        - if the file cannot be moved, log the reason and put the file in failed'''
        file = f[1]
        root = f[0]
        #print('process_file called')
        '''
        paths()
        if multiple paths exist,
            ask for correct location
        elif 1 path:

        else:
            return failed
        if no_dupes():
            try:
                shutil.move the file to destination
                log it and put it in details
            except:
                something went wrong -> log it and add to failed
        else:
            log it and add to failed
        '''
        pass

    def iterate_dirs(self):
        '''Iterate through all files and directories in self.search, calling process dir on each directory that
        contains self.flag in the dirname'''
        #print('iterate_dirs called')
        d_move = []
        for sub in self.SEARCH:
            for root, dirs, files in os.walk(os.path.join(self.TOP,sub)):
                for d in dirs:
                    if d.count(self.FLAG) == 1:
                        d_move.append( (root, d) )
        return d_move

    def iterate_files(self):
        '''Iterate through all files and directories in self.search, returning a list each root/file pair that
        contains self.flag in the filename'''
        #print('iterate_files called')
        f_move = []
        for sub in self.SEARCH:
            for root, dirs, files in os.walk(os.path.join(self.TOP,sub)):
                for f in files:
                    if f.count(self.FLAG) == 1:
                        f_move.append( (root, f) )
        return f_move

    def runTele(self):
        '''Collect all the files and directories that need to be moved and move them'''
        start = time.time()
        files_to_move = self.iterate_files()
        dirs_to_move = self.iterate_dirs()
        for f in files_to_move:
            self.process_file(f)
        for d in dirs_to_move:
            self.process_file(d)
        finished = time.time()
        print('Total time elapsed: {}\n\n'.format(timedelta(seconds=(finished-start))))
        
    def log_it(self, name, dest):
        '''Write the successful move to self.log'''
        try:
            with open(self.log, 'a') as f:
                f.write('Moved {} to {}\n'.format(name, dest))
        except Exception as e:
            print('Something went wrong: {}'.format(e))

    def __str__(self):
    	'''Return string displaying when the bot was called, how many files were processed, and how many failed'''
    	string = self.title
    	string += '\n{} processed, {} failed'.format(self.num, self.failed)
    	return string

if __name__ == '__main__':
    TB = TeleBot(flag=('+=' if platform == 'win32' else '<<'))
    TB.runTele()
	
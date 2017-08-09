import os
import string
import shutil
from datetime import timedelta
import time

'''
Changelog:

TODO:
- Change to traverse whole file system
'''

DOWNLOADS = os.path.expanduser('~/Downloads')
TOP = os.pardir
FLAG = '<<'
SEARCH = ['Documents', 'Pictures', 'Desktop'] ## Add more directories if needed

def find_all_paths(target_dir):
    '''PURPOSE: 
    find all paths to a given directory
    RETURNS:
    array paths: empty if no target_dir exists, 
                otherwise contains absolute paths to every folder named target_dir
    '''
    paths = []
    for sub in SEARCH:
        if sub == target_dir:
            paths.append(os.path.join(TOP, sub))
        for root, dirs, files in os.walk(os.path.join(TOP,sub)):
            if target_dir in dirs:
                paths.append(os.path.join(root, target_dir))
    return paths

def no_dupes(fname, dirpath):
    '''PURPOSE: 
    Determines if the file to be moved already in that directory 
    (shutil.move overwrites files and puts directories INSIDE the target if they've got the same name,
    which is confusing for the user)
    RETURNS: 
    True if there is no file with fname already in the directory specified by dirpath 
    (True means it's okay to move the file there, False means it's not okay)
    '''
    if fname in os.listdir(dirpath):
        print '{} already exists in {}'.format(fname, dirpath)
        return False
    return True


def main():
    '''
    PURPOSE:
    examine each file in the ~/Downloads folder. If it is tagged with a '<<', then move the file or directory
    to the appropriate target_directory
    RETURNS:
    nothing'''
    num=0
    failed=0
    failure=[]
    # Count each item in DOWNLOADS folder
    for f in os.listdir(DOWNLOADS):
        if f.count(FLAG) == 1:
            num+=1
            target_dir, name = string.split(f, FLAG, maxsplit=1) ## Split to find target directory
            paths = find_all_paths(target_dir)
            if paths == []: ## No directory found
                print 'no dest'
                failed+=1
                failure.append(f)

            elif len(paths) > 1: ## Multiple Directories found
                print 'Multiple destinations found, please select one:'
                for x in range(len(paths)): 
                    print '{}: {}'.format(x+1, paths[x])
                chosen = paths[0]
                while True: 
                    try: ## Force user to select a directory
                        n = int(raw_input('> '))-1
                        if n not in range(1, len(paths)+1):
                            raise ValueError('')
                        chosen = paths[n]
                        break
                    except:
                        print 'Please choose a legal integer.'
                if no_dupes(name, chosen): ## Okay to move file
                    shutil.move(os.path.join(DOWNLOADS,f), os.path.join(chosen, name))
                else: ## File already exists in target_dir
                    failed+=1
                    failure.append(f)

            else: ## One Directory found
                if no_dupes(name, paths[0]): ## Okay to move file
                    shutil.move(os.path.join(DOWNLOADS,f), os.path.join(paths[0], name))
                else: ## File already exists in target_dir
                    failed+=1
                    failure.append(f)

    print '\nProcessed {} files, {} failed{}'.format(num, failed, ':' if failed > 0 else '!')
    for i in range(len(failure)):
        f = failure[i]
        print '{}: {}'.format(i+1, f)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print 'Total time elapsed:', timedelta(end-start)
    print('\nThanks for using TidyDL!')

import os
import string
import shutil
from datetime import datetime
from datetime import timedelta
import time
import levensh
import Tkinter

TOP = os.path.expanduser('~')
FLAG = '<<'
SEARCH = ['Downloads','Documents', 'Pictures', 'Desktop', 'Scripts'] ## Add more directories if needed

def find_all_paths(target_dir):
    '''
    PURPOSE: 
    find all paths to a given directory
    RETURNS:
    array paths: empty if no target_dir exists, 
                otherwise contains absolute paths to every folder named target_dir
    '''
    paths = []
    autocorrect = []
    for sub in SEARCH:
        if sub == target_dir:
            paths.append(os.path.join(TOP, sub))
        for root, dirs, files in os.walk(os.path.join(TOP,sub)):
            for a_dir in dirs:
                lev = levensh.fastMemLev(a_dir.lower(), target_dir.lower())
                if lev == 0:
                    paths.append(os.path.join(root, a_dir))
                if lev <= 2 and lev > 0:
                    autocorrect.append(os.path.join(root, a_dir))
        if len(paths) == 0:
            if len(autocorrect) > 0:
                '''TODO: UX - if there are no exact matches and there are some auto-correct matches,
                            DO SOMETHING with the auto-correct matches'''
                pass
            '''
            ## OLD CODE before levenshtein distance:
            if target_dir in dirs:
                paths.append(os.path.join(root, target_dir))
                '''
    return paths

def no_dupes(fname, dirpath):
    '''
    PURPOSE: 
    Determines if the file to be moved already in that directory 
    (shutil.move overwrites files and puts directories INSIDE the target if they've got the same name,
    which is confusing for the user)
    RETURNS: 
    True if there is no file with fname already in the directory specified by dirpath 
    (True means it's okay to move the file there, False means it's not okay)
    '''
    if fname in os.listdir(dirpath):
        return False
    return True

def log_it(fname, dirpath):
    '''
    PURPOSE:
    log down which items are being moved where in a text file in the same directory as this script
    '''
    with open('Tele_log.txt', 'a') as f:
        f.write('Moved {} to {}\n'.format(fname, dirpath))

def main():
    '''
    PURPOSE:
    for each file and folder in the folder hierarchy, if it had the flag '<<', then send that file or folder
    to the tagged folder (if it does not exist, do nothing and mark it as a failure)
    '''
    num=0
    failed=0
    failure=[]
    with open('Tele_log.txt', 'a') as logger:
        logger.write('==TidyTele Call @ {:.19}==\n'.format(str(datetime.now())))
    ## Process each FILE in the folder hierarchy
    for sub in SEARCH:
        for root, dirs, files in os.walk(os.path.join(TOP,sub)):
            for f in files:
                if f.count(FLAG) == 1:
                    num+=1
                    target_dir, name = string.split(f, FLAG, maxsplit=1) ## Split to find target directory
                    if name == '':
                        failed+=1
                        failure.append('{} ERROR: {}'.format(f, 'must name file post-<<'))
                        break
                    paths = find_all_paths(target_dir)
                    if paths == []: ## No directory found
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
                            log_it(name, chosen)
                            print '{} <-- {}'.format(paths[0], f)
                            shutil.move(os.path.join(root,f), os.path.join(chosen, name))
                        else: ## File already exists in target_dir
                            failed+=1
                            failure.append('{} already exists in {}'.format(name,chosen))

                    else: ## One Directory found
                        if no_dupes(name, paths[0]): ## Okay to move file
                            log_it(name, paths[0])
                            print '{} <-- {}'.format(paths[0], name, root)
                            shutil.move(os.path.join(root,f), os.path.join(paths[0], name))
                        else: ## File already exists in target_dir
                            failed+=1
                            failure.append('{} already exists in {}'.format(name,paths[0]))

    ## THEN Process each FOLDER in the folder hierarchy
    for sub in SEARCH:
        for root, dirs, files in os.walk(os.path.join(TOP,sub)):
            for d  in dirs:
                if d.count(FLAG) == 1:
                    num+=1
                    target_dir, name = string.split(d, FLAG, maxsplit=1) ## Split to find target directory
                    if name == '':
                        failed+=1
                        failure.append('{} ERROR: {}'.format(f, 'must name file post-<<'))
                        break
                    paths = find_all_paths(target_dir)
                    if paths == []: ## No directory found
                        failed+=1
                        failure.append(d)

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
                            log_it(name, chosen)
                            print '{} <-- {}'.format(paths[0], d)
                            shutil.move(os.path.join(root,d), os.path.join(chosen, name))
                        else: ## File already exists in target_dir
                            failed+=1
                            failure.append('{} already exists in {}'.format(name,chosen))

                    else: ## One Directory found
                        if no_dupes(name, paths[0]): ## Okay to move file
                            log_it(name, paths[0])
                            print '{} <-- {}'.format(paths[0], name, root)
                            shutil.move(os.path.join(root,d), os.path.join(paths[0], name))
                        else: ## File already exists in target_dir
                            failed+=1
                            failure.append('{} already exists in {}'.format(name, paths[0]))

    print '====================\nProcessed {} files, {} failed{}'.format(num, failed, ':' if failed > 0 else '!')
    with open('Tele_log.txt', 'a') as logger:
        if len(failure) > 0:
            logger.write('\nFailed:\n')
        for i in range(len(failure)):
            f = failure[i]
            print '{}: {}'.format(i+1, f)
            logger.write('{}: {}\n'.format(i+1, f))
        logger.write('\n')

if __name__ == '__main__':
    start = time.time()
    print '===================='
    main()
    print '--------------------'
    end = time.time()
    print 'Total time elapsed:', timedelta(seconds=(end-start))
    print('Thanks for using TidyTP!\n')
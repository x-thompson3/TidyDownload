from send2trash import send2trash

import os
import string
import shutil

DOWNLOADS = 'C:\\Users\\Xander\\Downloads'
TOP = 'C:\\Users\\Xander'
FLAG = '~'
SEARCH = ['Documents', 'Pictures', 'Music', 'Zips']

def find_path(target_dir):
    '''find the absolute path to the target directory'''
    path = None
    for sub in SEARCH:
        if sub == target_dir:
            path = os.path.join(TOP, sub)
            break
        for root, dirs, files in os.walk(os.path.join(TOP,sub)):
            if target_dir in dirs:
                path = os.path.join(root, target_dir)
                break
    return path

def main():
    num=0
    failed=0
    failure=[]
    for f in os.listdir(DOWNLOADS):
        print '.',
        if f.count(FLAG) == 1:
            num+=1
            target_dir, name = string.split(f, FLAG, maxsplit=1)
            path = find_path(target_dir)
            if path != None:
                shutil.move(os.path.join(DOWNLOADS,f), os.path.join(path, name))
            else:
                failed+=1
                failure.append(name)
    print '\nProcessed {} files, {} failed {}'.format(num, failed, ':' if failed > 0 else '')
    for f in failure:
        print(f)


if __name__ == '__main__':
    main()
    #input('\nThanks for using TidyDL!\nPress <any key> to Exit.')
    try:
        print('\nThanks for using TidyDL!')
        os.system('pause')  #windows, doesn't require enter
    except whatever:
        os.system('read -p "Press any key to continue"') #linux

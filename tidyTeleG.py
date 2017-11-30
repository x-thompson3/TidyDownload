import Tkinter as tk
import os
import string
import shutil
from datetime import datetime
from datetime import timedelta
import time
import levensh

TOP = os.path.expanduser('~')
FLAG = '<<'
SEARCH = ['Downloads', 'Movies', 'Documents', 'Pictures', 'Desktop', 'Scripts'] ## Add more top-level directories if needed

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
        if sub.lower() == target_dir.lower():
            paths.append(os.path.join(TOP, sub))
        for root, dirs, files in os.walk(os.path.join(TOP,sub)):
            for a_dir in dirs:
                lev = levensh.fastMemLev(a_dir.lower(), target_dir.lower())
                if lev == 0:
                    paths.append(os.path.join(root, a_dir))
                if lev <= 2 and lev > 0:
                    autocorrect.append(os.path.join(root, a_dir))
    if len(paths) == 0 and len(autocorrect) > 0:
        pass
        #print('autocorrect opportunity')
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
    return (not fname in os.listdir(dirpath))

def log_it(fname, dirpath):
    '''
    PURPOSE:
    log down which items are being moved where in a text file in the same directory as this script
    '''
    with open('Tele_log_G.txt', 'a') as f:
        f.write('Moved {} to {}\n'.format(fname, dirpath))
    return
    
def scrape(TW, top_label, details_label, success_box, failed_box):
    '''
    PURPOSE:
    begin search for files, adding the to the success and fail boxes as necessary
    '''
    with open('Tele_log_G.txt', 'a') as logger:
        logger.write('==TidyTele_GUI Call @ {:.19}==\n'.format(str(datetime.now())))
    d_list = []

    success_box.bind('<<ListboxSelect>>', lambda x: onselect(d_list, x, details_label))
    failed_box.bind('<<ListboxSelect>>', lambda x: onselect(d_list, x, details_label))
    details_label.set('')
    success_box.delete(0, tk.END)
    failed_box.delete(0, tk.END)

    num = 0
    failed = 0

    for sub in SEARCH:
        for root, dirs, files in os.walk(os.path.join(TOP,sub)):
            for f in files:
                if f.count(FLAG) == 1:
                    num+=1 
                    target_dir, name = string.split(f, FLAG, maxsplit=1) ## Split to find target directory
                    target_dir = target_dir.strip()
                    name = name.strip()
                    if name == '' or target_dir == '':
                        failed+=1
                        failed_box.insert(tk.END, f)
                        d_list.append( (0, '{}'.format(f), 'ERROR: must name file  Dest<<Name') )
                    else:
                        paths = find_all_paths(target_dir)
                        if paths == []: ## No directory found
                            #print('No directory found: {}'.format(target_dir))
                            failed+=1
                            failed_box.insert(tk.END, name)
                            d_list.append( (0, '{}'.format(name), 'ERROR: directory \'{}\' not found'.format(target_dir)) )

                        elif len(paths) == 1: ## One directory found
                            dest = paths[0]

                            ## MOVE THE FILE & LOG IT
                            if no_dupes(name, dest): ## Okay to move file
                                log_it(name, dest)
                                #print('Moved to: {}'.format(target_dir))
                                success_box.insert(tk.END, name)
                                d_list.append( (1, '{}'.format(name), 'Moved to: {}'.format(dest) ))
                                #log_it(name, paths[0])
                                #print '{} <-- {}'.format(dest, name, root)
                                shutil.move(os.path.join(root,f), os.path.join(dest, name))
                            else: ## File already exists in target_dir
                                #print('Dupe in: {}'.format(target_dir))
                                failed+=1
                                failed_box.insert(tk.END, name)
                                d_list.append( (0, '{}'.format(name), 'ERROR: {} already exists in directory \'{}\''.format(name, target_dir)) )
                        
                        else: #More than one directory found
                            '''Prompt the user for which destination'''
                            #print('More than one directory: {}'.format(target_dir))
                            dest = choose_from(TW, name, paths)
                            #print('Selected a ')
                            ## MOVE THE FILE & LOG IT
                            if no_dupes(name, dest): ## Okay to move file
                                log_it(name, dest)
                                #print('Moved to: {}'.format(target_dir))
                                success_box.insert(tk.END, name)
                                d_list.append( (1, '{}'.format(name), 'Moved to: {}'.format(dest) ))
                                #log_it(name, paths[0])
                                #print '{} <-- {}'.format(dest, name, root)
                                shutil.move(os.path.join(root,f), os.path.join(dest, name))
                            else: ## File already exists in target_dir
                                #print('Dupe in: {}'.format(target_dir))
                                failed+=1
                                failed_box.insert(tk.END, name)
                                d_list.append( (0, '{}'.format(name), 'ERROR: {} already exists in directory \'{}\''.format(name, target_dir)) )
                    top_label.set('Files found: {}, failed: {}'.format(num, failed))

    for sub in SEARCH:
        for root, dirs, files in os.walk(os.path.join(TOP,sub)):
            for d in dirs:
                if d.count(FLAG) == 1:
                    num+=1 
                    target_dir, name = string.split(d, FLAG, maxsplit=1) ## Split to find target directory
                    target_dir = target_dir.strip()
                    name = name.strip()
                    if name == '' or target_dir == '':
                        failed+=1
                        failed_box.insert(tk.END, d)
                        d_list.append( (0, '{}'.format(d), 'ERROR: must name file  Dest<<Name') )
                    else:
                        paths = find_all_paths(target_dir)
                        if paths == []: ## No directory found
                            #print('No directory found: {}'.format(target_dir))
                            failed+=1
                            failed_box.insert(tk.END, name)
                            d_list.append( (0, '{}'.format(name), 'ERROR: directory \'{}\' not found'.format(target_dir)) )

                        elif len(paths) == 1: ## One directory found
                            dest = paths[0]

                            ## MOVE THE FILE & LOG IT
                            if no_dupes(name, dest): ## Okay to move file
                                log_it(name, dest)
                                #print('Moved to: {}'.format(target_dir))
                                success_box.insert(tk.END, name)
                                d_list.append( (1, '{}'.format(name), 'Moved to: {}'.format(dest) ))
                                #log_it(name, paths[0])
                                #print '{} <-- {}'.format(dest, name, root)
                                shutil.move(os.path.join(root,d), os.path.join(dest, name))
                            else: ## File already exists in target_dir
                                #print('Dupe in: {}'.format(target_dir))
                                failed+=1
                                failed_box.insert(tk.END, name)
                                d_list.append( (0, '{}'.format(name), 'ERROR: {} already exists in directory \'{}\''.format(name, target_dir)) )
                        
                        else: #More than one directory found
                            '''Prompt the user for which destination'''
                            #print('More than one directory: {}'.format(target_dir))
                            dest = choose_from(TW, name, paths)
                            ## MOVE THE FILE & LOG IT
                            if no_dupes(name, dest): ## Okay to move file
                                log_it(name, dest)
                                #print('Moved to: {}'.format(target_dir))
                                success_box.insert(tk.END, name)
                                d_list.append( (1, '{}'.format(name), 'Moved to: {}'.format(dest) ))
                                #log_it(name, paths[0])
                                #print '{} <-- {}'.format(dest, name, root)
                                shutil.move(os.path.join(root,d), os.path.join(dest, name))
                            else: ## File already exists in target_dir
                                #print('Dupe in: {}'.format(target_dir))
                                failed+=1
                                failed_box.insert(tk.END, name)
                                d_list.append( (0, '{}'.format(name), 'ERROR: {} already exists in directory \'{}\''.format(name, target_dir)) )
                    top_label.set('Files found: {}, failed: {}'.format(num, failed))

    if num == 0:
        details_label.set('\n')
        top_label.set('No files found. You\'re Tidy!')

    #print '====================\nProcessed {} files, {} failed{}'.format(num, failed, ':' if failed > 0 else '!')
    with open('Tele_log_G.txt', 'a') as logger:
        if failed > 0:
            logger.write('\nFailed:\n')
        i = 1
        for p,name,err in d_list:
            if p==0:
                logger.write('{}: {}'.format(name, err))
        logger.write('\n')

def choose_from(root, name, paths):
    '''PURPOSE:
    Create Tkinter dialog/radio button window to select from possible destinations'''
    chooser = tk.Toplevel()
    chooser.wm_title('Chooser')
    NameLabel = tk.Label(chooser, text = 'Select from possible destinations for {}'.format(name))
    NameLabel.pack(anchor=tk.W)
    x=0
    v = tk.IntVar()
    v.set(0) # initialize

    for path in paths:
        b = tk.Radiobutton(chooser, text=path, variable=v, value=x)
        x+=1
        b.pack(anchor=tk.W)
    chooser.update()
    confirm_button = tk.Button(chooser, text='Confirm', command=chooser.destroy)
    confirm_button.pack(anchor=tk.E)
    root.wait_window(chooser)
    return paths[v.get()]


def onselect(d_list, evt, d_label):
    # Note here that Tkinter passes an event object to onselect()
    try:
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        msg = ''
        for x in d_list:
            if x[1] == value:
                msg = x[2]
        d_label.set('File: {}\n{}'.format(value, msg))
    except IndexError:
        pass


def main():
    '''Create a Tkinter GUI for TidyTele'''
    with open('Tele_log_G.txt', 'a') as logger:
        logger.write('==TidyTeleG Call @ {:.19}==\n'.format(str(datetime.now())))
    TeleWindow = tk.Tk()
    TeleWindow.geometry("550x300")
    TeleWindow.wm_title('Tidy Tele : A Quick and Easy File Mover')
 
    #############CREATE GUI ELEMENTS##################
    TopText = tk.StringVar()
    Details = tk.StringVar()
    TopLabel = tk.Label(TeleWindow, textvariable = TopText)
    SpacingLabelTop = tk.Label(TeleWindow, text = '    ')
    SpacingLabelColumn = tk.Label(TeleWindow, text= '             ')

    DetailsLabel = tk.Label(TeleWindow, textvariable = Details, anchor=tk.W, justify=tk.LEFT)
    Details.set('\n')
    SuccessLabel = tk.Label(TeleWindow, text='Files Moved:')
    FailedLabel = tk.Label(TeleWindow, text='Failed:')

    SuccessField = tk.Listbox(TeleWindow)
    FailedField = tk.Listbox(TeleWindow)


    start_button = tk.Button(TeleWindow, text = 'Begin', command=lambda : scrape(TeleWindow, TopText, Details, SuccessField, FailedField))
    kill_button = tk.Button(TeleWindow, text = 'Close', command=TeleWindow.destroy)

    ##############ORGANIZE GUI ELEMENTS#################
    TopLabel.grid(row=2,column=2, columnspan=5, sticky=tk.W)
    SpacingLabelTop.grid(row=1,column=1, rowspan=9, sticky=tk.W)
    DetailsLabel.grid(row=8,column=2, columnspan=5, sticky=tk.W+tk.E)
    
    SuccessLabel.grid(row=4, column=2)
    FailedLabel.grid(row=4, column=5)

    SuccessField.grid(row=5, column=2, rowspan=3, sticky=tk.E)

    FailedField.grid(row=5, column=5, rowspan=3, sticky=tk.E)
    SpacingLabelColumn.grid(row=2,column=3, columnspan=2, rowspan=5, sticky=tk.S+tk.N)

    start_button.grid(row=9, column=5, sticky=tk.E)
    kill_button.grid(row=9, column=6, sticky=tk.W)

    TeleWindow.mainloop()


if __name__ == "__main__":
    main()
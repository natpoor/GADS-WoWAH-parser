# Sept 27, 2013.
# This file will (hopefully) read all the little WoW AH files and make a db or csv.
# One file to unite them all! (It is like 3.5 GB of text or something.... Maybe SQL/SQLite?)
# Needs to:
# Read directory and file name structure so I don't have to type it in manually.
# Make that a data structure of some sort, easy to read so the program can scan through it.
# Then, using that list, read everything into a file. Questions here (file and data type).
# Actually, if I can read it, just read the files then.
# Writes to a CSV.


# PACKAGES
import csv
import re
import os           # This is for os.listdir
import os.path      # This is for the other dir stuff.
import string       # Maybe for directory name cycling etc.
import time

# VARIABLES
max_char = 0
max_guild = 0
mfc = 0
mdb = []
#write_data_loc = '/Users/natpoor/Dropbox/WoWAH work/'
write_data_loc = '/Users/natpoor/Documents/Academic Papers/WoW Avatar Hist DB/'     #iMac only. Don't hit DropBox whilst process.
write_data_file = 'wowah_data.csv'
write_data_filename = write_data_loc + write_data_file
main_folder_str = 'WoWAH/'
mfs = main_folder_str
imac = '/Users/natpoor/Documents/Academic Papers/WoW Avatar Hist DB/'   # Since currently it's local.
airbook = '/Users/natpoor/Documents/WoWAH folder/'

# LOCATION DIRS! Change as needed.
location_dir = airbook                  # Just set this one, everything falls into place.
the_dir = location_dir + mfs

#REGEX
line_re = re.compile(r'^.*"[\d+],\s(.*),\s(\d+),(\d+),\s?(\d*),.*".*$')
#                          dummy   time    seq  char   guild

# REGEX NOTES
# groups: 1=timestamp, 3=avatarID, 4=guild.
# [1] = "0, 03/30/06 23:59:49, 1,10772, , 1, Orc, Warrior, Orgrimmar, , 0",
#       "0, 01/10/09 00:03:50, 1,55517, , 3, Orc, Warlock, Orgrimmar, WARLOCK, 0", -- [1]
#    	"0, 01/10/09 00:04:10, 5,4002,1, 75, Orc, Hunter, Zul'Gurub, HUNTER, 0", -- [26]
#       "0, 01/10/09 00:04:10, 5,78122,342, 80, Orc, Hunter, The Storm Peaks, HUNTER, 0", -- [32]
#   	"0, 01/10/09 00:08:04, 51,64635,161, 80, Blood Elf, Paladin, The Obsidian Sanctum, PALADIN, 0", -- [447]
# dummy, query time, query sequence number, avatar ID, guild, level, race, class, zone, dummy, dummy


# TESTING REGEX HERE
test1 = '[1] = "0, 03/30/06 23:59:49, 1,10772, , 1, Orc, Warrior, Orgrimmar, , 0",'
test2 = '"0, 01/10/09 00:03:50, 1,55517, , 3, Orc, Warlock, Orgrimmar, WARLOCK, 0", -- [1]'
test3 = '[1] = "0, 03/30/06 23:59:49, 1,10772,17, 1, Orc, Warrior, Orgrimmar, , 0",'
test4 = '"0, 01/10/09 00:03:50, 1,55517,18, 3, Orc, Warlock, Orgrimmar, WARLOCK, 0", -- [1]'

test_list = [test1, test2, test3, test4]



# FUNCTIONS

def get_subdirs(the_folder):
    this_list = []
    this_list = os.listdir(the_folder)
    print 'From get_subdirs, a list is: ', this_list
    for item in this_list:
        if item.startswith('.'):
            this_list.remove(item)
    return(this_list)
# End of get_subdirs
# '.DS_Store'


def get_file_list(the_folder):
    this_list = []
    this_list = os.listdir(the_folder)
    for item in this_list:
        if item.startswith('.'):
            this_list.remove(item)
    return(this_list)
# End of get_file_list


def parse_and_write(file, output_file):
    for line in file:                           # Oh the first "line" is a hard return???
#       print 'A line is: ', line
        data = line_re.match(line)
        if data is not(None):
            timestamp = data.group(1)
            char = data.group(3)
            if data.group(4) is not(''):
                guild = data.group(4)
            else:
                guild = '-1'
            print timestamp

            new_line = char + ',' + guild + ',' + timestamp + '\n'
            output_file.write(new_line)
                
        else:
            print "Didn't match the regex."

# End of parse_and_write
# [1] = "0, 03/30/06 23:59:49, 1,10772, , 1, Orc, Warrior, Orgrimmar, , 0",
#       "0, 01/10/09 00:03:50, 1,55517, , 3, Orc, Warlock, Orgrimmar, WARLOCK, 0", -- [1]
# dummy, query time, query sequence number, avatar ID, guild, level, race, class, zone, dummy, dummy
# Hypotheses: 1. Most guilds are small (long tail); 2. Most guilds die;
# RQ: 1. Explore guild membership churn; 


def read_tree(output_file):
    global the_dir
    months_folders = get_subdirs(the_dir)
    for folder in months_folders:                                   # Run isdir(dir) first, try/except. Make sure no funny folders/dirs.
        folder = the_dir + folder                                   # Expands the folder name to the long version.
        day_folders = get_subdirs(folder)
        for day_folder in day_folders:
            day_folder = folder + '/' + day_folder
            file_list = get_file_list(day_folder)
            for file in file_list:
                try:
                    file = day_folder + '/' + file
                    with open(file, 'r') as f:
                        this_file = f.readlines()                          # Should read the whole file as a string?
                        parse_and_write(this_file, output_file)
                except IOError:
                    print 'Error opening hoped for data-text file,', str(file), ', reason: ', IOError
# End of read_tree



def write_data(): # Deprecated.
    global mdb
    fieldnames = ['char', 'guild', 'timestamp']
    
    with open(write_data_filename, 'w') as csvfile:
        the_file = csv.writer(csvfile)
        the_file.writerow(fieldnames)
        for line in mdb:
            the_file.writerow(line)
    
    print 'Wrote to: ', write_data_filename

# End of write_data


def Xmain():                         # Yeah the regex is fine!
	for test_item in test_list:
		print test_item
		results = line_re.match(test_item)
		if results is not(None):
			print 'Char: ' + results.group(3) + ' and Guild: ' + results.group(4)
		else:
			print 'What no match??? On ' + test_string

# End of this main


def main():	
    #open write file here
    output_file = open(write_data_filename, 'a')    # 'a' is very important, it appends the new data to the big file. 
    fieldnames = ('char, guild, timestamp\n')
    output_file.write(fieldnames)
    start_time = time.time()
    read_tree(output_file)
    #close write file here
    output_file.close()
    spent_time = time.time() - start_time
    mins_spent = int(spent_time / 60)
    secs_remainder = int(spent_time % 60)
    print 'Time of process: ', mins_spent, ':', secs_remainder     # 13:42 on iMac. Also 14:39 another time.
    
#    print 'Files scanned (or tried), ', mfc     # 138,084
#    print 'Max Chars: ', max_char               # They claim 91,065 ">= 1" NOT it starts at 0, my count says: 91064 + 1 = 91,065.
#    print 'Max Guilds: ', max_guild             # They say "An integer within [1, 513]" but no since they start at 0. 512 + 1 = 513.
# End of main


# Main call

main()





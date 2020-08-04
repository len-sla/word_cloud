# ########################################################################################################################################
# To automatically keep tidy( delete oldest files) USB memory stick on the  on the raspberry Pi  used for storing photos from monitoring 
# I tried to find as simple as possible  functions and use them.
# It looks like os library and glob doing their job and are able to handle easiest way this job
# there are only two simple functions 
# sorted_dir_list() which is creating sorted list with given folder as input
# to_big_delete_oldest() functions delete oldest files up to given limit( capacity in GB) with given granularity here 100 files
# excecuting is simple python max_size_occup.py
# of course the libraries pathlib and glob should be installed before if necessary
# ########################################################################################################################################



from pathlib import Path
import os, glob

folder_mon = '/media/pi/USB11/'
folder_monitoring = Path(folder_mon)



def sorted_dir_list(search_dir=folder_mon): #creating sorted  condition getmtime list with file names
	files = list(filter(os.path.isfile, glob.glob(folder_mon + "*")))
	files.sort(key=lambda x: os.path.getmtime(x))
	return files


def to_big_delete_oldest(max_size=40): # size is given in GB

	size_now= sum(f.stat().st_size for f in folder_monitoring.glob('**/*') if f.is_file() ) #calculating capacity by summing everything
	temp_list=sorted_dir_list()
	
	if (len(temp_list))==0:
		print( 'no files to delete in directory')
	else:
		print(' we are starting on the list :',len(temp_list), ' files  occupies :', size_now)
		print('')
		while  size_now > (max_size*1000000000): 
			
			for i in range(0,100): # here  you could give as second value number which say how many oldest file at  should be deleted before next checking occupied capacity
				
				print(i,': to delete  :', temp_list[i])
				os.remove(temp_list[i])
				print("% s removed successfully" % temp_list[i])
			print('\n... checking directory size...')
			temp_list=sorted_dir_list()
			size_now= sum(f.stat().st_size for f in folder_monitoring.glob('**/*') if f.is_file() )
			print('After deleting,  occupied capacity is :', size_now)

		print(' Bye ... ')

print('Lets start cleanup this folder... it will take a while, need to check directory...', folder_mon)

to_big_delete_oldest(40) #deleting oldest file so folder is no bigger than 40GB

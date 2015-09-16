import sys
import os
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("infile", help="enter the name of the inputfile here")
parser.add_argument("-l", "--limit", type=int, default=5000, help="enter the approximate number of rows to split the file by")
parser.add_argument("-f", "--firstrow_header", action="store_true", default=False, help="first row is header row, include in all split files")
args = parser.parse_args()
#print args.infile

#infile = open('2015.08.06 LOG Upload Wave1.csv')

# infile = open(args.infile)
# csv_f = csv.reader(infile)

if os.path.exists(args.infile):
		abspath = os.path.abspath(args.infile)
		path_parts = os.path.split(abspath)
		dirname = path_parts[0]
		full_filename = path_parts[1]
		full_filename_split = os.path.splitext(full_filename)
		filename = full_filename_split[0]
		file_ext = full_filename_split[1]
else:
	print "The filepath does not exist!"
	print "Exiting the script."
	sys.exit()

row_limit = args.limit
row_count = 0
current_id = None
first_write = True
header = None
outfile_count = 1
outfolder = "Uploads"
outfiledir = os.path.join(dirname, outfolder)

if not os.path.exists(outfiledir):
		os.makedirs(outfiledir)

def fileWrite (line, n):
	global first_write
	global outfiledir
	global filename
	outfilename = filename + " p" + str(n) + ".csv"
	outfilepath = os.path.join(outfiledir, outfilename)
	if (first_write == True):
		first_write = False
		with open(outfilepath, 'wb') as outfile:
			writer = csv.writer(outfile)
			if (args.firstrow_header == True):
				writer.writerow(header)
				writer.writerow(line)
				#print >> outfile, line
			else:
				writer.writerow(line)
	else:
		with open(outfilepath, 'ab') as outfile:
			writer = csv.writer(outfile)
			writer.writerow(line)
			#print >> outfile, line

with open(args.infile) as infile:
	csv_f = csv.reader(infile)
	if (args.firstrow_header == True):
		header = next(csv_f)
	for row in csv_f:
		row_count += 1
		if (row_count <= row_limit):
			current_id = row[0] 
			#row.append(outfile_count)
			#outfileList.append(row)
			#print outfile_count
			#print "here 1" + outfilename
			#print >> outfile, row
			fileWrite(row, outfile_count)
		elif (row_count > row_limit and row[0] == current_id):
			current_id = row[0]
			#row.append(outfile_count)
			#outfileList.append(row)
			#print "here 2" + outfilename
			#print >> outfile, row
			fileWrite(row, outfile_count)
		elif (row_count > row_limit and row[0] != current_id):
			row_count = 1
			outfile_count += 1
			first_write = True
			#row.append(outfile_count)
			#outfileList.append(row)
			#print "here 3" + outfilename	
			#print >> outfile, row
			fileWrite(row, outfile_count)



#print row_count
# for row in outfileList:
# 	print row
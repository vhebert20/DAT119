# -*- coding: utf-8 -*-
"""
Virginia L Hebert
Sun Dec 06 2020
DAT119, Python 1
Final Project
"""

import csv
import pandas as pd 
import os


"""This program pulls in USGS earthquake data that has been spatially combined (by the writer of the
program) with USGS fault data and attempts to do basic statistical analysis on the dataset as a whole,
or broken out by fault type (normal, thrust/reverse, left lateral, right lateral, strike slip)."""


def header_read(clean_file):
    """list just the headers in the file for easy reference later
    https://www.kite.com/python/docs/csv.DictReader"""    
    file_handler = open(clean_file, "r") # open file
    csv_reader = csv.DictReader(file_handler) # read to file
    print() # aesthetic line
    print(csv_reader.fieldnames) # print just the header row
    file_handler.close()
    return 


def clean_file(file_in, file_out):
    """create a subset of the file with just the columns/attributes to be analyzed 
    https://stackoverflow.com/questions/43697024/how-to-write-only-a-subset-of-fields-using-dictreader-and-dictwriter/43697829"""
    headers = ['name','Depth','Magnitude','age','slipsense','azimuth'] # headers I want - must match headers in original csv
    with open(file_in, newline='') as rf: # open the file
        reader = csv.DictReader(rf, delimiter=',')
        with open(file_out, 'w', newline='') as wf: # create new file
            writer = csv.DictWriter(wf, delimiter=',', extrasaction='ignore', fieldnames=headers) # match headers of old file to new file
            writer.writeheader()
            print() # aesthetic line
            for row in reader:     
               writer.writerow(row)
    return    


def subset_data(clean_file): # fault type in quotes
    """create subsets of the data by fault type
    https://stackoverflow.com/questions/10530301/how-to-filter-from-csv-file-using-python-script"""
    headers = ['name','Depth','Magnitude','age','slipsense','azimuth']
    print("Fault types are Normal, Thrust, Left Lateral, Right Lateral, and Strike Slip.", end = "")
    fault_choice = input("What attribute would you like to export - N, T, LL, RL, or SS? ")            
    while fault_choice.upper() != "N" and fault_choice.upper() != "T" and fault_choice.upper() != "LL" and fault_choice.upper() != "RL" and fault_choice.upper() != "SS":
        print() # aesthetic line
        print("That wasn't a valid choice, try again.")
        fault_choice = input("What attribute would you like to export - N, T, LL, RL, or SS? ")
    else:
        if fault_choice.upper() == "N":
            subset_out = "normal_fault.csv"
        elif fault_choice.upper() == "T":
            subset_out = "thrust_fault.csv"
        elif fault_choice.upper() == "LL":
            subset_out = "left_lateral_fault.csv"
        elif fault_choice.upper() == "RL":
            subset_out = "right_lateral_fault.csv"
        elif fault_choice.upper() == "SS":
            subset_out = "strike_slip_fault.csv"            
    fin = open(clean_file, "r") # open file
    reader = csv.reader(fin) # read to file
    fout = open(subset_out, 'w', newline = "") # create new file for each fault type   
    writer = csv.writer(fout)
    writer.writerow(headers) # write header row
    for column in reader:
       if column[4] == fault_choice.upper(): # adjust "fault_type" for each type of fault
           writer.writerow(column) # write row of data if column matches fault type
    fin.close()
    fout.close()
    return


def data_by_header(clean_file):
    """view file by columns/headers in dictionaries
    https://stackoverflow.com/questions/19486369/extract-csv-file-specific-columns-to-list-in-python/19487003"""    
    with open(clean_file, "r") as file_handler: # open file
        csv_reader = csv.DictReader(file_handler) # read to file
        fault_data = {} # create empty dictionary
        for row in csv_reader:
                for header, value in row.items(): # create dictionary pairs
                    try:
                        fault_data[header].append(value)
                    except KeyError:
                        fault_data[header] = [value]
        print() # aesthetic line
        print(fault_data)
    return 


def read_file(clean_file):
    """basic file read by row"""    
    file_handler = open(clean_file, "r")    
    csv_reader = csv.reader(file_handler)    
    print() # aesthetic line
    for row in csv_reader: 
        print(row)    
    file_handler.close()
    return


def type_tally(clean_file):
    """tally the number of each type of faults"""    
    file_handler = open(clean_file, "r") # open file
    csv_reader = csv.reader(file_handler) # print csv to file
    Normal = 0 # normal count
    Thrust = 0 # thrust count
    LL = 0 # left lateral count
    RL = 0 # right lateral count
    SS = 0 # strike slip count
    none = 0 # if no type is noted
    for flag in csv_reader: # increase tally for each fault if present 
        if flag[4] == "N":
            Normal += 1 
        elif flag[4] == "T":
            Thrust += 1
        elif flag[4] == "R":  # T and R are both thrust faults
            Thrust += 1   
        elif flag[4] == "RL":
            RL += 1  
        elif flag[4] == "LL":
            LL += 1    
        elif flag[4] == "SS":
            SS += 1
        else:
            none += 1
    print() # aesthetic line
    print("FAULT TYPE TALLY")
    print("NormaL Faults:", Normal)    
    print("Thrust Faults:", Thrust)
    print("Left Lateral Faults:", LL)
    print("Right Lateral Faults:", RL)
    print("Strike Slip Faults:", SS)            
    file_handler.close()
    return 
    

def avg_depth_by_fault_type(clean_file):
    """calculate the average depth of earthquake initiation by each fault type"""    
    file_handler = open(clean_file, "r") # open file
    csv_reader = csv.reader(file_handler) # print csv to file
    count_N = 0 # set all counts to 0
    sum_N = 0 # set all sums to 0
    count_T = 0
    sum_T = 0   
    count_RL = 0
    sum_RL = 0    
    count_LL = 0
    sum_LL = 0    
    count_SS = 0
    sum_SS = 0   
    for column in csv_reader:
        if column[4] == "N":
            sum_N = sum_N + float(column[1]) # sum the depths by each fault type
            count_N = count_N + 1 # increase count by one for each instance
            avg_N = format(sum_N / count_N, ".2f") # calculate average by fault type, to two decimal places
        elif column[4] == "T" or column[4] == "R":  # T and R are both thrust faults
            sum_T = sum_T + float(column[1])
            count_T = count_T + 1
            avg_T = format(sum_T / count_T, ".2f")
        elif column[4] == "RL":
            sum_RL = sum_RL + float(column[1])
            count_RL = count_RL + 1
            avg_RL = format(sum_RL / count_RL, ".2f")
        elif column[4] == "LL":
            sum_LL = sum_LL + float(column[1])
            count_LL = count_LL + 1
            avg_LL = format(sum_LL / count_LL, ".2f")
        elif column[4] == "SS":
            sum_SS = sum_SS + float(column[1])
            count_SS = count_SS + 1
            avg_SS = format(sum_SS / count_SS, ".2f")
    print() # aesthetic line
    print("AVERAGE DEPTH OF EARTHQUAKES BY FAULT TYPE")
    print("Normal Faults:", avg_N, "km")
    print("Thrust Faults:", avg_T, "km")
    print("Left Lateral Faults:", avg_LL, "km")
    print("Right Lateral Faults:", avg_RL, "km")
    print("Strike Slip Faults:", avg_SS, "km")
    file_handler.close()    
    return 


def avg_mag_by_fault_type(clean_file):
    """calculate the average depth of earthquake initiation by each fault type"""    
    file_handler = open(clean_file, "r") # open file
    csv_reader = csv.reader(file_handler) # print csv to file
    count_N = 0 # set all counts to 0
    sum_N = 0 # set all sums to 0
    count_T = 0
    sum_T = 0   
    count_RL = 0
    sum_RL = 0    
    count_LL = 0
    sum_LL = 0    
    count_SS = 0
    sum_SS = 0   
    for column in csv_reader:
        if column[4] == "N":
            sum_N = sum_N + float(column[2]) # sum the magnitudes by each fault type
            count_N = count_N + 1 # increase count by one for each instance
            avg_N = format(sum_N / count_N, ".2f") # calculate average by fault type, to two decimal places
        elif column[4] == "T" or column[4] == "R":  # T and R are both thrust faults
            sum_T = sum_T + float(column[2])
            count_T = count_T + 1
            avg_T = format(sum_T / count_T, ".2f")
        elif column[4] == "RL":
            sum_RL = sum_RL + float(column[2])
            count_RL = count_RL + 1
            avg_RL = format(sum_RL / count_RL, ".2f")
        elif column[4] == "LL":
            sum_LL = sum_LL + float(column[2])
            count_LL = count_LL + 1
            avg_LL = format(sum_LL / count_LL, ".2f")
        elif column[4] == "SS":
            sum_SS = sum_SS + float(column[2])
            count_SS = count_SS + 1
            avg_SS = format(sum_SS / count_SS, ".2f")
    print() # aesthetic line
    print("AVERAGE MAGNITUDE OF EARTHQUAKES BY FAULT TYPE")
    print("Normal Faults:", avg_N)
    print("Thrust Faults:", avg_T)
    print("Left Lateral Faults:", avg_LL)
    print("Right Lateral Faults:", avg_RL)
    print("Strike Slip Faults:", avg_SS)
    file_handler.close()    
    return 


def avg_azi_by_fault_type(clean_file):
    """calculate the average azimuth of each fault type"""   
    file_handler = open(clean_file, "r") # open file
    csv_reader = csv.reader(file_handler) # print csv to file
    count_N = 0 # set all counts to 0
    sum_N = 0 # set all sums to 0
    count_T = 0
    sum_T = 0   
    count_RL = 0
    sum_RL = 0    
    count_LL = 0
    sum_LL = 0    
    count_SS = 0
    sum_SS = 0   
    for column in csv_reader:
        if column[4] == "N":
            sum_N = sum_N + int(column[5]) # sum the azimuths by fault type
            count_N = count_N + 1 # increase count by one for each instance
            avg_N = format(sum_N / count_N, ".0f") # calculuate average with no decimals
        elif column[4] == "T" or column[4] == "R": # T and R are both thrust faults
            sum_T = sum_T + int(column[5])
            count_T = count_T + 1
            avg_T = format(sum_T / count_T, ".0f")
        elif column[4] == "RL":
            sum_RL = sum_RL + int(column[5])
            count_RL = count_RL + 1
            avg_RL = format(sum_RL / count_RL, ".0f")
        elif column[4] == "LL":
            sum_LL = sum_LL + int(column[5])
            count_LL = count_LL + 1
            avg_LL = format(sum_LL / count_LL, ".0f")
        elif column[4] == "SS":
            sum_SS = sum_SS + int(column[5])
            count_SS = count_SS + 1
            avg_SS = format(sum_SS / count_SS, ".0f")
    print() # aesthetic line
    print("AVERAGE AZIMUTH OF FAULTS BY FAULT TYPE")
    print("Normal Faults:", avg_N, "degrees")
    print("Thrust Faults:", avg_T, "degrees")
    print("Left Lateral Faults:", avg_LL, "degrees")
    print("Right Lateral Faults:", avg_RL, "degrees")
    print("Strike Slip Faults:", avg_SS, "degrees")
    file_handler.close()    
    return 
    

def age_by_fault_type(clean_file):
    """calculate average age of each fault type"""
    file_handler = open(clean_file, "r") # open the file
    csv_reader = csv.reader(file_handler) # read to file
    count_N = 0 # setting all counts to 0
    sum_N = 0 # setting all sums to 0
    count_T = 0
    sum_T = 0   
    count_RL = 0
    sum_RL = 0    
    count_LL = 0
    sum_LL = 0    
    count_SS = 0
    sum_SS = 0 
    for column in csv_reader:
        column[3] = column[3].replace("<", "") # remove the < from the ages
        column[3] = column[3].replace(",", "") # remove the , from the ages
        if column[4] == "N":
             sum_N = sum_N + int(column[3]) # sum the ages
             count_N = count_N + 1 # increase count by one
             avg_N = format(sum_N / count_N, ".0f") # average to zero decimal places
        elif column[4] == "T" or column[4] == "R": # T and R are both thrust faults
             sum_T = sum_T + int(column[3])
             count_T = count_T + 1
             avg_T = format(sum_T / count_T, ".0f")
        elif column[4] == "RL":
             sum_RL = sum_RL + int(column[3])
             count_RL = count_RL + 1
             avg_RL = format(sum_RL / count_RL, ".0f")
        elif column[4] == "LL":
             sum_LL = sum_LL + int(column[3])
             count_LL = count_LL + 1
             avg_LL = format(sum_LL / count_LL, ".0f")
        elif column[4] == "SS":
             sum_SS = sum_SS + int(column[3])
             count_SS = count_SS + 1
             avg_SS = format(sum_SS / count_SS, ".0f")
    print() # aesthetic line
    print("AVERAGE AGE OF FAULTS BY FAULT TYPE")
    print("Normal Faults:", avg_N, "years")
    print("Thrust Faults:", avg_T, "years")
    print("Left Lateral Faults:", avg_LL, "years")
    print("Right Lateral Faults:", avg_RL, "years")
    print("Strike Slip Faults:", avg_SS, "years")
    file_handler.close()    
    return  


def thrust_fix(clean_data, clean_data_edit):
    """change the "R" to "T" in the fault type column for easier analysis"""
    rf = open(clean_data, 'r') # open the file
    reader = csv.reader(rf) # read to a file
    wf = open(clean_data_edit, 'w', newline='') # create new file
    writer = csv.writer(wf) # create blank to write to
    for column in reader:
        if column[4] == "R":
            column[4] = column[4].replace("R", "T") # switch the T for R
        elif column[4] == "N":
            column[4] = column[4]
        elif column[4] == "T":
            column[4] = column[4]
        elif column[4] == "SS":
            column[4] = column[4]
        elif column[4] == "RL":
            column[4] = column[4]    
        elif column[4] == "LL":
            column[4] = column[4]            
        writer.writerow(column)
    rf.close()
    wf.close()
    return


def basic_plot(file_to_plot, x, y, source):
    """create a basic plot of x vs y using Pandas 
    https://matplotlib.org/3.2.0/gallery/misc/plotfile_demo_sgskip.html"""
    crossplot = pd.read_csv(file_to_plot) # read to file
    crossplot.plot(x, y, color = 'green', marker = 'o', linestyle = '', title = source)
    return


def boxplot(file_to_plot):
    """create a boxplot using Pandas 
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.boxplot.html"""
    plot = pd.read_csv(file_to_plot) # read to file
    boxplot_depth = plot.boxplot("Depth", by = "slipsense") # boxplot of Depth grouped by slipsense
    boxplot_mag = plot.boxplot("Magnitude", by = "slipsense") # boxplot of Magnitude grouped by slipsense
    boxplot_azi = plot.boxplot("azimuth", by = "slipsense") # boxplot of azimuth grouped by slipsense
    return 


def calc_pearson_matrix(file, fault_type):
    """calculating Pearson's correlation 
    https://levelup.gitconnected.com/pearson-coefficient-of-correlation-using-pandas-ca68ce678c04"""
    read_file = pd.read_csv(file) # read to file
    output = read_file.corr(method = 'pearson') # calculating correlation coefficient using Pearson method
    print() # aesthetic line
    print(fault_type.upper(), "CORRELATION COEFFICIENT")
    print(output)
    return


def all_stats(file, fault_type):
    """calculating all basic stats in one fell swoop
    https://stackoverflow.com/questions/45926230/how-to-calculate-1st-and-3rd-quartiles"""
    read_file = pd.read_csv(file) # read to file
    depth_stats = read_file.Depth.describe() # calculate basic stats for Depth of earthquakes
    azimuth_stats = read_file.azimuth.describe() # calculate basic stats for azimuth of faults
    magnitude_stats = read_file.Magnitude.describe() # calculate basic stats for Magnitude of earthquakes
    print() # aesthetic line
    print(fault_type.upper(), "STATISTICS")
    print(depth_stats)
    print() # aesthetic line    
    print(magnitude_stats)
    print() # aesthetic line
    print(azimuth_stats)
    return
  
    
def main():
    """pull all the file operations together and get input from user for file names and output"""   
    print() #aesthetic line    
    print("""This program uses earthquake and fault data from the USGS and does some basic statistics. Please follow the instructions to view the information.""")
    user_file_in = input("Please enter the name of the file you would like to edit, please include punctuation and file type: ")
    while os.path.isfile(user_file_in) == False: # flag if filename not correct
        print() #aesthetic line
        print("That is not valid - please check your DIRECTORY and FILE NAME and try again.")
        user_file_in = input("Please enter the name of the file you would like to edit, please include punctuation and file type: ")    
    else:
        print() #aesthetic line
        print("Only SOME of the columns in the original file are of interest in this analysis, so we will SUBSET the data now.")
        clean_file_out = input("Please enter a name for your SUBSETTED FILE, use underscores and the file type: ")
        clean_file(user_file_in, clean_file_out) # narrow data down to just columns of interest
        print("The HEADERS for the ORIGINAL file were: ", end = "")
        header_read(user_file_in)
        print() #aesthetic line
        print("The HEADERS for the SUBSET file are: ", end = "")
        header_read(clean_file_out)
        print() #aesthetic line
        print() #aesthetic line
        print("Since REVERSE and THRUST faults are the same thing, we will next run a process on the subsetted file that makes R = T.")
        print("We will call this one 'user_file_editted' and use it in the plots and Panda analyses.")
        thrust_fix(clean_file_out, "user_file_editted.csv") # creating new file with R changed to T, for thrust faults
        print() #aesthetic line
        user_choice = input("Now, would you like to run statistics/analysis or export data subsets? Choose STATS or EXPORT: ") 
        user_choice = user_choice.lower()
        for decision in user_choice:
            if decision in user_choice == "stats": # print out statistics for full and editted files
#                read_file(clean_file_out) # basic file print out, by row
                type_tally(clean_file_out) # tally of the number of faults of each type
                avg_depth_by_fault_type(clean_file_out) # average depth of each fault type
                avg_azi_by_fault_type(clean_file_out) # average azimuth of each fault type
                avg_mag_by_fault_type(clean_file_out) # average magnitude of each fault type
                age_by_fault_type(clean_file_out) # average age of each fault type
                all_stats("user_file_editted.csv", "ALL faults") # all basic stats for data in file
                calc_pearson_matrix("user_file_editted.csv", "ALL faults") # create matrix of correlation coefficient for data in file
                basic_plot("user_file_editted.csv", "Depth", "Magnitude", "All Data") # create a depth vs magnitude plot for data in file
                boxplot("user_file_editted.csv") # create a boxplot comparing attributes for each fault type
                fault_files = input("Would you like to create subfiles for each of the fault types, yes or no? ") # give the option to subset data by fault type
                while fault_files.lower() != "no":   
                    if fault_files.lower() != "yes": # flag for invalid answer    
                        print() #aesthetic line    
                        print("You didn't make a valid choice, try again.")
                        fault_files = input("Would you like to create subfiles for each of the fault types, yes or no? ")
                    elif fault_files.lower() == "yes":
                        print() #aesthetic line
                        subset_data("user_file_editted.csv") # create new csv with data based on fault type
                        fault_files = input("Would you like to create another subfile, yes or no? ")                    
                else: 
                    print() #aesthetic line 
                    print("I hope you found this information informative! Thanks for checking it out.")
                    break
            elif decision in user_choice == "export": # user chooses to just export to new files by fault type
                print() #aesthetic line
                subset_data("user_file_editted.csv") # create new csv with data based on fault type
                fault_files = input("Would you like to create another subfile, yes or no? ")    
                while fault_files.lower() != "no":
                    if fault_files.lower() != "yes": # flag for invalid answer    
                        print("You didn't make a valid choice, try again.")
                        fault_files = input("Would you like to create subfiles for each of the fault types, yes or no? ")
                    elif fault_files.lower() == "yes":
                        print() #aesthetic line
                        subset_data("user_file_editted.csv") # create new csv with data based on fault type
                        fault_files = input("Would you like to create another subfile, yes or no? ")                    
                else: 
                    print() #aesthetic line 
                    print("I hope you found this information informative! Thanks for checking it out.")
                    break
            else:
                print() #aesthetic line
                print("You didn't make a valid choice, try again.")
                user_choice = input("Would you like to run statistics or export data subsets? Choose STATS or EXPORT: ")      
    return

            
if __name__ == "__main__":
    main()
    

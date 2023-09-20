#! /usr/env python3
"""
Genomics CoFa Job interview assessment
Author: Yasmijn Balder

I created a separate files for the tables,
because I didn't have the time to parse the excel file
"""

from sys import argv
import csv

def main():
    """This code will be executed when called from the command line
    """

    # Create an empty dictionary for the samples and sequencing measurement
    platelayout = {}

    # Go through all for plates
    for plate in range(1,5):
        # Create strings with the format of the plate files
        emptysamplestring = "./Plate{} SampleIDs.csv"
        emptyconcstring = "./Plate{} conc..csv"
        # Create a specific string for the current plate number
        samplestring = emptysamplestring.format(plate)
        concstring = emptyconcstring.format(plate)
        # Create a dictionary with the sample and sequencing measurement
        platedict = merge_sample_conc(samplestring, concstring)
        # Add this plate's samples to the dictionary
        platelayout.update(platedict)


    # Create an emtpy dictionary for the QC metrics
    qcmetrics = {}

    # Open the csv file with the QC metrics
    with open("./Pipeline QC metrics.csv", 'r') as file:
        metricsfile = csv.reader(file)
        # Set a count at 0 to skip the header
        count = 0
        # Go through each row
        for row in metricsfile:
            if count == 0:
                # Skip the header
                count += 1
            else:
                # Separate the metrics
                metrics = row[0].split(';')
                # Save the sample ID to the dictionary with the list of metrics
                qcmetrics[metrics[0]] = [metrics[1], metrics[2], metrics[3], metrics[4], metrics[5]]

    # How many samples are there?
    print(len(qcmetrics))

def merge_sample_conc(sample_file, conc_file):
    """
    """
    # Create empty lists and a dictionary for the samples and measurements
    sampleslist = []
    conclist = []
    sampledict ={}

    # Open the csv file with the samples
    with open(sample_file, 'r') as sfile:
        samplesfile = csv.reader(sfile, delimiter = ';')
        # Set a count at 0 to skip the header
        count = 0
        # Go through each row
        for row in samplesfile:
            if count == 0:
                # Skip the header
                count+=1
            else:
                # Go through each sample
                for samples in row:
                    # Make sure that the well was not empty
                    if len(samples) > 1:
                        # Add list sample to the list
                        sampleslist.append(samples)

    # Open the csv file with the concentrations
    with open(conc_file, 'r') as cfile:
        concfile = csv.reader(cfile, delimiter = ';')
        # Set a count at 0 to skip the header
        count = 0
        # Go through each row
        for row in concfile:
            if count == 0:
                # Skip the header
                count += 1
            else:
                # Go through each measurement
                for conc in row:
                    # Make sure that the well was not empty
                    if len(conc) > 1:
                        # Add this measurement to the list
                        conclist.append(conc)

    # Create a dictionary, linking each sample with its measurement
    for count, row in enumerate(sampleslist):
        sampledict[row] = conclist[count]

    return sampledict

if __name__ == "__main__":
    main()

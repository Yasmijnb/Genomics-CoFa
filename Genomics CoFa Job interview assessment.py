#! /usr/env python3
"""
Genomics CoFa Job interview assessment
Author: Yasmijn Balder

I created a separate files for the tables,
because I didn't have the time to parse the excel file
"""

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
    print("{} samples input".format(len(platelayout)))
    print("{} samples have QC metrics".format(len(qcmetrics)))

    # Which samples are missing?
    print("\nThe following samples {} were not QC'ed:".format(len(platelayout)-len(qcmetrics)))
    print(platelayout.keys() - qcmetrics.keys())

    # How many samples have no read count?
    print("\nThe following {} samples have no read count".
    format(sum(measurement == "#NUM!" for measurement in platedict.values())))
    print([key for key, value in platedict.items() if value == "#NUM!"])

def merge_sample_conc(filename_one, filename_two):
    """Creates a dictionary with items from filename_one as keys and items from
    filename_two as values.

    Keyword arguments:
    filename_one -- string, file name of first csv file
    filename_two -- string, file name of second csv file
    """
    # Create empty lists and a dictionary for the data
    datalist_one = []
    datalist_two = []
    datadict ={}

    # Open the first csv file
    with open(filename_one, 'r') as fileone:
        file = csv.reader(fileone, delimiter = ';')
        # Set a count at 0 to skip the header
        count = 0
        # Go through each row
        for row in file:
            if count == 0:
                # Skip the header
                count += 1
            else:
                # Go through each value
                for value in row:
                    # Make sure a value is present
                    if len(value) > 1:
                        # Add list value to the list
                        datalist_one.append(value)

    # Open the second csv file
    with open(filename_two, 'r') as filetwo:
        file = csv.reader(filetwo, delimiter = ';')
        # Set a count at 0 to skip the header
        count = 0
        # Go through each row
        for row in file:
            if count == 0:
                # Skip the header
                count += 1
            else:
                # Go through each value
                for value in row:
                    # Make sure that a value is present
                    if len(value) > 1:
                        # Add this value to the list
                        datalist_two.append(value)

    # Create a dictionary, linking the item from table one with table two
    for count, value in enumerate(datalist_one):
        datadict[value] = datalist_two[count]

    return datadict

if __name__ == "__main__":
    main()

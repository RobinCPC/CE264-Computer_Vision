"""
A script to read dataset in different folder, test with Tesseract OCR, and
check the correctness with Levenshtein metric. Finally, will write the results
in csv file.
"""

import os
import glob
import csv
from stringMetirc import levenshteinDistance as ltDistance
from stringMetirc import read_file

def read_input( file, names, txts):
    with open(file, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            names.append(row[0])
            txts.append(row[1])

    # get rid off title
    names.pop(0)
    txts.pop(0)



if __name__ == '__main__':
    # get current directory
    folders = glob.glob('*/')
    print folders

    # move into each folder
    for fd in folders:
        print fd
        os.chdir(fd)     # move in
        # read input.csv (input dataset)
        in_file = 'InputData.csv'
        fname, true_text = [], []
        read_input(in_file, fname, true_text)
        #for f, t in zip(fname, true_text):
        #    print f,t

        # run tesseract
        import subprocess
        ocr_texts = []
        for fn in fname:
            tess_cmd = 'tesseract ' + fn + ' ' + fn[0:-4]
            ocr_str = subprocess.check_output(tess_cmd, shell=True)
            #ocr_texts.append(ocr_str)


        # read file to get ocr_output
        ocr_texts = []
        for fn in fname:
            file_name = fn[0:-3] + 'txt'
            #file_name = 'r_'+ fn[5:-3] +'txt'
            #print file_name

            #file_object = open(file_name, 'r')
            #ocr_texts.append(file_object.read())
            ocr_str = read_file(file_name)
            ocr_texts.append(ocr_str)
            #ocr_texts.append('\n'.join(ocr_str))

            #print ocr_text
        #for t in ocr_texts:
        #    print t

        # run Levenshtein
        levens = []
        for fn, src, res in zip(fname, true_text, ocr_texts):
            dis = ltDistance(src, res)
            levens.append(dis)
            #print 'File: %s' % fn
            #print 'True: %s' % src
            #print 'OCR: %s' % res
            #print 'Diff: %d' % dis

        # write to CSV file
        out_stat = 'result_stat.csv'
        with open(out_stat, 'wb') as csvfile:
            writeCSV = csv.writer(csvfile, delimiter=',')
            writeCSV.writerow(('Source', 'File_name', 'True_text', 'ocr_text', 'Levenshtein', 'Param'))
            for fn, src, res, dis in zip(fname, true_text, ocr_texts, levens):
                writeCSV.writerow((fd[0:-1], fn, src, res, dis, 'None'))


        os.chdir('..')  # move out


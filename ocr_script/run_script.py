"""
A script to read dataset in different folder, test with Tesseract OCR, and
check the correctness with Levenshtein metric. Finally, will write the results
in csv file.

Example Tesseract CLI: tesseract --tessdata-dir /usr/share imagename outputbase -l eng -psm 3
"""

import os
import glob
import csv
from stringMetirc import levenshteinDistance as ltDistance
from stringMetirc import read_file

def read_input( file, names, txts):
    import pdb
    pdb.set_trace()
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
        out_stat = 'result_stat_' + fd[0:-1] + '.csv'
        csvfile = open(out_stat, 'wb')
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(('Source', 'File_name', 'True_text', 'ocr_text', 'Levenshtein', 'Param', 'Config'))

        # run tesseract, compute Levenshtein metric and save results to CSV
        import subprocess
        #ocr_texts = []
        for ind, fn in enumerate(fname):
            # Baselien command for Tesseract.
            tess_cmd = 'tesseract ' + fn + ' ' + fn[0:-4]
            #ocr_str = subprocess.check_output(tess_cmd, shell=True)
            os.system(tess_cmd)
            #ocr_texts.append(ocr_str)
            file_name = fn[0:-3] + 'txt'
            print file_name
            ocr_text = read_file(file_name)
            dis = ltDistance(true_text[ind], ocr_text)
            writeCSV.writerow((fd[0:-1], fn, true_text[ind], ocr_text, dis, 'None', 'None'))

            # Add Page Segmentation Modes (-psm)
            psm_para = [1, 3, 4, 5, 6, 7, 8, 9, 10]
            for p in psm_para:
                fn_out = fn[:-4] + '_psm' + str(p)
                tess_cmd = 'tesseract ' + fn + ' ' + fn_out + ' -psm ' + str(p) + ' -c textord_heavy_nr=1'
                #ocr_str = subprocess.check_output(tess_cmd, shell=True)
                os.system(tess_cmd)
                #print tess_cmd
                file_name = fn_out + '.txt'
                ocr_text = read_file(file_name)
                dis = ltDistance(true_text[ind], ocr_text)
                writeCSV.writerow((fd[0:-1], fn, true_text[ind], ocr_text, dis, str(p), 'textord_heavy_nr=1'))



        # read file to get ocr_output
#        ocr_texts = []
#        for fn in fname:
#            file_name = fn[0:-3] + 'txt'
#            #file_name = 'r_'+ fn[5:-3] +'txt'
#            #print file_name
#
#            #file_object = open(file_name, 'r')
#            #ocr_texts.append(file_object.read())
#            ocr_str = read_file(file_name)
#            ocr_texts.append(ocr_str)
#            #ocr_texts.append('\n'.join(ocr_str))
#
#            #print ocr_text
#        #for t in ocr_texts:
#        #    print t
#
#        # run Levenshtein
#        levens = []
#        for fn, src, res in zip(fname, true_text, ocr_texts):
#            dis = ltDistance(src, res)
#            levens.append(dis)
#            #print 'File: %s' % fn
#            #print 'True: %s' % src
#            #print 'OCR: %s' % res
#            #print 'Diff: %d' % dis
#
#        # write to CSV file
#        out_stat = 'result_stat.csv'
#        with open(out_stat, 'wb') as csvfile:
#            writeCSV = csv.writer(csvfile, delimiter=',')
#            writeCSV.writerow(('Source', 'File_name', 'True_text', 'ocr_text', 'Levenshtein', 'Param'))
#            for fn, src, res, dis in zip(fname, true_text, ocr_texts, levens):
#                writeCSV.writerow((fd[0:-1], fn, src, res, dis, 'None'))

        csvfile.close()

        os.chdir('..')  # move out


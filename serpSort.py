def loadData(fName):
    serpDatLst = []
    f = open(fName)
    serpHdrLst = f.readline().strip().split(',')
    for line in f:
        serpDatLine = line.strip().split(',')
        serpDatLst.append([int(x) for x in serpDatLine] )
    f.close
    #return serpHdrLst, serpDatLst[0:11]  # return only first few ... for debug.
    return serpHdrLst, serpDatLst       # return all for non-debug.
#############################################################################

def rangeData(serpHdrLst, serpDatLst):
    minMaxLst = []
    for hIdx,hdr in enumerate(serpHdrLst):
        valLst = []
        for vals in serpDatLst:
            valLst.append(vals[hIdx])
        minVal = min(valLst)
        maxVal = max(valLst)
        minMaxLst.append((minVal, maxVal))
    return minMaxLst
#############################################################################

def genSerpSearchCriteriaLst(minMaxLst):
    import math

    diffs       = [b-a+1 for a,b in minMaxLst]
    numToGen    = math.prod(diffs)
    should      = ['inc'] * len(minMaxLst)
    currVals    = [x[0] for x in minMaxLst]
    serpSrchLst = []

    while len(serpSrchLst) < numToGen:

        serpSrchLst.append(currVals[:]) # <-- the ':' fixed a bug.

        for idx in range(len(currVals)-1, -1, -1):
            if should[idx] == 'inc':
                currVals[idx] += 1
                if currVals[idx]  > minMaxLst[idx][1]:
                    currVals[idx] = minMaxLst[idx][1]
                    should[idx] = 'dec'
                    continue

            if should[idx] == 'dec':
                currVals[idx] -= 1
                if currVals[idx]  < minMaxLst[idx][0]:
                    currVals[idx] = minMaxLst[idx][0]
                    should[idx] = 'inc'
                    continue

            break

    return serpSrchLst
#############################################################################

def genSerpSortedDataLst(serpSearchCriteriaLst, serpDataLst):
    serpSortedDataLst = []
    for critera in serpSearchCriteriaLst:
        for data in serpDataLst:
            if data == critera:
                serpSortedDataLst.append(data)
    return serpSortedDataLst
#############################################################################

def writeSerpToFile(serpHdr, serpDatLst):
    with open('serp_output.txt', 'w') as f:
        for val in serpHdr:
            f.write('{} '.format(val))
        f.write('\n')
        for vals in serpDatLst:
            for val in vals:
                f.write('{:2} '.format(val))
            f.write('\n')
    return
#############################################################################

def getFileName():
    from os import listdir
    from   os.path import isfile

    filesToDisplay = [f for f in listdir('.') if isfile(f) and f.endswith('.csv')]
    lclDict = {k: v for k,v in enumerate(filesToDisplay)}
    sortedKeys = sorted([k for k in lclDict.keys()])

    print()
    for k  in sortedKeys:
        print(' {:2d}: {}'.format(k, lclDict[k]) )
    print('  q: quit\n')

    valid = False
    while not valid:
        choice = input('  File to process --> ')
        if choice == 'q':
            return 'q'
        try:
            choiceInt = int(choice)
            valid = True
        except:
            print('  Invalid choice, try again')
        else: # there was no exception (conversion to int worked).
            if choiceInt not in sortedKeys:
                valid = False
                print('  Invalid choice, try again')

    return lclDict[choiceInt]
#############################################################################

if __name__ == '__main__':
    import pprint as pp

    inputFile = getFileName()
    if inputFile == 'q':
        print('\n  Exiting.\n')
        exit()
    else:
        print( '\n  Processing {}'.format(inputFile))

    serpHdr, serpDatLst = loadData(inputFile)
    print('\n  Unsorted data loaded.')
    minMaxLst = rangeData(serpHdr, serpDatLst)
    print('  Data ranged.')
    serpSearchCriteriaLst = genSerpSearchCriteriaLst(minMaxLst)
    print('  Serpentine counter created.')
    serpSortedDatLst = genSerpSortedDataLst(serpSearchCriteriaLst, serpDatLst)
    print('  Sorted data created.')
    writeSerpToFile(serpHdr, serpSortedDatLst)
    print('  Sorted data written to serp_output.txt.\n')

    #debug = True
    debug = False
    if debug:
        thingsToPprint = [serpDatLst, serpSortedDatLst]
        #thingsToPprint = [serpSearchCriteriaLst, serpDatLst, serpSortedDatLst]
        for x in thingsToPprint:
            print()
            pp.pprint(x)
            print()
        print(len(serpDatLst), len(serpSortedDatLst))

from sgeBuilder import buildSGE
import numpy as np

def iterateHomogeneous(homog, path):
    '''Loops through user's options for geochmistry ranges in hydrogen and 
    chlorine. Step choices of zero result in a constant abundance for that 
    species which is set by the minimum value they chose.
    
    Args:
        homog (dictionary) : User choices of geochemistry ranges from prompt
        path (string) : path to where the modeling grid files are stored
    
    Author: Travis Gabriel
    Last Edit: 5 Sept. 2016 - Tidied up comments, added option for a single 
        geochemistry (see 'if' statement).'''
    
    #Here, the user want to hold both species constant by setting the step 
    #value to zero. The minimum of both species is then used.
    if(homog['stepH'] == 0.0 and homog['stepCl'] == 0.0):
        WEH  = homog['minH']
        wtCl = homog['minCl']
        geochemistry = buildGeochemistry(homog['base'], WEH, wtCl)
        writeHomogeneousMCNPX(geochemistry, WEH, wtCl, path)
    #User wants to hold hydrogen constant, so step through chlorine values
    elif(homog['stepH']==0.0):
        #Set constant value of hydrogen to the minimum
        WEH=homog['minH']
        #generate list of chlorine values
        ClList = np.arange(homog['minCl'], homog['maxCl'], homog['stepCl'])
        #If the last item isn't the maximum, add it explicitly
        if(ClList[-1] != homog['maxCl']):
            ClList = np.append(ClList,homog['maxCl'])
        #Loop through chlorine list, build geochemistries, write MCNPX file
        for wtCl in ClList:
            geochemistry = buildGeochemistry(homog['base'], WEH, wtCl)
            writeHomogeneousMCNPX(geochemistry, WEH, wtCl, path)
    #User wants to hold hydrogen constant, so step through chlorine values
    elif(homog['stepCl']==0.0):
        #Set constant value of chlorine to the minimum
        wtCl = homog['minCl']
        #generate list of hydrogen values
        HList = np.arange(homog['minH'], homog['maxH'], homog['stepH'])
        #If the last item in the list isnt the maximum, add it explicitly
        if(HList[-1] != homog['maxH']):
            HList = np.append(HList,homog['maxH'])
        #loop through chlorine list, build geochem, write MCNPX file
        for WEH in HList:
            geochemistry = buildGeochemistry(homog['base'], WEH, wtCl)
            writeHomogeneousMCNPX(geochemistry, WEH, wtCl, path)
    #Here is a standard case where the user wants to loop through Hydrogen 
    #and chlorine values. Generally it follows the same procedures as above
    else:
        HList = np.arange(homog['minH'], homog['maxH'], homog['stepH'])
        if(HList[-1] != homog['maxH']):
            HList = np.append(HList,homog['maxH'])
        for WEH in HList:
            ClList = np.arange(homog['minCl'], homog['maxCl'], homog['stepCl'])
            if(ClList[-1] != homog['maxCl']):
                ClList = np.append(ClList,homog['maxCl'])
            for wtCl in ClList:
                geochemistry = buildGeochemistry(homog['base'], WEH, wtCl)
                writeHomogeneousMCNPX(geochemistry, WEH, wtCl, path)
#end of iterateHomogeneous

def buildGeochemistry(base, WEH, wtCl):
    '''Computes geochemical abundances where oxygen is swapped out for 
    hydrogen and chlorine abundance. This is because oxygen interacts weakly
    with neutrons.
    
    Args:
        base (dictionary): Essentially an array whose indicies are 
            the chemical species of interest and the value is the percentage 
            abundance as computed by buildGeochemistry().
        WEH (float) : Water equivalent hydrogen weight percentage
        wtCl (float) : Chlorine weight percentage
    Returns:
        geochemistry (dictionary) : altered geochemistry from the base where 
            Hydrogen and chlorine were added
    
    Author: Travis Gabriel, adapted from Jack Lightholder scripts
    Last Edit: 5 Sept. 2016 - Tidied up comments.'''
    
    #Find wt% hydrogen from WEH
    wtH = (WEH/9.)/100.
    
    #Find wt% oxygen from WEH, deprecated
    #O = WEH * (16/18.)/100.
    wtCl /= 100.
    
    #Load the base geochemistry file for the grid (usually informed by APXS/SAM/Chemin results)
    elementDict = dict(np.genfromtxt(base, names=['elements','wt%'], dtype="U2,<f8"))
    
    #Set Hydrogen abundance and sum up all abundances including the newly 
    #added hydrogen
    elementDict['H'] = np.copy(wtH)
    tmpSum = 0.0
    for element,abundance in elementDict.items():
        tmpSum += abundance
    
    #Delta should be the excess hydrogen amount
    delta = tmpSum - 1.0
    
    #Subtract excess hydrogen abundence from Oxygen
    elementDict['O'] -= delta
    
    #Repeat above, but for chlorine
    elementDict['Cl'] = np.copy(wtCl)
    tmpSum = 0.0
    for element,abundance in elementDict.items():
       tmpSum += abundance
    
    #Delta should be the excess chlorine amount
    delta = tmpSum - 1.0
    
    #Subtract excess abundence due to chlorine from oxygen
    elementDict['O'] -= delta
    
    #COMPUTE FINAL ABUNDANCE FOR CHECKS, SHOULD BE 1.00000 to high precision
    tmpSum = 0.0
    for element,abundance in elementDict.items():
        tmpSum += abundance
    #High precision check of abundance
    if(np.abs(tmpSum -1) > 1e13):
        print('Error: Geochemistry did not sum to 1. SUM: '+tmpSum)
    
    wtCl *= 100.
    return(elementDict)
#end of buildGeochemistry

def writeHomogeneousMCNPX(geochemistry, WEH, wtCl, pathGrids, sge=True):
    '''Writes a homogeneous geochemistry for one of the layers in a 2 layer 
    MCNPX file. An appropriately modified reference 2 layer MCNPX file must 
    be made so the routine can identify where to write the geochemistry before 
    it can be used as an input to this function.
    
    Args:
       geochemistry (dictionary): Essentially an array whose indicies are 
          the chemical species of interest and the value is the percentage 
          abundance as computed by buildGeochemistry().
       WEH (float) : Water equivalent hydrgen value for this file. This ensures 
          that the filename string is formatted to reflect the geochemistry.
       wtCl (float) : Same as WEH, but for Chlorine
       pathGrids (string) : Where the modeling grid files are stored
       sge (Optional[boolean]) : A flag that is used to decide wether a .sge
          file is written for the Newton cluster in addition to the MCNPX 
          input file.
       *args: Variable length argument list. Used to catch extraneous arguments, warn the user, and not halt execution.
    
    Author: Travis Gabriel, adapted from Jack Lightholder scripts
    Last Edit: 5 Sept. 2016 - Tidied up comments, changed from Jack's tabbing 
       to PEP-8 compliant 4-space indentations.'''
    
    #Build filename for MCNPX input that reflects the modeled abundances 
    #for this grid point. In the future it will be useful to list the 
    #abundance of Fe used in the geochemistry, but for now on the DAN project
    #we are keeping this constant per grid.
    fileNameGridPoint = str(wtCl) + 'CL_' + str(WEH) + 'H_Homogeneous.mx'
    
    #Open the reference input file for a 2-layer geochemistry of variable 
    #depth. The geochemistry lines are absent in this file and replaced
    #by double-hash flags, "##" denoting the layer number
    ref = open('inputref.txt')
    
    #Open the file you want to use at the MCNPX input for writing
    filePathGridPoint = pathGrids + 'mcnpx_inputs/'+ fileNameGridPoint
    writ = open(filePathGridPoint,'w')
    
    #Copy the lines in the reference file to the new file, except for 
    #the goechemistry and the geometry
    for line in ref:
        if(  line == '##Layer1\n'):
            soilCalculator(writ,    'top', geochemistry)
        elif(line == '##Layer2\n'):
            soilCalculator(writ, 'bottom', geochemistry)
        elif(line[:21] == 'c Surface description'):
            depthWriter(writ, 80.0000, 180.0000) #Top layer depth, bottom layer depth
        else:
            writ.write(line)
    
    #Close file writers
    ref.close()
    writ.close()
    
    #Make .sge input file for queing on Newton computing cluster
    if(sge == True):
        buildSGE(pathGrids, fileNameGridPoint)
#end of writeHomogeneousMCNPX

def soilCalculator(writ, layer, geo):
    '''Writes geochemistry to an MCNPX input file. Right now the routine 
    requires a hardcoded element species ID. Extraneous species in the 
    geochemistry dictionary will be ignored.
    
    Args:
        writ (file object) : Object for the MCNPX file with the new geochemistry.
        layer (string) : Either 'top' or 'bottom'. Tells the routine which 
            layer to write the geochemistry for.
        geo (dictionary): Essentially an array whose indicies are 
            the chemical species of interest and the value is the percentage 
            abundance as computed by buildGeochemistry().
    
    Author: Travis Gabriel, adapted from Jack Lightholder scripts
    Last Edit: 5 Sept. 2016 - Tidied up comments'''
    
    if(layer == 'top'):
        writ.write('m7010  $ Soil composition\n')
        writ.write('        8016.24c      -%0.9f\n'%(geo['O']))
        writ.write('       11023.60c      -%0.9f\n'%(geo['Na']))
        writ.write('       12000.60c      -%0.9f\n'%(geo['Mg']))
        writ.write('       13027.24c      -%0.9f\n'%(geo['Al']))
        writ.write('       14000.21c      -%0.9f\n'%(geo['Si']))
        writ.write('       15031.42c      -%0.9f\n'%(geo['P']))
        writ.write('       16000.60c      -%0.9f\n'%(geo['S']))
        writ.write('       19000.60c      -%0.9f\n'%(geo['K']))
        writ.write('       20000.42c      -%0.9f\n'%(geo['Ca']))
        writ.write('       22000.42c      -%0.9f\n'%(geo['Ti']))
        writ.write('       24000.42c      -%0.9f\n'%(geo['Cr']))
        writ.write('       25055.42c      -%0.9f\n'%(geo['Mn']))
        writ.write('       26000.21c      -%0.9f\n'%(geo['Fe']))
        writ.write('       28000.42c      -%0.9f\n'%(geo['Ni']))
        writ.write('       30000.40c      -%0.9f\n'%(geo['Zn']))
        writ.write('       35079.55c      -%0.9f\n'%(geo['Br']))
        writ.write('        1001.42c      -%0.9f\n'%(geo['H']))
        writ.write('       17000.60c      -%0.9f\n'%(geo['Cl']))
    elif(layer == 'bottom'):
        writ.write('m8010  $ Soil composition\n')
        writ.write('        8016.24c      -%0.9f\n'%(geo['O']))
        writ.write('       11023.60c      -%0.9f\n'%(geo['Na']))
        writ.write('       12000.60c      -%0.9f\n'%(geo['Mg']))
        writ.write('       13027.24c      -%0.9f\n'%(geo['Al']))
        writ.write('       14000.21c      -%0.9f\n'%(geo['Si']))
        writ.write('       15031.42c      -%0.9f\n'%(geo['P']))
        writ.write('       16000.60c      -%0.9f\n'%(geo['S']))
        writ.write('       19000.60c      -%0.9f\n'%(geo['K']))
        writ.write('       20000.42c      -%0.9f\n'%(geo['Ca']))
        writ.write('       22000.42c      -%0.9f\n'%(geo['Ti']))
        writ.write('       24000.42c      -%0.9f\n'%(geo['Cr']))
        writ.write('       25055.42c      -%0.9f\n'%(geo['Mn']))
        writ.write('       26000.21c      -%0.9f\n'%(geo['Fe']))
        writ.write('       28000.42c      -%0.9f\n'%(geo['Ni']))
        writ.write('       30000.40c      -%0.9f\n'%(geo['Zn']))
        writ.write('       35079.55c      -%0.9f\n'%(geo['Br']))
        writ.write('        1001.42c      -%0.9f\n'%(geo['H']))
        writ.write('       17000.60c      -%0.9f\n'%(geo['Cl']))
#end of soilCalculator

def depthWriter(writ, topLayerDepth, bottomLayerDepth):
    '''Writes depth information of layer 1 and 2 in the 2-layer MCNPX geochemistry
     model.
    
    Args:
        writ (file object) : Object for the MCNPX file with the new geochemistry.
        topLayerDepth (float) : depth of the top layer in cm
        bottomLayerDepth (float) : depth of the bottom layer in cm
    
    Author: Travis Gabriel, adapted from Jack Lightholder scripts
    Last Edit: '''
    writ.write('c Surface description\n')
    topInfo    = '31        pz -' + str(topLayerDepth) + '   $ Top layer\n'
    bottomInfo = '32        pz -' + str(bottomLayerDepth) + ' $ 2nd subsurface layer\n'
    writ.write(topInfo)
    writ.write(bottomInfo)
#end of depthWriter

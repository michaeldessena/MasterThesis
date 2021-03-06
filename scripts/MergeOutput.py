import os 
import sys
import glob
import shutil
import argparse



def PreSet(dir=[]):
    for item in dir:    # {PATH}/output*
        path=os.path.join(pathMAIN, item)
        subdir=glob.glob(os.path.join(path, '*/'))
        for sub in subdir:  #{PATH}/output{name}/00*
            result=os.path.join(sub, 'result.yoda')
            if os.path.exists(result)==False:
                for i in dir:
                    head_tail= os.path.split(sub)
                    aa = head_tail[0]
                    a = os.path.normpath(aa)
                    a = a.split(os.sep)
                    a = a[-1]
                    subb = os.path.join(pathMAIN, i, a)
                    try:
                        shutil.rmtree(subb)
                        print('removed {} <--------------------'.format(subb))
                    except:
                        print('Doesnt removed'.format(subb))
                        #pass
    number=[]
    for item in dir:
        path=os.path.join(pathMAIN, item)
        subdir=glob.glob(os.path.join(path, '*/'))
        k=0
        for sub in subdir:
            k=k+1
        number.append(k)
    
    maxim = max(number)
    #differ = []
    #for i in number:
    #    diff = i-minor
    #    differ.append(int(diff))

    print('##############################################################################')
    #for item in dir:    # {PATH}/output*
    #    path=os.path.join(pathMAIN, item)
    #    subdir=glob.glob(os.path.join(path, '00*'))
    #    for i in differ:
    #        if i != 0:
    #            a=subdir[-i]
    #            try:
    #                shutil.rmtree(a)
    #                print('removed {} <--------------------'.format(a))
    #            except:
    #                print('Doesnt Removed {}'.format(a))
    #                #pass
    #
    for item in dir:
        path=os.path.join(pathMAIN, item)
        subdir=glob.glob(os.path.join(path, '*/'))
        for sub in subdir:
            head_tail= os.path.split(sub)
            aa = head_tail[0]
            a = os.path.normpath(aa)
            a = a.split(os.sep)
            a = a[-1]

            #print(a)
            maxim = str(maxim).zfill(4)
            
            subb = os.path.join(pathMAIN, item, a)
            #print('if ', a, ' > ', maxim)
            if int(a)>int(maxim):
                try:
                    shutil.rmtree(subb)
                    print('removed {} <--------------------'.format(subb))
                except:
                    print('Doesnt Removed {}'.format(subb))
                    #pass

    for item in dir:
        cmd = './checkMySimulation2.sh {}'.format(item) 
        os.system(cmd)


def SetOUTPUT(directories = []):
    dir = directories
    #a = '' 
    #MAINcontent = os.listdir(pathMAIN) 
    #while a != 'stop':
    #    a = input('Insert a folder output to merge, once you have inserted all the direcotry digit "stop"')
#
    #    if a != 'stop' and a in MAINcontent:
    #        dir.append(os.path.join(pathMAIN,a))
    #    elif a not in MAINcontent:
    #        print('The choosen directory is not in {}'.format(pathMAIN))

    kk=0
    names = []
    for item in dir:
        name = ''
        if '13TeV2' in item:
            name='13TeV2' 
        elif '7TeV' in item:
            name= '7TeV'
        elif '1TeV' in item:
            name ='1TeV'
        elif '13TeV' in item:
            name='13TeV'

        names.append(name)
        dirContent = glob.glob(os.path.join(item, '*/'))
        print(dirContent)
        if kk==0:
            #for j in dirContent:

            shutil.copytree(os.path.join(item), pathDESTINATION)
            dirContent=glob.glob(os.path.join(item, '*/'))
            k=0
            for j in dirContent:
                k_filled = str(k).zfill(4)
                try:
                    os.rename(os.path.join(pathDESTINATION, k_filled,'result.yoda'), os.path.join(pathDESTINATION, k_filled,'result{}.yoda'.format(name)) )
                except:
                    pass
                k=k+1

            #print('MOVE:  {} -----> {}'.format(os.path.join(j),pathDESTINATION))
        else:
            k=0
            for j in dirContent:
                k_filled = str(k).zfill(4)
                try:
                    shutil.copy(os.path.join(j, 'result.yoda'), os.path.join(pathDESTINATION, k_filled, 'result{}.yoda'.format(name)))
                except:
                    pass
                #print('MOVE:  {} -----> {}'.format( os.path.join(j, 'result.yoda'), os.path.join(pathDESTINATION, k_filled, 'result{}.yoda'.format(name)) ) )
                k=k+1
        kk=kk+1

def Merge():
    
    dirContent=glob.glob(os.path.join(pathDESTINATION, '*/'))
    for item in dirContent:
        cmd = 'yodamerge --output {}'
        cmd = cmd.format(os.path.join(item, 'result.yoda'))
        resultContent = glob.glob(os.path.join(item, 'result*.yoda')) 
        for file in resultContent:
            cmd = cmd + ' ' + file
        print(cmd+'\n')
        os.system(cmd)

if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Run all the MCNNTUNES tuning program')
    parser.add_argument("data_folders", nargs='+', metavar='DATA FOLDER', type=str,help="input data folder")
    parser.add_argument("-o","--output", help="output folder", type=str, default='output_merger')
    args = parser.parse_args()

    NAMEOUTPUT=args.output
    NAMELIST=args.data_folders

    pathMAIN = os.getcwd()
    pathDESTINATION = os.path.join(pathMAIN, NAMEOUTPUT)
    
    PreSet(NAMELIST)
    SetOUTPUT(NAMELIST)
    Merge()
    
    

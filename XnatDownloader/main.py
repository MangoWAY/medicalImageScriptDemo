import xnat
import os
'''
We need the aseg.mgz, aseg.stats, and MR data
'''

root = 'OASIS3'
mserver = 'https://central.xnat.org'
uname = 'your user name'
psw = 'your password'

def getXnatSession():
    if not os.path.exists(root):
        os.makedirs(root)
    session = xnat.connect(server=mserver,user=uname,password=psw)
    print('Get session')
    return session

def writeBytesFile(path,stream):
    data = stream.open().read()
    with open(path,'wb') as out:
        out.write(data)

def xnatDownload(session):
    mSubjects = session.projects['OASIS3'].subjects
    print('Get OASIS3 project')
    counter = 0
    for sj_key in mSubjects:
        cursj = mSubjects[sj_key]
        print('%d Curretn subject'%counter ,sj_key)
        if not os.path.exists(os.path.join(root,sj_key)):
            os.makedirs(os.path.join(root,sj_key))
        else:
            continue
        for exp_key in cursj.experiments:
            #we just need the MRsession
            try:
                curexp = cursj.experiments[exp_key]
                fsfile = curexp.assessors[0].resources['DATA'].files
                tmp = fsfile['aseg.mgz']
                tmp = fsfile['aseg.stats']
                print('    Curretn experiment', exp_key)
                if not os.path.exists(os.path.join(root,sj_key,exp_key)):
                    os.makedirs(os.path.join(root,sj_key,exp_key))
                print(' '*7,fsfile['aseg.mgz'])
                writeBytesFile(os.path.join(root,sj_key,exp_key,'aseg.mgz'),fsfile['aseg.mgz'])
                print(' '*9,'save!')
                print(' '*7,fsfile['aseg.stats'])
                writeBytesFile(os.path.join(root,sj_key,exp_key,'aseg.stats'),fsfile['aseg.stats'])
                print(' '*9,'save!') 
            except:
                pass
        counter +=1

def main():
    xnatDownload(getXnatSession())

if __name__ == '__main__':
    main()
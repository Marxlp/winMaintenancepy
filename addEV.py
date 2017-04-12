#coding:utf-8
#python2.7
import argparse
import _winreg

winregConst = {0:'REG_NONE',1:'REG_SZ',2:'REG_EXPAND_SZ',3:'REG_BINARY',4:'REG_DWORD',5:'REG_BIG_EDDIAN',
                       6:'REG_LINK',7:'REG_MULTI_SZ',8:'REG_RESOURCE_LIST',9:'REG_FULL_RESOURCE_DESCRIPTOR'}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This python program is to modify the environtment variables of the current user",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='subCom',help="""sub-command help""")
    envList = subparsers.add_parser('list',help='list the environment variables')
    envList.add_argument('name',nargs='?',default=None,help='the name of environment variable that you want to list')
    envList.add_argument('-p','--pretty',action='store_true',help='pretty the print of the environment variable')
    
    envAdd = subparsers.add_parser('add',help='add an environment variable')
    envAdd.add_argument('name',help = 'the name of environment variable that you want to add')
    envAdd.add_argument('data', help = ' the value of the key')

    envDelete = subparsers.add_parser('delete',help='delete an environmental variable')
    envDelete.add_argument('name',help = 'the name of the environment variable that you want to delete')
    
    envAppend = subparsers.add_parser('append',help='append a value to the key')
    envAppend.add_argument('name',help='the name of the environment variable that you want to add')
    envAppend.add_argument('data',help='the data of the given environment variable name')

    parser.add_argument('-l',help='list the environment variable after change')
    
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                          'Environment')
    subkey,number,modifyTime = _winreg.QueryInfoKey(key)
    valueNames = [_winreg.EnumValue(key,index)[0] for index in range(number)]
    
    args = parser.parse_args()
    if args.subCom == 'list':
        try:
            if args.name is None:
                for index,content in enumerate(valueNames):
                    print("%d:\t%s"%(index,content))
            else:
                try:
                    try:
                        valueIndex = int(args.name)
                        valueString = _winreg.EnumValue(key,valueIndex)[1]
                    except ValueError:
                        valueString = _winreg.QueryValueEx(key,args.name)[0]
                    if args.pretty:
                        for index,slip in enumerate(valueString.split(';')):
                            print('%d:\t%s'%(index,slip))
                    else:
                        print("%s"%(valueString))
                except:
                    print("The value name doesn't exist")
        except WindowsError:
            print('Priviledge is not enough to modify the registry\nexit')
            
    elif args.subCom == 'add':
        try:
            if args.name is None:
                print("The value wasn't given")
            else:
                _winreg.SetValueEx(key,args.name,0,_winreg.REG_SZ,args.data)
                _winreg.FlushKey(key)
        except WindowsError:
            print('Priviledge is not enough to modify the registry\nexit')
            
    elif args.subCom == 'delete':
        try:
            if args.name is None:
                print("The value wasn't given")
            else:
                if args.name in valueNames:
                    assure = raw_input("Are you sure to delete the value:%s[y/n]"%(args.name))
                    if assure  in ['y','Y']:
                        _winreg.DeleteValue(key,args.name)
                        _winreg.FlushKey(key)
                else:
                    print("The value name isn't in the environment list")
        except WindowsError:
            print('Priviledge is not enough to modify the registry\nexit')
    elif args.subCom == 'append':
        try:
            if args.name is None:
                assure = raw_input("The data will be appended to the end of the 'PATH' [y/n]")
                if assure  in ['y','Y']:
                    oldPath = _winreg.QueryValueEx(key,'PATH')[0]
                    _winreg.SetValueEx(key,args.name,0,_winreg.REG_EXPAND_SZ,oldPath + ';' + args.data)
                    _winreg.FlushKey(key)
            else:
                if args.name not in valueNames:
                    assure = raw_input("The value %s does not exist.Do you want create it?[y/n]")
                    if assure  in ['y','Y']:
                        _winreg.SetValueEx(key,args.name,0,_winreg.REG_SZ,args.data)
                        _winreg.FlushKey(key)
                oldContent = _winreg.QueryValueEx(key,args.name)[0]
                _winreg.SetValueEx(key,args.name,0,_winreg.REG_SZ,oldContent + ';' + args.data)
                _winreg.FlushKey(key)
        except WindowsError:
            print('Priviledge is not enough to modify the registry\nexit')

    if args.l is not None:
        if args.subCom  in ['delete','append','add']:
            print("Name\t\tType\t\tData")
            for index in range(_winreg.QueryInfoKey(key)[1]):
                name,data,type_data = _winreg.EnumValue(key,index)
                print("%s\t\t%s\t\t%s"%(name,winregConst[type_data],data))
        

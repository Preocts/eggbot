#configio.py
# Created by Preocts
# Version 1.0.1
# Date: 30/11/2019
# v1.0.1 - Preocts - Initial Creation

#Class Def

from os import walk

class eggConfigFile:
    def __init__(self):
        # Dict to hold [GuildName as string : Settings() as list]
        self.configFile = dict()
        self.activeConfig = ''
    
    def hasGuild(self, name):
        #return True if found, False if not
        if name in self.configFile:
            return True
        else:
            return False
    
    def addConfig(self, guild, config):
        #returns True - adds guild if not found, no warn
        if self.hasGuild(guild):
            self.configFile[guild].append(config)
        else:
            self.configFile[guild] = [config]
        return True

    def getConfig(self, guild, name):
        #return String on success, False if config not set/found
        if self.hasGuild(guild):
            for outText in self.configFile[guild]:
                if name in outText:
                    return outText.replace(str(name) + '=', '')
        return False
        
    def editConfig(self, guild, name, config):
        #returns True on success, false on fail
        if self.hasGuild(guild):
            for outText in self.configFile[guild]:
                if name in outText:
                    self.configFile[guild].remove(outText)
                    self.configFile[guild].append(str(name) + '=' + config)
                    return True
        return False
    
    def isAllowedChat(self, guild, name):
        #returns boolean
        if self.hasGuild(guild):
            if name in self.getConfig(guild, 'allowedChatRooms').split(','):
                return True
            else:
                return False

    def saveConfig(self, fileName, saveNote):
        #write to provided filename - returns false on all exceptions
        #Console error outputs are ON by default
        try:
            with open(fileName, 'w') as f:
                f.write(f'#Egg Bot Config file : Last save note - {saveNote}')
                for guildname in self.configFile:
                    #print(f'> {guildname}')
                    f.write(f'\n@{guildname}\n')
                    for config in self.configFile[guildname]:
                        #print(f'>> {config}')
                        f.write(f'\t&{config}\n')
            return True
        except:
            print(f'[WARN] eggConfigFile.saveConfig - Errored attempting to write file: {fileName} with note: {saveNote}')
            return False
    
    def loadConfig(self, fileName):
        #read fileName into class - returns false on all execptions
        #Console outputs are ON by default
        try:
            with open(fileName) as f:
                for line in f:
                    line = line.lstrip(' \t') #Remove leading space/tab               
                    if len(line) == 0: break
                    if line[0] == '@':
                        guildName = line.strip('@\n') #Remove key and trailing CR
                    elif (line[0] == '&') and ('=' in line): 
                        fConfig = line.split('=', 1)
                        fConfig[0] = fConfig[0].strip('& \n')
                        fConfig[1] = fConfig[1].strip(' \n')
                        commandSet = '='.join(fConfig)
                        eggConfig.addConfig(guildName, commandSet)
            self.activeConfig = fileName
            return True
        except:
            print(f'[WARN] eggConfigFile.loadConfig - Errored attempting to read file: {fileName}')
            return False

    def listConfig(self, guild):
        if self.hasGuild(guild):
            return self.configFile[guild]
        return False
        
    def listActiveConfig(self):
        return self.activeConfig
        
    def listConfigFiles(self):
        result = []
        for (dirpath, dirnames, filenames) in walk('./'):
            for file in filenames:
                if '.egg' in file:
                    result.append(file)
            break
        return result
        

eggConfig = eggConfigFile()

print('Testing ConfigIO.py Start')

if eggConfig.loadConfig('base.egg'):
    
    if eggConfig.getConfig('Preocts Place', 'autowelcomDM'):
        print(eggConfig.getConfig('Preocts Place', 'autowelcomeDM'))
    else:
        print('We don\'t have that config')
    
    print('Old value: ' + eggConfig.getConfig('Preocts Place', 'autowelcomeDMImage'))
    if eggConfig.editConfig('Preocts Place', 'autowelcomeDMImage', 'egg.png'):
        print('New value: ' + eggConfig.getConfig('Preocts Place', 'autowelcomeDMImage'))
    else:
        print('That configuation was not found.')

    print('Active config: ' + eggConfig.listActiveConfig())
    
    eggConfig.saveConfig('base02.egg', 'New Version')

try:
    with open('notthere.txt') as f:
        print('we opened it')
except:
    print('Errored')

if eggConfig.listConfig('Preocts Place'):
    for item in eggConfig.listConfig('Preocts Place'):
        print(item)
else:
    print('Guild Config Empty')
    
print(eggConfig.listConfigFiles())

print('Testing ConfigIO.py End')

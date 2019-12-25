import json


#config = {}

#config['shoulderBird'] = {'Guild Name Here' : { 'User Name' : 'regexSearch' } }

#print(config)

#data = json.dumps(config, indent=5)

#print('\n\n')

#print(data)

#exit()

try:
    with open('base.json') as json_file:
        data = json.load(json_file)
        #print(data)
except:
        print(f'[WARN] eggConfigFile.loadConfig - Errored attempting to read file:')
        exit()


#print(json.dumps(data, indent=5))
print('\n\n')

if "shoulderBird" in data:
    dictSB = data["shoulderBird"]
    
if "guildConfig" in data:
    dictGD = data['guildConfig']


print(dictSB)
dictSB['New Guild Name'] = {}
print(dictSB)
newName = 'Preocts'
newReg = '(preocts)'
dictSB['New Guild Name'][newName] = newReg
print(dictSB)



#print('\n\n')
#print(dictGD)
#dictSB = {}
#bigDict = {}
#bigDict['shoulderBird'] = dictSB
#bigDict['guildConfig'] = dictGD

#print('\n\n')
#print(bigDict)
#print('\n\n')
#print(data)

#for segs in data:
        #print(f'\n--\n{segs}')
#print(dictGD['Guild Name Here'])


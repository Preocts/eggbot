# egg_bot 
# Created by Preocts
# Version 0.1.3
# Permissions integer assumed: 502848
# https://discordapp.com/api/oauth2/authorize?client_id=621083281156472845&permissions=502848&scope=bot

import os #Where are we in the OS?
import discord #Mother-load of Discord API stuff
import datetime #Date/Time functions
import re #regular expressions
from dotenv import load_dotenv #Specifically to input secret token

#Get our secret token for OAuth
load_dotenv()

#Class Def
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

#Globals
dClient = discord.Client() #dClient becomes our instance of Discord
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER = os.getenv('BOT_OWNER')
eggConfig = eggConfigFile()
botVersion = '0.1.3 : Tacky Egg'

#Event Definitions - All Coroutines (stop and start anytime)

#ON READY - connection established
@dClient.event
async def on_ready():
    #Added 0.1.1 - Preocts - Output connection details to log
    logOutput('Egg Laid - Connection Established')
    for guild in dClient.guilds:
        logOutput('Connected to ' + str(guild.name) + ' : ' + str(guild.id))
    return

#ON DISCONNECT - connection closed or lost
@dClient.event
async def on_disconnect():
    #Added 0.1.1 - Preocts - Output discconects to log
    logOutput('Egg Dropped - Connection Dropped')
    #print(f'{dClient.user} has disconnected from Discord!')
    return

#ON MESSAGE - Bot Commands
@dClient.event
async def on_message(message):
    #Added 0.0.1 - Preocts - Listens for commands and takes action
    #Added 0.1.1 - Preocts - Core commands listen for OWNER
    #                      - Logging
    #                      - Nay Alert
    #Change 0.1.2 - Preocts - sendChatMessage()
    #Change 0.1.2 - Preocts - Control flow by channel type
    #Removed 0.1.2 - Preocts - Nay Alert (replaced)
    #Added 0.1.2 - Preocts - Shoulder Bird calls
    
    if message.author == dClient.user: #Are we us? Ew, don't listen
        return
    
    #Is this a TextChannel?
    if (str(type(message.channel)) == '<class \'discord.channel.TextChannel\'>'):
        
        #Shoulder Bird runs
        await shoulderBird(message, 'nay(|omii|o|nay|maii|omaise|onaise)', 'SquidToucher', 'Bleats\' Pasture')
        await shoulderBird(message, '(pre(|oct|octs)|oct(|s)|egg)', 'Preocts', 'Preocts Place')
        await shoulderBird(message, '(pre(|oct|octs)|oct(|s)|egg)', 'Preocts', 'Bleats\' Pasture')
        
        #Are we allowed to listen/respond in this room?
        if not(eggConfig.isAllowedChat(message.guild.name, message.channel.name)):
            return False

    #COMMANDS
    #This can get messy - idealy few of these or a way to import them

    if message.content[0] == '!':
        bFoundCommand = False

        #Version command - Owner Only
        if (message.content.startswith('!eggbot') and \
            (str(message.author.id) == str(OWNER))):
            await sendChatMessage(message.channel, 'Beep boop, I am Egg_Bot. version: '\
                + str(botVersion) + ' :egg:', 0)
            #await message.delete()
            bFoundCommand = True
            
        #Break current Connection - Owner Only
        if (message.content.startswith('!disconnect') and \
            (str(message.author.id) == str(OWNER))):
            await sendChatMessage(message.channel, 'Farewell!', 0)
            #await message.delete()
            await dClient.close()
            bFoundCommand = True
            
        #Trigger OnJoin greeting - From Guild only - Owner Only
        if (message.content.startswith('!greetme') and \
            (message.guild) and (str(message.author.id) == str(OWNER))):
            await on_member_join(discord.utils.get(message.guild.members, id=message.author.id))
            await message.delete()
            bFoundCommand = True
            
        #Output command log if we ran a command
        if bFoundCommand:
            logOutput('Ran command: ' + str(message.content) + \
                ' | User: ' + str(message.author) + \
                ' | Guild: ' + str(message.guild) + \
                ' | Channel: ' + str(message.channel) + \
                ' | Type: ' + str(message.type))
        else:
            logOutput('Failed to find command: ' + str(message.content) + \
                ' | User: ' + str(message.author) + \
                ' | Guild: ' + str(message.guild) + \
                ' | Channel: ' + str(message.channel) + \
                ' | Type: ' + str(message.type))
        return True

    #OTHER CHAT CRAP
    return    

#ON JOIN - Welcome the new user
@dClient.event
async def on_member_join(newMember):
    #Added 0.1.1 - Preocts - Sends message to new joins
    #Added 0.1.2 - Preocts - Added [MENTION]
    
    #Log action
    logOutput('on_member_join: ' + str(newMember.display_name) + \
        ' | User: ' + str(newMember.id) + \
        ' | Account Created: ' + str(newMember.created_at) + \
        ' | Guild: ' + str(newMember.guild))
    
    #Exit if not guild is not configured
    if not(eggConfig.hasGuild(str(newMember.guild))):
        logOutput('ALERT, Guild not found: ' + str(newMember.guild))
        return
    
    #Gather the things
    DM = eggConfig.getConfig(str(newMember.guild), 'autowelcomeDM')
    DMI = eggConfig.getConfig(str(newMember.guild), 'autowelcomeDMImage')
    CHAT = eggConfig.getConfig(str(newMember.guild), 'autowelcomeChat')
    CHATI = eggConfig.getConfig(str(newMember.guild), 'autowelcomeChatImage')
    CHANNEL = eggConfig.getConfig(str(newMember.guild), 'autowelcomeChannel')

    #print(f'{DM} | {DMI} | {CHAT} | {CHATI} | {CHANNEL}')
    
    lsHolders = ['[MENTION]', '[USERNAME]', '[GUILDNAME]', '\\n']
    lsMember = [newMember.mention, str(newMember.display_name), str(newMember.guild), '\n']

    if DM: #Send DM Greeting
        for rp in lsHolders:
            DM = DM.replace(rp, lsMember[lsHolders.index(rp)])
        #print(DM)
        await newMember.create_dm()
        if DMI:
            await newMember.dm_channel.send(file=discord.File(str(DMI)))
        await newMember.dm_channel.send(str(DM))
    
    if CHAT and CHANNEL: #Send Channel Greeting to specific room
        chatRoom = discord.utils.get(dClient.get_all_channels(), \
            guild__name=str(newMember.guild), name=CHANNEL)
        if chatRoom:
            for rp in lsHolders:
                CHAT = CHAT.replace(rp, lsMember[lsHolders.index(rp)])
            #print(CHAT)
            if CHATI:
                await chatRoom.send(file=discord.File(str(CHATI)))
            await chatRoom.send(CHAT)
    return

#Send Chat Messages
async def sendChatMessage(dChannel, sMessage, nTime):
    #Added 0.1.2 - Preocts - Handle all Chat Messages
    #Check config permissions
    #[discord.channel.DMChannel/TextChannel/GroupChannel], [string], <delete after # second>
    #Wrote this Thanksgiving day.  I'm thankful for my partner, Traveldog, who made this possible
    
    #Text channels have different rules
    if (str(type(dChannel)) == '<class \'discord.channel.TextChannel\'>'):
        #Check to see that we are allowed
        if eggConfig.isAllowedChat(dChannel.guild.name, dChannel.name):
            if nTime > 0:
                await dChannel.send(sMessage, delete_after=nTime)
            else:
                await dChannel.send(sMessage)
            return True
        else:
            return False
    else: #Private Message - Just do it
        if nTime > 0:
            await dChannel.send(sMessage, delete_after=nTime)
        else:
            await dChannel.send(sMessage)
        return True    
    return False

#Log File Output
def logOutput(outLine):
    #Added 0.1.1 - Preocts - Writes outLine to egg.log, provides timestamp and new line
    with open('egg.log','a') as f:
        f.write(f'{datetime.datetime.now()}  ::  {outLine}\n')

#SHOULDER BIRD
async def shoulderBird(sMessage, sSearch, sTarget, sSource):
    #Added 0.1.2 - Preocts - Start to create flexible bird
    #Searches sMessage for regEx(sSearch) and alerts sTarget if found from sSource

    if (sMessage.guild.name == sSource):
        findRg = re.compile(r'{}\b'.format(sSearch), re.I)
        found = findRg.search(sMessage.content)
        if found:
            BIRD = discord.utils.get(sMessage.guild.members, name=sTarget)
            #Only a few know why this is called BIRD. <3 
            if not(BIRD):
                return False
            await BIRD.create_dm()
            await BIRD.dm_channel.send('Mention alert: **' + \
                str(sMessage.author.display_name) + \
                '** mentioned you in **' + str(sMessage.channel) + \
                '** saying: \n`' + sMessage.content + '`')
            return True
        return False
    return False

# ###################################################### #
#Run the instance of a Client (.run bundles the needed start, connect, and loop)

print ('Attempting to load base config')

if not(eggConfig.loadConfig('base.egg')):
    print('Failed loading base.egg. Hatch aborted')

print ('Configuration loaded')
print ('Connecting to the Client now\n')
dClient.run(TOKEN)

#May Bartmoss have mercy on your data for running this bot.
#We are all only eggs
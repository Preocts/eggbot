# egg_bot 
# Created by Preocts
# preocts@preocts.com | Preocts#8196 Discord
# Permissions integer assumed: 502848

#Addition imports
import os #Where are we in the OS?
from sys import argv # 
import discord #Mother-load of Discord API stuff
import datetime #Date/Time functions
import re #regular expressions
from dotenv import load_dotenv #Specifically to input secret token
import json #JSON!

#Get our secret token for OAuth
load_dotenv()

#Class Def
class eggConfigFile:
    def __init__(self):
        # Dict to hold [GuildName as string : Settings() as list]
        # 0.2.1 Updated
        self.guildConfig = {}
        self.shoulderBird = {}
        self.activeConfig = ''
    
    def hasGuild(self, name):
        #return True if found, False if not
        #0.2.1 Updated
        if name in self.guildConfig:
            return True
        else:
            return False

    def addConfig(self, guild, name, config):
        #adds config, creates guild if doesn't exist
        #returns false if config already exists
        #0.2.1 Updated
        if self.hasGuild(guild):
            if name in self.guildConfig[guild]:
                return False
        else:
            self.guildConfig[guild] = {}
        self.guildConfig[guild][name] = config
        return True

    def editConfig(self, guild, name, config):
        #edits existing config, true on success
        #false on missing guild or config name
        #0.2.1 Updated
        if self.hasGuild(guild):
            if name in self.guildConfig[guild]:
                self.guildConfig[guild][name] = config
                return True
        return False

    def getConfig(self, guild, name):
        #return String on success, False if config/guild not set/found
        if self.hasGuild(guild):
            if name in self.guildConfig[guild]:
                return self.guildConfig[guild][name]
        return False
    
    def isAllowedChat(self, guild, channel):
        #returns True if we can chat in channel
        if self.hasGuild(guild):
            if 'allowedChatRooms' in self.guildConfig[guild]:
                if channel in self.guildConfig[guild]['allowedChatRooms'].split(','):
                    return True
        return False

    def saveConfig(self, fileName):
        #write to provided filename - returns false on all exceptions
        #Console error outputs are ON by default
        #0.2.1 Updated
        json_dict = {}
        json_dict['guildConfig'] = self.guildConfig
        json_dict['shoulderBird'] = self.shoulderBird
        try:
            with open(fileName, 'w') as f:
                f.write(json.dumps(json_dict, indent=5))
            return True
        except:
            print(f'[WARN] eggConfigFile.saveConfig - Errored attempting to write file: {fileName} with note: {saveNote}')
            return False
    
    def loadConfig(self, fileName):
        #read fileName into class - returns false on all execptions
        #Console outputs are ON by default
        #0.2.1 Updated
        try:
            with open(fileName) as f:
                json_dict = json.load(f)
                if 'shoulderBird' in json_dict:
                    self.shoulderBird = json_dict['shoulderBird']
                    if DEBUG: 
                        print(f'shoulderBird Config Load:\n{self.shoulderBird}\n')
                if 'guildConfig' in json_dict:
                    self.guildConfig = json_dict['guildConfig']
                    if DEBUG: 
                        print(f'guildConfig Congif Load:\n{self.guildConfig}\n')
                self.activeConfig = fileName
                return True
        except:
            print(f'[WARN] eggConfigFile.loadConfig - Errored attempting to read file: {fileName}')
            return False

    def listConfig(self, guild):
        #returns dict of config for given server, False if none
        #0.2.1 Updated
        if self.hasGuild(guild):
            return self.guildConfig[guild]
        return False
        
    def listActiveConfig(self):
        #returns class global of loaded config filename
        #0.2.1 Updated
        return self.activeConfig
        
    def listConfigFiles(self):
        #returns list of .egg files in working directory
        #0.2.1 Updated
        result = []
        for (dirpath, dirnames, filenames) in os.walk('./'):
            for file in filenames:
                if '.egg' in file:
                    result.append(file)
            break
        return result                

#Globals
dClient = discord.Client() #dClient becomes our instance of Discord
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER = os.getenv('BOT_OWNER')
DEBUG = False #console spam control
eggConfig = eggConfigFile()
botVersion = '0.2.1 : Gooey Egg'

#Event Definitions - All Coroutines (stop and start anytime)

#ON READY - connection established
@dClient.event
async def on_ready():
    #Added 0.1.1 - Preocts - Output connection details to log
    logOutput('egg.log', 'Egg hatched! Connection Established!')
    print('Egg successfully hatched.\nConnection to Discord Established.')
    print('Available Guilds:')
    for guild in dClient.guilds:
        print(f'\t{guild}')
        logOutput('egg.log', 'Connected to ' + str(guild.name) + ' : ' + str(guild.id))
    print('All futher communication in log file.')
    return

#ON DISCONNECT - connection closed or lost
@dClient.event
async def on_disconnect():
    #Added 0.1.1 - Preocts - Output discconects to log
    logOutput('egg.log', 'Egg Dropped - Connection Dropped')
    print(f'{dClient.user} has disconnected from Discord!')
    return

#ON MESSAGE - Bot Commands
@dClient.event
async def on_message(message):
    
    if message.author == dClient.user: #Are we us? Ew, don't listen
        return
 
    #Is this a DM?
    #<class 'discord.channel.DMChannel/TextChannel/GroupChannel'>
    if str(type(message.channel)) == '<class \'discord.channel.DMChannel\'>':
        await handler_DMChannel(message)
        return True
 
    #Is this a TextChannel?
    if str(type(message.channel)) == '<class \'discord.channel.TextChannel\'>':

        #Set Alert if not configured
        if not(eggConfig.hasGuild(message.guild.name)):
            logOutput('egg.log', 'ALERT, Guild not found but bot is active : ' + message.guild.name)
            eggConfig.addConfig(message.guild.name, 'allowedChatRooms', '')
        
        #Shoulder Bird runs
        await shoulderBird(message, 'nay(|omii|o|nay|maii|omaise|onaise|may)', 'SquidToucher', 'Bleats\' Pasture')
        await shoulderBird(message, '(pre(|oct|octs)|oct(|s)|egg)', 'Preocts', 'Preocts Place')
        await shoulderBird(message, '(pre(|oct|octs)|oct(|s)|egg)', 'Preocts', 'Bleats\' Pasture')

    #COMMANDS - TO BE DELETED
    #This can get messy - idealy few of these or a way to import them

    #Are we allowed to listen/respond in this room?
    if not(eggConfig.isAllowedChat(message.guild.name, message.channel.name)):
        return False

    if (len(message.content) > 0) and (message.content[0] == '!'):
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
            logOutput('egg.log', 'Ran command: ' + str(message.content) + \
                ' | User: ' + str(message.author) + \
                ' | Guild: ' + message.guild.name + \
                ' | Channel: ' + str(message.channel) + \
                ' | Type: ' + str(message.type))
        else:
            logOutput('egg.log', 'Failed to find command: ' + str(message.content) + \
                ' | User: ' + str(message.author) + \
                ' | Guild: ' + message.guild.name + \
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
    logOutput('egg.log', 'on_member_join: ' + str(newMember.display_name) + \
        ' | User: ' + str(newMember.id) + \
        ' | Account Created: ' + str(newMember.created_at) + \
        ' | Guild: ' + str(newMember.guild))
    
    #Exit if not guild is not configured
        #Set Alert if not configured

    if not(eggConfig.hasGuild(str(newMember.guild))):
        logOutput('egg.log', 'ALERT, Guild not found but bot is active : ' + str(newMember.guild))
        eggConfig.addConfig(newMember.guild.name, 'allowedChatRooms', '')
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
    #[discord.channel.TextChannel], [string], <delete after # second>
    #Wrote this Thanksgiving day.  I'm thankful for my partner, Traveldog, who made this possible
    
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
    return False

#Send DM Messages
async def sendDMMessage(dUser, sMessage):
    #Added 0.2.1 - Preocts - Handle all DM Messages
    #Check optout List
    #[discord.channel.DMChannel], [string]

    #ADD Check to see that we are allowed
    if not(dUser.dm_channel):
        await dUser.create_dm
    await dUser.dm_channel.send(str(sMessage))
    return True

#Log File Output
def logOutput(fileName, outLine):
    #Added 0.1.1 - Preocts - Writes outLine to egg.log, provides timestamp and new line
    #Updated 0.2.1 - Preocts - fileName added
    with open(fileName,'a') as f:
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

#Handler for DM Messages
async def handler_DMChannel(message):
    #Added 0.2.1 - Preocts - Handles DM commands/chat
    
    if len(message.content) <= 0: #Empty content
        return False
    
    #Handle plain text messages
    if message.content[0] != '!':
        await sendDMMessage(message.author, 'Hello, I\'m just a bot so if you\'re looking for some social interaction you will need to DM someone else.' + \
            '\n\nYou can type !help for a list of commands available to you.' + \
            '\nYou can type !stop and I will only DM you again if you DM me first')
        return True
    
    #Hardcoded Commands
    contentList = message.content.split(' ')
    if contentList[0] == '!disconnect' and \
        str(message.author.id) == str(OWNER):
        await dClient.close()
        return
    if contentList[0] == '!help':
        await sendDMMessage(message.author, 'Preocts hasn\'t created this part of the program yet. "Soon"')
        return
    if contentList[0] == '!stop':
        await sendDMMessage(message.author, 'Preocts hasn\'t created this part of the program yet. "Soon"' + \
        '\nIf for some reason the bot is annoying you or you passionately don\'t ever want to see this ' + \
        'name in your DM list again, contact Preocts#8196 with that request')
        return
    if contentList[0] == '!optin':
        await sendDMMessage(message.author, 'Preocts hasn\'t created this part of the program yet. "Soon"')
        return
    await sendDMMessage(message.author, 'That command was not found.')
    return

# ###################################################### #
#Run the instance of a Client (.run bundles the needed start, connect, and loop)

if len(argv) >= 2: #were we given a file to load?
    inputFile = argv[1]
else: #no params given
    inputFile = 'base.egg'

print (f'Hatch cycle started.\nShell version: {botVersion}')
print (f'Attempting to load configuration from: {inputFile}')
if eggConfig.loadConfig(inputFile):
    print(f'Successfull loaded: {inputFile} \n Continuing hatch cycle...')
else:
    print('Invalid or missing file. Hatch aborted!')
    exit()

#exit()

print('Hatching onto Discord now.')
dClient.run(TOKEN)

#May Bartmoss have mercy on your data for running this bot.
#We are all only eggs
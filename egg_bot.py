"""
Egg Bot, Discord Utility Bot

Created by Preocts
preocts@preocts.com | Preocts#8196 Discord
Permissions integer assumed: 502848

https://github.com/Preocts/Egg_Bot

"""

#Additional imports
import os #Where are we in the OS?
from sys import argv #command line import
import discord #Mother-load of Discord API stuff
import datetime #Date/Time functions
import re #regular expressions
from dotenv import load_dotenv #Specifically to input secret token
import json #JSON!

#Class Def
class eggConfigFile:
    def __init__(self):
        # Dict to hold [GuildName as string : Settings() as list]
        # 0.2.1 Updated
        self.guildConfig = {}
        self.shoulderBird = {}
        self.botCommands = {}
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

    #   ShoulderBird
    def getBirds(self, guildname):
        """
        Guild specifc
        Returns a dict of user configs for ShoulderBird by guildname
        Returns false if not found
        """
        #Do we have this guild setup and is there anything there?
        if (guildname in self.shoulderBird) and len(self.shoulderBird[guildname]):
            return self.shoulderBird[guildname]

        return False

    def getBird(self, guildname, username):
        """
        User specific
        Returns a dict of user config for ShoulderBird by guildname
        Returns false if not found
        """
        #Do we have this guild setup and is there anything there?
        if (guildname in self.shoulderBird) and len(self.shoulderBird[guildname]):
            if username in self.shoulderBird[guildname]:
                return self.shoulderBird[guildname][username]

        return False

    def putBird(self, guildname, username, regex):
        """
        Creates or replaces a user's settings for a given guild
        Will create the guild listing if unset
        """
        #Literally just assign is. No gaurdrails at this time
        self.shoulderBird[guildname] = {username : regex}

        return True

    def delBird(self, guildname, username):
        """
        Deletes an entry.
        Returns false if not found
        """
        if guildname in self.shoulderBird:
            if username in self.shoulderBird[guildname]:
                del self.shoulderBird[guildname][username]
                return True
        return False

    #   botCommands
    def listCommand(self, cmdGuild):
        #Returns list of command names for Guild
        if len(cmdGuild) <= 0: return False

        if cmdGuild in self.botCommands:
            cmdList = []
            for c in self.botCommands[cmdGuild]:
                cmdList.append(c)
            return str(cmdList)
        return False

    def getCommand(self, cmdGuild, cmdName):
        #Returns dict of command if found
        if len(cmdName) <= 0:
            return False

        if cmdGuild in self.botCommands:
            if cmdName.lower() in self.botCommands[cmdGuild]:
                return self.botCommands[cmdGuild][cmdName.lower()]
        return False

    def putCommand(self, cmdGuild, cmdInput):
        #Sets a command, returns false if exists (use editCommand)
        #testing/parse.py has a VERY detailed view of what we're doing here
        if len(cmdGuild) <= 0 or len(cmdInput) <= 0:
            return False

        inputPieces = cmdInput.split(' | ')
        #Pop and split in one line
        cmdLine = inputPieces.pop(0).split(' ')

        #Validation check: Do we have any commands for this guild?
        #If not, make the guild in the config
        if not(cmdGuild in self.botCommands):
            #Create an empty dictionary for this mock guild
            self.botCommands[cmdGuild] = {}

        #Create the command dict if it doesn't exist
        if not(cmdLine[1] in self.botCommands[cmdGuild]):
            self.botCommands[cmdGuild][cmdLine[1].lower()] = {}

        #Do we have any options? If we don't, nothing more to do.
        #The command is created even though it would be empty
        if len(inputPieces) > 0:
            for piece in inputPieces:
                #split our small piece into two pieces at the = sign - only once,
                piece = piece.split(' = ', 1)

                #We check for a lenght of 2. If our split has less than or more
                #than two pieces we assume the input was bad and ignore the piece.
                if len(piece) == 2:
                    self.botCommands[cmdGuild][cmdLine[1].lower()][piece[0].lower()] = piece[1]
        return True

    def delCommand(self, cmdGuild, cmdName):
        #Deletes a command, returns True on success, False on fail
        if len(cmdName) <= 0:
            return False

        if cmdGuild in self.botCommands:
            if cmdName.lower() in self.botCommands[cmdGuild]:
                del self.botCommands[cmdGuild][cmdName.lower()]
                return True
        return False

    #   SAVE / LOAD CONFIG FILE
    def saveConfig(self, fileName):
        #write to provided filename - returns false on all exceptions
        #Console error outputs are ON by default
        #0.2.1 Updated
        json_dict = {}
        json_dict['guildConfig'] = self.guildConfig
        json_dict['shoulderBird'] = self.shoulderBird
        json_dict['botCommands'] = self.botCommands
        try:
            with open(fileName, 'w') as f:
                f.write(json.dumps(json_dict, indent=4))
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
                    if DEBUG: print(f'shoulderBird Config Load:\n{self.shoulderBird}\n')
                if 'guildConfig' in json_dict:
                    self.guildConfig = json_dict['guildConfig']
                    if DEBUG: print(f'guildConfig Congif Load:\n{self.guildConfig}\n')
                if 'botCommands' in json_dict:
                    self.botCommands = json_dict['botCommands']
                    if DEBUG: print(f'guildConfig Congif Load:\n{self.guildConfig}\n')
                self.activeConfig = fileName
                return True
        except:
            print(f'[WARN] eggConfigFile.loadConfig - Errored attempting to read file: {fileName}')
            return False

#Get our secret token for OAuth
load_dotenv()

#Globals
dClient = discord.Client() #dClient becomes our instance of Discord
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER = os.getenv('BOT_OWNER')
DEBUG = False #console spam control
eggConfig = eggConfigFile()
botVersion = '0.2.2 : Gooey Egg'

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

    if len(message.content) <= 0: #Catch for empty content
        return False

    #Are we us? Ew, don't listen
    if message.author == dClient.user:
        return False

    #DM channel command search
    if str(type(message.channel)) == '<class \'discord.channel.DMChannel\'>':
        cmdDict = eggConfig.getCommand('', message.content.split()[0].strip(' '))

    #Chat channel command search
    elif str(type(message.channel)) == '<class \'discord.channel.TextChannel\'>':
        if not(eggConfig.hasGuild(message.guild.name)):
            logOutput('egg.log', 'ALERT, Guild not found but bot is active : ' + message.guild.name)
            #Set Guild into loaded config to stop multiple alerts
            eggConfig.addConfig(message.guild.name, 'allowedChatRooms', '')

        cmdDict = eggConfig.getCommand(message.guild.name, message.content.split()[0].strip(' '))

        #Does ShoulderBird have a listing for this guild?
        nest = eggConfig.getBirds(message.guild.name)
        if nest:
            #Send this to the bird!
            for bird in nest:
                await shoulderBird(message, nest[bird], bird)

    #exit on GroupChannels or anything unexpected
    else:
        return False

    #If we found a command, handle it
    #Check permissions to confirm this command can be run
    if cmdDict and commandPermsCheck(message, cmdDict):

        #content = output to discord client - do this first
        if ('content' in cmdDict) and (len(cmdDict['content']) > 0):
            if str(type(message.channel)) == '<class \'discord.channel.DMChannel\'>':
                await sendDMMessage(message.author, cmdDict['content'])
            else:
                await sendChatMessage(message.channel, cmdDict['content'], 0)

        #Action = pre-defined actions to take in code - do this last
        if ('action' in cmdDict) and (len(cmdDict['action']) > 0):

            #Set cmdGuild to avoid object has no attribute for 'name' in DM channels
            if str(type(message.channel)) == '<class \'discord.channel.DMChannel\'>':
                cmdGuild = ''
            else:
                cmdGuild = message.guild.name

            #Disconnect the bot - Cannot be run by anyone but OWNER
            if cmdDict['action'] == 'disconnect':
                if str(message.author.id) == str(OWNER):
                    await dClient.close()

            #Create a new command
            if cmdDict['action'] == 'edit-command':
                if eggConfig.putCommand(cmdGuild, message.content):
                    if DEBUG: print('Command created')
                    eggConfig.saveConfig(eggConfig.activeConfig)
                else:
                    if DEBUG: print('Command not created')

            #Delete a command
            if cmdDict['action'] == 'delete-command':
                if eggConfig.delCommand(cmdGuild, message.content.split()[1]):
                    if DEBUG: print('Command deleted')
                    eggConfig.saveConfig(eggConfig.activeConfig)
                else:
                    if DEBUG: print('Command not deleted')

            #Spit out a command into chat (full config)
            if cmdDict['action'] == 'get-command':
                if eggConfig.getCommand(cmdGuild, message.content.split()[1]):
                    if DEBUG: print('Showing command')
                    outMessage = message.content.split()[1]
                    for o in eggConfig.getCommand(cmdGuild, message.content.split()[1]):
                        outMessage += ' | ' + o + ' = ' + eggConfig.getCommand(cmdGuild, message.content.split()[1])[o]

                    if str(type(message.channel)) == '<class \'discord.channel.DMChannel\'>':
                        await sendDMMessage(message.author, outMessage)
                    else:
                        await sendChatMessage(message.channel, outMessage, 0)
                else:
                    if DEBUG: print('Command not found')

            #Spit out all commands for guild
            if cmdDict['action'] == 'list-command':
                if eggConfig.listCommand(cmdGuild):
                    if DEBUG: print('Showing all commands')
                    if str(type(message.channel)) == '<class \'discord.channel.DMChannel\'>':
                        await sendDMMessage(message.author, eggConfig.listCommand(cmdGuild))
                    else:
                        await sendChatMessage(message.channel, eggConfig.listCommand(cmdGuild), 0)
                else:
                    if DEBUG: print('Command not found')
        return True

    """
    #DM only condition - prompt user they are speaking to a bot
    elif str(type(message.channel)) == '<class \'discord.channel.DMChannel\'>':
        await sendDMMessage(message.author, 'Hello, I\'m just a bot so if you\'re' + \
            'looking for some social interaction you will need to DM someone else.' + \
            '\n\nYou can type **help** for a list of commands available to you.' + \
            '\nYou can type !stop and I will only DM you again if you DM me first')
    """
    return False

#ON JOIN - Welcome the new user
@dClient.event
async def on_member_join(newMember):
    """ on_member_join {disord.member}
    0.2.3 - Precots - update to properly use DM/Chat calls
    """

    #Log action
    logOutput('egg.log', 'on_member_join: ' + str(newMember.display_name) + \
        ' | User: ' + str(newMember.id) + \
        ' | Account Created: ' + str(newMember.created_at) + \
        ' | Guild: ' + str(newMember.guild))

    #Exit if not guild is not configured
    if not(eggConfig.hasGuild(str(newMember.guild))):
        logOutput('egg.log', 'ALERT, Guild not found but bot is active : ' + str(newMember.guild))
        eggConfig.addConfig(newMember.guild.name, 'allowedChatRooms', '')
        return False

    #Gather the configuations
    DM = eggConfig.getConfig(str(newMember.guild), 'autowelcomeDM')
    CHAT = eggConfig.getConfig(str(newMember.guild), 'autowelcomeChat')
    CHANNEL = eggConfig.getConfig(str(newMember.guild), 'autowelcomeChannel')

    lsHolders = ['[MENTION]', '[USERNAME]', '[GUILDNAME]', '\\n']
    lsMember = [newMember.mention, str(newMember.display_name), str(newMember.guild), '\n']

    if DM: #Send DM Greeting
        for rp in lsHolders:
            DM = DM.replace(rp, lsMember[lsHolders.index(rp)])
        sendDMMessage(newMember.name, DM)

    if CHAT and CHANNEL: #Send Channel Greeting to specific room
        chatRoom = discord.utils.get(dClient.get_all_channels(), \
            guild__name=str(newMember.guild), name=CHANNEL)
        if chatRoom:
            for rp in lsHolders:
                CHAT = CHAT.replace(rp, lsMember[lsHolders.index(rp)])
            sendChatMessage(chatRoom, CHAT, 0)
    return True

#Send Chat Messages
async def sendChatMessage(dChannel, sMessage, nTime):
    #Added 0.1.2 - Preocts - Handle all Chat Messages
    #Check config permissions
    #[discord.channel.TextChannel], [string], <delete after # second>
    #Wrote this Thanksgiving day.  I'm thankful for my partner, Traveldog, who made this possible

    #Check to see that we are allowed
    if nTime > 0:
        await dChannel.send(sMessage, delete_after=nTime)
        return True
    else:
        await dChannel.send(sMessage)
        return True

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
async def shoulderBird(sMessage, sSearch, sTarget):
    #Added 0.1.2 - Preocts - Start to create flexible bird
    #Searches sMessage for regEx(sSearch) and alerts sTarget if found

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


def commandPermsCheck(message, cmdDict):
    #Checks exclusive for Chat: Channels and Roles
    if str(type(message.channel)) == '<class \'discord.channel.TextChannel\'>':

        #If the channel is not in 'channels' then fail. Blank/unset 'channels' means any are allowed
        if ('channels' in cmdDict) \
            and (not(message.channel.name in cmdDict['channels']) \
            and (len(cmdDict['channels']) > 0)):

            if DEBUG: print('Failed Channel')
            return False

        #If the user role is not in 'roles' then fail. Blank/unset 'roles' means any are allowed
        #Roles live in a discord.py formated list so we need to step through it
        if ('roles' in cmdDict):
            roleList = []
            for roles in message.author.roles:
                roleList.append(roles.name)

            #Use a set to compare since a user can have many roles and many roles can be defined in the config
            #set math. Set1 - Set2 = Set3. If Set1 = Set3 we didn't remove anything so no matching roles found
            #set() arranges the list differently! Compare set to set, don't convert back to list
            if (set(roleList) - set(cmdDict['roles'].split(', ')) == set(roleList)) \
            and (len(cmdDict['roles']) > 0):

                if DEBUG: print('Failed Roles')
                return False

    #If the user is not listed in 'users' (case-sensitive) then fail. Blank/unset 'users' means any are allowed
    if ('users' in cmdDict) \
        and (not(message.author.name in cmdDict['users'].split(', ')) \
        and (len(cmdDict['users']) > 0)):

        if DEBUG: print(f'User can not run this: {message.author.name}')
        return False
    return True

# ###################################################### #
#Run the instance of a Client (.run bundles the needed start, connect, and loop)

if __name__ == '__main__':

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

    print('Hatching onto Discord now.')
    dClient.run(TOKEN)

#May Bartmoss have mercy on your data for running this bot.
#We are all only eggs

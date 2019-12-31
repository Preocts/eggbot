import json

#SETUP - This emulates info we'd normally gather from chat and discord.py classes

#Mock command dictionary, normally in eggConfigFile class
botCommands = {} 
#botCommands = {'Preocts Place': {'testcommand': {}}} #what happens if we have that command?

#Pretend a command came from this guild
mockGuild = 'Preocts Place'

#Pretend someone typed this into chat. Normally from message.content
mockInput = 'a!command testcommand | role = owner, mods | breaks | channel=general,hot-spot | content=This is what my = command is'
#mockInput = 'a!command emtpycommand will not break but will not do anything'

print(f'\nWe start with this\n{mockInput}\n')

"""
    How are we manipulating the input string?
    We split the string into a list with the " | " being the delimiter. The spaces here are vital
    as they allow a | to be used in the command so long as it borders a character that isn't a space.
    
    If there are no " | " options, the action is still successful as we have a [0] index on the list
    
    "!testcommand This is a test"
    becomes
    ["!testcommand This is a test"]
    
    "!testcommand This is a test | role = mod | channel = general"
    becomes
    ["!testcommand This is a test", "role = mod", "channel = general"]
"""

inputPieces = mockInput.split(' | ')
print(f'inputPieces:\n{inputPieces}\n')

"""
    Now we the [0] index and split it into a cmdLine holder. This is our trigger and options, space delimited
    This removes it from pieces which, if they exist, will be used later.
    
    If inputPieces has a 0 length we know no further information was given (useful later)
"""
#Pop and split in one line
cmdLine = inputPieces.pop(0).split(' ')

print(f'cmdLine:\n{cmdLine}\n')
print(f'inputPieces:\n{inputPieces}\n')

"""
    At this point we run a search for a matching command. For the test we assume we find the
    matching commmand and move on to running the correct process.
    
    This example is creating a new command and storing it into the eggConfigFile in JSON format
    
    Comments will walk through our actions.
    
    We know cmdLine[0] is our trigger or command.
    
    When looking at the conditions searching for X in botCommands, this is the nested structure:
    botCommands{} -> Guild name{} -> Command Name{} -> Command configs{}
"""

#A look at what we start with
print(f'\nbotCommand start: {botCommands}\n')

#This condition would be the search for existing command in eggConfigFile"
if cmdLine[0] == 'a!command':
    
    #Validation check: Do we have any commands for this guild? If not, make the guild in the config
    if not(mockGuild in botCommands):
        print('Guild doesn\'t exist! Creating guild entry in botCommands')
        #Create an empty dictionary for this mock guild
        botCommands[mockGuild] = {}
        print(f'\nbotCommand update: {botCommands}\n')
    
    #For add command we know cmdLine[1] will be the name of the command being added
    #Validation check: Make sure we don't already have this command. Prevents accidently writing over it
    if cmdLine[1] in botCommands[mockGuild]:
        print('Command exists, use e!command or d!command instead')
        exit()
    
    #Add the nested dict now that we know 100% the partent dict exists
    botCommands[mockGuild][cmdLine[1]] = {}
    print(f'\nbotCommand update: {botCommands}\n')
    #Do we have any options? If we don't, nothing more to do. The command is created even though it would be empty
    if len(inputPieces) > 0:
        
        #inputPieces is a list. We're going to step through it one at a time.
        for piece in inputPieces:
            
            #split our small piece into two pieces at the = sign - only once, at the first "="
            piece = piece.split('=', 1)
            
            #We check for a lenght of 2. If our split has less than or more than two pieces we assume
            #the input was bad and ignore the piece.
            if len(piece) == 2:
                #piece is now a list that looks like this: ['index', 'value']
                #Add this piece into the nested dictionary. This is going into the fourth nesting
                print (f'Adding config: {piece}')
                botCommands[mockGuild][cmdLine[1]][piece[0]] = piece[1]
    
    print(f'\nbotCommand final: {botCommands}\n')
    print('Readable JSON format\n')
    print(json.dumps(botCommands, indent=5))

exit()
"""
So we take the full chat input:
 a!command testcommand | role = owner, mods | breaks | channel=general,hot-spot | content=This is what my command is

Break it into two lists
 ["a!command", "testcommand"]
 ["role = owner, mods", "breaks", "channel=general,hot-spot", "content=This is what my command is"]
 
Search for a command matching index[0] of the first list

Use the index[1] of the first list to create a new command entry in the config

Step through the second list and break each segment into another list
 ["role", "owner, mods"]
 ["breaks"]
 ["channel", "general,hot-spot"]
 ["content", "This is what my command is"]
 
For each of these that has exactly two segments, we turn them into a nested dict ending with the following view from botCommands:
Notice that ["breaks"] is dropped.  It is considered invalid input.
{
     "Preocts Place": {
          "testcommand": {
               "role ": " owner, mods",
               "channel": "general,hot-spot",
               "content": "This is what my command is"
          }
     }
}
"""

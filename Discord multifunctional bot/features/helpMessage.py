from settings import *

helpMessage = '''
# *** VOICE COMMANDS ***  #

{0}join
Will join the voice channel that you're in.

{0}leave
Will leave the voice channel that the you're in.

{0}play [song or video to search for on YouTube]
Will begin playing the audio of the video/song provided.

{0}pause
Will pause the current audio stream.

{0}resume
Will resume the current audio stream.

{0}stop
Will stop and end the audio stream and delete the audio file.

# *** TRANSLATE COMMANDS ***  #

{0}translate [text]
Will return you a translated text (base: from russian to english)

{0}set_lang [language from] [language to]
Will change the language for {0}translate command.

{0}list_lang
Will return the list of supported languages for {0}translate command.

# *** STATUS COMMANDS ***  #
(Admin roots required)

{0}set_status [status]
Will set the game playing status of the bot.

{0}reset_status 
Will reset the game playing status of the bot to ONLINE.

# *** FUN COMMANDS ***  #

{0}joke
Posts a random Chuck Norris joke.

{0}coinflip
Will flip a coin and post the result.

{0}roll [# of dice] D[# of sides] Example: !roll 3 D6
Will roll the dice specified and post the result.

{0}slots
Will post a slot machine result.

{0}cat
Will post a random cat picture or gif.

{0}catgif
Will post a random cat gif.

# *** ELSE ***  #

{0}python_help [library name you are having problems with]
Will send you a personal message with link for fixing your problem.

{0}count []
Will send you counted number of your example

{0}invite_link
Will send a personal message with the invite link of the bot.

{0}code
Will send you a github url with all bot code.

{0}shutdown
Will make the bot logout and shutdown. Will only work for owner of the bot.

'''.format(config.COMMANDPREFIX)

from chatterbotapi import ChatterBotFactory, ChatterBotType 
from listener import *
from os import system
from subprocess import check_output

factory = ChatterBotFactory()

bot = factory.create(ChatterBotType.CLEVERBOT)
botSession = bot.create_session()

listen = Listener()
broken = False  #<-- False if working True if unable to reach google asr api; Also used for type choice
voice = '' 
choice = 2

# let user chose if he or she would like to speak or type
while choice != 'speak' and choice != 'type':
	choice = raw_input('Would you like to speak or type: ').lower()
	if choice != 'speak' and choice != 'type': print 'You must enter speak or type.'

# create list of available voices 
names = []
out = check_output('say -v ?', shell=True)
outArray = out.split('\n')
for i in outArray:
	x = i.find(' ')
	names.append(i[:x])
names.pop()  #<------------------ Remove empty string at end of list

# print available voices in two columns 
print "Available voices:"
cnt = 0;
while cnt < len(names)-1:
	print '    {:15} {}'.format(names[cnt], names[cnt+1])
	cnt+=2

while not any(voice == val.lower() for val in names) and not voice in names: #<--- makes case-insensitive (sorta) from stackoverflow -> goo.gl/VwNGTx
	voice = raw_input("Pick a voice or press enter for default: ")
	if voice == '':
		voice = False
		break

if choice == 'speak': 
	print 'Start talking' 
else: 
	print 'Start typing'

print 'Press Control-C to quit'

while (True):
	# catch KeyboardInterrupt a.k.a Cntr-C and quit nicely
	try:
		# store what user says as say or default to typing
		try:
			if choice == 'speak':
				say = listen.get_utterance()
			else:
				say = raw_input('You: ')
				broken = True
		except (urllib2.HTTPError, urllib2.URLError):
			say = raw_input("Speech recognigtion not working. Type instead: ")
			broken = True

		# Create computer response or warn user of error and exit 
		if say != [] and say != None:
			say = say['result'][0]['alternative'][0]['transcript'] if not broken else say
			if not broken: print 'You:', say
			try:
				rsp = botSession.think(say)
				print 'Bot:', rsp
				if voice != False:
					system('say -v %s "%s"' % (voice, rsp))
				else:
					system('say "%s"' % rsp)
			except urllib2.URLError:
				print 'Could not connect to server. Please check your internet connection and try again.'
				break
		else:
			print "Sorry. I did not get that. Could you please repeat yourself?"
			if voice != False:
				system("say -v {} Sorry. I did not get that. Could you please repeat yourself?".format(voice))
			else:
				system("say Sorry. I did not get that. Could you please repeat yourself?")
	
	except KeyboardInterrupt:
		print '\nquitting'     # Probobly don't need the lowercase one but idk what computer are like
		if 'Cellos' in names or 'cellos' in names:
			system('say -v cellos good good good good good good bye good good bye good good bye good good good good good good good good good good good good bye')
		else: 
			system('say goodbye')
		break;
import random

from settings import *


# Returns random result to a coin flip
def get_coin_face():
	coin_faces = ['Heads', 'Tails']

	return random.choice(coin_faces)


# Returns a random slot machine screen, uses discord emoji in the display
def get_slots_screen():
	slots = ['chocolate_bar', 'bell', 'tangerine', 'apple', 'cherries', 'seven']
	slot1 = slots[random.randint(0, 5)]
	slot2 = slots[random.randint(0, 5)]
	slot3 = slots[random.randint(0, 5)]
	slot4 = slots[random.randint(0, 5)]

	slot_output = '|\t:{}:\t|\t:{}:\t|\t:{}:\t|\t:{}:\t|\n'.format(slot1, slot2, slot3, slot4)

	if slot1 == slot2 and slot2 == slot3 and slot3 == slot4 and slot4 != 'seven':
		return slot_output + '$$ GREAT $$'

	elif slot1 == 'seven' and slot2 == 'seven' and slot3 == 'seven' and slot4 == 'seven':
		return slot_output + '$$ JACKPOT $$'

	elif slot1 == slot2 and slot3 == slot4 or slot1 == slot3 and slot2 == slot4 or slot1 == slot4 and slot2 == slot3:
		return slot_output + '$ NICE $'

	else:
		return slot_output


# Rolls dice using both the number of dice and number of sides per dice given
def roll_dice(message_text):
	message = message_text.split()
	dice_rolls = []
	if len(message) == 3:
		if message[1].isdigit() and message[2][1:].isdigit() and int(message[1]) > 0 and int(message[2][1:]) > 0:

			if message[2][0].lower() == 'd':
				if int(message[1]) <= 20 and int(message[2][1:]) <= 100:
					for i in range(int(message[1])):
						dice_rolls.append(random.randint(1, int(message[2][1:])))

					dice_output = 'Rolled ' + message[1] + ' x D' + message[2][1:] + ': '
					for i in range(len(dice_rolls)):
						dice_output += str(dice_rolls[i])

						if i < len(dice_rolls) - 1:
							dice_output += ' + '

					dice_output += ' = ' + str(sum(dice_rolls))

					return dice_output

				else:
					return 'Exceeded maximum. Maximum allowed: {}roll 20 D100'.format(config.COMMANDPREFIX)

			else:
				return 'You must specify the number of sides per dice properly. Usage: {}roll 3 D6'.format(config.COMMANDPREFIX)

		else:
			return 'Invalid syntax. Must use positive numbers. Usage: {}roll 3 D6'.format(config.COMMANDPREFIX)

	else:
		return 'Incorrect number of arguments. Usage: {}roll 3 D6'.format(config.COMMANDPREFIX)

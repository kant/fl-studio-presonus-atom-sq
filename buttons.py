import device
import ui
import channels
import mixer
import general
import playlist
import transport
import midi
import patterns
import data
import plugins
from direction import Directions
from lights import Lights
from modes import Modes
from notes import Notes
import _random

from midi import *

current_arrow = 0
arrow_index = 0

# arrow_status = False

class Buttons:

	scale = 0
	scale_choice = 0
	note = 0
	root_note = 0
	touchpad_value = 0
	lower_limit = 0
	upper_limit = 0
	g_rotate = [2, 3, 4]
	g_iter = 0
	

	def __init__(self, event):

		event = event
		self.act_out(event)


	def act_out(self, event):
		push = Modes(event)
		print(event.midiId, event.data1, event.data2, event.midiChan, event.midiChanEx)
		global j
		global f
		# global touchpad_value




		# if event.midiId == 144 and event.midiChanEx == 137:			# 137 selects for notes
		# 	notes = Notes(event)

		if event.midiId == 144 and event.midiChanEx == 256:			# 256 selects for functions i.e. transport etc 
			# message = Midi2(event)
			if event.data2 > 0:


				if event.data1 not in data.ud_arrow:
					Directions.arrow_status = False

				if event.data1 == data.tsport["play"]:
					transport.start()
					print('Play')
					event.handled = True

				elif event.data1 == data.tsport["stop"]:
					transport.stop()
					print('Stop')	
					event.handled = True

				elif event.data1 == data.tsport["record"]:
					transport.record()
					print('Toggle Record')	
					event.handled = True 

				elif event.data1 == data.tsport["metronome"]:	 
					print('Toggle Metronome')
					transport.globalTransport(midi.FPT_Metronome, 110)
					event.handled = True

				elif event.data1 == data.tsport["shift_play"]:
					transport.globalTransport(midi.FPT_LoopRecord, 113)
					print('Toggle Loop')	
					event.handled = True 

				elif event.data1 == data.tsport["shift_stop"]:
					transport.globalTransport(midi.FPT_Undo, 20)
					print('Undo/Redo')
					event.handled = True

				elif event.data1 == data.tsport["shift_record"]:
					transport.globalTransport(midi.FPT_Save, 92)
					print('Save')
					event.handled = True

				elif event.data1 in data.buttons["solo"]:
					if ui.getFocused(0):
						mixer.soloTrack(mixer.trackNumber())
						event.handled = True

					elif ui.getFocused(1):
						channels.soloChannel(channels.channelNumber())	
						event.handled = True

				elif event.data1 in data.buttons["mute"]: 
					if ui.getFocused(0):
						mixer.muteTrack(mixer.trackNumber())
						event.handled = True

					elif ui.getFocused(1):
						channels.muteChannel(channels.channelNumber())	
						event.handled = True	
					
					else:
						event.handled = True		

				elif event.data1 in data.ud_arrow:
					direct = Directions(event)

				elif event.data1 in data.buttons["arm"]:
					print('arm track')
					if ui.getFocused(0):
						mixer.armTrack(mixer.trackNumber())
						event.handled = True
					elif ui.getFocused(1):
						mixer.linkTrackToChannel(0)
				# elif event.data1 == data.buttons["zoom"]: 

				elif event.data1 == data.pads['left_arrow']:
					if ui.getFocused(5) and plugins.isValid(channels.selectedChannel()):
						print('plugin')
						plugins.prevPreset(channels.selectedChannel())
						event.handled = True
					else:
						ui.left()
						event.handled = True

				elif event.data1 == data.pads['right_arrow']:
					if ui.getFocused(5) and plugins.isValid(channels.selectedChannel()):
						print('plugin')
						plugins.nextPreset(channels.selectedChannel())
						event.handled = True
					else:
						ui.right()
						print('right')
						event.handled = True

		if event.midiId == 176 and event.data1 == data.pads['touch']:				# this selects for touchpad and allows it to go to zero
			Buttons.touchpad_value = event.data2

		if event.midiId == 176 and event.data2 > 0:
			
			if event.data1 == data.knobs["jog_wheel"]:
				print('jogging')
				if event.data2 == 1:
					ui.next()

				elif event.data2 == 65:
					ui.previous()

				# if ui.getFocused(1):
				# 	if event.data2 == 65:
				# 		print('channels focused')
				# 		if channels.channelNumber() > 0:
				# 			channels.selectOneChannel(channels.channelNumber() - 1)
				# 			# Lights.update_pattern()
				# 			print("selectOneChannel")
				# 			event.handled = True

				# 	elif event.data2 == 1:
				# 		if channels.channelNumber() < channels.channelCount() - 1:
				# 			channels.selectOneChannel(channels.channelNumber() + 1)
				# 			event.handled = True
				# 		else:
				# 				print('Channels Maxed')

				# elif ui.getFocused(0):
				# 		if event.data2 == 65:
				# 			if mixer.trackNumber() > 0:
				# 				mixer.setTrackNumber(mixer.trackNumber() - 1)
				# 				event.handled = True

				# 		elif event.data2 == 1:
				# 			mixer.setTrackNumber(mixer.trackNumber() + 1)
				# 			event.handled = True

				# elif ui.getFocused()
				# else:
				# 	event.handled = True

			if event.midiChanEx == 130:						# 1-6 buttons

				if event.data1 == data.buttons["button_1"]:
					print('quantize')
					channels.quickQuantize(channels.channelNumber())
					event.handled = True


				elif event.data1 == data.buttons["button_4"]:
					print("Random")
					for i in range(patterns.getPatternLength(patterns.patternNumber())):
						channels.setGridBit(channels.channelNumber(), i, 0)
					for z in range (patterns.getPatternLength(patterns.patternNumber())):
						y = num_gen()
						if y > (Buttons.touchpad_value * 516):
							channels.setGridBit(channels.channelNumber(), z, 1)
						else:
							pass
					event.handled = True

				elif event.data1 == data.buttons["button_5"]:
					Buttons.note_gen()

			if event.midiChanEx == 128:						# A - H Buttons

				if event.data1 == data.pads["a"]:
					if ui.getFocused(4):
						ui.selectBrowserMenuItem()		

					else:	
						ui.enter()
						print('enter')
						print('a')

				elif event.data1 == data.pads["b"]:
					channels.showCSForm(channels.channelNumber(), -1)
					print('b')

				elif event.data1 == data.pads["c"]:
					print('c')

				elif event.data1 == data.pads["d"]:
					print('View Plugin Picker')
					transport.globalTransport(midi.FPT_F8, 67)
					event.handled = True	

				elif event.data1 == data.pads["e"]:
					print('e')
					push.mode_change()

				elif event.data1 == data.pads["f"]:
					print('sub-mode')
					push.sub_mode()

				elif event.data1 == data.pads["g"]:
					Buttons.g_iter += 1
					if Buttons.g_iter >= len(Buttons.g_rotate):
						Buttons.g_iter = 0
					ui.setFocused(Buttons.g_rotate[Buttons.g_iter])
					print("g")

				elif event.data1 == data.pads['h']:
					if ui.getFocused(0):
						ui.setFocused(1)
					else:
						ui.setFocused(0)
					print('Focus')
					event.handled = True 				


	def note_gen():

		for i in range(patterns.getPatternLength(patterns.patternNumber())):
			note = data.scales[Buttons.scale_choice][Buttons.root_note][int(mapvalues(num_gen(), 0 + Buttons.lower_limit, len(data.scales[Buttons.scale_choice][Buttons.root_note]) - Buttons.upper_limit, 0, 65535))]
			# note = scales[0][0][int(mapvalues(num_gen(), 0, len(scales[0][0])-40, 0, 65535))]
			print(note)
			channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), i, 0, note, 1)
			#channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), i, 0, int(mapvalues(num_gen(), 48 , 96, 0, 65535)), 1)

def num_gen():
	# print('num_gen')
	rand_obj = _random.Random()
	rand_obj.seed()
	rand_int = rand_obj.getrandbits(16) 
	return rand_int 


def mapvalues(value, tomin, tomax, frommin, frommax):
	input_value = value
	solution = tomin + (tomax-(tomin))*((input_value - frommin) / (frommax - (frommin)))
	if  -0.01 < solution < 0.01:
		solution = 0
#	print(f"Solution: {solution}")
	return solution

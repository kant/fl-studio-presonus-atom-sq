import ui
import channels
import device
import patterns
import plugins
from modes import Modes
from lights import Lights
import data
import plugindata


temp_step = [0]
class Notes:

	def __init__(self, event):
		print(f'notes event: {event.data1}')

		if event.midiId == 144:
			temp_step.clear()
			temp_step.append(event.data1)
			print(f'temp step: {temp_step}')

		event = event
		self.light = Lights()
		self.range_one = [i for i in range(36, 52)]
		self.range_two = [i for i in range(52, 68)]
		self.decide(event)


	def decide(self, event):
		if ui.getFocused(5) and plugins.isValid(channels.selectedChannel()):
			self.drum_plugins(event)
		elif self.get_mode() == 0:
			self.keyboard(event)
			# Lights.clear_pattern()
		elif self.get_mode() == 1:
			print('get mode is 1')
			print(f'step_iter: {Modes.step_iter}')
			self.step_mode(event)
		elif self.get_mode() == 2:
			self.pad_channel(event)

	def keyboard(self, event):
		Lights.keyboard_lights()
		channels.midiNoteOn(channels.selectedChannel(), event.data1, event.data2)
		Lights.keyboard_lights()
		print('keyboard')
		event.handled = True
				
	def step_mode(self, event):
		
		if Modes.step_iter == 2 and event.data1 >= 52:
			print('select pattern')
			patterns.jumpToPattern(event.data1 - 51)
			self.light.light_pattern()
			event.handled = True

		elif Modes.step_iter == 0:

			if channels.getGridBit(channels.selectedChannel(), event.data1 - 36) == 0:						
				channels.setGridBit(channels.selectedChannel(), event.data1 - 36, 1)	
				event.handled = True
			else:															
				channels.setGridBit(channels.selectedChannel(), event.data1 - 36, 0)    
				# self.light.update_pattern()
				event.handled = True
			
			Lights.update_pattern()

			if Modes.step_iter == 1:
				self.light.light_pattern()
			else:	
				self.light.update_second()	

	def pad_channel(self, event):
		print('in pad channel')
		if  event.data1 < (channels.channelCount() + 36):
			channels.selectOneChannel(event.data1-36) 
			channels.midiNoteOn(event.data1-36, 60, event.data2)
			Lights.light_channels()
			event.handled = True

		else:
			Lights.light_channels()


	def drum_plugins(self, event):

		if event.midiId == 128 and event.data2 != 0:
			print('skip')
		elif plugins.getPluginName(channels.selectedChannel()) == 'FPC' and event.data1 in plugindata.atom_sq_pads:
			print('FPC')
			Lights.clear_pattern()
			channels.midiNoteOn(channels.selectedChannel(), plugindata.FPC_pads[plugindata.atom_sq_pads.index(event.data1)], event.data2)
			event.handled = True
		elif plugins.getPluginName(channels.selectedChannel()) == 'Slicex':
			Lights.clear_pattern()
			channels.midiNoteOn(channels.selectedChannel(), event.data1 + 24, event.data2)
			event.handled = True

	def get_mode(self):
		return Modes.mode


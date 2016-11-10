import os

import libaudioverse
import platform_utils.paths

sound_dir = os.path.join(platform_utils.paths.embedded_data_path(), 'sounds')

class SoundLoader(object):

	def __init__(self, server, world):
		self.server = server
		self.world = world
		self.cache=dict()

	def play_stationary(self, key,m):
		s=self.load_sound(key)
		s.source.position=m.x,m.y,m.z
		s.play()
	def load_sound(self, key):
		self.source = libaudioverse.SourceNode(self.server, self.world)
		if key not in self.cache:
			b = libaudioverse.Buffer(self.server)
			b.load_from_file(os.path.join(sound_dir, key+".ogg"))
			self.cache[key] = b
		b = self.cache[key]
		n = libaudioverse.BufferNode(self.server)
		n.buffer.value =b
		n.connect(0, self.source, 0)
		return Sound(n,self.source)

class Sound(object):

	def __init__(self, buffer_node,source):
		self.buffer_node = buffer_node
		self.source = source

	def stop(self):
		self.buffer_node.state = libaudioverse.NodeStates.stop

	def is_playing(self):
		return self.buffer_node.state == libaudioverse.NodeStates.playing

	def play(self,loop=False):
		self.buffer_node.connect(0, self.source, 0)
		self.buffer_node.position=0
		self.buffer_node.looping=loop
		self.buffer_node.state = libaudioverse.NodeStates.playing

	def free(self,loop=False):
		self.buffer_node.disconnect()
		del self

class audio_world(object):
	def __init__(self,md=125,density=0.8,reverbcutoff=22050,reverbtime=1.0):
		libaudioverse.initialize()
		self.server=libaudioverse.Server()
		self.server.set_output_device()
		self.world = libaudioverse.EnvironmentNode(self.server,"default")
		self.world.panning_strategy = libaudioverse.PanningStrategies.hrtf
		self.world.orientation = 0, 1, 0, 0, 0, 1
		self.world.max_distance=md
		self.world.distance_model=libaudioverse.DistanceModels.inverse_square
		self.world.min_reverb_level=1
		self.world.max_reverb_level=1
		self.reverb = libaudioverse.FdnReverbNode(self.server)
		send = self.world.add_effect_send(channels = 4, is_reverb = True, connect_by_default = True)
		self.world.connect(send, self.reverb, 0)
		self.reverb.connect(0, self.server)
		self.reverb.density=density
		self.reverb.cutoff_frequency=reverbcutoff
		self.reverb.t60=reverbtime
		self.reverb.default_reverb_distance=50

	def set_reverb_distance(distance):
		self.reverb.default_reverb_distance=50

	def set_reverb_time(time):
		self.reverb.t60=time

	def set_reverb_cutoff(cutoff)
		self.reverb.cutoff_frequency=reverbcutoff

	def set_reverb_density(density):
		self.reverb.density=density

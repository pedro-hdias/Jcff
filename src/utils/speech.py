from accessible_output2.outputs.auto import Auto
import time

auto = Auto()

def speech(t):
	auto.speak(t)
	time.sleep(1)

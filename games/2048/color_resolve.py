from gester.attributes import Color

def color_resolve(value):
	color : Color
	text : str
	if (value == 0):
		color = Color("color", 204, 179, 192)
		text = ""
	elif (value == 2):
		color = Color("color", 238, 218, 228)
		text = "2"
	elif (value == 4):
		color = Color("color", 237, 200, 224)
		text = "4"
	elif (value == 8):
		color = Color("color", 242, 121, 177)
		text = "8"
	elif (value == 16):
		color = Color("color", 245, 99, 149)
		text = "16"
	elif (value == 32):
		color = Color("color", 246, 95, 124)
		text = "32"
	elif (value == 64):
		color = Color("color", 246, 59, 94)
		text = "64"
	elif (value == 128):
		color = Color("color", 237, 114, 207)
		text = "128"
	elif (value == 256):
		color = Color("color", 237, 97, 204)
		text = "256"
	elif (value == 512):
		color = Color("color", 237, 80, 200)
		text = "512"
	elif (value == 1024):
		color = Color("color", 237, 63, 197)
		text = ""
	elif (value == 2048):
		color = Color("color", 237, 46, 194)
		text = "2048"
	else:
		raise RuntimeError("Invalid Value Detected!")

	return color, text
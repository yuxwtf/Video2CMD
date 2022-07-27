import os, shutil, time, cv2, threading, string
import ascii2text
import pywhatkit
from pydub import AudioSegment 
from pydub.playback import play
from PIL import Image

count = 0
inputfile = None

def toascii(in_, out, mode):
	img = Image.open(in_)
	width, height = img.size
	aspect_ratio = height/width
	new_width = 120
	new_height = aspect_ratio * new_width * 0.55
	img = img.resize((new_width, int(new_height)))
	img = img.convert('L')
	pixels = img.getdata()
	if mode == 1:
		chars = string.punctuation
	elif mode == 2:
		chars = ["B","S","#","&","@","$","%","*","!",":","."]
	else:
		chars = ["B","S","#","&","@","$","%","*","!",":","."]
	new_pixels = [chars[pixel//25] for pixel in pixels]
	new_pixels = ''.join(new_pixels)
	new_pixels_count = len(new_pixels)
	ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
	ascii_image = "\n".join(ascii_image)
	with open(f"{out}.txt", "w") as f:
	  f.write(ascii_image)
	  f.close()

def splitframes(inputfile):
	global count
	try:
		os.mkdir(f'./temp/{inputfile}')
	except:
		pass
	vidcap = cv2.VideoCapture(inputfile)
	success,image = vidcap.read()
	count = 0
	print('spliting video...', end="\r")
	while success:
	  cv2.imwrite(f'./temp/{inputfile}/{count}.jpg', image)
	  print(f'[DEBUG] {count}.jpg SPLITTED !')
	  success,image = vidcap.read()
	  count += 1
	os.system('cls')
	print(f'Splitted {count-1} frames !')

def convert_to_ascii(inputfile, mode):
	for i in range(count):
		if mode == 1:
			pywhatkit.image_to_ascii_art(f'./temp/{inputfile}/{i}.jpg', f'./temp/{inputfile}/{i}')
		elif mode == 2:
			toascii(f'./temp/{inputfile}/{i}.jpg', f'./temp/{inputfile}/{i}', mode=1)
		elif mode == 3:
			toascii(f'./temp/{inputfile}/{i}.jpg', f'./temp/{inputfile}/{i}', mode=2)
		else:
			pywhatkit.image_to_ascii_art(f'./temp/{inputfile}/{i}.jpg', f'./temp/{inputfile}/{i}')
		os.remove(f"./temp/{inputfile}/{i}.jpg")
		print(f'[DEBUG] {i}.png CONVERTED TO ASCCI !')
	os.system('cls')
	print(f'Converted {count-1} images to ASCII !')

def startsong(s):
	play(s)

def init_title(inputfile):
	while True:
		os.system(f'title VIDEO2CMD ^| Playing: {inputfile} ^| Frames: {count} ^| Speed: ~60FPS')

def startanim(inputfile, speed):
	os.system(f'ffmpeg.exe -i {inputfile} -ab 160k -ac 2 -ar 44100 -vn ./temp/{inputfile}/audio.wav')
	os.system('cls')
	s = AudioSegment.from_wav(f"./temp/{inputfile}/audio.wav")
	st = threading.Thread(target=startsong, args=(s,))
	st.start()
	time.sleep(0.2)
	for i in range(count):
		f = open(f'./temp/{inputfile}/{i}.txt', 'r')
		frame = f.read()
		print(frame, end='\r', flush=True)
		f.close()
		os.remove(f"./temp/{inputfile}/{i}.txt")
		time.sleep(speed)
		os.system('title ')
	shutil.rmtree(f'./temp/{inputfile}')
	time.sleep(2)
	os.system('cls')
	print("		Thanks for using VIDEO2CMD by Yux !")
	input('')
	exit()



f = input('video file : ')
asciimode = int(input('ASCII mode ? (1/2/3) : '))
try:
	ut = threading.Thread(target=init_title, args=(f,))
	ut.start()
	try:
		splitframes(f)
		convert_to_ascii(f, mode=int(asciimode))
		startanim(f, 0.0110)
	except:
		os.rmdir(f'./temp/{f}')
		splitframes(f)
		convert_to_ascii(f, mode=int(asciimode))
		startanim(f, 0.0110)
except Exception as e:
	print(e)

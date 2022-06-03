import os, shutil, time, cv2, threading, sys
import pywhatkit
from pydub import AudioSegment 
from pydub.playback import play 

count = 7776
inputfile = None


def splitframes(inputfile):
	global count
	os.mkdir(f'./temp/{inputfile}')
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

def convert_to_ascii(inputfile):
	for i in range(count):
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
	ut = threading.Thread(target=init_title, args=(inputfile,))
	ut.start()
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

try:
	try:
		splitframes(f)
		convert_to_ascii(f)
		startanim(f, 0.0110)
	except:
		shutil.rmtree(f'./temp/{f}')
		splitframes(f)
		convert_to_ascii(f)
		startanim(f, 0.0130)
except Exception as e:
	print(e)

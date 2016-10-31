import time
import sys

def display_message(percentage):
	sys.stdout.write("\rInstalling ... %d%%"%percentage)
	sys.stdout.flush()

def main():
	for i in range(0,101,10):
		display_message(i)
		time.sleep(0.5)
	print ("\rInstalling [DONE]   ")
	time.sleep(1)

if __name__ == '__main__':
	main()

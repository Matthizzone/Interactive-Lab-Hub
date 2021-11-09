from __future__ import print_function
import qwiic_joystick
import time
import sys
import math
import statistics as stat

def avg_no_outl(a):
    median = stat.median(a)
    summ = 0
    nums = 0
    
    for i in range(len(a)):
        if a[i] == -511:
            i += 1
            continue
        if (abs(median - a[i]) < 100):
            summ += a[i]
            nums +=1
        i +=1
    
    if (nums == 0):
        return median
    
    return summ / nums

def runExample():

	print("\nSparkFun qwiic Joystick   Example 1\n")
	myJoystick = qwiic_joystick.QwiicJoystick()

	if myJoystick.connected == False:
		print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myJoystick.begin()

	print("Initialized. Firmware Version: %s" % myJoystick.version)

	# . 0   < 1   > 2   ^ 3   v 4
	line = ""
	clear = "\n" * 20
	last_dir = ""
	current_dir = ""
	last_button = 1
	seq = ""
	smoothing = 10
	joy_x_list = [0] * smoothing
	joy_y_list = [0] * smoothing
	just_deleted = True
	just_cleared = True

	lookup = {"^<v>^>" : "a", 
			  "^<v>^v" : "a",
			  "^<v>^>v" : "a",
			  "^<v>v" : "a",
			  "^<>^v" : "a",
			  "^<v>^v" : "a",
			  ">^<v>^>" : "a", 
			  ">^<v>^v" : "a",
			  ">^<v>^>v" : "a",
			  ">^<v>v" : "a",
			  ">^<>^v" : "a",
			  ">^<v>^v" : "a",
			  "^v^>v" : "b",
			  "^v>v" : "b",
			  "^<v" : "c",
			  ">^<v" : "c",
			  ">^<v>" : "c",
			  "^<v>" : "c",
			  "><v>" : "c",
			  "^<v^" : "d",
			  "^<v^v" : "d",
			  "^v^<v" : "d",
			  "<v^v" : "d",
			  "<v>^v" : "d",
			  "^<v^" : "d",
			  ">^<v" : "e",
			  ">^<v>" : "e",
			  "><v" : "e",
			  ">^v" : "e",
			  "v^><>" : "f",
			  ">^v<>" : "f",
			  "^<v^v<" : "g",
			  "^<v>v<" : "g",
			  "^<v>^>v<" : "g",
			  "^<v>^v<" : "g",
			  "^<v<" : "g",
			  "<v<" : "g",
			  "<v>v<" : "g",
			  "^v>" : "h",
			  "^v^>" : "h",
			  "v^" : "i",
			  "v<^" : "j",
			  "v<v^" : "j",
			  "^v><v" : "k",
			  "^v><>" : "k",
			  "^v><" : "k",
			  "^v<v" : "k",
			  "^v" : "l",
			  "v" : "l",
			  "v^v^v" : "m",
			  "v^>v^>v" : "m",
			  "v>v>v" : "m",
			  "<v<v^>v" : "m",
			  "<^v^>v" : "m",
			  "v<^v^>v" : "m",
			  "v<^>v^>" : "m",
			  "<v^>v" : "m",
			  "<^><^>" : "m",
			  "<v>v>v" : "m",
			  "v^>V>V" : "m",
			  "v>v^>v" : "m",
			  "<^v^>" : "m",
			  "<^>v>" : "m",
			  "v<v>v" : "m",
			  "v<v>" : "m",
			  "<^v>" : "m",
			  "<^v>v" : "m",
			  "v^v>v" : "m",
			  "<v<v>v" : "m",
			  "^v>v>v" : "m",
			  "v^>v>v" : "m",
			  "v<v^>" : "m",
			  "v^v" : "n",
			  "v>v" : "n",
			  "<^>v" : "n",
			  "<^>" : "n",
			  "v<^>v" : "n",
			  "v<^>" : "n",
			  "^<^>" : "n",
			  "v<^v" : "n",
			  "<>" : "n",
			  "^<v>^" : "o",
			  "^<v>" : "o",
			  "<v>^" : "o",
			  "v^>v" : "p",
			  "v^>v" : "p",
			  "^>v^v" : "p",
			  ">v^v" : "p",
			  "^<v>^v>" : "q",
			  "^v^v>" : "q",
			  "<v>^v>" : "q",
			  "v>^v>" : "q",
			  "^<v^v>" : "q",
			  "v>" : "r",
			  "v^>" : "r",
			  ">^<>v<" : "s",
			  "^<>v" : "s",
			  ">^<>v" : "s",
			  "^<>v<" : "s",
			  ">^<v>v<" : "s",
			  "^v<>" : "t",
			  "v<>" : "t",
			  "<v>v" : "u",
			  "<v>" : "v",
			  "^v^v^" : "w",
			  "<v^v>" : "w",
			  "^v>v>" : "w",
			  "<>^<>v" : "w",
			  "v><" : "x",
			  "<v><" : "x",
			  "v<" : "x",
			  "<>v" : "y",
			  "<><" : "y",
			  ">v" : "y",
			  "><" : "y",
			  "<^><v>" : "z",
			  "^><v" : "z",
			  "<^><v" : "z",
			  "^><v>" : "z",
			  "" : " "}

	while True:
		for i in range(smoothing-1):
			joy_x_list[i] = joy_x_list[i+1]
			joy_y_list[i] = joy_y_list[i+1]
		
		joy_x_list[smoothing-1] = myJoystick.horizontal - 512
		joy_y_list[smoothing-1] = myJoystick.vertical - 512

		#if (avg_no_outl(joy_x_list) < -220):
			#print(joy_x_list, avg_no_outl(joy_x_list))

		joy_x = avg_no_outl(joy_x_list)
		joy_y = avg_no_outl(joy_y_list)

		if (joy_y < 200 and joy_y > -200):
			if (joy_x > 200 and not just_cleared):
				current_dir = ">"
			elif (joy_x < -400 and not just_deleted):
				current_dir = "<"
		elif (joy_x < 200 and joy_x > -200):
			if (joy_y > 200):
				current_dir = "v"
			elif (joy_y < -50):
				current_dir = "^"
		else:
			just_deleted = False
			just_cleared = False

		if (not current_dir == last_dir):
			seq += current_dir
			last_dir = current_dir

		if (not myJoystick.button == last_button):
			last_button = myJoystick.button
			if (myJoystick.button == 0):
				print(clear)

				if (joy_x < -200 or seq == "<"):
					if (len(line) > 0):
						line = line[:-1]
						just_deleted = True
				elif (joy_x > 200 or seq == ">"):
					line = ""
					just_cleared = True
				else:
					if (seq in lookup):
						line += lookup[seq]
					else:
						print("(" + seq + ")")
						line += "?"
				print(line + "_")

				seq = ""
				last_dir = ""
				current_dir = ""

		time.sleep(.01)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)

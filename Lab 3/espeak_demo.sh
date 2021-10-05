# from https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
espeak -ven+f2 -k5 -s150 --stdout  "Hello Matthew. Want to hear a history lesson? 400 years ago, christopher columbus ordered a pizza from dominos. It was covered with sea water and tasted like striped bass. He threw it on the ground and stepped on it, inspiring his voyage to the americas." | aplay

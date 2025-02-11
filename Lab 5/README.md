# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms needs to be aware of.

## Prep

1.  Pull the new Github Repo.
2.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2021/Lab%202/prep.md), we offered the instruction at the bottom.
3.  Read about [OpenCV](https://opencv.org/about/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:

1. Raspberry Pi
1. Webcam 
1. Microphone (if you want to have speech or sound input for your design)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### OpenCV
A more traditional method to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python. We included 4 standard OpenCV examples: contour(blob) detection, face detection with the ``Haarcascade``, flow detection (a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (e.g. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example. 

Following is a nicer way you can run and see the flow of the `openCV-examples` we have included in your Pi. Instead of `ls`, the command we will be using here is `tree`. [Tree](http://mama.indstate.edu/users/ice/tree/) is a recursive directory colored listing command that produces a depth indented listing of files. Install `tree` first and `cd` to the `openCV-examples` folder and run the command:

```shell
pi@ixe00:~ $ sudo apt install tree
...
pi@ixe00:~ $ cd openCV-examples
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```

The flow detection might seem random, but consider [this recent research](https://cseweb.ucsd.edu/~lriek/papers/taylor-icra-2021.pdf) that uses optical flow to determine busy-ness in hospital settings to facilitate robot navigation. Note the velocity parameter on page 3 and the mentions of optical flow.

Now, connect your webcam to your Pi and use **VNC to access to your Pi** and open the terminal. Use the following command lines to try each of the examples we provided:
(***it will not work if you use ssh from your laptop***)

```
pi@ixe00:~$ cd ~/openCV-examples/contours-detection
pi@ixe00:~/openCV-examples/contours-detection $ python contours.py
...
pi@ixe00:~$ cd ~/openCV-examples/face-detection
pi@ixe00:~/openCV-examples/face-detection $ python face-detection.py
...
pi@ixe00:~$ cd ~/openCV-examples/flow-detection
pi@ixe00:~/openCV-examples/flow-detection $ python optical_flow.py 0 window
...
pi@ixe00:~$ cd ~/openCV-examples/object-detection
pi@ixe00:~/openCV-examples/object-detection $ python detect.py
```

**\*\*\*Try each of the following four examples in the `openCV-examples`, include screenshots of your use and write about one design for each example that might work based on the individual benefits to each algorithm.\*\*\***



![alt text](https://github.com/Matthizzone/Interactive-Lab-Hub/blob/Fall2021/Lab%205/contours_01.png)
Automatically generate a coloring book from a photograph album. By using edge detection, can simplify images to just an outline, which can be used to make any image into a coloring book image.

![alt text](https://github.com/Matthizzone/Interactive-Lab-Hub/blob/Fall2021/Lab%205/face_detect_01.png)
face detection bathroom febreeze: when a face is detected, spray the preferred scent of the user in the bathroom.

![alt text](https://github.com/Matthizzone/Interactive-Lab-Hub/blob/Fall2021/Lab%205/obj_detect_01.png)
Desk clutter meter: keep track of how many objects are on the desk to monitor how stressed the user is over time.

![alt text](https://github.com/Matthizzone/Interactive-Lab-Hub/blob/Fall2021/Lab%205/tracking_01.png)
"Invisible Ink": tracks what you write as you pretend to write it on a piece of paper with an unclicked pen.



#### MediaPipe

A more recent open source and efficient method of extracting information from video streams comes out of Google's [MediaPipe](https://mediapipe.dev/), which offers state of the art face, face mesh, hand pose, and body pose detection.

![Alt Text](mp.gif)

To get started, create a new virtual environment with special indication this time:

```
pi@ixe00:~ $ virtualenv mpipe --system-site-packages
pi@ixe00:~ $ source mpipe/bin/activate
(mpipe) pi@ixe00:~ $ 
```

and install the following.

```
...
(mpipe) pi@ixe00:~ $ sudo apt install ffmpeg python3-opencv
(mpipe) pi@ixe00:~ $ sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23
(mpipe) pi@ixe00:~ $ pip3 install mediapipe-rpi4 pyalsaaudio
```

Each of the installs will take a while, please be patient. After successfully installing mediapipe, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the hand pose detection script we provide:
(***it will not work if you use ssh from your laptop***)


```
(mpipe) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(mpipe) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control, and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting. Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py` lines 48-53. 

**\*\*\*Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.\*\*\***



Yoga form analyzer: Tells the user how to improve their yoga. Will tell them if their arms are too low or if they need to work on hip flexibility.



(You might also consider how this notion of percentage control with hand tracking might be used in some of the physical UI you may have experimented with in the last lab, for instance in controlling a servo or rotary encoder.)



#### Teachable Machines
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple. However, its simplicity is very useful for experimenting with the capabilities of this technology.

![Alt Text](tm.gif)

To get started, create and activate a new virtual environment for this exercise with special indication:

```
pi@ixe00:~ $ virtualenv tmachine --system-site-packages
pi@ixe00:~ $ source tmachine/bin/activate
(tmachine) pi@ixe00:~ $ 
```

After activating the virtual environment, install the requisite TensorFlow libraries by running the following lines:
```
(tmachine) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ sudo chmod +x ./teachable_machines.sh
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ ./teachable_machines.sh
``` 

This might take a while to get fully installed. After installation, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the example script:
(***it will not work if you use ssh from your laptop***)

```
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python tm_ppe_detection.py
```


(**Optionally**: You can train your own model, too. First, visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. Second, use the webcam on your computer to train a model. For each class try to have over 50 samples, and consider adding a background class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate, or export your model as a 'Tensorflow' model, and select 'Keras'. You will find an '.h5' file and a 'labels.txt' file. These are included in this labs 'teachable_machines' folder, to make the PPE model you used earlier. You can make your own folder or replace these to make your own classifier.)

**\*\*\*Whether you make your own model or not, include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.\*\*\***



Link of testing out the tm_ppe-detection.py
https://youtu.be/0DH8-8Y1KVM
This highly trainable model would allow any kind of visual cue detection. This could range from objects as a whole or configurations of them. One idea I had is related to the idea I had for hand_pose.py, but instead of a Yoga form analyzer, it is simply a yoga pose detector.



*Don't forget to run ```deactivate``` to end the Teachable Machines demo, and to reactivate with ```source tmachine/bin/activate``` when you want to use it again.*


#### Filtering, FFTs, and Time Series data. (optional)
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the accelerometer, try the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

**2. Set up averaging** Can you average your signal in N-sample blocks? N-sample running average?

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

**\*\*\*Include links to your code here, and put the code for these in your repo--they will come in handy later.\*\*\***


### Part B
### Construct a simple interaction.

Pick one of the models you have tried, pick a class of objects, and experiment with prototyping an interaction.
This can be as simple as the boat detector earlier.
Try out different interaction outputs and inputs.

**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***

https://youtu.be/qCGPUTJhkSU
Using Google's Teachable Machines, I created the yoga pose detector.

This device takes as input a constant video feed of a person performing yoga poses and outputs one of four possibility that I chose to train the model on: Easy Seat, Tree Pose, Triangle Pose and Crane Pose. After testing the device on myself I found that the model has a strong preference for guessing Easy Seat when the entire body is not in frame. Also, in an attempt to confuse the model, I tried to show it some in between poses, specifically a pose that combined Easy Seat and Tree Pose to see what it would do. It seemed to oscillate back and forth between the two. I also tested camera angles that the model was not trained on, such as a floor-level camera for Tree Pose, and it was suprisingly resilient to this change, still guessing Tree Pose.



### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it do what it is supposed to do? When show the poses at a reasonable angle (not from straight down or straight up, which would conceal too much information), the model accurately categorizes between the 4 yoga poses. It even succeeds (I would say) when the user challenges the model by mixing poses together, as the model oscillates back and forth between the two that are being mixed between.
1. When does it fail? It fails if the entire person isn't in frame. Even if the user's foot is outside the frame, the model ignores the whole leg and resorts to guessing easy seat.
1. When it fails, why does it fail? The pose detection used by Teachable Machines must be a wholistic process. Let's say a user's hands aren't visible (outside the top of the frame), but the rest of the pose is Tree Pose. For a human, it is easy to figure out the correct pose by assuming the rest of the information, but the model can't do process of elimination or any kind of fill in the blank work that we can, so it guesses it's default answer of Easy Seat.
1. Based on the behavior you have seen, what other scenarios could cause problems? If there are multiple people in the frame, the machine might get confused who it is supposed to be analyzing. In a yoga studio (a location where this device is most likely to be implemented), there usually are mirrors on 2 walls. This means the model might mistake the reflection for another person and get confused.

**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system? No, all the users sees is the name of a pose and a confidence level. There is no way for the user to tell if the machine is actually correct, just guessing, or whether or not the machine has been trained on a that particular pose.
1. How bad would they be impacted by a miss classification? A miss classification would result in the user being confused.
1. How could change your interactive system to address this? Instead of just the name of the pose, a picture of the pose should appear on screen too so the user can tell if there is a mismatch between the example picture and the one they are doing.
1. Are there optimizations you can try to do on your sense-making algorithm? The algorithm should have a "I don't know this pose, what should I call it?" feature so that the user can add new poses if it is outside the machine's scope of knowledge.

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for? X can be used to categorize yoga poses. If a user stands in front of the camera and performs the pose, the pose will be named.
* What is a good environment for X? If a student is learning new yoga poses, they can test them out in front of the camera to see if the camera will detect it, and name it properly. In a place where there isn't much distraction/few other people such as at home or a yoga studio (without mirrors, as described above).
* What is a bad environment for X? A bad environment would be a yoga studio with many mirrors, a crowded indoor space like during a yoga class or outside where there are many people. Or in a tight space where the user cannot get their entire body in frame.
* When will X break? X will break when there are multiple people in the camera's view, when the use performs a pose the machine hasn't been trained on yet, or when the user tries to mix two poses together.
* When it breaks how will X break? X "breaking" will mean a misclassification, or the classifier will alternative between two choices and never settle on one.
* What are other properties/behaviors of X? X tends to be very confident (100%) if the pose is done correctly and in proper view. If the user is just walking around or transition from standing or walking to a real pose, the model flutters about between all four options.
* How does X feel? To use X feels like a test of your yoga ability. If you show the camera the poses you just learned correctly, your reward is a correct classification by the machine.

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***

In this video, I test out the trained yoga pose classifier: https://youtu.be/qCGPUTJhkSU
If the next part, I intend to change it up a bit. Instead of having multiple different poses, there will be just one pose, but done in 4 slightly different ways, only one of which is techincally correct. For example, one will have "arms too low" or "back not straight". I will test this device on a user to see if the machine can tell the subtle differences apart between correct and incorrect yoga poses, and use that to give the user constructive criticism to improve their form.

I noticed that with the current device design, it is impossible to read feedback without stopping your yoga to go read what the laptop says. I would like to address this by running this device from the Raspberry Pi to change its form. Instead of the device being a huge gaming laptop with textual display, it would be the lightweight webcamand use text-to-speech to enable the user to get feedback while doing the yoga pose. This would eliminate the need to stop, walk towards the display and read the comments.



### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**\*\*\*Include a short video demonstrating the finished result.\*\*\***

Unfortuantely, I ran into a lot of issues testing my ideas from the above questions. First I tried implementing the Teachable Machine on the Raspberri Pi, but found it to be more complicated than I thought. First I tried training the model on my laptop, downloading it and running it on the Pi, but I couldn't figure out how to link all the pieces back together. When you download a model from Teachable Machines, the resulting ZIP has 3 files: two JSON and weights.bin (the actual weights and biases the model settled on). I did not know how to this matrix to perform classification on the PI, even after some research. The next thing I tried was accessing the internet from the Pi and training it there from the native browser on the PI, Chromium, but it kept crashing. The window where the webcam livefeed is displayed opened for a brief moment and then closed without showing anything but a black screen. Unfortunately this meant I had the abandon the idea of running Teachable machine on the Pi, and the idea of combining it with text-to-speech.

Next I tested my hypothesis that the Teachable Machine would not classify well if there were many people in the frame. I had some friends in the class (Maggie Horowitz, center, and Ethan Change, right) attempt to advert the classifier while I performed legitamate poses. At the same time, not everyone is fully in the frame at all times. This tests the other hypothesis I had that the classifier would not perform well if it did have the full visual picture of the poser. We all stood in front of the camera and recorded a video. Since Teachable Machines only allows images for upload, I chose three key screenshots where everyone was the most still to give the machine the best chance at success. Here are the results for those three images:

![alt text](https://github.com/Matthizzone/Interactive-Lab-Hub/blob/Fall2021/Lab%205/result.png)

I was very surprised with the results. For some of the video, Maggie and Ethan were doing the YMCA dance, and in the left image, you can see both of them in the middle of the "M" pose. The teachable machine was able to single out just Maggie and classify it as the Tree Pose, which wasn't too far off! For the center image, you can see that Maggie is doing the tree pose and at the same time, I am doing easy seat (partly outside the frame), and somehow the model detected both of us at the same time (71% easy seat and 29% tree pose)! I suspect that this was just a coincidence though. In the image you can see blue dots on me but not Maggie, meaning the model was not analyzing her. The reason why 29% tree pose appearing was just do to classification error, likely arising from the occlusion of the left side of my body outside the frame. You can see that same effect did not happen in the right image, where the model is analyzing Maggie only, and it is not also classifying me doing Crane Pose.

Finally, I upgraded the Yoga Pose Detector to distinguish slight variations of the same pose instead of entirely different poses. All the poses are Triangle Pose, but there are four incorrect forms and one with correct form. For each incorrect form, the classification label is the feedback that would have been said out loud with text-to-speech. Here are the labels:
1. correct
2. widen your stance
3. arm too low
4. bend more at the back
5. gaze up

I took more training photos, and created the new model. In this video, you can see the classification in action:
https://youtu.be/SATvS0aYc9I

This video shows that minute differences in pose are beyond the capability of Google's Teachable Machines. In the video, I tested the five poses above in order, and found that the model almost always classifies them as "Raise back arm up to the sky." Unfortunately, this meant that not only could I not get text-to-speech to work or the model to run on the Pi, but the core funcitonality of the device couldn't be achieved either. This idea turned out to be beyond the capabilities of the resources offered in class.

Instead, the idea remains unimplemented. However, I still learned a lot about the design of the devices between parts 1 and 2 of this lab, and might try implementing this (with added functionality) for the final project.


# Breakout-Game with Face Dectection

This is the basic implementation of Pygame + OpenCV Breakout-Game with Face Dectection. It can be found [here](https://github.com/anthopark/Face-Breakout).
Pygame integrates with OpenCV to deploy pre-trained deep learning-based face detector.
The breakout game uses x-coordinate of a detected face to control the paddle.

## Prerequisites
The following software/packages are required to run this project.

* [Python3](https://www.python.org/)
* [OpenCV(3.3 or greater)](https://opencv.org/)
* [pygame(1.9.4 or greater)](https://www.pygame.org/docs/)
* [imutils (computer vision/image processing Python package created by the author of pyimagesearch.com)](https://github.com/jrosebr1/imutils)


## How to running the game?

Please run the command below:

```sh
$ python3 main.py -p deploy.prototxt.txt -m res10_300x300_ssd_iter_140000.caffemodel
```

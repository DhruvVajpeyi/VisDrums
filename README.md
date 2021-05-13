# VisDrums
 Computer Vision based drums
 
## Authors
1. Tarek Saidee
2. Dhruv Vajpeyi
3. Cheng Chen 


## Prerequisites
* Having access to TWO cameras is required, the type of camera doesn't matter. If you only have access to 
one, you can use your phone as a camera by downloading and installing a software that plugs in your phone camera to your 
machine. The software we used was [IVCam](https://www.e2esoft.com/ivcam/)

* Having drawn at least one circle (we recommend 3) on a plane sheet of paper. The circles need to be smooth but not 
necessarily perfect.

## How to run the project
1. You first need to install all the packages needed to run this project. This can be easily done by running the following
command ``pip install -r requirements.txt``

2. To start the application you can this command ``python main.py``

## Things to consider

* You need to setup both cameras in a specifc way
    * The first camera (top down view) need to be above the drawn circles in order to detect them and it has to be stable
    * The second camera (side view) need to be on the same level as your sheet of paper. 
* Keep your drumsticks within the both camera's views so they don't get lost by the tracking algorithm because the algorithm 
might not be able to find them again even if they come back into frame.


## Controls/Steps after running the project
1. First thing you need to do is initialize circle detection by clicking ``c``. That will start detecting the drawn circles
using the top down camera
2. Second thing is start tracking the drumsticks from the **top down camera**. Clicking ``t`` will allow you to free-select two areas that contain the 
tip of each stick. After each selection, click ``space`` to either move on to selecting the 2nd stick or to go back to the 
main program.
3. Similar to the previous step, you need to track the sticks from the side camera. This is done the same way but you need to
click ``s`` to start the tracking process as explained in step 2.
4. **Start drumming and have fun!**
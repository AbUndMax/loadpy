[![GitHub](https://img.shields.io/badge/GitHub-loadpy-blue?logo=github)](https://github.com/AbUndMax/loadpy)
[![License](https://img.shields.io/badge/License-CC_BY--NC_4.0-blue)](https://github.com/AbUndMax/loadpy/blob/main/LICENSE.md)
[![Java](https://img.shields.io/badge/Python-3.6+-blue?logo=python)](https://www.python.org/downloads/release/python-360/)
[![Badge](https://img.shields.io/github/v/release/AbUndMax/loadpy?color=brightgreen)](https://github.com/AbUndMax/loadpy/releases/latest)

# loadpy
This is a small python packages that provides simple laoding animations for CLI applications:

There are two types of loading animations that are provided by this package:
1. Throbber
2. Loading Bar

## Install

Download the wheel file from the [latest release](https://github.com/AbUndMax/loadpy/releases/latest) and install it with pip:
```bash
pip install loadpy-x.x.x.whl
```
replace x.x.x with the version number of the downloaded wheel file.

Then you are ready to use the package in your python scripts.
```python
import loadpy
```

## Throbber
<p align="center">
    <img src="images/throbber.gif" alt="Throbber">
</p>

### Parameters

The throbber symbolizes a running process. It constructor has 3 parameters:
1. `desc` : The description of the process that is being run.
2. `end`: The end message that is displayed when the process is completed.
3. `timeout`: The time interval between each throbber symbol. Default is 0.1 seconds.

### Start and stopping a throbber animation
To start the animation, call the `start` method on the throbber object.  
To stop the animation, call the `stop` method on the same object.

### Example

```python
from loadpy import Throbber

throbber = loadpy.Throbber(desc="Loading", end="Done!", timeout=0.2)

throbber.start()
time.sleep(4)
throbber.stop()
```
This example generates the animation above. - time.sleep represents a process that takes 4 seconds to complete.


## Loading Bar
<p align="center">
    <img src="images/loadingBar.gif" alt="Throbber">
</p>

### Parameters

The loading bar is used for processes that have repeating steps and thus the percent of currently finished steps can be displayed. It constructor has 2 parameters:
1. `total` : The total number of steps that are to be completed.
2. `desc`: The description of the process that is being run.

### Updating the loading bar
The loading Bar will be initially printed to the console as soon as the object is instantiated. To update the loading bar, call the `load` method on the object and pass the current value ir step of the process.

### Example

```python
from loadpy import LoadingBar

steps = range(100)
total_steps = len(steps)

loadingBar = loadpy.LoadingBar(total_steps, desc="Loading")

for i in steps:
    loadingBar.load(i)
    time.sleep(0.1)
```
This example generates the animation above. - time.sleep is used here, so the bar isn't instantly finished.

### Usage & Tips
The idea is, that if a loop is used that will take a while, the bar can be displayed on how far the process has come. 
- If the running variable of the loop is a increasing number like above (i), the loading bar can be updated with the current value of i and should be initialized with the total number of i.
- If the running variable is a list of items, the loading bar can be updated with the index of the item in the list and should be initialized with the length of the list.
- Generally: As long as we know the number of steps / length of the process, the loading bar can be used.
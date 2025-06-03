
# COPYRIGHT © 2024 Niklas Max G.
# This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
# More details at: https://github.com/AbUndMax/loadpy/blob/main/LICENSE.md
# For a quick overview, visit https://creativecommons.org/licenses/by-nc/4.0/

"""
This module contains the Throbber and LoadingBar classes for displaying
loading animations in the console. The Throbber class provides a simple
spinner animation, while the LoadingBar class displays a progress bar
indicating the percentage of completion.

author: Niklas Gerbes
github: https://github.com/AbUndMax/loadpy
date: 2025-05-13
"""

import itertools
import threading
import time
import math
import sys


class Throbber:
    """
    A class to display a simple loading animation in the console.
    The animation consists of a spinner that rotates to indicate
    that a process is ongoing.
    The spinner rotates with a specified timeout between frames.
    The animation can be started and stopped using the start() and stop()
    methods, respectively.
    
    Attributes:
        desc (str): The description of the loading process.
        end (str): The message to display when the loading is complete.
        timeout (float): The time in seconds between each frame of the spinner.
    """
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.__running = False
        self.__thread = None


    def start(self):
        """
        Start the loading animation.
        This method creates a new thread to run the animation
        in the background, allowing the main program to continue
        executing while the animation is displayed.
        """
        self.__running = True
        self.__thread = threading.Thread(target=self.__animate)
        self.__thread.start()


    def __animate(self):
        """
        The main animation loop that runs in a separate thread.
        This method displays a rotating spinner in the console
        to indicate that a process is ongoing. The spinner
        rotates continuously until the animation is stopped or interrupted.
        """
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if not self.__running:
                break
            sys.stdout.write(f'\r{self.desc} {c}')
            sys.stdout.flush()
            time.sleep(self.timeout)
        
        
    def __print_end(self, end):
        """
        Print the end message and clear the spinner from the console.
        This method is called when the animation is stopped or
        interrupted. It clears the spinner and prints the end message
        to indicate that the loading process is complete.
        """
        sys.stdout.write('\r' + ' ' * (len(self.desc) + 2))
        sys.stdout.write(f'\r{end}\n')
        sys.stdout.flush()
        
        
    def __end_and_join_thread(self):
        """
        End the animation and wait for the thread to finish.
        This method is called when the animation is stopped or interrupted.
        It ensures that the thread is properly terminated and cleaned up.
        """
        self.__running = False
        if self.__thread is not None:
            self.__thread.join()
        

    def stop(self):
        """
        Stop the loading animation.
        This method sets the running flag to False, which causes
        the animation thread to exit. It also waits for the thread
        to finish before returning.
        """
        self.__end_and_join_thread()
        self.__print_end(self.end)
            
            
    def interupt(self, interrupt_message):
        """
        Interrupt the loading animation.
        This method is an alias for stop() and can be used to
        stop the animation and printout a interrupt message.
        """
        self.__end_and_join_thread()
        self.__print_end(interrupt_message)


class LoadingBar:
    """
    A class to display a loading bar in the console.
    The loading bar updates dynamically as the progress changes.
    It shows the percentage of completion and a visual representation
    of the progress.
    The loading bar is displayed in the format:
    [ ## 12 -- -- -- -- -- -- -- -- ] % finished
    
    Attributes:
        total (int): The total number of steps in the loading process.
        desc (str): The description of the loading process.
        current (int): The current progress value.
    """
    
    __bar_end = "] % finished"

    def __init__(self, total, desc="Loading"):
        self.total = total - 1
        self.__finished = False
        self.__bar_start = desc + ": ["
        self.__percent = -1
        self.current = 0
        self.__percent = 0
        self.load(0)


    def load(self, current):
        """
        Update the loading bar with the current progress.
        The current progress is represented as a percentage of the total.
        The loading bar is displayed in the console, and it updates
        dynamically as the progress changes.

        Args:
            current (int): The current progress value, which should be between 0 and total.
        """
        self.current = current
        current_percent = int(current / self.total * 100)

        if self.__percent < current_percent < 100:
            self.__percent = current_percent
            self.__print_bar(current_percent)

        elif not self.__finished and current_percent == 100:
            self.__print_bar(100, final=True)

        else:
            return
        
        
    def update(self):
        """
        Update the loading bar by incrementing the current progress by 1.
        This method is useful for tracking progress in a loop or iterative process.
        """
        self.current += 1
        self.load(self.current)
        

    def __print_bar(self, current_percent, final=False):
        current_percent_string = f" {current_percent:02.0f}"
        repetitions = int(math.floor(math.floor(current_percent) / 10.0))

        bar = self.__bar_start
        bar = bar + " ##" * (repetitions if repetitions < 9 else 9) + current_percent_string
        bar += " --" * (10 - repetitions - 1) + ("" if current_percent >= 100 else " ") + self.__bar_end

        if final:
            self.__finished = True
            sys.stdout.write(f'\r{bar}\n\n')
        else:
            sys.stdout.write(f'\r{bar}')

        sys.stdout.flush()
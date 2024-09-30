
# COPYRIGHT © 2024 Niklas Max G.
# This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
# More details at: https://github.com/AbUndMax/loadpy/blob/main/LICENSE.md
# For a quick overview, visit https://creativecommons.org/licenses/by-nc/4.0/


import itertools
import threading
import time
import math
import sys


class Throbber:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.__running = False
        self.__thread = None

    def start(self):
        self.__running = True
        self.__thread = threading.Thread(target=self.__animate)
        self.__thread.start()

    def __animate(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if not self.__running:
                break
            sys.stdout.write(f'\r{self.desc} {c}')
            sys.stdout.flush()
            time.sleep(self.timeout)
        sys.stdout.write('\r' + ' ' * (len(self.desc) + 2))
        sys.stdout.write(f'\r{self.end}\n')
        sys.stdout.flush()

    def stop(self):
        self.__running = False
        if self.__thread is not None:
            self.__thread.join()


class LoadingBar:
    __bar_end = "] % finished"

    def __init__(self, total, desc="Loading"):
        self.total = total - 1
        self.__finished = False
        self.__bar_start = desc + ": ["
        self.__percent = -1
        self.load(0)
        self.__percent = 0

    def load(self, current):
        current_percent = int(current / self.total * 100)

        if self.__percent < current_percent < 100:
            self.__percent = current_percent
            self.__print_bar(current_percent)

        elif not self.__finished and current_percent == 100:
            self.__print_bar(100, final=True)

        else:
            return

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

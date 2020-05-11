import cmd
from typing import Optional, List
from stats_computers import GreaterLessBetweenStats


DEFAULT_STATS_COMPUTER = GreaterLessBetweenStats


class DataCapture:
    def __init__(self, stats_computer: Optional["stats_computers.StatsBase"] = None):
        self._stats_computer = stats_computer or DEFAULT_STATS_COMPUTER()

    def add(self, val: int):
        self._stats_computer.add(val)

    def get_data(self):
        return self._stats_computer.get_data()

    def build_stats(self):
        return self._stats_computer.calculate()


class DataCaptureShell(cmd.Cmd):
    """Simple shell for entering data and asing questions"""

    intro = 'Welcome to the Stats shell. Type help or ? to list commands. To exit type: quit.\n'
    prompt = '(stats) '
    capture = DataCapture()
    stats = None


    def do_add(self, val):
        'Add a value to dataset.'
        self.capture.add(int(val))

    def do_reset(self, arg):
        'Reset the data collector.'
        self.capture = DataCapture()
        self.stats = None

    def do_list(self, arg):
        'List values currently stored.'
        print(self.capture.get_data())

    def do_calc(self, arg):
        'Calculate stats on collected data.'
        self.stats = self.capture.build_stats()

    def do_gt(self, arg):
        'Display the number of values greater than X.' 
        if not self.stats:
            print('Please run calc before asking questions.')
        else:
            print(self.stats.greater(int(arg)))

    def do_greater(self, arg):
       'Display the number of values greater than X.' 
       return self.do_gt(arg)

    def do_lt(self, arg):
        'Display the number of values less than X.'
        if not self.stats:
            print('Please run calc before asking questions.')
        else:
            print(self.stats.less(int(arg)))

    def do_less(self, arg):
        'Display the number of values less than X.'
        return self.do_lt(arg)
    
    def do_btw(self, args):
        """Display the number of values betwen a low and high value.
        
        Ex: btw 3 6 
        """
        if not self.stats:
            print('Please run calc before asking questions.')
        else:
            low, high = args.split(" ")
            print(self.stats.between(int(low), int(high)))

    def do_quit(self, arg):
        'Close the stats window, and exit:  BYE'
        print('Thank you for using Stats')
        return True

    def do_exit(self, arg):
        'Close the stats window, and exit:  BYE'
        return self.do_quit(arg)

if __name__ == '__main__':
    DataCaptureShell().cmdloop()

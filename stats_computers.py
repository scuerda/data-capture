from abc import ABC, abstractmethod
from collections import Counter, namedtuple
from typing import Optional, List


class StatsBase(ABC):
    """Base class for a stats engine class.
    
    Defines two expected methods for adding data
    """

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


GreaterLess = namedtuple("GreaterLess", ["less", "greater"])


class GreaterLessBetweenStats(StatsBase):
    """Stats Computer which offers methods for determing counts of data 
    elements less than, greater than and between arbitrary values
    
    """

    def __init__(self):
        self.data = []
        self.value_counts = Counter()
        self.summary_stats = dict()
        self.min = 0
        self.max = 0
        self.count = 0

    def get_data(self):
        return self.data

    def _update_min_max(self, data_point: int):
        """Manage setting min and max when we add a new data point to the tracked dataset
        
        The min and max values of the stored data are used for generating the range of dict keys that
        allow answering the less than, greater than, and between queries.
        """
        if self.min == 0 and self.max == 0:
            self.min = data_point
            self.max = data_point
        else:
            if data_point < self.min:
                self.min = data_point
            elif data_point > self.max:
                self.max = data_point

    def add(self, data_point: int):
        """Add a new data point to the tracked dataset.

        When we add a new data point, we need to execute the following steps:
            1) Check if we should update the known min or max
            2) Update the count of seen data points
            3) Update our internal counter, which tracks the number of times a given value has been added
            4) Store the value in original insert order (probably YAGNI, but maybe?)

        We do some of these checks and booking keeping on the add step in order to minimize the work
        to be done during the calculation of the summary data set.
        """

        # update min/mix
        self._update_min_max(data_point)

        # update count of values
        self.value_counts[data_point] += 1

        # update count of items seen
        self.count += 1

        # add store value in case we want to use the original values in some future calculation
        self.data.append(data_point)

    def calculate(self):
        """Generate a dictionary which allows us to answer the less than, greater than, and between questions.

        We start knowing that the inital possible maximum number of values less than any arbitrary value is 0 and that
        the initial possible maximium number of values greater than an any arbitrary value is the count of values seen
        so far.

        We then iterate over the range of possible values within the min and max seen values and calculate a moving window
        of values that are less than or greater than any value within that range.

        On each iteration we check to see the number of times that value has been added to the dataset (0 or more).
        We subtract that count from the possible values greater than the current value and increase the count of possible
        values less than the current values. We store these intermediate values in a dictionary which allows us to 
        answer the questions in O(1) time complexity.

        """
        current_less = 0
        current_greater = self.count
        for i in range(self.min, self.max + 1):
            v_at_i = self.value_counts[i]
            current_greater -= v_at_i
            self.summary_stats[i] = GreaterLess(less=current_less, greater=current_greater)
            current_less += v_at_i
        return self

    def less(self, less_than: int) -> int:
        """Answer the question: How many values are less than X?

        Since we have the min and max known values, if the the submitted value is less than our
        known minimum, we know the answer is 0 without checking our dictionary. Similarly, if the
        submitted value is greater than the max, all seen values will be less and so we return the count
        of seen values. Otherwise we check our dictionary.
        """
        if less_than <= self.min:
            return 0
        elif less_than > self.max:
            return self.count
        else:
            return self.summary_stats[less_than].less

    def greater(self, greater_than: int) -> int:
        """Answer the question: How many values are greater than X?

        Since we have the min and max known values, if the the submitted value is greater than our
        known maximum, we know that 0 seen values are greater without checking our dictionary. Similarly, if the
        submitted value is less than the known minimum, all seen values will be greater than the submitted value 
        and so we return the count of seen values. Otherwise we check our dictionary.
        """
        if greater_than >= self.max:
            return 0
        elif greater_than < self.min:
            return self.count
        else:
            return self.summary_stats[greater_than].greater

    def between(self, low: int, high: int) -> int:
        """Answer the question: How many values are between X and Y?
        
        We can resuse the existin less and greater methods and the stored count
        """
        return self.count - self.less(low) - self.greater(high)

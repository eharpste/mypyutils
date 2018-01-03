from concept_formation.continuous_value import ContinuousValue
import math

class ExtendedCV(ContinuousValue):

    def __init__(self,bin_size=None):
        self.min = math.inf
        self.max = -math.inf
        self.bin_size = bin_size
        self.bins={}
        self.total = 0
        super(ExtendedCV, self).__init__()

    def range(self):
        return self.max - self.min

    def standard_error(self):
        if self.num == 0:
            return float('nan')
        return self.biased_std() / math.sqrt(self.num)

    def update(self,x):
        if math.isnan(x):
            raise ValueError
        if x < self.min:
            self.min = x
        if x > self.max:
            self.max = x
        self.total += x
        if self.bin_size is not None:
            xv = round(x / self.bin_size) * self.bin_size
            if xv not in self.bins:
                self.bins[xv] = 0
            self.bins[xv] += 1
        super(ExtendedCV, self).update(x)

    def combine(self,other):
        if other.min < self.min:
            self.min = other.min
        if other.max > self.max:
            self.max = other.max
        self.total += other.total
        if self.bin_size == other.bin_size:
            for k in other.bins:
                if k not in self.bins:
                    self.bins[k] = 0
                self.bins[k] += other.bins[k]
        else:
            raise ValueError("Can't combine two ExtendedCVs with different bin_sizes.")
        super(ExtendedCV, self).combine(other)

    def output_json(self):
        if self.bin_size is None:
            return {
                'mean':self.unbiased_mean(),
                'std':self.unbiased_std(),
                'n':self.num,
                'min':self.min,
                'max':self.max
            }
        else:
            return {
                'mean':self.unbiased_mean(),
                'std':self.unbiased_std(),
                'n':self.num,
                'min':self.min,
                'max':self.max,
                'bins':self.bins
            }

    def __repr__(self):
        """
        The textual representation of a continuous value."
        """
        return "%0.4f (%0.4f) [%i,%i] <%i>" % (self.unbiased_mean(), self.unbiased_std(), self.min,self.max, self.num)

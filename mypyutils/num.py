from concept_formation.continuous_value import ContinuousValue
import math


class ExtendedCV(ContinuousValue):

    def __init__(self, bin_size=None):
        self.min = math.inf
        self.max = -math.inf
        self.bin_size = bin_size
        self.bins = {}
        self.total = 0
        super(ExtendedCV, self).__init__()

    def range(self):
        return self.max - self.min

    def standard_error(self):
        if self.num == 0:
            return float('nan')
        return self.biased_std() / math.sqrt(self.num)

    def update(self, x):
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

    def combine(self, other):
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
            raise ValueError("Can't combine two ExtendedCVs with different"
                             "bin_sizes.")
        super(ExtendedCV, self).combine(other)

    def median_bin(self):
        if self.bin_size is None or self.num == 0:
            return float('nan')
        else:
            count = 0
            keys = [k for k in self.bins]
            keys.sort()
            for i, k in enumerate(keys):
                if self.num // 2 - count > self.bins[k]:
                    count += self.bins[k]
                elif self.num // 2 - count <= self.bins[k]:
                    return k

    def output_json(self):
        if self.bin_size is None:
            return {
                'mean': self.unbiased_mean(),
                'std': self.unbiased_std(),
                'n': self.num,
                'min': self.min,
                'max': self.max
            }
        else:
            return {
                'mean': self.unbiased_mean(),
                'std': self.unbiased_std(),
                'n': self.num,
                'min': self.min,
                'max': self.max,
                'bins': self.bins
            }

    def __repr__(self):
        """
        The textual representation of a continuous value."
        """
        if isinstance(self.min, int) and isinstance(self.max, int):
            return "%0.4f (%0.4f) [%i,%i] <%i>" % (self.unbiased_mean(),
                                                   self.unbiased_std(),
                                                   self.min, self.max,
                                                   self.num)
        else:
            return "%0.4f (%0.4f) [%f,%f] <%i>" % (self.unbiased_mean(),
                                                   self.unbiased_std(),
                                                   self.min, self.max,
                                                   self.num)


class Frequencies:

    def __init__(self, lis=None):
        self.freqs = {}
        self.n = 0

        if lis is not None and isinstance(lis, list):
            for v in lis:
                self.update(v)

    def keys(self, min_n=-1):
        return {k for k in self.freqs if self.freqs[k] > min_n}

    def inc(self, item):
        if item not in self.freqs:
            self.freqs[item] = 0
        self.freqs[item] += 1
        self.n += 1

    def dec(self, item):
        if item not in self.freqs:
            return
        self.freqs[item] -= 1
        if self.freqs[item] == 0:
            self.freqs.pop(item)
        self.n -= 1

    def freq(self, key):
        if key in self.freqs:
            return self.freqs[key]
        else:
            return 0

    def update(self, item, inc=True):
        if inc:
            self.inc(item)
        else:
            self.dec(item)

    def batch_update(self, collection, inc=True):
        for c in collection:
            self.update(c, inc)

    def output_json(self, percent=False):
        if percent:
            return self.percentages()
        else:
            return self.counts()

    def counts(self):
        return {k: self.freqs[k] for k in self.freqs}

    def percentages(self):
        return {k: self.freqs[k] / self.n * 100 for k in self.freqs}

    def ranked_count(self):
        ret = [(self.freqs[k], k) for k in self.freqs]
        ret.sort(reverse=True)
        return ret


def map_val(val, in_min, in_max, out_min, out_max):
    """
    Function based on the map function for the arduino
    https://www.arduino.cc/reference/en/language/functions/math/map/
    """
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

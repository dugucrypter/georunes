from matplotlib.ticker import LogFormatter


class LogStandardFormatter(LogFormatter):
    def __init__(self, max_num=1000000, min_num=0.001,
                 **kwargs
                 ):
        self.max_num = max_num
        self.min_num = min_num
        LogFormatter.__init__(self, **kwargs)


    def _num_to_string(self, x, vmin, vmax):
        if x > self.max_num:
            s = '%1.0e' % x
        elif x < self.min_num:
            s = '%1.0e' % x
        else:
            s = self._pprint_val(x, vmax - vmin)
        return s

    def _pprint_val(self, x, d):
        # If the number is not too big and it's an int, format it as an int.
        if abs(x) < self.max_num and x == int(x):
            return '%d' % x
        fmt = ('%1.3e' if d < 1e-2 else
               '%1.3f' if d <= 1 else
               '%1.2f' if d <= 10 else
               '%1.1f' if d <= 1e5 else
               '%1.1e')
        s = fmt % x
        tup = s.split('e')
        if len(tup) == 2:
            mantissa = tup[0].rstrip('0').rstrip('.')
            exponent = int(tup[1])
            if exponent:
                s = '%se%d' % (mantissa, exponent)
            else:
                s = mantissa
        else:
            s = s.rstrip('0').rstrip('.')
        return s

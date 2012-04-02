#!/usr/local/python2.7/bin/python
# -*- coding: UTF-8 -*-


def firstn(n):
        """Build and return a list"""

        num, nums = 0, []

        while num < n:
                nums.append(num)
                num += 1
        return nums


class firstn2(object):
        """Using the generator pattern (an iterable)"""

        def __init__(self, n):
                self.n = n
                self.num, self.nums = 0, []

        def __iter__(self):
                return self

        def next(self):
                if self.num < self.n:
                        cur, self.num = self.num, self.num + 1
                        return cur
                else:
                        raise StopIteration()


def firstn3(n):
        """ a generator that yields items instead of returning a list"""

        num = 0
        while num < n:
                yield num
                num += 1


if __name__ == '__main__':
        """
        sum_of_first_n = sum (firstn(1000000))
        print sum_of_first_n
        """

        """
        sum_of_first_n = sum (firstn2(1000000))
        print sum_of_first_n
        """

        sum_of_first_n = sum(firstn3(1000000))
        print sum_of_first_n

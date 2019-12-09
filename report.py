#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
# from __future__ import print_function
import functools
from random import randint, seed
from time import perf_counter


def BubbleSort(array):
    # array に対し破壊的
    for i in range(len(array) - 1):
        for j in reversed(range(i, len(array) - 1)):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]

    return array


def QuickSort(array, start=0, end=None):  # array[start:end]でありarray[end]は含まない
    # array に対し破壊的
    end = len(array) if end is None else end
    if end - start == 1:
        return array
    assert 0 <= start
    assert start < end - 1
    assert end - 1 < len(array)

    pivot = find_pivot(array, start, end)
    if pivot is None:
        return array

    partision_index = partition(array, pivot, start, end)

    # listをと分けて後で結合させると,分ける際新しくlistが作られメモリを消費するので,使わない
    QuickSort(array, start, partision_index)
    QuickSort(array, partision_index, end)
    return array


def find_pivot(array, start=0, end=None):
    # array に対し破壊的
    end = len(array) if end is None else end
    assert 0 <= start
    assert start < end - 1
    assert end - 1 < len(array)

    first = array[start]
    for i in range(start + 1, end):  # sliceを使い array[1:] とすると,新しくlistが作られメモリを消費するので,使わない
        if first != array[i]:
            return first if first > array[i] else array[i]

    return None


def partition(array, pivot, start=0, end=None):
    # arrayに対し破壊的
    end = len(array) if end is None else end
    assert 0 <= start
    assert start < end - 1
    assert end - 1 < len(array)

    left_index, right_index = start, end - 1

    while True:
        while array[left_index] < pivot:
            left_index += 1
        while array[right_index] >= pivot:
            right_index -= 1
        if left_index > right_index:
            return left_index
        array[left_index], array[right_index] = array[right_index], array[left_index]


def MergeSort(array):
    # array に対し非破壊的
    if len(array) == 1:
        return array

    left = MergeSort(array[:len(array)//2])
    right = MergeSort(array[len(array)//2:])
    return merge(left, right)


def merge(left, right):
    integration = []
    left_index, right_index = 0, 0
    while True:
        if left_index == len(left):
            integration.extend(right[right_index:])
            break
        elif right_index == len(right):
            integration.extend(left[left_index:])
            break

        if left[left_index] < right[right_index]:
            integration.append(left[left_index])
            left_index += 1
        else:
            integration.append(right[right_index])
            right_index += 1
    return integration


def time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        return end - start
    return wrapper


def main():
    seed(0)

    for n in [100, 500, 1000]:
        cum_times = {
            "BubbleSort": 0,
            "QuickSort": 0,
            "MergeSort": 0
        }
        for _ in range(10):
            array = [randint(-n, n) for _ in range(n)]  # randint(a, b) は a <= n <= b を満たす乱数を生成する

            cum_times["BubbleSort"] += time(BubbleSort)(array[:])
            cum_times["QuickSort"] += time(QuickSort)(array[:])
            cum_times["MergeSort"] += time(MergeSort)(array[:])

        print("\nn={}".format(n))
        print("BubbleSort: {:.3e}[ms]".format(cum_times["BubbleSort"]))
        print("QuickSort: {:.3e}[ms]".format(cum_times["QuickSort"]))
        print("MergeSort: {:.3e}[ms]".format(cum_times["MergeSort"]))


if __name__ == "__main__":
    main()

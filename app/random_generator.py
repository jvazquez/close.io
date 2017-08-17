'''
Created on Aug 15, 2017

@author: jvazquez
@todo Queue max size is lower than the random words
'''
from multiprocessing import Queue, Process, cpu_count, current_process
from os import getpid
import random

import urllib.request


def obtain_random_words(word_site, queue):
    myself = current_process().name
    mypid = getpid()
    print("({}) {} starting".format(mypid, myself))
    with urllib.request.urlopen(word_site) as response:
        response = response.read()
    queue.put(response.splitlines()[:100])
    print("({}) {} leaving".format(mypid, myself))


def obtain_random_numbers(queue):
    myself = current_process().name
    mypid = getpid()
    print("({}) {} starting".format(mypid, myself))
    queue.put(random.sample(range(1, 1000), 100))
    print("({}) {} leaving".format(mypid, myself))


def randomizer():
    queue = Queue()
    word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co"
    process_list = [Process(target=obtain_random_words,
                            args=(word_site, queue,)),
                    Process(target=obtain_random_numbers,
                            args=(queue,))]
    for process in process_list:
        process.start()

    for process in process_list:
        process.join()

    mixed_list = [queue.get() for _p in process_list]
    salad = mixed_list[0] + mixed_list[1]
    random.shuffle(salad)
    return salad


if __name__ == "__main__":
    salad = randomizer()
    with open("salad.txt", "w") as target:
        target.write(",".join(salad))

    print("Random list is ready")

'''
Created on Aug 15, 2017

@author: jvazquez
@todo Queue max size is lower than the random words
'''
from multiprocessing import Queue, Process
import random

import urllib.request


def obtain_random_words(word_site, queue):
    with urllib.request.urlopen(word_site) as response:
        response = response.read()
    words = response.splitlines()
    random.shuffle(words)
    queue.put(words[:100])


def obtain_random_numbers(queue):
    queue.put(random.sample(range(1, 1000), 100))


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
    words = list(map(lambda element: str(element, "utf-8"),
                     mixed_list[1]))
    salad = mixed_list[0] + words
    random.shuffle(salad)
    return salad


if __name__ == "__main__":
    salad = randomizer()
    with open("salad.txt", "w") as target:
        target.write(",".join(map(str, salad)))

    print("Random list is ready")

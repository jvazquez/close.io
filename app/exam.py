'''
Created on Aug 17, 2017

@author: jvazquez
'''
if __name__ == "__main__":
    with open("salad.txt", "r") as content:
        stuff = content.readline().split(",")

    for something in filter(lambda data: isinstance(data[1], int) and data[1] % 2 != 0 or
                            data[0] % 2 == 0,
                            enumerate(stuff)):
        print (something)

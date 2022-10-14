"""
Write a multithreaded program that creates packets from a message. The program shall read a message
of no more than 255 characters (terminated by a newline character) from the standard input and shall
use threads to create packets from the input as described following:
a. The program shall have a buffer of size 12 bytes.
b. The program shall create three thread namely thread #1, thread #2, and thread #3.
c. Thread #1 shall run to transfer characters from the input string into the buffer
d. Thread #2 shall convert all the characters in the buffer to upper case
e. Thread #3 shall create packages from the contents of the buffer.
f. Each packet shall have the following values separated by colons
i. A two digit packet number. First packet is 0
ii. A count (two digits) of the number of characters in the message portion of the packet.
iii. The message
"""

import threading
import time
import sys


# the project should use the producer consumer model

# buffer class that will be used to store the message from the user input
# the buffer will have a capacity of 12 bytes
class Buffer:
    def __init__(self):
        self.buffer = []
        self.capacity = 12
        self.lock = threading.Lock()

    def add(self, item):
        self.buffer.append(item)

    def remove(self):
        return self.buffer.pop(0)

    def is_full(self):
        return len(self.buffer) == self.capacity

    def is_empty(self):
        return len(self.buffer) == 0

    def __str__(self):
        return str(self.buffer)

    def __repr__(self):
        return str(self.buffer)

    def __len__(self):
        return len(self.buffer)

    def __getitem__(self, index):
        return self.buffer[index]

    def __setitem__(self, index, value):
        self.buffer[index] = value

    def __delitem__(self, index):
        del self.buffer[index]

    def __iter__(self):
        return iter(self.buffer)

    def __contains__(self, item):
        return item in self.buffer

    def __add__(self, other):
        return self.buffer + other.buffer


# The Packet class is a class that represents a packet. It has two attributes: packet_number and message. It has two
# special functions: __str__ and __repr__.
class Packet:
    def __init__(self, packet_number, message):
        """
        This function takes in a packet number and a message and assigns them to the packet number and message attributes of
        the object.

        :param packet_number: The number of the packet
        :param message: The message to be sent
        """
        self.packet_number = packet_number
        self.message = message

    def __str__(self):
        """
        The function takes a packet object and returns a string representation of the packet
        :return: The packet number, the length of the message, and the message itself.
        """
        return f"{self.packet_number:02d}:{len(self.message):02d}:{self.message}"

    def __repr__(self):
        """
        The __repr__ function is a special function that is called when you print an object
        :return: The string representation of the object
        """
        return self.__str__()


# the thread one class will be used to transfer characters from the input string into the buffer and implement
# the producer consumer model with synchronization and mutual exclusion
class ThreadOne(threading.Thread):
    def __init__(self, buffer, message):
        threading.Thread.__init__(self)
        self.buffer = buffer
        self.message = message

    def run(self):

        # loop through the message and add each character to the buffer
        # implement error handling for the buffer being full and the message being too long to fit in the buffer at once
        for character in self.message:
            # acquire the lock
            self.buffer.lock.acquire()
            # check if the buffer is full
            while self.buffer.is_full():
                # if the buffer is full, release the lock and wait for the buffer to be empty
                print("Thread 1: Buffer is full. Waiting for thread 2 to empty the buffer \n")
                self.buffer.lock.release()
                time.sleep(1)
                # self.buffer.lock.acquire()

            self.buffer.add(character)
            # release the lock
            self.buffer.lock.release()
            # sleep for 0.5 seconds
            print(f"Thread 1: {self.buffer} \n")
            time.sleep(1)


# the thread two class will be used to remove each character from the buffer and convert it to uppercase and add it
# back to the buffer it will also implement the producer consumer model with synchronization and mutual exclusion
class ThreadTwo(threading.Thread):
    def __init__(self, buffer):
        threading.Thread.__init__(self)
        self.buffer = buffer

    def run(self):
        # loop through the buffer when the buffer is full then remove all the characters and convert them to upper
        # case and add them back to the buffer and release the lock
        # acquire the lock
        while True:
            self.buffer.lock.acquire()
            # check if the buffer is empty
            if self.buffer.is_empty():
                # if the buffer is empty, release the lock and wait for the buffer to be full
                print("Thread 2: Buffer is empty. Waiting for thread 1 to fill the buffer \n")
                self.buffer.lock.release()
                time.sleep(1)
                # self.buffer.lock.acquire()

            # loop through the buffer and convert all the characters to upper case
            for index in range(len(self.buffer)):
                self.buffer[index] = self.buffer[index].upper()

            # release the lock
            self.buffer.lock.release()
            # sleep for 0.5 seconds
            print(f"Thread 2: {self.buffer} \n")
            time.sleep(1)


# thread three class will be used to create packets from the contents of the buffer
# class should stop when all the packets are created and the buffer is empty
class ThreadThree(threading.Thread):
    def __init__(self, buffer):
        threading.Thread.__init__(self)
        self.buffer = buffer
        self.packet_number = 0

    def run(self):
        # loop through the buffer when the buffer is full then remove all the characters and convert them to upper
        # case and add them back to the buffer and release the lock
        # acquire the lock
        while True:
            self.buffer.lock.acquire()
            # check if the buffer is empty
            if self.buffer.is_empty():
                # if the buffer is empty, release the lock and wait for the buffer to be full
                print("Thread 3: Buffer is empty. Waiting for thread 1 to fill the buffer \n")
                self.buffer.lock.release()
                time.sleep(1)
                # self.buffer.lock.acquire()

            message = ""
            for index in  range(len(self.buffer)):
                message += self.buffer[index]

            packet = Packet(self.packet_number, message)
            self.packet_number += 1

            print(f"Thread 3: {packet} \n")
            self.buffer.lock.release()
            time.sleep(1)





# the main function will be used to get the user input and create the threads
def main():
    message = "HelloWorldIamAdam"
    buffer = Buffer()
    thread_one = ThreadOne(buffer, message)
    thread_two = ThreadTwo(buffer)
    thread_three = ThreadThree(buffer)
    thread_one.start()
    thread_two.start()
    thread_three.start()
    thread_one.join()
    thread_two.join()
    thread_three.join()

    # for packet in thread_three.packets:
    #    print(packet)


if __name__ == "__main__":
    main()

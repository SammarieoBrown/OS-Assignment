import threading
import time
import sys


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


class Packet(object):
    def __init__(self, packet_number, message):
        self.packet_number = packet_number
        self.message = message

    def __str__(self):
        return f"{self.packet_number:02d}:{len(self.message):02d}:{self.message}:"

    def __repr__(self):
        return f"{self.packet_number:02d}:{len(self.message):02d}:{self.message}:"

    def __len__(self):
        return len(self.message)

    def __getitem__(self, index):
        return self.message[index]

    def __setitem__(self, index, value):
        self.message[index] = value

    def __delitem__(self, index):
        del self.message[index]

    def __iter__(self):
        return iter(self.message)

    def __contains__(self, item):
        return item in self.message


class ThreadOne(threading.Thread):
    def __init__(self, buffer, message):
        threading.Thread.__init__(self)
        self.buffer = buffer
        self.message = message

    def run(self):
        """
        The function loops through the message and adds each character to the buffer.

        The function also implements error handling for the buffer being full and the message being too long to fit in the
        buffer at once.

        The function acquires the lock, checks if the buffer is full, and if it is, releases the lock and waits for the
        buffer to be empty.

        The function then adds the character to the buffer, releases the lock, and sleeps for 0.5 seconds.
        """

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


class ThreadTwo(threading.Thread):
    def __init__(self, buffer):
        threading.Thread.__init__(self)
        self.buffer = buffer

    def run(self):
        """
        The function loops through the buffer and converts all the characters to upper case
        """
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


class ThreadThree(threading.Thread):

    def __init__(self, buffer):
        threading.Thread.__init__(self)
        self.buffer = buffer
        self.packet_number = 0
        self.packet = Packet(self.packet_number, "")

    def run(self):
        """
        It checks if the buffer is empty, if it is, it waits for thread 1 to fill it. If it isn't, it adds the buffer's
        contents to the packet until the packet is full, then it prints the packet and starts a new one
        """
        while True:
            self.buffer.lock.acquire()
            if self.buffer.is_empty():
                print("Thread 3: Buffer is empty. Waiting for thread 1 to fill the buffer \n")
                self.buffer.lock.release()
                time.sleep(1)
            else:
                for index in range(len(self.buffer)):
                    self.packet.message += self.buffer.remove()
                    if len(self.packet) == 5:
                        print(f"Thread 3: {self.packet} \n")
                        self.packet_number += 1
                        self.packet = Packet(self.packet_number, "")
                self.buffer.lock.release()
                time.sleep(1)



# the main function will create the buffer, the message, and the threads
def main():
    # create the buffer
    buffer = Buffer()

    # create the message
    message = "HelloWorldIamAdam"

    # create the threads
    thread_one = ThreadOne(buffer, message)
    thread_two = ThreadTwo(buffer)
    thread_three = ThreadThree(buffer)

    # start the threads
    thread_one.start()
    thread_two.start()
    thread_three.start()

    # join the threads
    thread_one.join()
    thread_two.join()
    thread_three.join()


if __name__ == "__main__":
    main()

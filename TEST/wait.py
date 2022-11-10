import MyUtils
import time

def fun():
    while True:
        time.wait(0.6)
        print('0.6')



def main():
    fun()
    while True:
        time.wait(1)
        print('1')

if __name__ == '__main__':
    main()

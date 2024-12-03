import os

def test():
    os.system("start cmd /k python server.py")
    for i in range(3):
        os.system("start cmd /k python client.py")

if __name__ == '__main__':
    test()
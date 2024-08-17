import time


def typewrite(text, *, delay=0.2, end='\n'):
    for letter in text.split(' '):
        print(letter, end=' ', flush=True)
        time.sleep(delay)

    print(end, end='')
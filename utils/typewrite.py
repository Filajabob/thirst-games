import time


def typewrite(text, *, delay=0.3, end='\n'):
    print(text)
    return
    for letter in text.split():
        print(letter, end=' ', flush=True)
        time.sleep(delay)

    print(end, end='')
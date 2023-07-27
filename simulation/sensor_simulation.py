import time
import numpy as np


def main():
    t = 0
    Tm = 0
    Tnm = 0
    M = False

    while True:
        print(np.random.uniform(0, 0.1))
        if t == 0:
            M = True
            Tm = t + 18 + np.random.normal(loc=0.1, scale=0.1) + np.random.normal(loc=0.1, scale=0.1)
        elif t > Tm:
            M = False
            print(M)
            Tnm = t + 22 + np.random.normal(loc=0.1, scale=0.1)
        elif t > Tnm:
            M = True
            Tm = t + 18 + np.random.normal(loc=0.1, scale=0.1) + np.random.normal(loc=0.1, scale=0.1)

        print(M)
        t = t + 1
        print(t)
        print(Tm)
        print(Tnm)

        time.sleep(0.001)


if __name__ == "__main__":
    main()

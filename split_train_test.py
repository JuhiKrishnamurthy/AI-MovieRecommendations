import sys
import random

def main():
    ifile = open(sys.argv[1])
    train_file = open("train.data","w")
    test_file = open("test.data","w")
    thresh = float(sys.argv[2])
    for line in ifile:
        #line = line.rstrip("\r\n")
        p = random.random()
        if (p<thresh):
            train_file.write(line)
        else:
            test_file.write(line)
    
    ifile.close()
    train_file.close()
    test_file.close()
    return
if __name__ == "__main__":
    main()



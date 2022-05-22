import sys
import random

def main():
    nitems = 1682
    test_file = open(sys.argv[1])
    out_file = open("gt.data","w")
    for line in test_file:
        #find the rated items
        # remove one in random.
        # place them at last col
        line = line.rstrip("\r\n")
        line_items = line.split(",")
        rated_items =[ i for i in range(1,nitems+1) if (float(line_items[i]) >0) ]
        if (len(rated_items) == 0):
            continue
        x = random.randrange(0, len(rated_items))
        dropped_item = rated_items[x]
        dropped_rating = line_items[dropped_item]
        line_items[dropped_item] = '0.0'
        line_items.append(str(dropped_item))
        line_items.append(str(dropped_rating))

        outline = ",".join(line_items)
        out_file.write(outline+"\n")

    test_file.close()
    out_file.close()
    return

if __name__ == "__main__":
    main()






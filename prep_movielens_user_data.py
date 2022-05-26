import sys

def main():
    nusers = 943
    nitems = 1682

    ratings_file = open(sys.argv[1])
    user_rating_mat = []
    for u in range(nusers+1):
        user_rating_mat.append([0.0]*(nitems+1))

    for line in ratings_file:
        line = line.rstrip("\r\n")
        if (line == ""):
            continue
        line_items = line.split("\t")
        uid = int(line_items[0])
        item_id = int(line_items[1])
        rating = float(line_items[2])
        
        user_rating_mat[uid][item_id] = rating

    ratings_file.close()
    user_item_data_file = open("u_i_mat.data","w")
    for u in range(nusers):
        u_str = str(u) +"," + ",".join([str(r) for r in user_rating_mat[u]])
        user_item_data_file.write(u_str+"\n")

    user_item_data_file.close()
    return

if __name__ == "__main__":
    main()


    
    

        
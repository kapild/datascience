


def get_bb_grid(ne, sw, num=8):

    ne_tuple = ne.split(",")
    sw_tuple = sw.split(",")
    n_val = float(ne_tuple[0])
    e_val = float(ne_tuple[1])
    s_val = float(sw_tuple[0])
    w_val = float(sw_tuple[1])

    x_delta = (e_val - w_val)/num
    y_delta = (n_val - s_val)/num


    for y_index in range(0, num):
        for x_index in range(0, num):
            yield str(y_index) + "," + str(x_index),  str(s_val + (y_index+1) * y_delta) + "," + str(w_val + (x_index + 1) * x_delta), \
                str(s_val + y_index * y_delta) + "," + str(w_val+x_index * x_delta)

if __name__ == "__main__":
    for bb in get_bb_grid("37.811954,-122.363148", "37.705689,-122.528629"):
        print bb
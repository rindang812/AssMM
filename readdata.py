
def getData (path):
    """
    Input: path to the file.txt
        :param path:

    Output: data
        :return: n, m, M, alpha, beta, T, epsilon, S_u, V_u, confirms, S_o, V_o
    """
    f =open (path, 'r')
    param =[]
    vin =[]
    vout =[]
    line = f.readline()
    while line != "":
        if (line.startswith("//")):
            line = line.replace("// ","")
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            # print (line)
        else:
            line = line.replace('\n', "")
            arr = line.split("\t")
            if (len(arr) == 12):
                param = arr
            if (len(arr) == 7):
                vin.append(arr)
            if (len(arr) == 3):
                vout.append(arr)
        line = f.readline()

    n = int(param[0])
    m = int(param[1])
    M = int(param[3])
    alpha = float(param[4])
    T = int(param[5])
    epsilon = int(param[6])
    beta = int(param[7])

    # Get data form Vin
    S_u =[]
    V_u =[]
    confirms =[]
    for row in vin:
        S_u.append(int(row[1]))
        V_u.append(int(row[2]))
        confirms.append(int(row[3]))
   
   
    # Get data from Vout
    S_o =[]
    V_o =[]
    for row in vout:
        S_o.append(int(row[1]))
        V_o.append(int(row[2]))
  
    return n, m, M, alpha, beta, T, epsilon, S_u, V_u, confirms, S_o, V_o
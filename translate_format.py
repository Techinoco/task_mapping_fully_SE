from moga_taskmapping_bbdlp import *
from data_formatting import rootsinks_filter
from re import findall

PE_HEAD = "100000_0000000_1111__"
SE_HEAD = "100001_00000__"

def translate_format(alu_config, se_config, const_config, file_path):
    """
    translate format of configurations to generate conf. file
    from alu_config, se_config, and const_config.
    pos_alu = ALU(NUM_COLUMN)_(NUM_ROW)
    You must put ALU_config[N], SE_config[N], CONST_config[N] into this function.
    """

    f = open(file_path, 'w')

    dict_instr = {"NOP": "0000",
                  "ADD": "0001",
                  "SUB": "0010",
                  "MULT": "0011",
                  "SL": "0100",
                  "SR": "0101",
                  "SRA": "0110",
                  "SEL": "0111",
                  "CAT": "1000",
                  "NOT": "1001",
                  "AND": "1010",
                  "OR": "1011",
                  "XOR": "1100",
                  "EQL": "1101",
                  "GT": "1110",
                  "LT": "1111"}
    dict_sel = {"S": "000",
                "E": "001",
                "W": "010",
                "DS": "011",
                "SE": "100",
                "SW": "101",
                "CA": "110",
                "CB": "111"}
# CONST_Bはまだ
    dict_se_n = {"ALU": "0000",
                 "S": "0001",
                 "E": "0010",
                 "W": "0011",
                 "DS": "0100",
                 "SE": "0101",
                 "SW": "0110",
                 "CONST": "0111"}
    dict_se_e = {"ALU": "0000",
                 "S": "0001",
                 "E": "0010",
                 "W": "0011",
                 "DS": "0100",
                 "SE": "0101",
                 "SW": "0110",
                 "CONST": "0111"}
    dict_se_w = {"ALU": "0000",
                 "S": "0001",
                 "E": "0010",
                 "W": "0011",
                 "DS": "0100",
                 "SE": "0101",
                 "SW": "0110",
                 "CONST": "0111"}
    dict_se_s = {"ALU": "0000",
                 "N": "0001",
                 "E": "0010",
                 "W": "0011",
                 "DS": "0100",
                 "SE": "0101",
                 "SW": "0110",
                 "CONST": "0111"}
    constants = {"C_0A": "0000_",
                 "C_1A": "0001_",
                 "C_2A": "0010_",
                 "C_3A": "0011_",
                 "C_4A": "0100_",
                 "C_5A": "0101_",
                 "C_6A": "0110_",
                 "C_7A": "0111_",
                 "C_0B": "1000_",
                 "C_1B": "1001_",
                 "C_2B": "1010_",
                 "C_3B": "1011_",
                 "C_4B": "1100_",
                 "C_5B": "1101_",
                 "C_6B": "1110_",
                 "C_7B": "1111_"}
    # constants = {"C_0A": "00000000000000000",
    #              "C_1A": "00000000000000000",
    #              "C_2A": "00000000000000000",
    #              "C_3A": "00000000000000000",
    #              "C_4A": "00000000000000000",
    #              "C_5A": "00000000000000000",
    #              "C_6A": "00000000000000000",
    #              "C_7A": "00000000000000000",
    #              "C_0B": "00000000000000000",
    #              "C_1B": "00000000000000000",
    #              "C_2B": "00000000000000000",
    #              "C_3B": "00000000000000000",
    #              "C_4B": "00000000000000000",
    #              "C_5B": "00000000000000000",
    #              "C_6B": "00000000000000000",
    #              "C_7B": "00000000000000000"}

    ## ALU
    Prv = "100000_0000000_1111__1010_000_111__00000001_000100000000\t//\tError\tPre\tVen\tTion"
    Prv8_0 = "100000_0000000_1111__0000_000_000__00000001_000100000000\t//\tALU8_0\tError\tPre\tVention"
    out = "100000_0000000_1111__0000_000_000__11111111_1111111111\t//\tNOP\n"
    f.write(out)
    for pos_alu in alu_config:
        for_pe = PE_HEAD
        instr = alu_config[pos_alu]["instr"]
        for_pe = for_pe + dict_instr.get(instr) + "_"
        for sourceA in alu_config[pos_alu]:
            if sourceA != "instr" and alu_config[pos_alu][sourceA] == "A":
                break
        for sourceB in alu_config[pos_alu]:
            if sourceB != "instr" and alu_config[pos_alu][sourceB] == "B":
                break
        for_pe = for_pe + dict_sel.get(sourceA) + "_" + dict_sel.get(sourceB) + "_"
        for_pe = for_pe + "_"
        numbers = findall(r'[0-9]+', pos_alu)
        num_column = int(numbers[0])
        if len(numbers) >= 2:
            num_row = int(numbers[1])
        # num_column = int(pos_alu[3:4])
        # num_row = int(pos_alu[5:6])
        for row in range(7, -1, -1):
            if row == num_row:
                for_pe = for_pe + "1"
            else:
                for_pe = for_pe + "0"
        for_pe = for_pe + "_"
        for column in range(11, -1, -1):
            if column == num_column:
                for_pe = for_pe + "1"
            else:
                for_pe = for_pe + "0"
        for_pe = for_pe + "\t//\t" + pos_alu + "\t" + instr + "\t" + sourceA + "\t" + sourceB
        if pos_alu == "ALU8_2":
            for_pe = for_pe[:42] + '1' + for_pe[43:] + "(Error prevention)"
            # print(for_pe)
            # print(Prv)
            # print(Prv8_0)
            f.write(for_pe)
            f.write('\n')
            f.write(Prv)
            f.write('\n')
            f.write(Prv8_0)
            f.write('\n')
        else:
            # print(for_pe)
            f.write(for_pe)
            f.write('\n')
        if pos_alu == "ALU8_0":
            Prv8_0 = for_pe + "(E)"

    # for i, unused_c in enumerate(ALU_usage):
    #     unused_c.reverse()
    #     columns = ['0','0','0','0','0','0','0','0','0','0','0','0']
    #     columns[i] = '1'
    #     out = "100000_0000000_1111__0000_000_000__"
    #     for j, unused_r in enumerate(unused_c):
    #         out = out + unused_r
    #     out = out + '_'
    #     for k, column in enumerate(columns):
    #         out = out + column
    #     out = out + '\n'
    #     f.write(out)

    ## SE
    for pos_se in se_config:
        numbers = findall(r'[0-9]+', pos_se)
        num_column = int(numbers[0])
        if len(numbers) >= 2:
            num_row = int(numbers[1])
        # num_column = int(pos_se[2:3])
        # num_row = int(pos_se[4:5])
        for_se = SE_HEAD

        ## North
        in_to_N = str(se_config[pos_se]["N"])
        if in_to_N[0:1] == "A":
            numbers = findall(r'[0-9]+', in_to_N)
            column_A = int(numbers[0])
            if len(numbers) >= 2:
                row_A = int(numbers[1])
            # column_A = int(in_to_N[3:4])
            # row_A = int(in_to_N[5:6])
            if column_A == num_column and row_A == num_row:
                for_se = for_se + dict_se_n["ALU"] + "_"
            elif column_A == num_column - 1 and row_A == num_row - 1:
                for_se = for_se + dict_se_n["SW"] + "_"
            elif column_A == num_column + 1 and row_A == num_row - 1:
                for_se = for_se + dict_se_n["SE"] + "_"
            elif column_A == num_column and row_A == num_row - 1:
                for_se = for_se + dict_se_n["DS"] + "_"
            else:
                print("invalid ALU position", se_config[pos_se]["N"], "for North port of", pos_se)
                return 0
        elif in_to_N[0:1] == "S":
            numbers = findall(r'[0-9]+', in_to_N)
            column_S = int(numbers[0])
            if len(numbers) >= 2:
                row_S = int(numbers[1])
            # column_S = int(in_to_N[2:3])
            # row_S = int(in_to_N[4:5])
            if column_S == num_column - 1 and row_S == num_row:
                for_se = for_se + dict_se_n["W"] + "_"
            elif column_S == num_column + 1 and row_S == num_row:
                for_se = for_se + dict_se_n["E"] + "_"
            elif column_S == num_column and row_S == num_row - 1:
                for_se = for_se + dict_se_n["S"] + "_"
            else:
                print("invalid SE position", se_config[pos_se]["N"], "for North port of", pos_se)
                return 0
        elif in_to_N[0:1] == "C":
            numbers = findall(r'[0-9]+', in_to_N)
            row_C = int(numbers[0])
            # row_C = int(in_to_N[2:3])
            AorB_C = in_to_N[3:4]
            if row_C == num_row and AorB_C == "A":
                for_se = for_se + dict_se_n["CONST"] + "_"
            else:
                print("invalid CONST position", se_config[pos_se]["N"], "for North port of", pos_se)
                return 0
        elif in_to_N[0:1] == "R":
            for_se = for_se + dict_se_n["S"] + "_"
        else:
            for_se = for_se + dict_se_n["ALU"] + "_"

        ## South
        in_to_S = str(se_config[pos_se]["S"])
        if in_to_S[0:1] == "A":
            numbers = findall(r'[0-9]+', in_to_S)
            column_A = int(numbers[0])
            if len(numbers) >= 2:
                row_A = int(numbers[1])
            # column_A = int(in_to_S[3:4])
            # row_A = int(in_to_S[5:6])
            if column_A == num_column and row_A == num_row:
                for_se = for_se + dict_se_s["ALU"] + "_"
            else:
                print("invalid ALU position", se_config[pos_se]["S"], "for South port of", pos_se)
                return 0
        elif in_to_S[0:1] == "S":
            numbers = findall(r'[0-9]+', in_to_S)
            column_S = int(numbers[0])
            if len(numbers) >= 2:
                row_S = int(numbers[1])
            # column_S = int(in_to_S[2:3])
            # row_S = int(in_to_S[4:5])
            if column_S == num_column and row_S == num_row + 1:
                for_se = for_se + dict_se_s["N"] + "_"
            elif column_S == num_column + 1 and row_S == num_row:
                for_se = for_se + dict_se_s["E"] + "_"
            elif column_S == num_column - 1 and row_S == num_row:
                for_se = for_se + dict_se_s["W"] + "_"
            else:
                print("invalid SE position", se_config[pos_se]["S"], "for South port of", pos_se)
                return 0
        else:
            for_se = for_se + dict_se_s["ALU"] + "_"

        ## East
        in_to_E = str(se_config[pos_se]["E"])
        if in_to_E[0:1] == "A":
            numbers = findall(r'[0-9]+', in_to_E)
            column_A = int(numbers[0])
            if len(numbers) >= 2:
                row_A = int(numbers[1])
            # column_A = int(in_to_E[3:4])
            # row_A = int(in_to_E[5:6])
            if column_A == num_column and row_A == num_row:
                for_se = for_se + dict_se_e["ALU"] + "_"
            elif column_A == num_column and row_A == num_row - 1:
                for_se = for_se + dict_se_e["DS"] + "_"
            elif column_A == num_column + 1 and row_A == num_row - 1:
                for_se = for_se + dict_se_e["SE"] + "_"
            elif column_A == num_column - 1 and row_A == num_row - 1:
                for_se = for_se + dict_se_e["SW"] + "_"
            else:
                print("invalid ALU position", se_config[pos_se]["E"], "for East port of", pos_se)
                return 0
        elif in_to_E[0:1] == "S":
            numbers = findall(r'[0-9]+', in_to_E)
            column_S = int(numbers[0])
            if len(numbers) >= 2:
                row_S = int(numbers[1])
            # column_S = int(in_to_E[2:3])
            # row_S = int(in_to_E[4:5])
            if column_S == num_column and row_S == num_row - 1:
                for_se = for_se + dict_se_e["S"] + "_"
            elif column_S == num_column - 1 and row_S == num_row:
                for_se = for_se + dict_se_e["W"] + "_"
            else:
                print("invalid SE position", se_config[pos_se]["E"], "for East port of", pos_se)
                return 0
        else:
            for_se = for_se + dict_se_e["ALU"] + "_"

        # West
        in_to_W = str(se_config[pos_se]["W"])
        if in_to_W[0:1] == "A":
            numbers = findall(r'[0-9]+', in_to_W)
            column_A = int(numbers[0])
            if len(numbers) >= 2:
                row_A = int(numbers[1])
            # column_A = int(in_to_W[3:4])
            # row_A = int(in_to_W[5:6])
            if column_A == num_column and row_A == num_row - 1:
                for_se = for_se + dict_se_w["DS"] + "_"
            elif column_A == num_column + 1 and row_A == num_row - 1:
                for_se = for_se + dict_se_w["SE"] + "_"
            else:
                print("invalid ALU position", se_config[pos_se]["W"], "for West port of", pos_se)
                return 0
        elif in_to_W[0:1] == "S":
            numbers = findall(r'[0-9]+', in_to_W)
            column_S = int(numbers[0])
            if len(numbers) >= 2:
                row_S = int(numbers[1])
            # column_S = int(in_to_W[2:3])
            # row_S = int(in_to_W[4:5])
            if column_S == num_column and row_S == num_row - 1:
                for_se = for_se + dict_se_w["S"] + "_"
            elif column_S == num_column + 1 and row_S == num_row:
                for_se = for_se + dict_se_w["E"] + "_"
            else:
                print("invalid SE position", se_config[pos_se]["W"], "for West port of", pos_se)
                return 0
        else:
            for_se = for_se + dict_se_w["S"] + "_"

        for_se = for_se + "_"

        for row in range(7, -1, -1):
            if row == num_row:
                for_se = for_se + "1"
            else:
                for_se = for_se + "0"
        for_se = for_se + "_"
        for column in range(11, -1, -1):
            if column == num_column:
                for_se = for_se + "1"
            else:
                for_se = for_se + "0"
        for_se = for_se + "\t//\t" + pos_se + "\t" + "N(" + in_to_N + ")\tS(" + in_to_S + ")\tE(" + in_to_E + ")\tW(" +  in_to_W + ")"
        # print(for_se)
        f.write(for_se)
        f.write('\n')

    ## CONST
    for pos_const in const_config:
        val_const = int(const_config[pos_const])
        if val_const < 0:
            val_const = abs(val_const)
            val_const = (0b11111111111111111 ^ val_const) + 1
        val_const = format(val_const, 'b').zfill(17)
        constants[pos_const] = constants[pos_const] + val_const
    for pos_const in constants:
        if len(constants[pos_const]) == 5:
            constants[pos_const] = constants[pos_const] + "00000000000000000"
            const_config[pos_const] = 0
        for_const = "100010_00_" + constants[pos_const] + "__000000000000000000\t//\t" + pos_const + "\t" + str(const_config[pos_const])
        # print(for_const)
        f.write(for_const)
        f.write('\n')
    f.close()

def generate_manipulater_format(sinks, dmani_path, REG_config):
    """
    """
    roots = []
    for reg in REG_config:
        roots.append(int(reg.split('_')[-1]))
    roots.sort()
    # __,sinks = rootsinks_filter(tasksonly_graph)
    f = open(dmani_path, 'w')
    for root in roots:
        # out = str(hof[root][0]) + " <- \n"
        out = str(root) +  " <- \n"
        f.write(out)
    for sink in sinks:
        out = str(sink[0]) + " -> \n"
        f.write(out)
    f.close()

def format_data_manipulater(path_of_file_for_dmani, path_for_output):
    """
    This func. translates format for data manipulater and inputs.
    Innput file format is following.

    ...

    """

    """
    Define for_LD and for_ST
    """
    for_LD = ["0000", "0000", "0000", "0000", "0000", "0000",
               "0000", "0000", "0000", "0000", "0000", "0000"]
    for_ST = ["0000", "0000", "0000", "0000", "0000", "0000",
              "0000", "0000", "0000", "0000", "0000", "0000"]
    map_LD = [ "0" for i in range(12) ]
    map_ST = [ "0" for i in range(12) ]

    data4LDs = [ [] for i in range(12) ]
    addr4STs = [ [] for i in range(12) ]
    dmem = []
    f = open(path_of_file_for_dmani)
    lines = f.readlines()
    f.close()
    f = open(path_for_output, 'w')

    """
    Understand sentences in the file
    """
    for line in lines:
        print(line[:len(line)-1])
        words = line.split()
        column = words[0]
        if int(column) < 0 or int(column) > 11:
            print("Invalid column number: " + column)
            return
        LD = words[1] == "<-"
        ST = words[1] == "->"
        if LD and not(ST):
            for phaseLD, data in enumerate(words[2:]):
                data4LDs[int(column)].append(data)
        if ST and not(LD):
            for phaseST, memaddr in enumerate(words[2:]):
                addr4STs[int(column)].append(int(memaddr))
    print('\n')

    """
    Put data in memory
    """
    for i in range(phaseLD+1):
        for data4LD in data4LDs:
            if len(data4LD) != 0:
                d_decimal = int(data4LD[i])
                d_original = d_decimal
                if d_original < 0:
                    d_decimal = abs(d_original)
                    d_decimal = (0b1111111111111111111111111 ^ d_decimal) + 1
                d_bynary = format(d_decimal, 'b').zfill(25)
                d_bynary = d_bynary + "\t//\t" + str(d_original)
                dmem.append(d_bynary)
    for i, b_data in enumerate(dmem): # Write data in dmem into output file
        head = format(i, 'b').zfill(12)
        for_write = head + "_" + b_data
        print(for_write)
        f.write(for_write)
        f.write('\n')
    f.write('\n')

    """
    Format for_LD
    """
    daddr = 0
    for column, data4LD in enumerate(data4LDs):
        if len(data4LD) != 0:
            for_LD[column] = format(daddr, 'b').zfill(4)
            map_LD[column] = "1"
            daddr += 1
    for_LD.reverse()
    map_LD.reverse()
    for_write = "001100000010_0" # Write for_LD into output file
    for b_port in for_LD[:6]:
        for_write = for_write + "_" + b_port
    print(for_write)
    f.write(for_write)
    f.write('\n')
    for_write = "001100000001_0"
    for b_port in for_LD[6:]:
        for_write = for_write + "_" + b_port
    print(for_write)
    f.write(for_write)
    f.write('\n')
    for_write = "001100000011_0000000000000_" # Write map_LD into output file
    for b_map in map_LD:
        for_write = for_write + b_map
    print(for_write)
    f.write(for_write)
    f.write('\n')

    """
    Format for_ST
    """
    for column, addr4ST in enumerate(addr4STs):
        if len(addr4ST) != 0:
            for_ST[int(addr4ST[0])] = format(column, 'b').zfill(4)
            map_ST[int(addr4ST[0])] = "1"
            # for_ST[column] = format(addr4ST[0], 'b').zfill(4)
            # map_ST[column] = "1"
    for_ST.reverse()
    map_ST.reverse()
    for_write = "010000000010_0" # Write for_ST into output file
    for b_port in for_ST[:6]:
        for_write = for_write + "_" + b_port
    print(for_write)
    f.write('\n')
    f.write(for_write)
    f.write('\n')
    for_write = "010000000001_0"
    for b_port in for_ST[6:]:
        for_write = for_write + "_" + b_port
    print(for_write)
    f.write(for_write)
    f.write('\n')
    for_write = "010000000011_0000000000000_" # Write map_ST into output file
    for b_map in map_ST:
        for_write = for_write + b_map
    print(for_write)
    f.write(for_write)
    f.write('\n')
    f.write('\n')

    # Write EOF into output file
    for_write = "111111_00_0111_0_00000000_0000000000000111 // EOF"
    f.write(for_write)
    f.write('\n')
    f.write(for_write)
    f.write('\n')
    f.close()


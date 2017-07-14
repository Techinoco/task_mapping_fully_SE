def translate_format(alu_config, se_config, file_path):
    """
    translate format of configurations to generate conf. file
    from alu_config and se_config.
    pos_alu = ALU(NUM_COLUMN)_(NUM_ROW)
    """

    f = open(file_path, 'w')
    
    dict_instr = {"NOP": "0000", "ADD": "0001", "SUB": "0010", "MULT": "0011", "SL": "0100", "SR": "0101", "SRA": "0110", "SEL": "0111", "CAT": "1000", "NOT": "1001", "AND": "1010", "OR": "1011", "XOR": "1100", "EQL": "1101", "GT": "1110", "LT": "1111"}
    dict_sel = {"S": "000", "E": "001", "W": "010", "DS": "011", "SE": "100", "SW": "101", "CL": "110", "CR": "111"}
    dict_se_n = {"ALU": "000", "S": "001", "E": "010", "W": "011", "DS": "100", "SE": "101", "SW": "110", "CONST": 111}
    dict_se_s = {"ALU": "00", "N": "01", "E": "10", "W": "11"}
    dict_se_e = {"ALU": "000", "S": "001", "W": "010", "DS": "011", "SE": "100", "SW": "101"}
    dict_se_w = {"S": "00", "E": "01", "DS": "10", "SE": "11"}

    ## ALU
    for pos_alu in alu_config:
        for_pe = "100000_0000000_1111__"
        for_pe = for_pe + dict_instr.get(alu_config[pos_alu]["instr"]) + "_"
        for direction in alu_config[pos_alu]:
            if direction == "CR" or direction == "CL":
                # if alu_config[pos_alu][direction] is not None:
                if alu_config[pos_alu][direction] != "None":
                    for_pe = for_pe + dict_sel.get(direction) + "_"
            elif direction != "instr":
                if alu_config[pos_alu][direction] == 1:
                    for_pe = for_pe + dict_sel.get(direction) + "_"
            # if direction != "instr" and direction != "CR" and direction != "CL":
            #     if alu_config[pos_alu][direction] == 1:
            #         for_pe = for_pe + dict_sel.get(direction) + "_"
        for_pe = for_pe + "_"
        num_column = pos_alu[3:4]
        num_row = pos_alu[5:6]
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
        print(for_pe)
        f.write(for_pe)
        f.write('\n')

    ## SE
    for pos_se in se_config:
        num_column = int(pos_se[2:3])
        num_row = int(pos_se[4:5])
        for_se = "100001_0000000_0000__"
        
        ## North
        in_to_N = str(se_config[pos_se]["N"])
        if in_to_N[0:1] == "A":
            column_A = int(in_to_N[3:4])
            row_A = int(in_to_N[5:6])
            if column_A == num_column and row_A == num_row:
                for_se = for_se + dict_se_n["ALU"] + "_"
            elif column_A == num_column - 1 and row_A == num_row - 1:
                for_se = for_se + dict_se_n["SW"] + "_"
            elif column_A == num_column + 1 and row_A == num_row - 1:
                for_se = for_se + dict_se_n["SE"] + "_"
            elif column_A == num_column and row_A == num_row - 1:
                for_se = for_se + dict_se_n["DS"] + "_"
            else:
                print("invalid ALU position for North port")
                return 0
        elif in_to_N[0:1] == "S":
            column_S = int(in_to_N[2:3])
            row_S = int(in_to_N[4:5])
            if column_S == num_column - 1 and row_S == num_row:
                for_se = for_se + dict_se_n["W"] + "_"
            elif column_S == num_column + 1 and row_S == num_row:
                for_se = for_se + dict_se_n["E"] + "_"
            elif column_S == num_column and row_S == num_row - 1:
                for_se = for_se + dict_se_n["S"] + "_"
            else:
                print("invalid SE position for North port")
                return 0
        else:
            for_se = for_se + dict_se_n["ALU"] + "_"

        ## South
        in_to_S = str(se_config[pos_se]["S"])
        if in_to_S[0:1] == "A":
            column_A = int(in_to_S[3:4])
            row_A = int(in_to_S[5:6])
            if column_A == num_column and row_A == num_row:
                for_se = for_se + dict_se_s["ALU"] + "_"
            else:
                print("invalid ALU position for South port")
                return 0
        elif in_to_S[0:1] == "S":
            column_S = int(in_to_S[2:3])
            row_S = int(in_to_S[4:5])
            if column_S == num_column and row_S == num_row + 1:
                for_se = for_se + dict_se_s["N"] + "_"
            elif column_S == num_column + 1 and row_S == num_row:
                for_se = for_se + dict_se_s["E"] + "_"
            elif column_S == num_column - 1 and row_S == num_row:
                for_se = for_se + dict_se_s["W"] + "_"
            else:
                print("invalid SE position for South port")
                return 0
        else:
            for_se = for_se + dict_se_s["N"] + "_"

        ## East
        in_to_E = str(se_config[pos_se]["E"])
        if in_to_E[0:1] == "A":
            column_A = int(in_to_E[3:4])
            row_A = int(in_to_E[5:6])
            if column_A == num_column and row_A == num_row:
                for_se = for_se + dict_se_e["ALU"] + "_"
            elif column_A == num_column and row_A == num_row - 1:
                for_se = for_se + dict_se_e["DS"] + "_"
            elif column_A == num_column + 1 and row_A == num_row - 1:
                for_se = for_se + dict_se_e["SE"] + "_"
            elif column_A == num_column - 1 and row_A == num_row - 1:
                for_se = for_se + dict_se_e["SW"] + "_"
            else:
                print("invalid ALU position for East port")
                return 0
        elif in_to_E[0:1] == "S":
            column_S = int(in_to_E[2:3])
            row_S = int(in_to_E[4:5])
            if column_S == num_column and row_S == num_row - 1:
                for_se = for_se + dict_se_e["S"] + "_"
            elif column_S == num_column - 1 and row_S == num_row:
                for_se = for_se + dict_se_e["W"] + "_"
            else:
                print("invalid SE position for East port")
                return 0
        else:
            for_se = for_se + dict_se_e["W"] + "_"

        # West
        in_to_W = str(se_config[pos_se]["W"])
        if in_to_W[0:1] == "A":
            column_A = int(in_to_W[3:4])
            row_A = int(in_to_W[5:6])
            if column_A == num_column and row_A == num_row - 1:
                for_se = for_se + dict_se_w["DS"] + "_"
            elif column_A == num_column + 1 and row_A == num_row - 1:
                for_se = for_se + dict_se_w["SE"] + "_"
            else:
                print("invalid ALU position for West port")
                return 0
        elif in_to_W[0:1] == "S":
            column_S = int(in_to_W[2:3])
            row_S = int(in_to_W[4:5])
            if column_S == num_column and row_S == num_row - 1:
                for_se = for_se + dict_se_w["S"] + "_"
            elif column_S == num_column + 1 and row_S == num_row:
                for_se = for_se + dict_se_w["E"] + "_"
            else:
                print("invalid SE position for West port")
                return 0
        else:
            for_se = for_se + dict_se_w["E"] + "_"

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
        print(for_se)
        f.write(for_se)
        f.write('\n')

    f.close()
        
        




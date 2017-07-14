import load_data
from math import ceil
from optimize_pipeline import *
# from translate_format import *
import translate_format
from data_formatting import generate_map_file
from copy import deepcopy
from re import findall

max_column = 12
confp_path = "Ando/data/bitstreams/confp.dat"
map_path = "Ando/data/test.map"
delay_path = "Ando/data/delay.tbl"
org_path = "Ando/data/data.org"
data_path = "Ando/data/bitstreams/data.dat.test"
dac_path = "Ando/data/bitstreams/dac.conf"
MinMax_path = "Ando/data/MinMax.dat"

__,sinks = rootsinks_filter(tasksonly_graph)
hof_sinks = []
# ALU_usage = [[['1','1','1','1','1','1','1','1'] for i in range(12)] for j in range(len(load_data.hof))] # 1 is unused

def make_sinks():
    for sol in load_data.hof:
        sol_sinks = []
        for sink in sinks:
            sol_sinks.append(sol[sink])
        hof_sinks.append(sol_sinks)

make_sinks()

# def register_NOP():
#     for sol_num,sol in enumerate(load_data.ALU_config):
#         for ALU,v in sol.items():
#             coords = findall(r'[0-9]+', ALU)
#             x = int(coords[0])
#             y = int(coords[1])
#             ALU_usage[sol_num][x][y] = '0'

def generate_confp(hof, tasks, graph, alu_config, se_config, const_config, num_pr, confp_path, map_path, table_path):
    generate_map_file(hof, tasks, graph, map_path)
    read_graph(map_path, table_path)
    pr_pos, sub_graphs, min_max_delay = opt_pipeline(vpcma_graph, num_pr)
    translate_format.translate_format(alu_config, se_config, const_config, confp_path)
    add_pipeline_to_confp(pr_pos, confp_path)
    add_EOF_to_confp(confp_path)
    compress_confp()
    return min_max_delay

def add_EOF_to_confp(confp_path):
    out = "\n11111100_00000000_00000000_00000000_00000000_0000_000\n"
    f = open(confp_path, 'a')
    f.write(out)

def add_pipeline_to_confp(pr_pos, confp_path):
    out = "100110_0000000_1110_000__"
    b_pr_pos = ["0" for i in range(7)]
    for pr in pr_pos:
        b_pr_pos[int(pr)] = "1"
    b_pr_pos.reverse()
    for b_pr in b_pr_pos:
        out = out + b_pr + "_"
    out = out + "00000000_000000000000 // PREG " + ",".join(map(str,pr_pos))
    f = open(confp_path, 'a')
    f.write(out)

def generate_dac(num_pr, data_path, dac_path):
    """
    Generates dac.conf.

    args: num_pr, data_path, dac_path

    num_pr: the number of used pipeline registers.
    data_path: the path to read data.dat, pre-defined in generate_bitstream.py
    dac_path: the path to write dac.conf, pre-defined in generate_bitstream.py
    """
    delay = int(num_pr)
    f = open(data_path)
    lines = f.readlines()
    f.close()
    f = open(dac_path, 'w')
    head_addr_ld = 0x0
    head_addr_st = 0x30
    phase = 0
    num_roots = 0
    num_sinks = 0
    for line in lines:
        words = line.split()
        if words[1] == "<-":
            num_roots += 1
        elif words[1] == "->":
            num_sinks += 1
        tmp_phase = len(words) - 2
        if tmp_phase > phase:
            phase = tmp_phase
    # delay
    b_delay = format(delay, 'b').zfill(4)
    out = "0000_" + b_delay + "_0000_1111\t// 0\t:\tDELAY " + str(delay) + "\n"
    f.write(out)
    # SET_LD
    b_head_addr_ld = format(head_addr_ld, 'b').zfill(8)
    b_num_roots = format(num_roots, 'b').zfill(4)
    out = "1100_" + b_head_addr_ld + "_" + b_num_roots + "\t// 1\t:\tSET_LD #"
    out = out + str(head_addr_ld) + ",#" + str(num_roots) + "\n"
    f.write(out)
    # SET_ST
    b_head_addr_st = format(head_addr_st, 'b').zfill(8)
    b_num_sinks = format(num_sinks, 'b').zfill(4)
    out = "1101_" + b_head_addr_st + "_" + b_num_sinks + "\t// 2\t:\tSET_ST #"
    out = out + str(head_addr_st) + ",#" + str(num_sinks) + "\n"
    f.write(out)
    # LDST_ADD
    for i in range(phase):
        j = i + 3
        out = "0111_0000_0000_0000\t// "
        out = out + str(j) + "\t:\tLDST_ADD #0,#0\n"
        f.write(out)
    # DONE
    j += 1
    out = "0000_0000_0000_1110\t// " + str(j) + "\t:\tDONE\n"
    f.write(out)
    f.close

def duplicate_mapping():
    """
    Duplicates mapping of load_data.ALU_config, load_data.SE_config, and load_data.REG_config with duplicating sinks of hole of fame.

    args: none
    """
    rightests = []
    for i, hof in enumerate(load_data.hof):
        rightest = 0
        for coord in hof:
            if rightest < coord[0]:
                rightest = coord[0]
        rightests.append(rightest)
        geta = rightest + 1
        first_geta = geta
        possibility = int(max_column/geta) - 1
        duplicated_sinks = []
        for j in range(possibility):
            for sink in hof_sinks[i]:
                duplicated_sinks.append(((sink[0]+geta),sink[1]))
            geta = geta + first_geta
        hof_sinks[i].extend(duplicated_sinks)
    for sol_num, ALU_config_hof in enumerate(load_data.ALU_config):
        ALUs = ALU_config_hof.keys()
        geta = rightests[sol_num]
        geta = geta + 1
        first_geta = geta
        possibility = int(max_column/geta) - 1
        # p_poss = "Geta: " + str(geta) + ", Possibility: " + str(possibility)
        # print(p_poss)
        duplicated_ALU_config = {}
        for i in range(possibility):
            # p_out = "Geta : " + str(geta)
            # print(p_out)
            tmp_ALU_config = deepcopy(ALU_config_hof)
            for ALU in ALUs:
                tmp_config = tmp_ALU_config.pop(ALU)
                tmp_coord = findall(r'[0-9]+', ALU)
                # print(ALU)
                # print(tmp_coord)
                tmp_coord[0] = str(int(tmp_coord[0]) + geta)
                tmp_ALU = "ALU" + str(tmp_coord[0]) + "_" + str(tmp_coord[1])
                tmp_ALU_config.update({tmp_ALU:tmp_config})
            duplicated_ALU_config.update(tmp_ALU_config)
            geta = geta + first_geta
        load_data.ALU_config[sol_num].update(duplicated_ALU_config)
    for sol_num, SE_config_hof in enumerate(load_data.SE_config):
        SEs = SE_config_hof.keys()
        geta = rightests[sol_num]
        geta = geta + 1
        first_geta = geta
        possibility = int(max_column/geta) - 1
        # p_poss = "Geta: " + str(geta) + ", Possibility: " + str(possibility)
        # print(p_poss)
        duplicated_SE_config = {}
        for i in range(possibility):
            # p_out = "Geta : " + str(geta)
            # print(p_out)
            tmp_SE_config = deepcopy(SE_config_hof)
            for SE in SEs:
                tmp_config = tmp_SE_config.pop(SE)
                tmp_coord = findall(r'[0-9]+', SE)
                # print(SE)
                # print(tmp_coord)
                tmp_coord[0] = str(int(tmp_coord[0]) + geta)
                tmp_SE = "SE" + str(tmp_coord[0]) + "_" + str(tmp_coord[1])
                for direction,value in tmp_config.items():
                    if (value != 0) and (value[0] != "C"):
                        src_pos = findall(r'[0-9]+', value)
                        src_pos[0] = str(int(src_pos[0]) + geta)
                        if value[0] == "R":
                            tmp_value = "REG_IN_"
                        elif value[0] == "A":
                            tmp_value = "ALU"
                        elif value[0] == "S":
                            tmp_value = "SE"
                        tmp_value = tmp_value + src_pos[0]
                        if len(src_pos) >= 2:
                            tmp_value = tmp_value + "_" + src_pos[1]
                        tmp_config[direction] = tmp_value
                tmp_SE_config.update({tmp_SE:tmp_config})
            duplicated_SE_config.update(tmp_SE_config)
            geta = geta + first_geta
        load_data.SE_config[sol_num].update(duplicated_SE_config)
    for sol_num, REG_config_hof in enumerate(load_data.REG_config):
        REGs = REG_config_hof.keys()
        geta = rightests[sol_num]
        geta = geta + 1
        first_geta = geta
        possibility = int(max_column/geta) - 1
        duplicated_REG_config = {}
        for i in range(possibility):
            # p_out = "Geta : " + str(geta)
            # print(p_out)
            tmp_REG_config = deepcopy(REG_config_hof)
            for REG in REGs:
                tmp_value = tmp_REG_config.pop(REG)
                tmp_coord = findall(r'[0-9]+', REG)
                # print(SE)
                # print(tmp_coord)
                tmp_coord[0] = str(int(tmp_coord[0]) + geta)
                tmp_REG = "REG_IN_" + str(tmp_coord[0])
                tmp_value_num = findall(r'[0-9]+', tmp_value)
                tmp_value_num[0] = str(int(tmp_value_num[0]) + geta)
                tmp_value = "REG_IN_VAL_" + tmp_value_num[0]
                tmp_REG_config.update({tmp_REG:tmp_value}) #
            duplicated_REG_config.update(tmp_REG_config)
            geta = geta + first_geta
        load_data.REG_config[sol_num].update(duplicated_REG_config)

def generate(sol_num, num_pr):
    """
    Generates all of files for configurations, confp.dat, data.dat, and dac.conf.
    Through filling blanks of data.org, data.dat will be generated.

    args: sol_num, num_pr

    sol_num: solution number of hole of fame (hof).
    num_pr: the number of used pipeline registers.
    """
    min_max_delay=generate_confp(load_data.hof[sol_num], load_data.tasks,
        load_data.tasks_graph, load_data.ALU_config[sol_num],
        load_data.SE_config[sol_num], load_data.CONST_config[sol_num],
        num_pr, confp_path, map_path, delay_path)
    translate_format.generate_manipulater_format(hof_sinks[sol_num], org_path, load_data.REG_config[sol_num])
    out = "Write " + org_path + ", and type y"
    print(out)
    while True:
        y_n = input('>> ')
        if y_n == "y":
            break
    translate_format.format_data_manipulater(org_path, data_path)
    generate_dac(num_pr, org_path, dac_path)
    p_out = "#####\nMinimum Max delay: " + str(ceil(min_max_delay)) + "\n#####\n"
    f = open(MinMax_path, 'w')
    f.write(p_out)
    f.close()

def compress_confp():
    """
    Compresses confp.dat when multiple PEs (ALUs with SELs) and SEs have the same functionality.

    args: none
    """
    f = open(confp_path, 'r')
    lines = f.readlines()
    f.close()
    ALU_group = {}
    SE_group = {}
    others = []
    ALU_head = translate_format.PE_HEAD
    SE_head = translate_format.SE_HEAD
    for line in lines:
        line = line.replace('\n','')
        words = line.split('__')
        if words[0] == ALU_head:
            if line[-4:-1] == "(E)":
                continue
            infos = line.split('\t')
            pos = infos[2]
            if pos == "NOP":
                continue
            func = infos[3] + '(' + infos[4] + ',' + infos[5] + ')'
            if pos == "Error":
                continue
            pos = findall(r'[0-9]+', pos)[0] +'_'+ findall(r'[0-9]+', pos)[1]
            r = words[2].split('_')[0]
            c = words[2].split('_')[1].split('\t')[0]
            if r == "00000101":
                r = "00000100"
            key = words[1] +'__'+ r
            if key in ALU_group:
                c_c = ALU_group[key]['column']
                g_c = c
                n_c = format((int(c_c, 2) | int(g_c, 2)), 'b').zfill(12)
                ALU_group[key]['column'] = n_c
                ALU_group[key]['pos'].append(pos)
            else:
                ALU_group.update({key:{'column':c, 'pos':[pos], 'func':func}})
        elif words[0] == SE_head:
            infos = line.split('\t')
            pos = infos[2]
            func = infos[3] + ' ' + infos[4] + ' '+ infos[5] + ' ' + infos[6]
            pos = findall(r'[0-9]+', pos)[0] +'_'+ findall(r'[0-9]+', pos)[1]
            r = words[2].split('_')[0]
            c = words[2].split('_')[1].split('\t')[0]
            key = words[1] +'__'+ r
            if key in SE_group:
                c_c = SE_group[key]['column']
                g_c = c
                n_c = format((int(c_c, 2) | int(g_c, 2)), 'b').zfill(12)
                SE_group[key]['column'] = n_c
                SE_group[key]['pos'].append(pos)
            else:
                SE_group.update({key:{'column':c, 'pos':[pos], 'func':func}})
        else:
            others.append(line)
    f = open(confp_path, 'w')
    out = '100000_0000000_1111__0000_000_000__11111111_1111111111 // distributing NOP\n'
    print(out)
    f.write(out)
    for key,ALU in ALU_group.items():
        out = '// ' + ALU['func'] + ' '
        for pos in ALU['pos']:
            out = out +' '+ pos
        out = out + '\n'+ ALU_head +'__'+ key +'_'+ ALU['column']
        print(out)
        f.write(out + '\n')
    for key,SE in SE_group.items():
        out = '// '+ SE['func'] +' '
        for pos in SE['pos']:
            out = out +' '+ pos
        out = out +'\n'+ SE_head +'__'+ key +'_'+ SE['column']
        print(out)
        f.write(out + '\n')
    for other in others:
        out = other
        print(out)
        f.write(out + '\n')

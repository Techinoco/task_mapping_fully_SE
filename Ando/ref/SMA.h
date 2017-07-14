////////////////////////////////////////////////////////////////
//  DATA = CARRY + WORD
////////////////////////////////////////////////////////////////
`define DATA_W                          25
`define SMA_DATA_MSB                    24
`define DATA_B                          `SMA_DATA_MSB:0

`define DATA_2_W                        50
`define DATA_2_MSB                      49
`define DATA_2_B                        `DATA_2_MSB:0

`define DATA_3_W                        75
`define DATA_3_MSB                      74
`define DATA_3_B                        `DATA_3_MSB:0

`define DATA_4_W                        100
`define DATA_4_MSB                      99
`define DATA_4_B                        `DATA_4_MSB:0

`define DATA_7_W                        175
`define DATA_7_MSB                      174
`define DATA_7_B                        `DATA_7_MSB:0

`define DATA_8_W                        200
`define DATA_8_MSB                      199
`define DATA_8_B                        `DATA_8_MSB:0

`define DATA_10_W                        250
`define DATA_10_MSB                      249
`define DATA_10_B                        `DATA_10_MSB:0

`define DATA_11_W                        275
`define DATA_11_MSB                      274
`define DATA_11_B                        `DATA_11_MSB:0

`define DATA_12_W                        300
`define DATA_12_MSB                      299
`define DATA_12_B                        `DATA_12_MSB:0

`define DATA_16_W                       400
`define DATA_16_MSB                     399
`define DATA_16_B                       `DATA_16_MSB:0

`define HALF_DATA_W                     13
`define HALF_DATA_MSB                   12
`define HALF_DATA_B                     `HALF_DATA_MSB:0

`define HALF_DATA_4_W                   52
`define HALF_DATA_4_MSB                 51
`define HALF_DATA_4_B                   `HALF_DATA_4_MSB:0

`define HALF_DATA_8_W                   104
`define HALF_DATA_8_MSB                 103
`define HALF_DATA_8_B                   `HALF_DATA_8_MSB:0

`define DATA_0_RNG                       24:0
`define DATA_1_RNG                       49:25
`define DATA_2_RNG                       74:50
`define DATA_3_RNG                       99:75
`define DATA_4_RNG                      124:100
`define DATA_5_RNG                      149:125
`define DATA_6_RNG                      174:150
`define DATA_7_RNG                      199:175

`define CONST_DATA_W                    17
`define CONST_DATA_MSB                  16
`define CONST_DATA_B                    `CONST_DATA_MSB:0
`define CONST_DATA_EXT_W                8

`define CONST_DATA_4_W                  68
`define CONST_DATA_4_MSB                67
`define CONST_DATA_4_B                  `CONST_DATA_4_MSB:0

`define CONST_DATA_8_W                  136
`define CONST_DATA_8_MSB                135
`define CONST_DATA_8_B                  `CONST_DATA_8_MSB:0

`define CONST_DATA_10_W                  170
`define CONST_DATA_10_MSB                169
`define CONST_DATA_10_B                  `CONST_DATA_10_MSB:0

`define CONST_DATA_12_W                  204
`define CONST_DATA_12_MSB                203
`define CONST_DATA_12_B                  `CONST_DATA_10_MSB:0


////////////////////////////////////////////////////////////////
//    WORD
////////////////////////////////////////////////////////////////
`define WORD_W                          24
`define WORD_MSB                        23
`define WORD_B                          `WORD_MSB:0
`define WORD_RNG                        `WORD_MSB:0

`define WORD_2_W                        48
`define WORD_2_MSB                      47
`define WORD_2_B                        `WORD_2_MSB:0

`define WORD_3_W                        72
`define WORD_3_MSB                      71
`define WORD_3_B                        `WORD_3_MSB:0

`define WORD_BIT                        5
`define WORD_BIT_W                      5
`define WORD_BIT_MSB                    4
`define WORD_BIT_B                      `WORD_BIT_MSB:0

`define WORD_2_BIT                      6
`define WORD_2_BIT_W                    6
`define WORD_2_BIT_MSB                  5
`define WORD_2_BIT_B                    `WORD_2_BIT_MSB:0

`define HALF_WORD_W                     12
`define HALF_WORD_MSB                   11
`define HALF_WORD_B                     `HALF_WORD_MSB:0

`define CONST_WORD_W                    16
`define CONST_WORD_MSB                  15
`define CONST_WORD_B                    `CONST_WORD_MSB:0


////////////////////////////////////////////////////////////////
//    CARRY
////////////////////////////////////////////////////////////////
`define CARRY_W                         1
`define CARRY_MSB                       0
`define CARRY_B                         `CARRY_MSB:0
`define CARRY_RNG                       24

`define CARRY_2_W                       2
`define CARRY_2_MSB                     1
`define CARRY_2_B                       `CARRY_2_MSB:0


////////////////////////////////////////////////////////////////
//    PE NUM
////////////////////////////////////////////////////////////////
`define PE_ROW_NUM                      8
`define PE_ROW_NUM_MAX                  7
`define PE_ROW_NUM_RNG                  `PE_ROW_NUM_MAX:0
`define PE_ROW_ADR_W                    3
`define PE_ROW_ADR_MSB                  2
`define PE_ROW_ADR_B                    `PE_ROW_ADR_MSB:0

`define PE_COL_NUM                      12
`define PE_COL_NUM_MAX                  11
`define PE_COL_NUM_RNG                  `PE_COL_NUM_MAX:0
`define PE_COL_ADR_W                    4
`define PE_COL_ADR_MSB                  3
`define PE_COL_ADR_B                    `PE_COL_ADR_MSB:0

`define PE_COL_ADR_8_W                  24
`define PE_COL_ADR_8_MSB                23
`define PE_COL_ADR_8_B                  `PE_COL_ADR_8_MSB:0

`define PE_NUM                          96
`define PE_NUM_RNG                      95:0
`define PE_ADR_W                        7
`define PE_ADR_MSB                      6
`define PE_ADR_B                        `PE_ADR_MSB:0

////////////////////////////////////////////////////////////////
//    ENTIRE CONFIGURATION DATA
////////////////////////////////////////////////////////////////
`define CONF_OP_ACT_W                   10
`define CONF_OP_ACT_MSB                 9
`define CONF_OP_ACT_B                   `CONF_OP_ACT_MSB:0
`define CONF_NETWORK_W                  16 ///////////////
`define CONF_NETWORK_MSB                15 ///////////////
`define CONF_NETWORK_B                  `CONF_NETWORK_MSB:0
`define CONF_OP_NET_W                  20 ///////////////
`define CONF_OP_NET_MSB                19 ///////////////
`define CONF_OP_NET_B                  `CONF_OP_NET_MSB:0

// following value especially used by CONF_CTRL.v
`define CONF_ALU_RNG                     9:6
`define CONF_SEL_A_RNG                   5:3
`define CONF_SEL_B_RNG                   2:0
`define CONF_SE_RNG                      9:0 //NSEW=3232

`define CONF_SE_A_RNG                   20:9 ///////////////
`define CONF_SE_B_RNG                    8:0 ///////////////

////////////////////////////////////////////////////////////////
//   FUNCTION ACTIVE BIT
////////////////////////////////////////////////////////////////
`define ACTIVE_BIT_W                    4
`define ACTIVE_BIT_MSB                  3
`define ACTIVE_BIT_B                    `ACTIVE_BIT_MSB:0

`define ACTIVE_BIT_8_W                  32
`define ACTIVE_BIT_8_MSB                31
`define ACTIVE_BIT_8_B                  `ACTIVE_BIT_8_MSB:0

`define ACTIVE_BIT_64_W                 256
`define ACTIVE_BIT_64_MSB               255
`define ACTIVE_BIT_64_B                 `ACTIVE_BIT_64_MSB:0

`define ACTIVE_BIT_80_W                 320
`define ACTIVE_BIT_80_MSB               319
`define ACTIVE_BIT_80_B                 `ACTIVE_BIT_80_MSB:0

`define ACTIVE_BIT_96_W                 384
`define ACTIVE_BIT_96_MSB               383
`define ACTIVE_BIT_96_B                 `ACTIVE_BIT_96_MSB:0

////////////////////////////////////////////////////////////////
//   ALU CONFIGURATION DATA
////////////////////////////////////////////////////////////////
`define CONF_ALU_W                      4
`define CONF_ALU_MSB                    3
`define CONF_ALU_B                      `CONF_ALU_MSB:0

`define CONF_ALU_4_W                    16
`define CONF_ALU_4_MSB                  15
`define CONF_ALU_4_B                    `CONF_ALU_4_MSB:0

`define CONF_ALU_8_W                    32
`define CONF_ALU_8_MSB                  31
`define CONF_ALU_8_B                    `CONF_ALU_8_MSB:0

`define CONF_ALU_12_W                   48
`define CONF_ALU_12_MSB                 47
`define CONF_ALU_12_B                   `CONF_ALU_12_MSB:0

`define CONF_ALU_64_W                   256
`define CONF_ALU_64_MSB                 255
`define CONF_ALU_64_B                   `CONF_ALU_64_MSB:0

`define CONF_ALU_80_W                   320
`define CONF_ALU_80_MSB                 319
`define CONF_ALU_80_B                   `CONF_ALU_80_MSB:0

`define CONF_ALU_96_W                   384
`define CONF_ALU_96_MSB                 383
`define CONF_ALU_96_B                   `CONF_ALU_96_MSB:0

`define CONF_ALU_NOP                    `CONF_ALU_W'b0000
`define CONF_ALU_ADD                    `CONF_ALU_W'b0001
`define CONF_ALU_SUB                    `CONF_ALU_W'b0010
`define CONF_ALU_MULT                   `CONF_ALU_W'b0011
`define CONF_ALU_SL                     `CONF_ALU_W'b0100
`define CONF_ALU_SR                     `CONF_ALU_W'b0101
`define CONF_ALU_SRA                    `CONF_ALU_W'b0110
`define CONF_ALU_SEL                    `CONF_ALU_W'b0111
`define CONF_ALU_CAT                    `CONF_ALU_W'b1000
`define CONF_ALU_NOT                    `CONF_ALU_W'b1001
`define CONF_ALU_AND                    `CONF_ALU_W'b1010
`define CONF_ALU_OR                     `CONF_ALU_W'b1011
`define CONF_ALU_XOR                    `CONF_ALU_W'b1100
`define CONF_ALU_EQL                    `CONF_ALU_W'b1101
`define CONF_ALU_GT                     `CONF_ALU_W'b1110
`define CONF_ALU_LT                     `CONF_ALU_W'b1111


////////////////////////////////////////////////////////////////
//    DIRECT LINK INTERCEPTOR
////////////////////////////////////////////////////////////////
//`define CONF_DL_W                       2
//`define CONF_DL_MSB                     1
//`define CONF_DL_B                       `CONF_DL_MSB:0
//
//`define CONF_DL_3_W                     6
//`define CONF_DL_3_MSB                   5
//`define CONF_DL_3_B                     `CONF_DL_3_MSB:0
//
//`define CONF_DL_4_W                     8
//`define CONF_DL_4_MSB                   7
//`define CONF_DL_4_B                     `CONF_DL_4_MSB:0
//
//`define CONF_DL_8_W                     16
//`define CONF_DL_8_MSB                   15
//`define CONF_DL_8_B                     `CONF_DL_8_MSB:0
//
//`define CONF_DL_64_W                    128
//`define CONF_DL_64_MSB                  127
//`define CONF_DL_64_B                    `CONF_DL_64_MSB:0
//
//`define CONF_DL_NORTH                   0
//`define CONF_DL_NORTH_NORTH             1


////////////////////////////////////////////////////////////////
//    ALU INPUT SELECTOR CONFIGURATION DATA
////////:////////////////////////////////////////////////////////
`define CONF_SEL_W                    3
`define CONF_SEL_MSB                  2
`define CONF_SEL_B                    `CONF_SEL_MSB:0

`define CONF_SEL_4_W                  12
`define CONF_SEL_4_MSB                11
`define CONF_SEL_4_B                  `CONF_SEL_4_MSB:0

`define CONF_SEL_8_W                  24
`define CONF_SEL_8_MSB                23
`define CONF_SEL_8_B                  `CONF_SEL_8_MSB:0

`define CONF_SEL_12_W                 36
`define CONF_SEL_12_MSB               35
`define CONF_SEL_12_B                 `CONF_SEL_12_MSB:0

`define CONF_SEL_64_W                 192
`define CONF_SEL_64_MSB               191
`define CONF_SEL_64_B                 `CONF_SEL_64_MSB:0

`define CONF_SEL_80_W                   240
`define CONF_SEL_80_MSB                 239
`define CONF_SEL_80_B                   `CONF_SEL_80_MSB:0

`define CONF_SEL_96_W                   288
`define CONF_SEL_96_MSB                 287
`define CONF_SEL_96_B                   `CONF_SEL_96_MSB:0

`define CONF_SEL_SOUTH                `CONF_SEL_W'b000
`define CONF_SEL_EAST                 `CONF_SEL_W'b001
`define CONF_SEL_WEST                 `CONF_SEL_W'b010
`define CONF_SEL_DL_S                 `CONF_SEL_W'b011
`define CONF_SEL_DL_SE                `CONF_SEL_W'b100
`define CONF_SEL_DL_SW                `CONF_SEL_W'b101
`define CONF_SEL_CONST_A              `CONF_SEL_W'b110
`define CONF_SEL_CONST_B              `CONF_SEL_W'b111



////////////////////////////////////////////////////////////////
// SE.v
////////////////////////////////////////////////////////////////
`define CONF_SE_W                     16
`define CONF_SE_MSB                   15
`define CONF_SE_B                     `CONF_SE_MSB:0

`define CONF_SE_4_W                   64
`define CONF_SE_4_MSB                 63
`define CONF_SE_4_B                   `CONF_SE_4_MSB:0

`define CONF_SE_8_W                   128
`define CONF_SE_8_MSB                 127
`define CONF_SE_8_B                   `CONF_SE_8_MSB:0

`define CONF_SE_12_W                  192
`define CONF_SE_12_MSB                191
`define CONF_SE_12_B                  `CONF_SE_12_MSB:0

`define CONF_SE_64_W                  1024
`define CONF_SE_64_MSB                1023
`define CONF_SE_64_B                  `CONF_SE_64_MSB:0

`define CONF_SE_80_W                  1280
`define CONF_SE_80_MSB                1279
`define CONF_SE_80_B                  `CONF_SE_80_MSB:0

`define CONF_SE_96_W                  1536
`define CONF_SE_96_MSB                1535
`define CONF_SE_96_B                  `CONF_SE_96_MSB:0

`define CONF_SE_A_80_W                  1280
`define CONF_SE_A_80_MSB                1279
`define CONF_SE_A_80_B                  `CONF_SE_A_80_MSB:0

`define CONF_SE_A_96_W                  1536
`define CONF_SE_A_96_MSB                1535
`define CONF_SE_A_96_B                  `CONF_SE_A_96_MSB:0

`define CONF_SW_W                     4
`define CONF_SW_MSB                   3
`define CONF_SW_B                     `CONF_SW_MSB:0
`define CONF_SW_B2                    1:0
`define CONF_SW_B3                    2:0

`define CONF_SW_ALU             `CONF_SW_W'b0000
`define CONF_SW_SOUTH           `CONF_SW_W'b0001
`define CONF_SW_NORTH           `CONF_SW_W'b0001
`define CONF_SW_EAST            `CONF_SW_W'b0010
`define CONF_SW_WEST            `CONF_SW_W'b0011
`define CONF_SW_DL_S            `CONF_SW_W'b0100
`define CONF_SW_DL_SE            `CONF_SW_W'b0101
`define CONF_SW_DL_SW           `CONF_SW_W'b0110
`define CONF_SW_CONST_A           `CONF_SW_W'b0111
`define CONF_SW_CONST_B           `CONF_SW_W'b1000

////////////////////////////////////////////////////////////////
//    GLOBAL ADDRESS AND DATA
////////////////////////////////////////////////////////////////
`define GLB_ADR_W                       12
`define GLB_ADR_MSB                     11
`define GLB_ADR_B                       `GLB_ADR_MSB:0

`define GLB_DATA_W                      25
`define GLB_DATA_MSB                    24
`define GLB_DATA_B                      `GLB_DATA_MSB:0

`define DATAH_W                      12
`define DATAH_MSB                    11
`define DATAH_B                      `DATAH_MSB:0

`define GLB_ADR_HEAD_W                  6
`define GLB_ADR_HEAD_MSB                5
`define GLB_ADR_HEAD_B                  `GLB_ADR_HEAD_MSB:0
`define GLB_ADR_HEAD_RNG                11:6

// CONF_OP_ACT(16)  = CONF_ALU(4), CONF_ALU_SEL_A(4), CONF_ALU_SEL_B(4), xxACTIVE(4)xx
// CONF_NETWORK(24) = CONF_CAS(1), CONF_SE_A(12), CONF_SE_B(9), CONF_DL(2)
`define GLB_ADR_HEAD_CONF_OP_ACT        `GLB_ADR_HEAD_W'b100000
`define GLB_ADR_HEAD_CONF_NETWORK       `GLB_ADR_HEAD_W'b100001
`define GLB_ADR_HEAD_CONST              `GLB_ADR_HEAD_W'b100010
`define GLB_ADR_HEAD_IMEM               `GLB_ADR_HEAD_W'b100011
`define GLB_ADR_HEAD_PC                 `GLB_ADR_HEAD_W'b100100
`define GLB_ADR_HEAD_CUR_INST           `GLB_ADR_HEAD_W'b100101
`define GLB_ADR_HEAD_CONF_PREG          `GLB_ADR_HEAD_W'b100110
`define GLB_ADR_HEAD_FR                 `GLB_ADR_HEAD_W'b100111
`define GLB_ADR_HEAD_CONF_PEADR         `GLB_ADR_HEAD_W'b101000
`define GLB_ADR_HEAD_CONF_PEADR2        `GLB_ADR_HEAD_W'b101001
//`define GLB_ADR_HEAD_SR                 `GLB_ADR_HEAD_W'b101000
//`define GLB_ADR_HEAD_GR                 `GLB_ADR_HEAD_W'b101001
`define GLB_ADR_HEAD_PREV_RD_LOW        `GLB_ADR_HEAD_W'b101010
`define GLB_ADR_HEAD_PREV_RDEB          `GLB_ADR_HEAD_W'b101011
`define GLB_ADR_HEAD_PREV_OPCODE        `GLB_ADR_HEAD_W'b101100
`define GLB_ADR_HEAD_LOADING            `GLB_ADR_HEAD_W'b101101
`define GLB_ADR_HEAD_FR_PTR             `GLB_ADR_HEAD_W'b101110
`define GLB_ADR_HEAD_DRAR               `GLB_ADR_HEAD_W'b101111
`define GLB_ADR_HEAD_RDEB               `GLB_ADR_HEAD_W'b110000
`define GLB_ADR_HEAD_STORING            `GLB_ADR_HEAD_W'b110001
`define GLB_ADR_HEAD_DWOR_PTR           `GLB_ADR_HEAD_W'b110010
`define GLB_ADR_HEAD_DWAR               `GLB_ADR_HEAD_W'b110011
`define GLB_ADR_HEAD_WDEB               `GLB_ADR_HEAD_W'b110100
`define GLB_ADR_HEAD_DONE               `GLB_ADR_HEAD_W'b110101
`define GLB_ADR_HEAD_CONF_CAS           `GLB_ADR_HEAD_W'b110110
`define GLB_ADR_HEAD_PREV_PC            `GLB_ADR_HEAD_W'b110111
`define GLB_ADR_HEAD_PREV_BANK_SEL      `GLB_ADR_HEAD_W'b111000
`define GLB_ADR_HEAD_STRIDE             `GLB_ADR_HEAD_W'b111001
`define GLB_ADR_HEAD_DWOR               `GLB_ADR_HEAD_W'b111010
`define GLB_ADR_HEAD_CUR_DWOR           `GLB_ADR_HEAD_W'b111011
`define GLB_ADR_RT0_DBG           	`GLB_ADR_HEAD_W'b111100
`define GLB_ADR_RT1_DBG           	`GLB_ADR_HEAD_W'b111101
`define GLB_ADR_LM   	        	`GLB_ADR_HEAD_W'b111110

// PG_MULT_IN_A == {dcare(8), ACTIVE(1),   MULT_IN_A(16)};
// PG_MULT_IN_B == {dcare(8), PG_FF_IN(1), MULT_IN_B(16)};
`define GLB_ADR_HEAD_PG_MULT_IN_A       `GLB_ADR_HEAD_W'b111101
`define GLB_ADR_HEAD_PG_MULT_IN_B       `GLB_ADR_HEAD_W'b111110
`define GLB_ADR_HEAD_PG_MULT_OUT        `GLB_ADR_HEAD_W'b111111


////////////////////////////////////////////////////////////////
//    ROMULTIC BIT
////////////////////////////////////////////////////////////////
`define ROMULTIC_W                      20
`define ROMULTIC_MSB                    19
`define ROMULTIC_B                      `ROMULTIC_MSB:0


////////////////////////////////////////////////////////////////
//    DATA MEMORY
////////////////////////////////////////////////////////////////
`define DMEM_ENTRY                      1024
`define DMEM_ENTRY_RNG                  1023:0
`define DMEM_ADR_W                      10
`define DMEM_ADR_MSB                    9
`define DMEM_ADR_B                      `DMEM_ADR_MSB:0

`define RAM_ENTRY                       512
`define RAM_ENTRY_RNG                   511:0
`define RAM_ADR_W                       9
`define RAM_ADR_MSB                     8
`define RAM_ADR_B                       `RAM_ADR_MSB:0

`define BANK_RG_RNG                     11:0

////////////////////////////////////////////////////////////////
//    CONST DATA CONTROLLER
////////////////////////////////////////////////////////////////
`define CONST_REG_ENTRY                 16
`define CONST_REG_ENTRY_RNG             15:0
`define CONST_REG_ADR_W                 4
`define CONST_REG_ADR_MSB               3
`define CONST_REG_ADR_B                 `CONST_REG_ADR_MSB:0


////////////////////////////////////////////////////////////////
//    DATA ACCESS CONTROLLER
////////////////////////////////////////////////////////////////
`define IMEM_W                          14
`define IMEM_MSB                        13
`define IMEM_B                          `IMEM_MSB:0
`define IMEM_ENTRY                      64
`define IMEM_ENTRY_RNG                  63:0
`define IMEM_ADR_W                      6
`define IMEM_ADR_MSB                    5
`define IMEM_ADR_B                      `IMEM_ADR_MSB:0

`define IMM_W                           6
`define IMM_MSB                         5
`define IMM_B                           `IMM_MSB:0
`define IMM_EXT_W                       4

`define GPR_W                           10
`define GPR_MSB                         9
`define GPR_B                           `GPR_MSB:0
`define HALF_GPR_W                      5
`define HALF_GPR_MSB                    4
`define HALF_GPR_B                      `HALF_GPR_MSB:0
`define GPR_ENTRY                       16
`define GPR_ENTRY_RNG                   15:0
`define GPR_ADR_W                       4
`define GPR_ADR_MSB                     3
`define GPR_ADR_B                       `GPR_ADR_MSB:0
`define GPR_STRIDE                      15

`define ENABLE                  1'b1
`define ENABLE_N                1'b0
`define DISABLE                 1'b0
`define DISABLE_N               1'b1

`define HIGH                    1'b1
`define HIGH_N                  1'b0
`define LOW                     1'b0
`define LOW_N                   1'b1

`define ACTIVE                  1'b1
`define ACTIVE_N                1'b0
`define SLEEP                   1'b0
`define SLEEP_N                 1'b1

`define TRUE                    1'b1
`define FALSE                   1'b0
`define NULL                    1'b0

`define USE                     1'b1
`define UNUSE                   1'b0
`define USE_N                   1'b0
`define UNUSE_N                 1'b1

`define VALID                   1'b1
`define INVALID                 1'b0
`define VALID_N                 1'b0
`define INVALID_N               1'b1

`define TBL_W 2
`define DMEMA_W 6
`define REG_W 4
`define REG 16
`define CPU_W 16
`define DEPTH 64
`define INSTA_W 8
`define ZERO `DATA_W'b0
`define LDTBL_W 48
`define MAP_W 12
`define EXA_W 12
`define DBGDAT_W 4
`define DBGSEL_W 3
`define EXSEL 11:8
`define EXSELB 11:6
`define DLY 4

`define EX_BANK0 4'b0000
`define EX_BANK1 4'b0001
`define EX_IMEM 4'b0010
`define EX_LTBL 4'b0011
`define EX_STBL 4'b0100
`define EX_ACT 6'b100000
`define EX_NET 6'b100001
`define EX_CONST 6'b100010

`define OP_REG 4'b0000
`define OP_LD_ADD 4'b0001
`define OP_ST_ADD 4'b0010
`define OP_LDI 4'b0011
`define OP_ADDI 4'b0100
`define OP_LD_ADDL 4'b0101
`define OP_ST_ADDS 4'b0110
`define OP_LD_ST_ADD'b0111
`define OP_BEZ 4'b1000
`define OP_BEZD 4'b1001
`define OP_BNZ 4'b1010
`define OP_BNZD 4'b1011
`define OP_SET_LD 4'b1100
`define OP_SET_ST 4'b1101

`define F_NOP 4'b0000
`define F_ADD 4'b0001
`define F_SUB 4'b0010
`define F_MV 4'b0011
`define F_DONE 4'b1110
`define F_DELAY 4'b1111

`define LD_RD1 12
`define LD_RD2 13
`define ST_RD1 14
`define ST_RD2 15

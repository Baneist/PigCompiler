from base import list_dict as ldict, mid_code as mcode
from analyser import getVar
from random import randint
ostr = []
ofile = open('output.s', 'w')
dg_begin = 0x10010000

varaddr = []
def varaddrInit():
    for i in ldict['var']:
        varaddr.append(i[1] + varaddr[-1] if varaddr else i[1])
    for i, item in enumerate(ldict['var']):
        varaddr[i] -= item[1]

def getVarAddress(name, func):
    save = 0
    for i in range(len(ldict['var'])):
        if ldict['var'][i][0] == name:
            if ldict['var'][i][2] == func:
                return varaddr[i]
            elif ldict['var'][i][2] == '$global':
                save = i
    return varaddr[save]
    
def getVarAddressFromId(id, func):
    t = 0
    for i in range(len(ldict['var'])):
        if ldict['var'][i][2] == func:
            if t == id:
                return varaddr[i]
            t += 1
    return 0

reg_list = ['$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7', '$t8', '$t9']
def LReg(name, func, id = 9):
    ostr.append('lw {}, {}'.format('$v0' if id == 99 else reg_list[id], getVarAddress(name, func) + dg_begin))
    return reg_list[id]
def SReg(name, func, id = 9):
    ostr.append('sw {}, {}'.format('$v0' if id == 99 else reg_list[id], getVarAddress(name, func) + dg_begin))
    return reg_list[id]

def genCode():
    varaddrInit()
    bp = 4*len(ldict['var'])
    sp = 0
    nowfunc = '$global'
    ostr.append('lui $ra, 0x40') 
    ostr.append('addi $ra, $ra, 0xc')
    ostr.append('j main')
    ostr.append('j __END__')
    for i in range(len(mcode)):
        ostr.append('#' + str(i) + ': ' + str(mcode[i]))
        if i+100 in ldict['link_point']: #设置跳转点
            ostr.append('L' + str(i+100) + ':')
        code = mcode[i]
        if code[0] == 'j':
            ostr.append('j L' + str(code[3]) if code[1] == '' else 'j ' + code[1])
            #if code[1] == '': rmgr.freeFunc(nowfunc)
        elif code[0] == ':':
            ostr.append(code[1] + ':')
            nowfunc = code[1]
        elif code[0] == 'ret':
            ostr.append('jr $ra')
            ostr.append('')
        elif code[0] == 'call':
            ostr.append('add $a0, $ra, $zero')
            ostr.append('jal ' + code[1])
            ostr.append('add $ra, $a0, $zero')
        elif code[0] == 'par':
            ostr.append('sw {}, {}'.format(LReg(code[1], nowfunc, 0), getVarAddressFromId(code[2], code[3]) + dg_begin))
        elif code[0] == '=':
            if code[1] == '#eax':
                SReg(code[3], nowfunc, 9)
            elif code[3] == '#eax':
                LReg(code[1], nowfunc, 9)
            else:  
                LReg(code[1], nowfunc, 0)
                SReg(code[3], nowfunc, 0)
        elif code[0] == '=l':
            ostr.append('lw {}, {}({})'.format(reg_list[0], dg_begin + getVarAddress(code[1], nowfunc), LReg(code[2], nowfunc, 1)))
            SReg(code[3], nowfunc, 0)
        elif code[0] == '=r':
            ostr.append('sw {}, {}({})'.format(LReg(code[1], nowfunc, 0), dg_begin + getVarAddress(code[3], nowfunc), LReg(code[2], nowfunc, 1)))
        elif code[0] == '=i':
            ostr.append('addi {}, $zero, {}'.format(reg_list[0], int(code[1])))
            SReg(code[3], nowfunc, 0)
        elif code[0] == 'j<':
            ostr.append('blt {}, {}, L{}'.format(LReg(code[1], nowfunc, 0), LReg(code[2], nowfunc, 1), code[3]))
        elif code[0] == 'j<=':
            ostr.append('ble {}, {}, L{}'.format(LReg(code[1], nowfunc, 0), LReg(code[2], nowfunc, 1), code[3]))
        elif code[0] == 'j>':
            ostr.append('bgt {}, {}, L{}'.format(LReg(code[1], nowfunc, 0), LReg(code[2], nowfunc, 1), code[3]))
        elif code[0] == 'j>=':
            ostr.append('bge {}, {}, L{}'.format(LReg(code[1], nowfunc, 0), LReg(code[2], nowfunc, 1), code[3]))
        elif code[0] == 'j==':
            ostr.append('beq {}, {}, L{}'.format(LReg(code[1], nowfunc, 0), LReg(code[2], nowfunc, 1), code[3]))
        elif code[0] == 'j!=':
            ostr.append('bne {}, {}, L{}'.format(LReg(code[1], nowfunc, 0), LReg(code[2], nowfunc, 1), code[3]))
        elif code[0] == 'jnz':
            ostr.append('bne {}, $zero, L{}'.format(LReg(code[1], nowfunc, 0), code[3]))
        elif code[0] == '+':
            ostr.append('add {}, {}, {}'.format(reg_list[2], LReg(code[1], nowfunc, 0), LReg(code[2], nowfunc, 1)))
            SReg(code[3], nowfunc, 2)
        elif code[0] == '-':
            ostr.append('sub {}, {}, {}'.format(reg_list[2], LReg(code[1], nowfunc, 0), LReg(code[2], nowfunc, 1)))
            SReg(code[3], nowfunc, 2)
        elif code[0] == '*':
            LReg(code[1], nowfunc, 0)
            if isinstance(code[2], int):
                ostr.append('addi {}, $zero, {}'.format(reg_list[1], code[2]))
            else:
                LReg(code[2], nowfunc, 1)
            ostr.append('mul {}, {}, {}'.format(reg_list[2], reg_list[0], reg_list[1]))
            SReg(code[3], nowfunc, 2)
        elif code[0] == '/':
            ostr.append('div {}, {}'.format(LReg(code[1], nowfunc, 0), LReg(code[2], nowfunc, 1)))
            ostr.append('mflo {}'.format(reg_list[2]))
            SReg(code[3], nowfunc, 2)
        ostr.append('')
    ostr.append('# compile finished.')
    ostr.append('__END__:')
    for i in ostr:
        ofile.write(i+'\n')
    ofile.close()
    print("\033[1;32;32m[Info]Code generate success!\033[0m")
    return True
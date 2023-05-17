from base import list_dict as ldict, mid_code as mcode, args
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
    ostr.append('lw {}, {}'.format('$v0' if id == 9 else reg_list[id], getVarAddress(name, func) + dg_begin))
    return reg_list[id]
def SReg(name, func, id = 9):
    ostr.append('sw {}, {}'.format('$v0' if id == 9 else reg_list[id], getVarAddress(name, func) + dg_begin))
    return reg_list[id]

'''
class RegManager:
    def __init__(self):
        self.vcode = mcode

    def CutCode(self):
        self.cut = []
        for i in range(len(self.vcode)):
            if self.vcode[i][0][0] == 'j' or self.vcode[i][0] == 'call' or self.vcode[i][0] == 'ret':
                self.cut.append(i)
        self.cut[-1] = self.cut[-1] + 1
    
    def AllocInformationGenerate(self):
        self.CutCode()
        huoyue = dict()
        self.aInfrom = []
        def setHuoyue(chy, nt, j, n, load = False):
            if self.vcode[j][n] not in huoyue: huoyue[self.vcode[j][n]] = (-1, False)
            nt[self.vcode[j][n]] = huoyue[self.vcode[j][n]]
            huoyue[self.vcode[j][n]] = (j, load) if load else (-1, False)
            if load: chy[self.vcode[j][n]] = (-1, True)
            elif self.vcode[j][n] in chy: chy.pop(self.vcode[j][n])
        
        for i in range(len(self.cut) - 1, -1, -1):
            chuoyue = dict()
            if i != 0: l = self.cut[i-1]; r = self.cut[i]
            else: r = l; l = 0
            tinform = []
            # print('range: ', l, r)
            for j in range(l, r):
                nt = {}
                if self.vcode[j][0] == '=':
                    if self.vcode[j][1] != '#eax': setHuoyue(chuoyue, nt, j, 1, True)
                    if self.vcode[j][3] != '#eax': setHuoyue(chuoyue, nt, j, 3, False)
                elif self.vcode[j][0] == '=l':
                    setHuoyue(chuoyue, nt, j, 2, True)
                    setHuoyue(chuoyue, nt, j, 3, False)
                elif self.vcode[j][0] == '=r':
                    setHuoyue(chuoyue, nt, j, 1, True)
                    setHuoyue(chuoyue, nt, j, 2, False)
                elif self.vcode[j][0] == 'par':
                    setHuoyue(chuoyue, nt, j, 1, True)
                elif self.vcode[j][0] == '=i':
                    setHuoyue(chuoyue, nt, j, 3, False)
                elif self.vcode[j][0] in {'j<', 'j<=', 'j>', 'j>=', 'j==', 'j!='}:
                    setHuoyue(chuoyue, nt, j, 1, True)
                    setHuoyue(chuoyue, nt, j, 2, True)
                elif self.vcode[j][0] == 'jnz':
                    setHuoyue(chuoyue, nt, j, 1, True)
                elif self.vcode[j][0] in ('+', '-'):
                    setHuoyue(chuoyue, nt, j, 1, True)
                    setHuoyue(chuoyue, nt, j, 2, True)
                    setHuoyue(chuoyue, nt, j, 3, False)
                elif self.vcode[j][0] == '*':
                    setHuoyue(chuoyue, nt, j, 1, True)
                    if not isinstance(self.vcode[j][2], int): setHuoyue(chuoyue, nt, j, 2, True)
                    setHuoyue(chuoyue, nt, j, 3, False)
                elif self.vcode[j][0] == '/':
                    setHuoyue(chuoyue, nt, j, 1, True)
                    setHuoyue(chuoyue, nt, j, 2, True)
                    setHuoyue(chuoyue, nt, j, 3, False)
                tinform.append(nt)
            tinform.reverse()
            self.aInfrom += tinform
            huoyue = chuoyue
        self.aInfrom.reverse()
        for i in range(len(self.vcode)):
            print('{}:'.format(i), self.vcode[i], self.aInfrom[i])

    regs = [None] * 10
    curBlock = 0
    def calcBlock(self, line):
        for i in range(len(self.cut)):
            if line < self.cut[i]:
                return i
        return len(self.cut) - 1
    def GetReg(self, name, function, line):
'''

class RegManager:
    regs = [None] * 28
    def __init__(self) -> None:
        pass
    def i2n(self, index):
        return '${}'.format(index+4)
    def save(self, code, func, index):
        ostr.append('sw {}, {}'.format(self.i2n(index), getVarAddress(code, func) + dg_begin))
    def load(self, code, func, index):
        ostr.append('lw {}, {}'.format(self.i2n(index), getVarAddress(code, func) + dg_begin))
    def get(self, code, func):
        if code == '#eax': return '$v0'
        if (code, func) in self.regs:
            return self.i2n(self.regs.index((code, func)))
        savei = None
        hasNone = (None in self.regs)
        for i in range(len(self.regs)):
            if self.regs[i] == None or (hasNone and self.regs[i] == (code, func)):
                self.regs[i] = (code, func)
                savei = i
                break
        else:
            savei = randint(0, len(self.regs) - 1)
        if self.regs[savei] != None:
            self.save(self.regs[savei][0], self.regs[savei][1], savei)
            self.load(code, func, savei)

    def clear(self):
        for i in range(len(self.regs)):
            if self.regs[i] != None and self.regs[i][0].startswith('@'):
                self.save(self.regs[i][0], self.regs[i][1], i)
                self.regs[i] = None

def genCode():
    varaddrInit()
    #regMgr = RegManager()
    #regMgr.AllocInformationGenerate()
    bp = 4 * len(ldict['var'])
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
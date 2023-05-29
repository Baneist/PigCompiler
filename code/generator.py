from base import list_dict as ldict, mid_code as mcode, args
from analyser import getVar
from random import randint
from copy import deepcopy
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

def searchFuncBelongFormName(name, func):
    for i in range(len(ldict['var'])):
        if ldict['var'][i][0] == name:
            if ldict['var'][i][2] == func:
                return func
    else:
        return '$global'

class RegManager:
    def __init__(self):
        self.vcode = mcode

    def cutCodeBlock(self):
        self.cut = []
        self.cutfunc = []
        self.rcnt = {}
        self.linesave = {}
        nowfunc = '$global'
        for i in range(len(self.vcode)):
            if self.vcode[i][0][0] == 'j' or self.vcode[i][0] == 'call' or self.vcode[i][0] == 'ret' or self.vcode[i][0] == ':':
                if self.vcode[i][0][0] == 'j':
                    self.cut.append(self.vcode[i][3] - 100)
                    self.cutfunc.append((self.vcode[i][3] - 100, nowfunc))
                if (i+1) not in self.cut:
                    self.cut.append(i+1)
                    self.cutfunc.append((i+1, nowfunc))
                if self.vcode[i][0] == ':':
                    nowfunc = self.vcode[i][1]
        self.cut.sort()
        self.cutfunc.sort()
        self.cut[-1] = self.cut[-1] + 1
    
    def allocInformationGenerate(self):
        self.cutCodeBlock()
        huoyue = dict()
        self.aInfrom = []
        nowfunc = '$global'
        def setHuoyue(chy, nt, j, n, load = False):
            name = searchFuncBelongFormName(self.vcode[j][n], nowfunc) + '.' + self.vcode[j][n]
            if name not in huoyue: huoyue[name] = (-1, False)
            nt[name] = huoyue[name]
            huoyue[name] = (j, load) if load else (-1, False)
            if load: chy[name] = (-1, True)
            elif name in chy: chy.pop(name)
        for i in range(len(self.cut) - 1, -1, -1):
            nowfunc = self.cutfunc[i][1]
            chuoyue = dict()
            if i != 0: l = self.cutfunc[i-1][0]; r = self.cutfunc[i][0]
            else: r = l; l = 0
            tinform = []
            shuoyue = deepcopy(huoyue)
            for j in range(r-1, l-1, -1):
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
                elif self.vcode[j][0] in ('+', '-', '/', '*'):
                    setHuoyue(chuoyue, nt, j, 1, True)
                    if not isinstance(self.vcode[j][2], int): setHuoyue(chuoyue, nt, j, 2, True)
                    setHuoyue(chuoyue, nt, j, 3, False)
                tinform.append(nt)
            self.aInfrom += tinform
            huoyue = shuoyue
            for a in chuoyue:
                if a not in huoyue: huoyue[a] = chuoyue[a]
        self.aInfrom.reverse()
    regs = [None] * 27
    ai_save = [None] * 27
    m_save = [None] * 27
    curBlock = 0
    def _calcBlock(self, line):
        for i in range(len(self.cut)):
            if line < self.cut[i]:
                return i
        return len(self.cut) - 1
    def _i2n(self, index):
        return '${}'.format(index+4)
    def _save(self, code, func, index):
        if self.m_save[index] == False and (self.ai_save[index][0] != -1 or self.ai_save[index][1] == True or code[0] != '@') or (code[0] == '@' and self.rcnt[(code, func)] == 1):
            ostr.append('sw {}, {} #save <{}> in func <{}>'.format(self._i2n(index), getVarAddress(code, func) + dg_begin, code, func))
    def _load(self, code, func, index):
            ostr.append('lw {}, {} #load <{}> in func <{}>'.format(self._i2n(index), getVarAddress(code, func) + dg_begin, code, func))
    
    def getReg(self, code, func, line, frommemory=True):
        if code == '#eax': return '$v0'
        if (code, func) in self.rcnt:
            self.rcnt[(code, func)] += 1
        else:
            self.rcnt[(code, func)] = 1
        self.linesave[(code, func)] = line
        if (code, func) in self.regs:
            self.ai_save[self.regs.index((code, func))] = self.aInfrom[line][searchFuncBelongFormName(code, func)+'.'+code]
            self.m_save[self.regs.index((code, func))] &= frommemory
            return self._i2n(self.regs.index((code, func)))
        savei = None
        hasNone = (None in self.regs)
        for i in range(len(self.regs)):
            if self.regs[i] == None or (self.regs[i][0][0] == '@' and self.rcnt[self.regs[i]] == 2 and self.linesave[self.regs[i]] < line):
                savei = i
                break
        else:
            savei = randint(0, len(self.regs) - 1)
        if self.regs[savei] != None:
            self._save(self.regs[savei][0], self.regs[savei][1], savei)
        self.regs[i] = (code, func)
        self.ai_save[i] = self.aInfrom[line][searchFuncBelongFormName(code, func)+'.'+code]
        self.m_save[i] = frommemory
        if frommemory: self._load(code, func, savei)
        return self._i2n(savei)
    def isBlockPointEnd(self, line):
        return line + 1 in self.cut
    def clear(self):
        for i in range(len(self.regs)):
            if self.regs[i] != None:
                self._save(self.regs[i][0], self.regs[i][1], i)
                self.regs[i] = None

def Generator():
    varaddrInit()
    regMgr = RegManager()
    regMgr.allocInformationGenerate()
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
            if regMgr.isBlockPointEnd(i): regMgr.clear()
            ostr.append('j L' + str(code[3]) if code[1] == '' else 'j ' + code[1])
            #if code[1] == '': rmgr.freeFunc(nowfunc)
        elif code[0] == ':':
            if regMgr.isBlockPointEnd(i): regMgr.clear()
            ostr.append(code[1] + ':')
            nowfunc = code[1]
        elif code[0] == 'ret':
            if regMgr.isBlockPointEnd(i): regMgr.clear()
            ostr.append('jr $ra')
            ostr.append('')
            nowfunc = '$global'
        elif code[0] == 'call':
            if regMgr.isBlockPointEnd(i): regMgr.clear()
            ostr.append('add $3, $ra, $zero')
            ostr.append('jal ' + code[1])
            ostr.append('add $ra, $3, $zero')
        elif code[0] == 'par':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            ostr.append('sw {}, {}'.format(v1, getVarAddressFromId(code[2], code[3]) + dg_begin))
            if regMgr.isBlockPointEnd(i): regMgr.clear()
        elif code[0] == '=':
            v3 = regMgr.getReg(code[3], nowfunc, i, False)
            v1 = regMgr.getReg(code[1], nowfunc, i)
            ostr.append('add {}, {}, $zero'.format(v3, v1))
            if regMgr.isBlockPointEnd(i): regMgr.clear()
        elif code[0] == '=l':
            v3 = regMgr.getReg(code[3], nowfunc, i, False)
            v2 = regMgr.getReg(code[2], nowfunc, i)
            ostr.append('lw {}, {}({})'.format(v3, dg_begin + getVarAddress(code[1], nowfunc), v2))
            if regMgr.isBlockPointEnd(i): regMgr.clear()
        elif code[0] == '=r':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            v2 = regMgr.getReg(code[2], nowfunc, i)
            ostr.append('sw {}, {}({})'.format(v1, dg_begin + getVarAddress(code[3], nowfunc), v2))
            if regMgr.isBlockPointEnd(i): regMgr.clear()
        elif code[0] == '=i':
            v3 = regMgr.getReg(code[3], nowfunc, i, False)
            ostr.append('addi {}, $zero, {}'.format(v3, int(code[1])))
            if regMgr.isBlockPointEnd(i): regMgr.clear()
        elif code[0] == 'j<':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            v2 = regMgr.getReg(code[2], nowfunc, i)
            if regMgr.isBlockPointEnd(i): regMgr.clear()
            ostr.append('blt {}, {}, L{}'.format(v1, v2, code[3]))
        elif code[0] == 'j<=':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            v2 = regMgr.getReg(code[2], nowfunc, i)
            if regMgr.isBlockPointEnd(i): regMgr.clear()
            ostr.append('ble {}, {}, L{}'.format(v1, v2, code[3]))
        elif code[0] == 'j>':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            v2 = regMgr.getReg(code[2], nowfunc, i)
            if regMgr.isBlockPointEnd(i): regMgr.clear()
            ostr.append('bgt {}, {}, L{}'.format(v1, v2, code[3]))
        elif code[0] == 'j>=':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            v2 = regMgr.getReg(code[2], nowfunc, i)
            if regMgr.isBlockPointEnd(i): regMgr.clear()
            ostr.append('bge {}, {}, L{}'.format(v1, v2, code[3]))
        elif code[0] == 'j==':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            v2 = regMgr.getReg(code[2], nowfunc, i)
            if regMgr.isBlockPointEnd(i): regMgr.clear()
            ostr.append('beq {}, {}, L{}'.format(v1, v2, code[3]))
        elif code[0] == 'j!=':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            v2 = regMgr.getReg(code[2], nowfunc, i)
            if regMgr.isBlockPointEnd(i): regMgr.clear()
            ostr.append('bne {}, {}, L{}'.format(v1, v2, code[3]))
        elif code[0] == 'jnz':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            if regMgr.isBlockPointEnd(i): regMgr.clear()
            ostr.append('bne {}, $zero, L{}'.format(v1, code[3]))
        elif code[0] == '+':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            v2 = regMgr.getReg(code[2], nowfunc, i)
            v3 = regMgr.getReg(code[3], nowfunc, i, False)
            ostr.append('add {}, {}, {}'.format(v3, v1, v2))
            if regMgr.isBlockPointEnd(i): regMgr.clear()
        elif code[0] == '-':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            v2 = regMgr.getReg(code[2], nowfunc, i)
            v3 = regMgr.getReg(code[3], nowfunc, i, False)
            ostr.append('sub {}, {}, {}'.format(v3, v1, v2))
            if regMgr.isBlockPointEnd(i): regMgr.clear()
        elif code[0] == '*':
            va = regMgr.getReg(code[1], nowfunc, i)
            if isinstance(code[2], int):
                ostr.append('addi {}, $zero, {}'.format('$2', code[2]))
                vb = '$2'
            else:
                vb = regMgr.getReg(code[2], nowfunc, i)
            v3 = regMgr.getReg(code[3], nowfunc, i, False)
            ostr.append('mul {}, {}, {}'.format(v3, va, vb))
            if regMgr.isBlockPointEnd(i): regMgr.clear()
        elif code[0] == '/':
            v1 = regMgr.getReg(code[1], nowfunc, i)
            v2 = regMgr.getReg(code[2], nowfunc, i)
            v3 = regMgr.getReg(code[3], nowfunc, i, False)
            ostr.append('div {}, {}'.format(v1, v2))
            ostr.append('mflo {}'.format(v3))
            if regMgr.isBlockPointEnd(i): regMgr.clear()
        ostr.append('')
    ostr.append('# compile finished.')
    ostr.append('__END__:')
    print("\033[1;32;32m[Info]Code generate success!\033[0m")
    return True
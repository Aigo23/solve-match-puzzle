import sys
import copy
import solve
import set
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mainwidget import Ui_Form

class MatchWidget(QWidget,Ui_Form):
    def __init__(self):
        super(MatchWidget,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Match Moving Game')
        self.setMinimumSize(1000,800)
        self.setMaximumSize(1000,800)
        self.move(200,0)
        self.problem = []
        self.result = []
        self.match = [0]*45
        self.matchlist=[self.match_1, self.match_2, self.match_3, self.match_4, self.match_5, self.match_6, self.match_7,
                   self.match_8, self.match_9, self.match_10, self.match_11, self.match_12, self.match_13, self.match_14,
                   self.match_15, self.match_16, self.match_17, self.match_18, self.match_19, self.match_20,self.match_21,
                   self.match_22, self.match_23, self.match_24, self.match_25, self.match_26, self.match_27,self.match_28,
                   self.match_29, self.match_30, self.match_31, self.match_32, self.match_33, self.match_34,self.match_35,
                   self.match_36, self.match_37, self.match_38, self.match_39, self.match_40, self.match_41,self.match_42,
                   self.match_43, self.match_44, self.match_45]
        self.radioButtonList = [self.radioButton_1, self.radioButton_2]
        self.LcdList = [self.ansnum1, self.ansnum2, self.ansnum3, self.ansnum4, self.ansnum5, self.ansnum6]
        self.slm = QStringListModel()
        self.input.clicked.connect(self.Input)
        self.solvebutt.clicked.connect(self.getsolve)
        self.setproblem.clicked.connect(lambda: self.getset(1))
        self.list.clicked.connect(self.dig_disp)
        self.hidebutt.clicked.connect(self.hideans)
        self.setproblem_2.clicked.connect(lambda: self.getset(2))

        self.hideans()

    def hideans(self):
        self.groupBox_2.hide()
        self.list.hide()
        self.label_2.hide()

    def showans(self):
        self.groupBox_2.show()
        self.list.show()
        self.label_2.show()

    def showmatch(self):
        for i in range(45):
            if self.match[i] == 0:
                self.matchlist[i].setStyleSheet("border:1px dotted white;\n")
            else:
                if i == 42:
                    self.matchlist[i].setStyleSheet("border-image: url(:/newPrefix/resource/match_imag2.png);")
                    #self.matchlist[i].setStyleSheet("border-image: url(:/resource/match_imag2.png);")
                elif (i == 44):
                    self.matchlist[i].setStyleSheet("border-image: url(:/newPrefix/resource/match_imag3.png);")
                elif (i % 7 == 0 or i % 7 == 3 or i % 7 == 6 or i == 43):
                    self.matchlist[i].setStyleSheet("border-image: url(:/newPrefix/resource/match_imag.png);")
                else:
                    self.matchlist[i].setStyleSheet("border-image: url(:/newPrefix/resource/match_imag2.png);")
                    #self.matchlist[i].setStyleSheet("border-image: /pythonProject/resource/match_imag2.png;")

    def getsolve(self):
        str = ''.join(self.problem)
        if str == '':
            QMessageBox.about(self, "提示", "请先输入表达式")
            return
        start_time = time.time()
        self.result.clear()
        for i in range(2):
            if self.radioButtonList[i].isChecked():
                break
        self.result.extend(solve.SolveProblem(i+1, str))
        if len(self.result) == 0:
            QMessageBox.about(self, "提示", "此题无解")
        else:
            self.showans()
            for i in range(6):
                self.LcdList[i].display(self.result[0][i])
            self.anop1.setText(self.result[0][6])
            self.anop2.setText('=')
            data = []
            for i in range(0, len(self.result)):
                str = ''
                str += repr(self.result[i][0]) + repr(self.result[i][1])
                str += self.result[i][6]
                str += repr(self.result[i][2]) + repr(self.result[i][3]) + '='
                str += repr(self.result[i][4]) + repr(self.result[i][5])
                data.append(str)
            self.slm.setStringList(data)
            self.list.setModel(self.slm)
            end_time = time.time()
            QMessageBox.about(self, "提示", "共搜索到"+ repr(len(self.result)) + '个答案，用时'
                              + repr(round(end_time - start_time, 3)) + '秒')

    def getset(self, mode):
        self.hideans()
        self.lineEdit.clear()
        for i in range(2):
            if self.radioButtonList[i].isChecked():
                break
        if mode == 1:
            equ = set.SetProblem(i+1)
        elif mode == 2:
            equ = set.randequ()
        self.problem.clear()
        self.problem.extend([repr(equ[0]), repr(equ[1]), equ[6], repr(equ[2]),
                             repr(equ[3]), '=', repr(equ[4]), repr(equ[5])])
        self.match.clear()
        for i in range(6):
            self.match.extend(list(solve.numstr[equ[i]]))
        for i in range(42):
            if self.match[i] == '0':
                self.match[i] = 0
            else:
                self.match[i] = 1
        if equ[6] == '+':
            self.match.extend([1, 1, 0])
        elif equ[6] == '-':
            self.match.extend([0, 1, 0])
        else:
            self.match.extend([0, 0, 1])
        self.showmatch()
        if mode == 2:
            for i in range(1,2):
                res = solve.SolveProblem(i,self.problem)
                if len(res)!=0: break
            self.radioButtonList[i-1].setChecked(True)
            QMessageBox.about(self, "提示", "已成功随机生成成立等式\n该题目至少移动"+repr(i)+
                              "根火柴\n系统评估本题难度为"+repr(i-0.1*len(res)));

    def Input(self):
        self.hideans()
        str = self.lineEdit.text()
        self.lineEdit.clear()
        flag = 1
        if len(str)!=8: flag = 0
        else:
            for i in [0,1,3,4,6,7]:
                if str[i]<'0' or str[i]>'9':
                    flag = 0
            if str[2] != '+' and str[2] != '-' and str[2] != '*':
                flag = 0
            if str[5]!='=': flag = 0
        if flag == 0:
            QMessageBox.about(self, "ERROR", "输入表达式有误！请输入两位数以内的加减法等式")
        else:
            self.problem.clear()
            self.problem.extend(list(str))
            self.match.clear()
            for i in [0, 1, 3, 4, 6, 7]:
                self.match.extend(list(solve.numstr[ord(str[i]) - ord('0')]))
            for i in range(42):
                if self.match[i] == '0': self.match[i] = 0
                else: self.match[i] = 1
            if str[2] == '+':
                self.match.extend([1,1,0])
            elif str[2] == '-':
                self.match.extend([0,1,0])
            else:
                self.match.extend([0,0,1])
            self.showmatch()

    def dig_disp(self,index):
        self.LcdList[0].display(ord(index.data()[0]) - ord('0'))
        self.LcdList[1].display(ord(index.data()[1]) - ord('0'))
        self.LcdList[2].display(ord(index.data()[3]) - ord('0'))
        self.LcdList[3].display(ord(index.data()[4]) - ord('0'))
        self.LcdList[4].display(ord(index.data()[6]) - ord('0'))
        self.LcdList[5].display(ord(index.data()[7]) - ord('0'))
        self.anop1.setText(index.data()[2])
        if index.data()[2] == '*':
            self.anop1.setText('×')
        self.anop2.setText('=')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_pyqt_form = MatchWidget()
    my_pyqt_form.show()
    sys.exit(app.exec_())
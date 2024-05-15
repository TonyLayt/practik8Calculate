# -*- coding: utf-8 -*-
"""
Created on Thu May  9 22:04:42 2024

@author: Kuzn
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from untitled import Ui_FormCalculator
import re

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FormCalculator()
        self.ui.setupUi(self)
        self.chekPoint = False
        self.chekOperators = False
        self.butnBlock = True 
        self.num = 1
        
        self.ui.btn_0.clicked.connect(lambda: self.addDigit("0"))
        self.ui.btn_1.clicked.connect(lambda: self.addDigit("1"))
        self.ui.btn_2.clicked.connect(lambda: self.addDigit("2"))
        self.ui.btn_3.clicked.connect(lambda: self.addDigit("3"))
        self.ui.btn_4.clicked.connect(lambda: self.addDigit("4"))
        self.ui.btn_5.clicked.connect(lambda: self.addDigit("5"))
        self.ui.btn_6.clicked.connect(lambda: self.addDigit("6"))
        self.ui.btn_7.clicked.connect(lambda: self.addDigit("7"))
        self.ui.btn_8.clicked.connect(lambda: self.addDigit("8"))
        self.ui.btn_9.clicked.connect(lambda: self.addDigit("9"))
        self.ui.btn_del.clicked.connect(lambda: self.clearAll())
        self.ui.btn_backspace.clicked.connect(lambda: self.backspace())
        self.ui.btn_point.clicked.connect(lambda: self.setPoint())
        self.ui.btn_plus.clicked.connect(lambda: self.mathematicalOperator("+"))
        self.ui.btn_minus.clicked.connect(lambda: self.mathematicalOperator("-"))
        self.ui.btn_multiply.clicked.connect(lambda: self.mathematicalOperator("*"))
        self.ui.btn_divide.clicked.connect(lambda: self.mathematicalOperator("/"))
        self.ui.btn_equal.clicked.connect(lambda: self.mathematicalOperator("="))
        
    def addDigit (self, text_btn):
        if self.ui.lineEdit.text() == '0':
            self.ui.lineEdit.setText(text_btn)
            self.chekOperators = False
        else:
            self.ui.lineEdit.setText(self.ui.lineEdit.text() + text_btn)
            self.chekOperators = False
    
    def clearAll(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit.setText("0")
        self.chekPoint = False
        if self.butnBlock == False:
            self. mathematicalOperator("Unblock")
    
    def backspace(self):
        if self.ui.lineEdit.text() != '0':
            self.ui.lineEdit.backspace()
        if not self.ui.lineEdit.text():
            self.ui.lineEdit.setText("0")
        
    def setPoint(self):
        if self.chekPoint == False:
            self.ui.lineEdit.setText(self.ui.lineEdit.text() + ".")
            self.chekPoint = True
            
    def splitExpression(self, expression):
        parts = re.findall(r'(\d+\.\d+|\d+|[+-/*])', expression)
        inclusive = []
        checOper = False 

        for i in range (len (parts)):
        
            if checOper == True:
                inclusive.append(parts[i]) 
            elif parts[0] == "-" and checOper == False:
                inclusive.append(parts[0] + parts[1])
                checOper = True
            else: 
                inclusive.append(parts[i]) 
                
        if checOper == True:
            inclusive.pop(1)
                
        return inclusive
    
    def mathematicalOperator(self, operator):
    
        expression = self.ui.lineEdit.text()
        
        if operator != "=" and "." in expression and expression.endswith("."):
            self.ui.lineEdit.setText(expression + "0" + operator)
            return
        
        if operator != "=" and self.chekOperators == False and operator != "Unblock":
            if operator == "-" and expression == "0" and self.chekOperators == False:
                self.ui.lineEdit.setText(operator)
                self.chekOperators = True
            else:
                self.ui.lineEdit.setText(expression + operator)
                self.chekPoint = False
                self.chekOperators = True
        else:
            try:
          
                parts = self.splitExpression(expression)
                print (parts)
                
                if "." in self.ui.lineEdit.text():
                    result = float(parts[0])
                else:
                    result = int(parts[0])
                            
                for i in range(1, len(parts), 2):
                                
                    op = parts[i]
                    if "." in self.ui.lineEdit.text():
                        self.num = float(parts[i+1])
                    else:
                        self.num = int(parts[i+1])
                                           
                    if op == '+':
                        result += self.num
                    elif op == '-':
                        result -= self.num
                    elif op == '*':
                        result *= self.num
                    elif op == '/':
                        if self.num == 0:
                            result = "WTF :D"
                        else:
                            result /= self.num   
            except:  None
                       
            if self.num == 0 or operator == "Unblock":
                if self.num == 0:
                    self.butnBlock = False
                    self.ui.lineEdit.setText(str(result))
                    
                if operator == "Unblock":
                    self.butnBlock = True
                
                self.ui.btn_0.setEnabled(self.butnBlock)
                self.ui.btn_1.setEnabled(self.butnBlock)
                self.ui.btn_2.setEnabled(self.butnBlock)
                self.ui.btn_3.setEnabled(self.butnBlock)
                self.ui.btn_4.setEnabled(self.butnBlock)
                self.ui.btn_5.setEnabled(self.butnBlock)
                self.ui.btn_6.setEnabled(self.butnBlock)
                self.ui.btn_7.setEnabled(self.butnBlock)
                self.ui.btn_8.setEnabled(self.butnBlock)
                self.ui.btn_9.setEnabled(self.butnBlock)
                self.ui.btn_backspace.setEnabled(self.butnBlock)
                self.ui.btn_point.setEnabled(self.butnBlock)
                self.ui.btn_plus.setEnabled(self.butnBlock)
                self.ui.btn_minus.setEnabled(self.butnBlock)
                self.ui.btn_multiply.setEnabled(self.butnBlock)
                self.ui.btn_divide.setEnabled(self.butnBlock)
                self.ui.btn_equal.setEnabled(self.butnBlock)
            else: self.ui.lineEdit.setText(str(round(result, 6)))
            self.chekOperators = False
        
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
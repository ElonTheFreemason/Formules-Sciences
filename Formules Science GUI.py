from tkinter import *
from tkinter.messagebox import *
import math
from xml.etree import ElementTree as ET
import re
from decimal import Decimal


#-----------------------------------------------------------------------MAIN VARIABLES-------------------------------------------------------------------------
tree = ET.parse('formulas.xml')  
root = tree.getroot()
items = []
lastVariables = []


#-------------------------------------------------------------------------FUNCTIONS-------------------------------------------------------------------------
def formula_search (doc, svar):
    return doc.findall('.//function[@name="' + svar + '"]...')

def list_variables (fnode, svar):
    list_var = {}
    for child in fnode.iter('var'):
        if (child.attrib.get("name") != svar):
            list_var[str(child.attrib.get("name"))] = 0
    return(list_var)

def get_equation (fnode, svar):
    equation_node = fnode.find('./function[@name="' + svar + '"]')
    return (equation_node.attrib.get('equation'))

def reset():
    all_widgets = main.grid_slaves()
    for widget in all_widgets:
        if(widget.config("text")[-1] != "What are you searching? " and widget != formula and widget.config("text")[-1] != " "):
            widget.destroy()
    next_step = Button(main, text="Next", command=get_formula, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=1, column=1, sticky=W, pady=4)
    history = Button(main, text="Previous answers", command=showHistory, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=0, column=10, sticky=W, pady=4)
    formula.delete(0, END)

def reset_error_msg():
    all_widgets = main.grid_slaves()
    for widget in all_widgets:
        if(widget.config("text")[-1] == "We don't have the formula to find that variable..." or widget.config("text")[-1] == "Please enter a number"):
            widget.destroy()

def get_unit (fnode, svar):
    unit_node = fnode.find('./var[@name="' + svar + '"]')
    return (unit_node.attrib.get('unit'))

def showHistory():
    iterator=1
    Label(main, text="  PREVIOUS ANSWERS", font="Consolas 10", bg="#c2d1e8").grid(row=0, column=4)
    global lastVariables
    while(len(lastVariables) > 5):
        del(lastVariables[0])
    for i in lastVariables:
        Label(main, text=i, font="Consolas 10", bg="#c2d1e8").grid(row=iterator, column=4)
        iterator+=1
    all_widgets = main.grid_slaves()
    for widget in all_widgets:
        if(widget.config("text")[-1] == "Previous answers"):
            widget.destroy()

def selectEquation(btnText):
    searched_variable = formula.get()
    items = formula_search(root, searched_variable)
    selected_equation = btnText[0]
    formula_node = items[int(selected_equation) - 1]
    lvar = list_variables(formula_node, searched_variable) 
    svar_unit = get_unit(formula_node, searched_variable)

    all_widgets = main.grid_slaves()
    for widget in all_widgets:
        if(widget.config("text")[-1] != "What are you searching? " and widget != formula and widget.config("text")[-1] != " "):
            widget.destroy()
    history = Button(main, text="Previous answers", command=showHistory, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=0, column=10, sticky=W, pady=4)

    i = 1
    textBoxes = []
    for qvar in lvar.items():
        qvar_unit = get_unit(formula_node, qvar[0])
        Label(main, text = "Enter the value of " + qvar[0] + " in " + qvar_unit + " : ", font="Consolas 10", bg="#c2d1e8").grid(row=i)
        varBox = Entry(main, font="Consolas 10", borderwidth=3, relief="sunken")
        varBox.grid(row=i, column=1)
        textBoxes.append(varBox)
        i += 1 

    def show_answer():
        try:
            reset_error_msg()
            variables = []
            for textBox in textBoxes:
                variables.append(textBox.get())
            s_equation = get_equation(formula_node, searched_variable) 
            i2 = 0
            for qvar in lvar.items():
                lvar[qvar[0]] = float(variables[i2])
                i2 += 1
                s_equation = s_equation.replace(qvar[0], str(lvar[qvar[0]]))                 
        except:
            reset_error_msg()
            error = Label(main, text = "Please enter a number", fg="red", font="Consolas 10", bg="#c2d1e8").grid(row=0, column=3) 
            
        ans = eval(s_equation)
        if(ans >= 10000 or ans < 0.001):
            s_answer = '%.2E' % Decimal(ans)
        else:
            s_answer = str(round(ans, 2))
        string_answer = searched_variable + " has a value of " + s_answer + svar_unit
        label_answer = Label(main, text=string_answer, font="Consolas 10", bg="#c2d1e8").grid(row=0, column=3)
        reset_window = Button(main, text='Next variable', command=reset, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=i + 1, column=1, sticky=W, pady=4)
        global lastVariables
        txtToAdd = searched_variable + " = " + s_answer + svar_unit
        lastVariables.append(txtToAdd)
        print(lastVariables)

    show_ans = Button(main, text='Show answer', command=show_answer, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=i + 1, column=1, sticky=W, pady=4)

def get_formula():
    reset_error_msg()
    all_widgets = main.grid_slaves()
    for widget in all_widgets:
        if(widget.config("text")[-1] == "Next"):
            widget.destroy()

    searched_variable = formula.get()
    items = formula_search(root, searched_variable)

    if (len(items) == 0):
        varError = Label(main, text = "We don't have the formula to find that variable...", fg="red", font="Consolas 10", bg="#c2d1e8").grid(row=0, column=3)
        next_step = Button(main, text="Next", command=get_formula, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=1, column=1, sticky=W, pady=4)

    elif(len(items) == 1):
        formula_node = items[0]
        svar_unit = get_unit(formula_node, searched_variable)
        lvar = list_variables(formula_node, searched_variable) 

        i = 2
        textBoxes = []
        for qvar in lvar.items():
            qvar_unit = get_unit(formula_node, qvar[0])
            Label(main, text = "Enter the value of " + qvar[0] + " in " + qvar_unit + " : ", font="Consolas 10", bg="#c2d1e8").grid(row=i)
            varBox = Entry(main, font="Consolas 10", borderwidth=3, relief="sunken")
            varBox.grid(row=i, column=1)
            textBoxes.append(varBox)
            i += 1   
        
        def show_answer():
            try:
                reset_error_msg()
                variables = []
                for textBox in textBoxes:
                    variables.append(textBox.get())
                s_equation = get_equation(formula_node, searched_variable) 
                i2 = 0
                for qvar in lvar.items():
                    lvar[qvar[0]] = float(variables[i2])
                    i2 += 1
                    s_equation = s_equation.replace(qvar[0], str(lvar[qvar[0]]))                 
            except:
                reset_error_msg()
                error = Label(main, text = "Please enter a number", fg="red", font="Consolas 10", bg="#c2d1e8").grid(row=0, column=3) 
            
            ans = eval(s_equation)
            if(ans >= 10000 or ans < 0.001):
               s_answer = '%.2E' % Decimal(ans)
            else:
               s_answer = str(round(ans, 2))
            string_answer = searched_variable + " has a value of " + s_answer + svar_unit
            label_answer = Label(main, text=string_answer, font="Consolas 10", bg="#c2d1e8").grid(row=0, column=3)
            reset_window = Button(main, text='Next variable', command=reset, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=i + 1, column=1, sticky=W, pady=4)
            global lastVariables
            txtToAdd = searched_variable + " = " + s_answer + svar_unit
            lastVariables.append(txtToAdd)
            print(lastVariables)

        show_ans = Button(main, text='Show answer', command=show_answer, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=i + 1, column=1, sticky=W, pady=4)
    
    elif(len(items) > 1):
        i3 = 1
        for i in range(0, len(items)):            
            s_equation = get_equation(items[i], searched_variable)
            text = str(i + 1) + " - " + s_equation
            equation = Button(main, text=text, command=lambda s=text: selectEquation(s), font="Consolas 10", borderwidth=3, relief="ridge")
            equation.grid(row=i3, column=1, sticky=W, pady=4)
            i3 += 1   


#----------------------------------------------------------------------CREATING THE GUI----------------------------------------------------------------------
main = Tk()
main.title("Science Formulas")
main.iconbitmap("icon.ico")

question = Label(main, text = "What are you searching? ", font="Consolas 10", bg="#c2d1e8").grid(row=0)
question = Label(main, text = " ", font="Consolas 10", bg="#c2d1e8").grid(row=0, column=5)

formula = Entry(main, font="Consolas 10", borderwidth=3, relief="sunken")
formula.grid(row=0, column=1)

next_step = Button(main, text="Next", command=get_formula, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=1, column=1, sticky=W, pady=4)
history = Button(main, text="Previous answers", command=showHistory, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=0, column=10, sticky=W, pady=4)

main.configure(background="#c2d1e8")

mainloop()
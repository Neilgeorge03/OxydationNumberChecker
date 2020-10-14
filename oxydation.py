import pandas as pd
import re
import tkinter as tk

main = pd.read_csv(r'/home/neil/Documents/Programing/polyatomic_ions.csv') #convert csv containing polyatomic ions into dictionary
polyatomic = pd.DataFrame(main, columns=["Chemical_Symbol","Oxidation_Number"])
symbol = polyatomic.Chemical_Symbol.to_list()
oxydation = polyatomic.Oxidation_Number.to_list()
Dictionary = dict(zip(symbol,oxydation))

main = pd.read_csv(r'/home/neil/Documents/Programing/Periodic Table.csv') #convert csv file with periodic table into a dictionary 
periodic = pd.DataFrame(main, columns=["Symbol","NumberofValence"])
symbol1 = periodic.Symbol.to_list()
valence = periodic.NumberofValence.to_list()
PeriodicTable = dict(zip(symbol1,valence))


def PolyAtomicIons(Formula): #detect and remove polyatomic ions contained in the chemical reaction
    for chemequation in symbol: #goes through all the polyatomic ions contained in the list
        chemequation1 = str(chemequation)+str(Dictionary[chemequation])
        if chemequation1 == Formula:
            return Formula
        elif chemequation in Formula: #checks if the polyatomic ion is contained in the chemical formula provided by the user
            charge = Dictionary[chemequation] #gives the value of the ionic charge of the polyatomic ion
            leftover = Formula.replace(chemequation,"") #removess the polyatomic ion from the equation
            for n in range(1,10): #checks if the chemical formula contain more than one of the same polyatomic ion (I.e. (OH)2)
                names1 = "("+chemequation+")"+str(n)
                if names1 in Formula:
                    charge = str(Dictionary[chemequation])[::-1]
                    charge = n*(int(charge))
                    charge = str(charge)[::-1]
                    leftover = Formula.replace(names1,"")
            if "-" in charge: #changes the charges to give the correct charge as the output
                charge1 = charge.replace("-", "+") 
            elif "+" in charge:
                charge1 = charge.replace("+", "-")
            else:
                charge1 = charge+"-"
            if len(leftover) == 0:
                return (str(ChargeChecker(chemequation,charge)))
            else: 
                return str(ChargeChecker(chemequation,charge)) + "    " +str(ChargeChecker(leftover, charge1))

    else: #doesn't exist returns the original formula
        return (ChargeChecker(Formula,str(0)))

def ChargeChecker(equation1, charge1):
    for ncharge in range(1,10):
        if str(ncharge)+"+" in equation1:
            charge1 = str(ncharge)+"+"
            equation1 = equation1.replace(charge1, "")
        elif str(ncharge)+"-" in equation1:
            charge1 = str(ncharge)+"-"
            equation1 = equation1.replace(charge1, "")
    if str(IonicBonds(equation1, charge1)) == "None":
        return equation1+"^"+charge1
    else:
        return IonicBonds(equation1, charge1) 
    return IonicBonds(equation1, charge1)


def IonicBonds(equation, charge): #seperates regular ones ionic equations
    allatoms = re.findall('[A-Z][^A-Z]*', equation)    
    for atoms in symbol1:
        if equation == "H2O2":
            return ("2H+ + 2O+")
        for times in range(1,100):
            newatom = atoms+str(times)
            if newatom in allatoms:  
                atom = newatom
                if PeriodicTable[atoms] >5:
                    negativecharge = times * (8-int(PeriodicTable[atoms]))
                    positivecharge = -1*(0 - negativecharge - int(str(charge)[::-1]))
                    return (equation.replace(atom,"")+"^"+str(positivecharge)+"+"+"   " + str(atoms)+str(times)+"^"+str(negativecharge)+"-")
                    equation = equation.replace(atom,"")
                elif PeriodicTable[atoms] == "nan":
                    print("Cu2SO4")
                    return equation + "^" + charge
                for atom in allatoms:
                    if PeriodicTable[atoms] <=6 and PeriodicTable[atoms] >= 3:
                        negativecharge = times * (8-int(PeriodicTable[atoms]))
                        positivecharge = -1*(0 - negativecharge - int(str(charge)[::-1]))
                        return (equation.replace(atom,"")+"^"+str(positivecharge)+"+"+"   " + str(atoms)+str(times)+"^"+str(negativecharge)+"-")
                        equation = equation.replace(newatom,"")
                
            elif atoms in allatoms:
                if PeriodicTable[atoms] >5:
                    negativecharge = (8-int(PeriodicTable[atoms]))
                    positivecharge = -1*(0 - negativecharge - int(str(charge)[::-1]))
                    return (equation.replace(atoms,"")+"^"+str(positivecharge)+"+"+"   " + str(atoms)+"^"+str(negativecharge)+"-")
                    equation = equation.replace(atoms,"")
                    
                elif PeriodicTable[atoms] <=6 and PeriodicTable[atoms] >= 3:
                    negativecharge = (8-int(PeriodicTable[atoms]))
                    positivecharge = -1*(0 - negativecharge - int(str(charge)[::-1]))
                    #return (equation.replace(atoms,"")+"^"+str(positivecharge)+"+"+"   " + str(atoms)+str(times)+"^"+str(negativecharge)+"-")
                    #equation = equation.replace(atoms,"")
                    
                     
    
    

thingy=""
count = 0
Formula = input("What's the equation you want to look at?\n")

Formula = Formula.split(" + ")
for things in Formula:
    if count<1: #add seperator 
        thingy += str(PolyAtomicIons(things))
        count += 1
    else:
        thingy += " + " + PolyAtomicIons(things)
print("It gives: "+thingy)
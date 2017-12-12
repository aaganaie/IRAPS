import tkinter as tk
from tkinter import StringVar
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn import linear_model
from tkinter import ttk
from matplotlib import style
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
style.use("ggplot")

f=Figure(figsize=(5,5),dpi=100)
A=f.add_subplot(111)
    
LARGE_FONT=("Verdana",20)

def builtin_analysis(self):
    
    
    Dataset.groupby("YEAR").sum()['ANNUAL'].plot(figsize=(13,10))
    #plt.show()

    Dataset.hist(figsize=(20,20))
    #plt.show()


    Dataset[['YEAR','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']].groupby('YEAR').sum().plot(figsize=(15,12))
    #plt.show()

    Dataset.groupby('SUBDIVISION').sum()['ANNUAL'].plot(kind='bar',figsize=(15,10))
    plt.show()

def ANALYSE(subdivision,year1,year2,self):
    year=[]
    
    for i in range(year1,year2+1):
        year.append(i)
    a=[]
    a=Dataset.ANNUAL[ (Dataset.YEAR>=year1) & (Dataset.YEAR<=year2) &(Dataset.SUBDIVISION==subdivision) ].values
    np.array(a)
    np.array(year)
    A.clear()
    A.plot(year,a)
    title="Analysis of "+subdivision+" from "+str(year1)+" to "+str(year2)
    A.set_title(title)
    A.set_ylabel('Rainfall (mm)')
    A.set_xlabel("Year")
       
    canvas=FigureCanvasTkAgg(f,self)
    canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
    
    canvas.show()
    

    toolbar=NavigationToolbar2TkAgg(canvas,self)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

def predict(Predict_District,Predict_Year,Predict_month,self):

    

    data=Dataset[Dataset.SUBDIVISION==Predict_District ]
    Features=[]
    Target=[]
    Features=data[['SUBDIVISION','YEAR']].values
    Target=data[[Predict_month]].values
    scaler=LabelEncoder()
    Features[:,0]=scaler.fit_transform(Features[:,0])
    model=linear_model.LinearRegression()
    X_train,X_test,y_train,y_test=train_test_split(Features,Target,test_size=0.3)
    model.fit(X_train,y_train)
    pd=X_train[0][0]
    Predict=model.predict([[pd,Predict_Year]])
    #print("Predicted Rainfall of given subdistrict is = ",Predict[0][0].astype(int))
    msg="Predicted Rainfall of given subdistrict is = "+str(Predict[0][0].astype(int))+" mm "
    button2=ttk.Button(self,text="Start Predicting ",
                          command=lambda: popupmsg(msg))
    button2.pack()
    
    


class IRAPS(tk.Tk):

    def __init__(self, *args,**kwargs):

        tk.Tk.__init__(self,*args,**kwargs)
        #tk.Tk.iconbitmap(self,default="Final IRAPS Logo No Seal.ico")
        
        container=tk.Frame(self)
        container.pack(side='top',fill='both',expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}

        for F in (StartPage,Pageone,Pagetwo,Pagethree):
            
            frame=F(container,self)

            self.frames[F]=frame

            frame.grid(row=0,column=0,sticky='nsew')
        self.show_frame(StartPage)


    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()

def popupmsg(msg):

##    def leavemini():
##        popup.destroy()
##    
    popup=tk.Tk()
    popup.wm_title("Predicted value ")
    label=ttk.Label(popup,text=msg,font=LARGE_FONT)
    label.pack(side="top",fill='x',pady=10)
    b1=ttk.Button(popup,text="OK",command=popup.destroy)
    b1.pack()
    popup.mainloop()

class StartPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text='''Welcome to IRAPS

                    We help you to analyse and predict Rainfall

                    Given are options to Select your choice .

                    Built-in Graphs are the Graphs we have build to show few analysis on given Data

                    Analyse will take user given inputs for Analysis

                    Prediction will help user to Predict future rainfall in District ''',font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="View Built-in Graphs",command=lambda: controller.show_frame(Pageone))
        button1.pack()
        button2=ttk.Button(self,text="Analysis",
                          command=lambda: controller.show_frame(Pagetwo))
        button2.pack()

        button3=ttk.Button(self,text="Prediction",
                          command=lambda: controller.show_frame(Pagethree))
        button3.pack()



class Pageone(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=ttk.Label(self,text='''We have plotted few graphs from Dataset to show you how different
                                    analysis we can do with Data''',font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="Show Graphs",command=lambda: builtin_analysis(self))
        button1.pack()

        
        button2=ttk.Button(self,text="Back To Main Page",
                          command=lambda: controller.show_frame(StartPage))
        button2.pack()
        


class Pagetwo(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=ttk.Label(self,text='''Analyse our own graphs:-
                                    First dropdown will help you to select Subdivision
                                    Second dropdown will help you to select Year1
                                    Third dropdown will help you to select Year2

                                    Click Analyse after selecting inputs ''',font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        options1=Dataset.SUBDIVISION.value_counts()
        options1=options1.index
        variable = StringVar()
        variable.set("ANDAMAN & NICOBAR ISLANDS") # default value

        b1 = tk.OptionMenu(self, variable, *options1)
        b1.pack()
        Data=Dataset[Dataset.SUBDIVISION==variable.get() ]
        options2=Data.YEAR.value_counts()
        options2=list(options2.index)
        #options2.sort()
        
        variable1 = StringVar()
        #variable1.set("1901")
        b2 = tk.OptionMenu(self, variable1, *options2)
        b2.pack()

        variable2= StringVar()
        #variable2.set("1901") # default value

        b3 = tk.OptionMenu(self, variable2, *options2)
        b3.pack()

        
        button1=ttk.Button(self,text="Analyse",command=lambda: ANALYSE(variable.get(),int(variable1.get()),int(variable2.get()),self))
        button1.pack()

        
        button2=ttk.Button(self,text="Back To Main Page",
                          command=lambda: controller.show_frame(StartPage))
        button2.pack()
        
    
    
class Pagethree(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=ttk.Label(self,text='''Predict Future values:-
                                    First dropdown will help you to select Subdivision
                                    Second dropdown will help you to select Year
                                    Third dropdown will help you to select Month

                                    Click Predict after selecting inputs ''',font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        options1=Dataset.SUBDIVISION.value_counts()
        options1=options1.index
        variable = StringVar()
        variable.set("ANDAMAN & NICOBAR ISLANDS") # default value

        b1 = tk.OptionMenu(self, variable, *options1)
        b1.pack()

        options2=[2018,2019,2020,2021]
        variable1 = StringVar()
        variable1.set("2018")
        b2 = tk.OptionMenu(self, variable1, *options2)
        b2.pack()

        options3=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
        variable2 = StringVar()
        variable2.set("JAN")
        b3 = tk.OptionMenu(self, variable2, *options3)
        b3.pack()

        button1=ttk.Button(self,text="OK",command=lambda: predict(variable.get(),int(variable1.get()),variable2.get(),self))
        button1.pack()
        
        button2=ttk.Button(self,text="Back To Main Page",
                          command=lambda: controller.show_frame(StartPage))
        button2.pack()
                
        
        
Dataset=pd.read_csv(r'Data/rainfall in india 1901-2015.csv')
Dataset=Dataset.fillna(value=0)
#print(Dataset.head(50))

app=IRAPS()
app.title("IRAPS")
app.geometry("1280x720")
app.mainloop()

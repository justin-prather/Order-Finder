from Tkinter import *
from datetime import datetime, timedelta

color2 = '#9A9A9A'
color= '#EF6C6C'
window_title = 'Order Finder'

def SetDate_Today():
    d=datetime.today()
    year.set(d.strftime('%Y'))
    month.set(d.strftime('%B'))
    day.set(d.strftime('%d'))

def SetDate_Tomorrow():
    d = datetime.today() + timedelta(days=1)
    year.set(d.strftime('%Y'))
    month.set(d.strftime('%B'))
    day.set(d.strftime('%d'))

def Execute_Search():
    print 'Searching!'

def AddRider():
    List_Riders.insert(END, Input_Rider.get())
    Input_Rider.delete(0, END)

def AddHorse():
    List_Horses.insert(END, Input_Horse.get())
    Input_Horse.delete(0, END)

def Automate_Search():
    print 'Automate Search!'

def Clear_Params():
    day.set('Day')
    month.set('Month')
    year.set('Year')

    Tournament.set('Tournament')

    Input_Rider.delete(0, END)
    Input_Horse.delete(0, END)

    List_Riders.delete(0, END)
    List_Horses.delete(0, END)

master = Tk()

dimensions = '700x450'

master.geometry( dimensions )
master.config( background=color )
master.title( window_title )
master.resizable( 0, 0 )

''' Main Label '''
Main_Label = Label( text='Order Finder', bg=color, font=( '', 20))
Main_Label.pack( side='top' )

'''Frames'''
Top_Container = Frame( master, height=20, bg=color2, relief=RAISED, bd=2 )
Top_Container.pack( side='top', fill=X, padx=10, pady=5 )

Second_Container = Frame( master, height=20, bg=color2, relief=RAISED, bd=2 )
Second_Container.pack( side='top', fill=X, padx=10, pady=5 )

Third_Container = Frame( master, height=20, bg=color2, relief=RAISED, bd=2 )
Third_Container.pack( fill=X, side='top', padx=10, pady=5 )

Rider_Container = Frame( master, height=20, bg=color2, relief=RAISED, bd=2 )
Rider_Container.pack( side='left', padx=5, pady=5, expand=True )

Fourth_Container = Frame( master, height=20, bg=color2, relief=RAISED, bd=2 )
Fourth_Container.pack( side='left', padx=5, pady=5, expand=True )

Horse_Container = Frame( master, height=20, bg=color2, relief=RAISED, bd=2 )
Horse_Container.pack( side='right', padx=5, pady=5, expand=True )

''' Labels '''
FE_Label = Label( Top_Container, text='Tournament: ', bg=color2)
FE_Label.pack(side='left', padx=5 )

SE_Label = Label( Second_Container, text='Date: ', bg=color2 )
SE_Label.pack(side='left', padx=5)

Rider_Label = Label( Rider_Container, text='Riders:', bg=color2)
Rider_Label.pack(padx=5, pady=5)

Horse_Label = Label( Horse_Container, text='Horses:', bg=color2)
Horse_Label.pack(padx=5, pady=5)

'''Input fields'''
Input_Rider = Entry( Third_Container, highlightbackground=color2)
Input_Rider.pack( side='left', padx=5)

Add_Rider = Button(Third_Container, highlightbackground=color2, text='Add Rider', command=AddRider)
Add_Rider.pack(side='left', padx=5)

Add_Horse = Button(Third_Container, highlightbackground=color2, text='Add Horse', command=AddHorse)
Add_Horse.pack(side='right', padx=5)

Input_Horse = Entry( Third_Container, highlightbackground=color2)
Input_Horse.pack(side='right', padx=5)

'''Dropdown menu'''
Year = [ '2012', '2013', '2014' ]
Months = ['January', 'Febuary', 'March', 'April', 'May','June', 'July', 'August', 'September', 'October', 'November', 'December']
Days = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]

Tournaments = { 'National':None, 'Contintal':None, 'Canada One':None, 'North American':None, 'PanAmerican':None}

day = StringVar()
month = StringVar()
year = StringVar()
day.set('Day')
month.set('Month')
year.set('Year')

Tournament = StringVar()
Tournament.set('Tournament')

Year_DD = apply(OptionMenu, (Second_Container, year) + tuple(Year) )
Year_DD.config(bg=color2, command=None )
Year_DD.pack(side='left', padx=5)

Month_DD = apply(OptionMenu, (Second_Container, month) + tuple(Months) )
Month_DD.config(bg=color2, command=None)
Month_DD.pack(side='left', padx=5)

Day_DD = apply(OptionMenu, (Second_Container, day) + tuple(Days) )
Day_DD.config(bg=color2, command=None)
Day_DD.pack(side='left', padx=5)

Tournament_DD = apply(OptionMenu, (Top_Container, Tournament) + tuple(Tournaments.keys()))
Tournament_DD.config(bg=color2, command=None)
Tournament_DD.pack(side='left', padx=5 )

'''Listboxes'''
List_Riders = Listbox(Rider_Container)
List_Riders.pack( padx=5, pady=5)

List_Horses = Listbox(Horse_Container)
List_Horses.pack( padx=5, pady=5)

'''Buttons'''
Today = Button(Second_Container, highlightbackground=color2, text='Today', command=SetDate_Today)
Today.pack(side='left', padx=5)

Tomorrow = Button(Second_Container, highlightbackground=color2, text='Tomorrow', command=SetDate_Tomorrow)
Tomorrow.pack(side='left', padx=5)

Search = Button(Fourth_Container, highlightbackground=color2, text='Search', command=Execute_Search)
Search.pack(padx=5, pady=5)

Automate = Button(Fourth_Container, highlightbackground=color2, text='Automate', command=Automate_Search)
Automate.pack(padx=5, pady=5)

Clear = Button(Fourth_Container, highlightbackground=color2, text='Clear', command=Clear_Params)
Clear.pack(padx=5, pady=5)

Remove_Rider = Button(Rider_Container, highlightbackground=color2, text='Remove', command=lambda lb=List_Riders: List_Riders.delete(ANCHOR))
Remove_Rider.pack(padx=5, pady=5)

Remove_Horse = Button(Horse_Container, highlightbackground=color2, text='Remove', command=lambda lb=List_Horses: List_Horses.delete(ANCHOR))
Remove_Horse.pack(padx=5, pady=5)

mainloop()
# def callback():
#     print e.get()

# def print_it(event):
#     print var.get()

# e = Entry(master, highlightbackground=color)
# e.grid(row=0, column=0)

# b = Button(master, text="Print", command=callback, highlightbackground=color)
# b.grid(row=0, column=1)

# var = StringVar()
# var.set('Month')

# opm = OptionMenu( master, var, 'January', 'Febuary', 'March', 'April', 'May',
#     'June', 'July', 'August', 'September', 'October', 'November', 'December', command=print_it )
# opm.config(bg=color)
# opm.grid(row=3, column=0)

# mainloop()

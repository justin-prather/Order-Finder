from Tkinter import *
from datetime import datetime, timedelta
from tkFileDialog import askopenfilename, askdirectory
from Order_Parser import Order_Parser
from Download_Orders_Results import PDF_Downloader
import sys

color2 = '#43464B'
color= '#8A0707'
window_title = 'Order Finder'
default_fp = '~/Desktop'

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
    files = []

    downloader = PDF_Downloader()

    downloader.gen_tournament_link( Tournaments.get(Tournament.get()), datetime.strptime( str(year.get() + month.get() 
        + day.get()), '%Y%B%d').date() )

    downloader.filePath = FP_Label['text']+'/'

    downloader.get_PDF_links()
    try:
        files = downloader.download_orders()
    except IOError:
        print 'Enter a valid file path'
        return
    for order in files:
    # for name in get_items( RiderVar.get() ):
        # for order in files:
        Order = Order_Parser( order )
        print Order.Parse_PDF()
        print Order.Order_Content()
        for name in get_items( RiderVar.get() ):
            # print 'searching for: ' + name
            text = ''
            try:
                text = Order.get_order_by_rider( name )
            except IndexError:
                print 'Possible error searching ' + order + ' for ' + name
            if not text == "":
                print Order.info.get('Class')
                print Order.info.get('Date_Time')
                print Order.info.get('Ring_Table')
                print text

        for name in get_items( HorseVar.get() ):
            # print 'searching for: ' + name
            text = ''
            try:
                text = Order.get_order_by_horse( name )
            except IndexError:
                print 'Possible error searching ' + order + ' for ' + name
            if not text == "":
                print Order.info.get('Class')
                print Order.info.get('Date_Time')
                print Order.info.get('Ring_Table')
                print text

def get_items( string_list ):
    L = []
    while '\'' in string_list:
        start = string_list.index('\'')+1
        end = string_list.index('\'', start )
        L.append(string_list[start:end])
        string_list = string_list[end+1:]
    return L

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

def change_fp():
    fp = askdirectory()
    FP_Label.config( text=fp)

master = Tk()

dimensions = '700x500'

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

FP_Container = Frame( master, bg=color2, relief=RAISED, bd=2 )
FP_Container.pack( side='top', fill=X, padx=10, pady=5 )

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

Directory = Label( FP_Container, text='Directory: ', bg=color2)
Directory.pack(side='left', padx=5, pady=5)

FP_Label = Label( FP_Container, text=default_fp, bg=color2)
FP_Label.pack(side='left', padx=5, pady=5)

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
Months = ['January', 'February', 'March', 'April', 'May','June', 'July', 'August', 'September', 'October', 'November', 'December']
Days = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31' ]

Tournaments = { 'Febuary Classic I':42, 'Febuary Classic II':13, 'Winter Farewell':14, 
    'Spring Welcome':20, 'April Classic':43, 'May Classic':19, 'National':23, 'Continental':25,
    'Canada One':26, 'North American':27, 'Pan American':41, 'Champions\' Welcome':40, 'Masters':29,
    'Harvest Classic':31, 'Oktoberfest':32}

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
RiderVar = StringVar()
List_Riders = Listbox(Rider_Container, listvariable=RiderVar)
List_Riders.pack( padx=5, pady=5)

HorseVar = StringVar()
List_Horses = Listbox(Horse_Container, listvariable=HorseVar)
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

Change = Button( FP_Container, highlightbackground=color2, text='Change', command=change_fp)
Change.pack(side='left', padx=5, pady=5)


mainloop()


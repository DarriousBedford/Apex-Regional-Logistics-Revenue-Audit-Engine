import tkinter
import tkinter.messagebox
import tkinter.font

FUEL_SURCHARGE = 2.75

class DispatchDashboard:
    def __init__(self, store_names):
        self.main_window=tkinter.Tk()
        self.main_window.title('Apex Dispatch Dashboard')

        # fram of the dashboard
        self.header_frame = tkinter.Frame(self.main_window)
        self.input_frame = tkinter.Frame(self.main_window)
        self.tier_frame = tkinter.Frame(self.main_window)
        self.button_frame = tkinter.Frame(self.main_window)
        self.store_frame = tkinter.Frame(self.main_window)
        self.rack_frame = tkinter.Frame(self.main_window)
        # the header
        self.header_label = tkinter.Label(self.header_frame, text='Shift Settlement', borderwidth=2, relief='ridge', width=40)

        self.header_label.pack()

        # miles input
        self.miles_label = tkinter.Label(self.input_frame, text='Miles:')
        self.miles_label.pack(side='left')
        self.miles_entry = tkinter.Entry(self.input_frame, width=10)
        self.miles_entry.pack(side='left')

        #payout display
        self.payout =tkinter.StringVar()
        self.payout_label = tkinter.Label(self.input_frame, textvariable=self.payout)
        self.payout_label.pack(side='left', ipadx=20, ipady=8)

        #tier selection
        self.tier = tkinter.IntVar()
        self.tier.set(1)
        self.tier_a = tkinter.Radiobutton(self.tier_frame, text='Tier A', variable=self.tier, value=1)
        self.tier_b = tkinter.Radiobutton(self.tier_frame, text='Tier B', variable=self.tier, value=2)
        self.tier_c = tkinter.Radiobutton(self.tier_frame, text='Tier C', variable=self.tier, value=3)
        self.tier_a.pack(side='left')
        self.tier_b.pack(side='left')
        self.tier_c.pack(side='left')

        #surcharge check
        self.surcharge = tkinter.IntVar()
        self.surcharge_check = tkinter.Checkbutton(self.tier_frame, text='Long-Haul surcharge', variable=self.surcharge)
        self.surcharge_check.pack(side='left')

        # store list
        self.store_list = tkinter.Listbox(self.store_frame, height=6, selectmode=tkinter.SINGLE)
        for name in store_names:
            self.store_list.insert(tkinter.END, name)
        self.store_list.bind('<<ListboxSelect>>', self.show_store)

        self.scrollbar = tkinter.Scrollbar(self.store_frame, orient=tkinter.VERTICAL)
        self.scrollbar.config(command=self.store_list.yview)
        self.store_list.config(yscrollcommand=self.scrollbar.set)

        self.store_list.pack(side='left')
        self.scrollbar.pack(side='right', fill=tkinter.Y)

        available = tkinter.font.families()
        if 'Helvetica' in available:
            family = 'Helvetica'
        else:
            family = 'Arial'
        self.heading_font = tkinter.font.Font(family=family, size=14, weight='bold', slant='italic')
        self.alert_font = tkinter.font.Font(family=family, size=10, underline=1)
        self.cancelled_font = tkinter.font.Font(family=family, size=10, overstrike=1)

        self.canvas = tkinter.Canvas(self.rack_frame, width=480, height=320)
        self.canvas.create_text(240,12, text='Staging Rack', font=self.heading_font)

        for row in range(2):
            for col in range(4):
                x1 = 20 + col * 90
                y1 = 30 + row * 70
                self.canvas.create_rectangle(x1, y1, x1 + 80, y1 + 60, fill='lightblue', outline='navy')
                self.canvas.create_text(x1 + 4, y1 + 4, text=f'Bin {row * 4 + col + 1}', anchor=tkinter.NW)

        # alright light over a frozen bin
        self.canvas.create_oval(260, 40, 280, 60, fill='red', outline='darkred')
        self.canvas.create_text(270, 75, text='FROZEN', font=self.alert_font)
        # forlift route

        self.canvas.create_line(20, 180, 370, 180, arrow=tkinter.LAST, dash=(5, 2))

        # curved path
        self.canvas.create_line(20, 210, 110, 250, 200, 210, 290, 250, smooth=True, width=2)

        # rack utilization gauge
        self.canvas.create_arc(390, 30, 470, 110, start=90, extent=-216, style=tkinter.PIESLICE, fill='green')
        self.canvas.create_text(430, 125, text='Rack\n60% full', justify='center')

        # loading dock
        self.canvas.create_polygon(360, 230, 470, 230, 470, 310, 340, 310, fill='gray', outline='black')
        self.canvas.create_text(405, 270, text='Loading\nDock', justify='center')

        # cancelled shipment

        self.canvas.create_text(20, 290, text='shipment 417', anchor=tkinter.NW, font=self.cancelled_font)

        self.canvas.pack()

        # seattle button
        self.settle_button = tkinter.Button(self.button_frame, text='Settle', command=self.settle)

        self.settle_button.pack(side='left', padx=10, pady=5)

        # remove and clear buttons
        self.remove_button = tkinter.Button(self.button_frame, text='Remove Store', command=self.remove_store)
        self.remove_button.pack(side='left', padx=10, pady=5)
        self.clear_button = tkinter.Button(self.button_frame, text='Clear', command=self.clear_stores)
        self.clear_button.pack(side='left', padx=10, pady=5)

        
        # quit out button
        self.quit_button = tkinter.Button(self.button_frame, text='Quit', command=self.main_window.destroy)
        self.quit_button.pack(side='left', padx=10, pady=5)
        # status bar of dashboard
        self.status_label = tkinter.Label(self.main_window, text='Ready', relief='sunken')
        # frames in order

        self.header_frame.pack()
        self.input_frame.pack()
        self.tier_frame.pack()
        self.button_frame.pack()
        self.store_frame.pack()
        self.rack_frame.pack()
        self.status_label.pack(fill=tkinter.X)
        

        
        
        tkinter.mainloop()
    def settle(self):
        try:
            miles = float(self.miles_entry.get())
            tier = self.tier.get()
            if tier == 1:
                rate = 0.58
            elif tier == 2:
                rate = 0.50
            else:
                rate = 0.45
            payout = miles * rate
            if self.surcharge.get() == 1:
                payout += FUEL_SURCHARGE
            
            self.payout.set(f'Payout: ${payout:,.2f}')
            tkinter.messagebox.showinfo('Settled', f'Payout: ${payout:,.2f}')
        except ValueError:
            self.payout.set('Enter a valid number')

    def show_store(self, event):
        selection = self.store_list.curselection()
        if selection:
            index = selection[0]
            name = self.store_list.get(index)
            self.status_label.config(text=f'Selected: {name}')

    def remove_store(self):
        self.store_list.delete(tkinter.ACTIVE)
    def clear_stores(self):
        self.store_list.delete(0, tkinter.END)
            

if __name__ == '__main__':
    DispatchDashboard(['Store 1', 'Store 2', 'Store 3'])

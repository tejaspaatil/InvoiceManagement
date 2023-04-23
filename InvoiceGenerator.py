from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql as myconn

# Create the main window
root = Tk()

# Set the window title
root.title("Invoice Generator")

# Set the window size
root.geometry("1540x780+0+0")
root.resizable(False,False)
root['background']='white'

def entrydata():
    if invoice_entry.get()=='' or gst_entry.get()=='':
        messagebox.showerror('Error','All fields are Required')
    else:
        con=myconn.connect(host='localhost',user='root',password='tejas02_',database="Entries")
        mycursor=con.cursor()
        query='insert into entrydata(invoice_number, company_name, gst_number, date, product_name, quantity, gstrate, price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
        mycursor.execute(query, (invoice_entry.get(),customer_entry.get(),gst_entry.get(),date_entry.get(),product_Entry.get(),quantity_entry.get(),GSTRate_entry.get(),price_entry.get()))
        

        con.commit()
        fetchdata()
        con.close()
    
def fetchdata():
    con=myconn.connect(host='localhost',user='root',password='tejas02_',database="Entries")
    mycursor=con.cursor()
    mycursor.execute("select * from entrydata")
    rows=mycursor.fetchall()
    if len(rows)!=0:
        Entries_Table.delete(*Entries_Table.get_children())
        for i in rows:
            Entries_Table.insert("",END,values=i)
            con.commit()
            con.close()


# Create labels and entry boxes for the invoice information

#======================INVOICE LABEL AND ENTRY=======================================
invoice_label = Label(root, text="Invoice Number :", bg='white')
invoice_label.place(x=50, y=50)

invoice_entry = Entry(root)
invoice_entry.place(x=200, y=50)

#======================CUSTOMER NAME LABEL AND ENTRY=======================================

customer_label = Label(root, text="Customer Name :", bg='white')
customer_label.place(x=50, y=90)

customer_entry = Entry(root)
customer_entry.place(x=200, y=90)

#======================GST NUMBER LABEL AND ENTRY=======================================

gst_label = Label(root, text="GST Number :", bg='white')
gst_label.place(x=50, y=130)

gst_entry = Entry(root)
gst_entry.place(x=200, y=130)

#======================PRODUCT LABEL AND ENTRY=======================================

# Create a label and listbox for the products
product_label = Label(root, text="Product :", bg='white')
product_label.place(x=50, y=200)

product_Entry = Entry(root)
product_Entry.place(x=200, y=200)

#======================QUANTITY LABEL AND ENTRY=======================================


quantity_label = Label(root, text="Quantity :", bg='white')
quantity_label.place(x=50, y=240)

quantity_entry = Entry(root)
quantity_entry.place(x=200, y=240)



#======================DATE LABEL AND ENTRY=======================================

# Create a label and entry box for the date
date_label = Label(root, text="Date (dd/mm/yyyy ):", bg='white')
date_label.place(x=50, y=280)

date_entry = Entry(root)
date_entry.place(x=200, y=280)

#======================GST Rate LABEL AND ENTRY=======================================


GSTRate_label = Label(root, text="GST Rate(%) :", bg='white')
GSTRate_label.place(x=50, y=320)

GSTRate_entry = Entry(root)
GSTRate_entry.place(x=200, y=320)

#======================PRICE LABEL AND ENTRY=======================================

# Create a label and entry box for the price
price_label = Label(root, text="Price :", bg='white')
price_label.place(x=50, y=360)

price_entry = Entry(root)
price_entry.place(x=200, y=360)

# Create a function to generate the bill
def generate_bill():
    # Get the invoice information from the entry boxes
    invoice_number = invoice_entry.get()
    customer_name = customer_entry.get()
    gst_number = gst_entry.get()
    
    # Get the selected product from the listbox
    selected_product = product_Entry.get()
    Quantity = quantity_entry.get()
    
    # Get the date and price from the entry boxes
    date = date_entry.get()
    gst_rate = GSTRate_entry.get()
    price = price_entry.get()
    
    # Create a text widget to display the bill
    bill_text = Text(root, height=20, width=50)
    bill_text.place(x=500, y=50)

    #===========================CALCULATE GST PRICE RATE==================================

    price = float(price_entry.get())
    rate = float(GSTRate_entry.get())
    gst = (price * rate) / 100

    #===========================CALCULATE TOTAL==================================

    Quantity = int(quantity_entry.get())
    price = float(price_entry.get())
    Total = (Quantity * price) + gst


    #==============================RESULT TEXT===============================
    
    # Insert the invoice information into the bill
    bill_text.insert(END, "Invoice Number: {}\n".format(invoice_number))
    bill_text.insert(END, "Customer Name: {}\n".format(customer_name))
    bill_text.insert(END, "GST Number: {}\n".format(gst_number))
    bill_text.insert(END, "----------------------------------------\n")
    
    # Insert the product, date, and price into the bill
    bill_text.insert(END, "Product: {}\n".format(selected_product))
    bill_text.insert(END, "Quantity: {}\n".format(Quantity))
    bill_text.insert(END, "Date: {}\n".format(date))
    bill_text.insert(END, "GST Rate(%): {}\n".format(gst_rate))
    bill_text.insert(END, "Price: {}\n".format(price))
    bill_text.insert(END, "----------------------------------------\n")
    bill_text.insert(END, "GST Price: {}\n".format(gst))
    bill_text.insert(END, "Total Price(with GST): {}\n".format(Total))

#==============================GENERATE BUTTON=======================


    
# Create a button to generate the bill
generate_button = Button(root, text="G:Generate Bill",command=generate_bill, bd=0, cursor='hand2', padx=20, pady=10, 
                         background='#E6F0FF',activebackground='#E6F0FF', fg='#FF9900',activeforeground='orange',font=('Bold', 9))
generate_button.place(x=50, y=400)

addentry_button = Button(root, text="A:Add Entry",command=entrydata,bd=0, cursor='hand2', padx=20, pady=10, 
                         background='#E6F0FF',activebackground='#E6F0FF', fg='orange',activeforeground='orange',font=('Bold', 9))
addentry_button.place(x=200, y=400)

#======================================SCROLLBAR=============================

Entries_Table = ttk.Treeview(root, columns=("Invoice Number","Company","GST Number","Date","Product Name","Quantity","Rate","Price"))



Entries_Table.heading("Invoice Number",text="Invoice Number")
Entries_Table.heading("Company",text="Comapany Name")
Entries_Table.heading("GST Number",text="GST Number")
Entries_Table.heading("Date",text="Date")
Entries_Table.heading("Product Name",text="Product Name")
Entries_Table.heading("Quantity",text="Quantity")
Entries_Table.heading("Rate",text="GST Rate")
Entries_Table.heading("Price",text="Price")

Entries_Table["show"]="headings"
Entries_Table.place(x=0,y=480)
fetchdata()


# Run the main loop
root.mainloop()

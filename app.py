from tkinter import *
from tkinter import filedialog
import tkinter as tk
import pytesseract
from PIL import Image, ImageTk
import os
import re
import math
import cv2
import numpy as np
from pytesseract import Output

# from matplotlib import pyplot as plt
import pymongo

# creat showimage function
def showimage():
    fln = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="select Image File",
        filetype=(("JPG file", "*.jpg"), ("PNG file", "*.png"), ("All Files", "*.*")),
    )
    img = Image.open(fln)
    img.thumbnail((350, 350))
    img = ImageTk.PhotoImage(img)
    # to show the image
    lbl.configure(image=img)
    lbl.image = img

    #  Get OCR output using Pytesseract
    custom_config = r"--oem 3 --psm 6"

    txt2.delete("1.0", "end")
    txt2.insert(
        INSERT, pytesseract.image_to_string(Image.open(fln), config=custom_config)
    )

    data_extracted = pytesseract.image_to_string(Image.open(fln), config=custom_config)

    # print(data_extracted)

    # Using rule-based approach to extract information form the receipt,
    # will be extracting the supermarket name, date of transaction, the items bought,
    # total costs per item and the # total amount paid using python commands and regular expressions.

    # here is the dictionary where to store the extracted information.
    receipt_Data = {}

    # first is to extract the the Suppermarket name
    # supermarket name is going to be constant in all receipts of this supermarket, and
    # that is in the first 3 lines. then creating a rule to caputure that
    splits = data_extracted.splitlines()
    supermarket_name = splits[0] + "  " + splits[1] + "  " + splits[2]

    # print(supermarket_name)

    # >>> s = 'abcdefgABCDEFGHIJKLMNOP'
    # >>> ''.join(c for c in s if c.isupper())
    # 'ABCDEFGHIJKLMNOP

    store_name = "".join(c for c in supermarket_name if c.isupper())
    # print(store_name)

    # extracting date of transation/ may be time also "%m/%j/%y %H:%M"
    date_pattern = r"([0-9]{1}\/[0-9]{2}\/[0-9]{2} [0-9]{2}:[0-9]{2})"
    # print(date_pattern)

    # Next is the Date using Regular Expression  for the date format on the text
    # import Regular Expression  ( date_pattern is 6/07/20)
    # import re

    date_pattern = r"([0-9]{1}\/[0-9]{2}\/[0-9]{2} [0-9]{2}:[0-9]{2})"
    dateTime = re.search(date_pattern, data_extracted).group()
    receipt_Data["date"] = dateTime

    # print(dateTime)
    # print(store_name, dateTime)

    # from the data_extracted get onlt the lines with £ , and put them in a list

    lines_with_pound = []
    for line in splits:
        if re.search(r"£", line):
            lines_with_pound.append(line)

    # print(lines_with_pound)

    lines_with_pound

    # get Line items, TOTAL COST, ignore SAlE, card visa, master ETC
    # items = []
    for line in lines_with_pound:
        if re.search(r"SAlE", line):
            continue

        if re.search(r"TOTAL", line):
            TOTAL = line

            # print(TOTAL)

    # extract the all the new line only the digits to get the cost of the items

    total = "".join(
        x.rstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for x in TOTAL
    )
    # print(total)

    # get items, total, ignore others like ... A chance to win a £1000 Tesco gift card, ...CHANGE DUE £0.00
    items = []
    for line in lines_with_pound:
        #    print(line)
        if re.search(
            "|".join(
                ["JOIN", "CHANGE", "VISA", "CASH", "CARD", "MASTERCARD", "A chance"]
            ),
            line,
        ):
            continue
        if re.search(r"TOTAL", line):
            total = line
        else:
            items.append(line)
    # print(items)

    items

    # print(store_name, dateTime, total, items)

    # convert items that is a list to string in other for clean-up the data
    # convert list to string and re-assign to all_items
    all_items = "\n".join(items)
    # print(all_items)

    # to extract the iteams bought from all_items, removing the digits and unwanted charater from the extrated data
    line_items = "".join(
        x.rstrip("0123456789£&$)(+-^%!¬`~#@][}{*x.|\\_<>'?«") for x in all_items
    )
    # print(line_items)

    # to extract the cost of each item, convert items into  list
    # going through each element of list
    # applying a filter on each character of the string for alphabet or numeric other then special symbol
    # joining the charactors back again and putting them in list renamed as "items_list", print the new list

    items_list = ["".join(list(filter(str.isalnum, item))) for item in items]

    # print(items_list)  # print the result

    # convert "items_list" items_string to enable the operationon with new line, then print the result
    items_list_to_str = "\n".join(items_list)
    # print(items_list_to_str)

    # extract the all the new line only the digits to get the cost of the items

    cost = "".join(
        x.rstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        for x in items_list_to_str
    )
    # print(cost)

    # print(line_items, cost)

    # covert cost to list, and assign it to costs
    costs = cost.split(sep="\n", maxsplit=-1)
    # print(costs)

    # covert all_line_itemsto list
    all_line_items = line_items.split(sep="\n", maxsplit=-1)
    # print(all_line_items)

    # type(all_line_items)

    # TEST ===== testing the software can calculated the sum of the items on the receicpt correctly

    # to confirm line items on the reciept extrated is correct apply this test method as unit test

    sum_total = sum(int(i) for i in costs) / 100

    # print(sum_total)
    # print(total)

    # covert store_name to list, and assign it to store_ID
    date_time = dateTime.split(sep="\n", maxsplit=-1)
    # print(date_time)
    # type(date_time)

    # covert store_name to list, and assign it to store_ID
    total_cost = total.split(sep="\n", maxsplit=-1)
    # print(total_cost)
    # type(total_cost)

    # covert store_name to list, and assign it to store_ID
    shop = store_name.split(sep="\n", maxsplit=-1)
    # print(shop)
    # type(shop)

    # print(all_line_items)
    # print(costs)
    # print(sum_total)
    # print(shop)
    # print(date_time)
    # print(total_cost)

    # Zip the two lists together, and create a dictionary out of the zipped lists - mapping

    shopped_line_items = dict(zip(all_line_items, costs))
    # print(shopped_line_items)

    # print(shop, date_time, total_cost, shopped_line_items)

    for s, d, t in zip(shop, date_time, total_cost):
        receipt_headers = {"Shop Name": s, "Date and Time": d, "Amount Spent": t}
    # print(receipt_headers)

    # print(receipt_headers, shopped_line_items)

    # import json
    # json.dumps(receipt_data)

    # print(receipt_headers)

    shopped_line_items

    # import and connect Mongo DB
    # import pymongo

    connection = pymongo.MongoClient("localhost", 27017)

    # Creat a database and collection and send data to the acquired to the  database
    database = connection["mydb_TESCO_290121"]
    collection = database["mycol_TESCO"]
    data = receipt_headers
    data = shopped_line_items

    collection.insert_one(receipt_headers)
    collection.insert_one(shopped_line_items)

    # print Database if data is successfully inserted
    print("Data inserted with record IDs", receipt_headers, " ", shopped_line_items)

    # display Database on the GUI
    txt3.delete("1.0", "end")
    txt3.insert(INSERT, receipt_headers, shopped_line_items)

    # txt4.delete("1.0", "end")
    # txt4.insert(INSERT, shop, date_time, total_cost, shopped_line_items)

    # print(all_line_items)
    # print(costs)
    # print(sum_total)
    # print(shop)
    # print(date_time)
    # print(total_cost)


############################# Tkinter GUI for displayin the actions to custumers#####################################

root = Tk()

t1 = StringVar()
wrapper = LabelFrame(root, text="Choose File")
wrapper.pack(fill="both", expand="yes", padx=10, pady=10)

lbl = Label(root)
lbl.pack(side=tk.LEFT, padx=10, pady=10)

wrapper2 = LabelFrame(root, text="Image Text")
wrapper2.pack(fill="both", expand="yes", padx=10, pady=10)

txt = Entry(wrapper, textvariable=t1)
txt.pack(side=tk.RIGHT, padx=10, pady=10)

wrapper3 = LabelFrame(root, text=" Data written on  Database")
wrapper3.pack(side=tk.RIGHT, fill="both", expand="yes", padx=10, pady=10)

wrapper4 = LabelFrame(root, text="Receipt Data")
wrapper4.pack(side=tk.LEFT, fill="both", expand="yes", padx=10, pady=10)

# # browse button
btn1 = Button(wrapper, bg="#20bebe", fg="white", text="Browse Image", command=showimage)
# btn1.pack(side=tk.LEFT, padx=10, pady=10)
btn1.place(x=30, y=10)


btn2 = Button(
    wrapper, bg="#20bebe", fg="white", text="......Exit.......", command=lambda: exit()
)
# btn2.pack(side=tk.LEFT, padx=10, pady=10)
btn2.place(x=130, y=10)


# btn = Button(wrapper, text="Browse", command=readTxt1)
# btn.pack(side=tk.LEFT, padx=10, pady=10)
btn3 = Button(wrapper, bg="#20bebe", fg="white", text="Button 3")
btn3.place(x=230, y=10)

txt2 = Text(wrapper2)
txt2.pack(padx=10, pady=10)

txt3 = Text(wrapper3)
txt3.pack(padx=10, pady=10)

txt4 = Text(wrapper4)
txt4.pack()

# # browse button
# browse_text = tk.StringVar()
# browse_btn = tk.Button(
#     root,
#     textvariable=browse_text,
#     # command=lambda: open_file(),
#     font="Raleway",
#     bg="#20bebe",
#     fg="white",
#     height=2,
#     width=15,
# )
# browse_text.set("Browse")
# browse_btn.grid(column=1, row=2)

root.geometry("960x650")
root.title("UK Supermarket Receipt App")
root.resizable(False, False)
root.mainloop()

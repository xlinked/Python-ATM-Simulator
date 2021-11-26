from tkinter import *
import time
import fileinput
import matplotlib.pyplot as plt

root = Tk()
root.geometry("700x550")
root.title("ATM Machine")
root.configure(bg="black")

tops = Frame(root, bg="black", width=800, height=50, relief=SUNKEN)
tops.pack(side=TOP)

f1 = Frame(root, bg="black", width=300, height=700, relief=SUNKEN)
f1.pack(side=LEFT)

f2 = Frame(root, bg="black", width=400, height=700, relief=SUNKEN)
f2.pack(side=RIGHT)

localtime = time.asctime(time.localtime(time.time()))

title_lbl = Label(tops, font=("monospaced", 36, "bold"), text="Python ATM", fg="LightBlue", bg="black", bd=10)
title_lbl.grid(row=0, column=0)
time_lbl = Label(tops, font=("monospaced", 20, "bold"), text=localtime, fg="LightBlue", bg="black", bd=10)
time_lbl.grid(row=1, column=0)
acct = ""
balance = ""
pin = ""


def login():
    global acct
    global balance
    global pin
    try:
        acct_num = acc_num_txt.get()
        pin = pin_txt.get()
        try:
            for line in open("users.txt", "r").readlines():  # Read the lines
                login_info = line.split()  # Split on the space, and store the results in a list of two strings
                if acct_num == "sysadmin" and pin == "1357" or acct_num == login_info[0] and pin == login_info[1]:
                    if acct_num == "sysadmin" and pin == "1357":
                        spacer1.config(text="Admin Login Successful", fg="LimeGreen")
                        admin_main()
                        return True
                    else:
                        spacer2.config(text="Login Successful", fg="LimeGreen")
                        acct = login_info[0]
                        pin = login_info[1]
                        balance = login_info[2]
                        user_main()
                        return True
                elif acct_num != login_info[0] and pin != login_info[1]:
                    spacer2.config(text="Incorrect Account Number/Pin! Try Again", fg="red")

        except IndexError:
            spacer2.config(text="Entry Not Valid! Try Again", fg="red")

    except ValueError:
        spacer2.config(text="Entry Not Valid! Try Again", fg="red")


# ***** User Main menu *****
def user_main():
    global acct
    time_lbl.config(text="Welcome Back " + acct)
    dep_lbl.grid(row=5, column=3, sticky=W)
    dep_txt.grid(row=5, column=4)
    with_lbl.grid(row=9, column=3, stick=W)
    with_txt.grid(row=9, column=4)
    change_pin_lbl.grid(row=12, column=3, stick=W)
    change_pin_txt.grid(row=12, column=4)
    acc_num_txt.delete(0, END)
    pin_txt.delete(0, END)


def deposit():
    global balance
    try:
        amount = dep_txt.get()
        try:
            new_dep_bal = float(balance) + float(amount)
            if float(amount) <= 0:
                spacer3.config(text="Enter Amount Greater then 0", fg="red")
            elif float(amount) == str:
                spacer3.config(text="Amount Entered is Invalid! Try Again", fg="red")
            else:
                with fileinput.FileInput("users.txt", inplace=True) as file:
                    for line in file:
                        print(line.replace(str(balance), str(new_dep_bal)), end='')

                balance = new_dep_bal
                spacer3.config(text="New Balance: $" + str(balance), fg="LimeGreen")
        except ValueError:
            spacer3.config(text="Amount Entered is Invalid! Try Again", fg="red")
    except TypeError:
        spacer3.config(text="Amount Entered is Invalid! Try Again", fg="red")


def withdrawn():
    global balance
    max_limit = 1000
    ten = 10

    try:
        wd = with_txt.get()
        try:
            new_wd_bal = float(balance) - float(wd)
            if float(wd) > float(new_wd_bal):
                spacer4.config(text="Insufficient Funds!", fg="red")

            elif float(wd) > float(max_limit):
                spacer4.configure(text="Maximum Withdrawal Limit $1000", fg="red")

            elif (float(wd) % ten) != 0:
                spacer4.configure(text="Multiples of $10 only! Try again", fg="red")

            else:
                with fileinput.FileInput("users.txt", inplace=True) as file:
                    for line in file:
                        print(line.replace(str(balance), str(new_wd_bal)), end='')

                balance = new_wd_bal
                spacer4.configure(text="New Balance: $" + str(balance), fg="LimeGreen")

        except ValueError:
            spacer4.configure(text="Amount Entered is Invalid! Try again", fg="red")
    except TypeError:
        spacer4.configure(text="Amount Entered is Invalid! Try again", fg="red")


def bal():
    global acct
    global balance
    spacer3.config(text="")
    spacer4.config(text="")
    spacer5.config(text="Total Balance: $" + str(balance))


def change_pin():
    replacement = change_pin_txt.get()
    current_pin = pin

    if replacement == current_pin:
        spacer5.config(text="Pin Cannot be the old Pin! Try Again", fg="red")

    else:
        with fileinput.FileInput("users.txt", inplace=True) as file:
            for line in file:
                print(line.replace(current_pin, replacement), end='')

        total_lbl.config(text="Pin Change Successful!", fg="LimeGreen")
        time_lbl.config(text="")
        change_pin_txt.delete(0, END)


def clear():
    spacer1.config(text="")
    spacer2.config(text="")
    spacer3.config(text="")
    spacer4.config(text="")
    spacer5.config(text="")
    total_lbl.config(text="")
    dep_txt.delete(0, END)
    with_txt.delete(0, END)
    change_pin_txt.delete(0, END)
    pin_txt.delete(0, END)
# ***** End of User menu *****


# ***** Admin Main Menu *****
def admin_main():
    change_pin_btn.grid_forget()
    time_lbl.config(text="Administrator Main Menu")
    dep_lbl.grid(row=5, column=3, sticky=W)
    dep_txt.grid(row=5, column=4)
    with_lbl.grid(row=9, column=3, stick=W)
    with_txt.grid(row=9, column=4)
    change_pin_lbl.grid(row=12, column=3, stick=W)
    change_pin_txt.grid(row=12, column=4)
    acc_num_txt.delete(0, END)
    pin_txt.delete(0, END)
    dep_lbl.config(text="Add/Delete Account:")
    with_lbl.config(text="Add Temporary Pin Num:")
    change_pin_lbl.config(text="Deposit Amount:")
    dep_btn.config(text="Delete User", command=delete_user)
    with_btn.config(text="Add User", command=add_new_user)
    bal_btn.config(text="Plot Accounts", command=plot_user_accounts)
    acc_num_txt.delete(0, END)
    pin_txt.delete(0, END)


# Add a new user to the users.txt file
def add_new_user():
    acct_num = dep_txt.get()
    new_pin = with_txt.get()
    dep_amt = change_pin_txt.get()
    with open("users.txt", "a") as file:
        file.write(acct_num)
        file.write(" ")
        file.write(new_pin)
        file.write(" ")
        file.write(dep_amt)
        file.write("\n")
    spacer3.config(text=acct_num + " Added Successfully!", fg="LimeGreen")
    spacer4.config(text="Temp Pin Added Successfully!", fg="LimeGreen")
    total_lbl.config(text="$" + dep_amt + " Added Successfully!", fg="LimeGreen")


# Deletes a users Username, pin and balance from the users.txt file
def delete_user():
    drop_user = dep_txt.get()

    with open("users.txt", "r") as file:
        lines = file.readlines()
    with open("users.txt", "w") as new_file:
        for line in lines:
            if not line.startswith(drop_user):
                new_file.write(line)
    spacer3.config(text=drop_user + " Deleted Successfully!", fg="LimeGreen")


def plot_user_accounts():
    with open("users.txt") as file:
        lines = file.readlines()
        x = [line.split()[0] for line in lines]
        y = [line.split()[2] for line in lines]

        plt.figure(figsize=(6, 5))

        # creating the bar plot
        plt.bar(x, y, color="blue", width=0.5)

        plt.xlabel("Account Numbers")
        plt.ylabel("Account Balances")
        plt.title("ATM Account Balance Graph")
        plt.show()


# Account Number label and entry
acc_num_lbl = Label(f1, font=("monospaced", 16, "bold"), fg="LightBlue", bg="black", bd=10,
                    text="Enter account number:")
acc_num_lbl.grid(row=0, column=3, sticky=W)
acc_num_txt = Entry(f1, font=("monospaced", 16, "bold"), bg="Blue", fg="LightBlue", bd=6)
acc_num_txt.grid(row=0, column=4)
spacer1 = Label(f1, font=("monospaced", 16, "bold"), fg="LimeGreen", bg="black")
spacer1.grid(row=1, column=4, sticky=W)

# Pin label and entry
pin_lbl = Label(f1, font=("monospaced", 16, "bold"), fg="LightBlue", bg="black", bd=10, text="Enter Pin:")
pin_lbl.grid(row=2, column=3, sticky=W)

pin_txt = Entry(f1, font=("monospaced", 16, "bold"), bg="Blue", fg="LightBlue", bd=6)
pin_txt.grid(row=2, column=4)
spacer2 = Label(f1, font=("monospaced", 16, "bold"), fg="LimeGreen", bg="black")
spacer2.grid(row=3, column=4, sticky=W)

# Submit button for account number
submit_btn = Button(f2, padx=16, pady=6, bd=10, fg="black", font=("monospaced", 16, "bold"),
                    width=7, text="Submit", highlightbackground="Blue", command=login)
submit_btn.grid(row=0, column=4)

total_lbl = Label(f1, text="", fg="LimeGreen", bg="black")
total_lbl.grid(row=4, columnspan=10)

# Deposit label and entry
dep_lbl = Label(f1, font=("monospaced", 16, "bold"), fg="LightBlue", bg="black", bd=10, text="Enter amount to deposit:")
dep_lbl.grid(row=5, column=3, sticky=W)
dep_lbl.grid_forget()
dep_txt = Entry(f1, font=("monospaced", 16, "bold"), bg="Blue", fg="LightBlue", bd=6, insertwidth=4)
dep_txt.grid(row=5, column=4)
dep_txt.grid_forget()

spacer3 = Label(f1, font=("monospaced", 16, "bold"), fg="LimeGreen", bg="black")
spacer3.grid(row=6, column=4, sticky=W)

dep_btn = Button(f2, padx=16, pady=6, bd=10, fg="black", font=("monospaced", 16, "bold"),
                 width=7, text="Deposit", highlightbackground="blue", command=deposit)

dep_btn.grid(row=4, column=4)

total_lbl = Label(f1, text="", fg="LimeGreen", bg="black")
total_lbl.grid(row=8, columnspan=10)

# Withdraw label and entry
with_lbl = Label(f1, font=("monospaced", 16, "bold"), fg="LightBlue", bg="black", bd=10,
                 text="Enter amount to withdraw:")
with_lbl.grid(row=9, column=3, stick=W)
with_lbl.grid_forget()
with_txt = Entry(f1, font=("monospaced", 16, "bold"), bg="Blue", fg="LightBlue", bd=6, insertwidth=4)
with_txt.grid(row=9, column=4)
with_txt.grid_forget()
spacer4 = Label(f1, font=("monospaced", 16, "bold"), fg="LimeGreen", bg="black")
spacer4.grid(row=10, column=4, sticky=W)

spacer5 = Label(f1, font=("monospaced", 16, "bold"), fg="LimeGreen", bg="black")
spacer5.grid(row=11, column=4, sticky=W)
# Change pin label and txt box
change_pin_lbl = Label(f1, font=("monospaced", 16, "bold"), fg="LightBlue", bg="black", bd=10, text="Enter New Pin:")
change_pin_lbl.grid(row=12, column=3, stick=W)
change_pin_lbl.grid_forget()
change_pin_txt = Entry(f1, font=("monospaced", 16, "bold"), bg="Blue", fg="LightBlue", bd=6, insertwidth=4)
change_pin_txt.grid(row=12, column=4)
change_pin_txt.grid_forget()

with_btn = Button(f2, padx=16, pady=6, bd=10, fg="black", font=("monospaced", 16, "bold"),
                  width=7, text="Withdrawal", highlightbackground="blue", command=withdrawn)
with_btn.grid(row=8, column=4)
# Balance Button
bal_btn = Button(f2, padx=16, pady=6, bd=10, fg="black", font=("monospaced", 16, "bold"),
                 width=7, text="Balance", highlightbackground="blue", command=bal)
bal_btn.grid(row=10, column=4)
# Reset Button
clear_btn = Button(f2, padx=16, pady=6, bd=10, fg="black", font=("monospaced", 16, "bold"),
                   width=7, text="Clear", highlightbackground="blue", command=clear)
clear_btn.grid(row=11, column=4)
# change pin
change_pin_btn = Button(f2, padx=16, pady=6, bd=10, fg="black", font=("monospaced", 16, "bold"),
                        width=7, text="Change Pin", highlightbackground="blue", command=change_pin)
change_pin_btn.grid(row=12, column=4)
# Exit Button
exit_btn = Button(f2, padx=16, pady=6, bd=10, fg="black", font=("monospaced", 16, "bold"),
                  width=7, text="Exit", highlightbackground="red", command=root.destroy)
exit_btn.grid(row=13, column=4)

total_lbl = Label(f1, text="", fg="LimeGreen", bg="black", font=("monospaced", 16, "bold"))
total_lbl.grid(row=13, column=4, sticky=W, columnspan=10)

# Adds padding on the right side of the buttons.
col_spacer = Label(f2, text=" ", bg="black")
col_spacer.grid(row=0, column=5)
row_spacer1 = Label(f2, text=" ", bg="black")
row_spacer1.grid(row=14, column=4)
row_spacer2 = Label(f2, text=" ", bg="black")
row_spacer2.grid(row=15, column=4)
row_spacer3 = Label(f2, text=" ", bg="black")
row_spacer3.grid(row=16, column=4)

root.mainloop()

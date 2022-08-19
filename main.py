# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import os
from datetime import datetime, timedelta
from operator import ge

from flask import Flask, redirect, render_template, request, session
from numpy import row_stack

import btree1
from flask_session import Session


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#    print_hi('PyCharm')


TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')
# app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

voterfilename="voter.txt"
traversalfilename="traversalfile.txt"
idfilename="id.txt"

@app.route('/')
def homepage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)


@app.route('/about')
def aboutpage():
    return render_template("about.html")


@app.route('/adminlogin')
def adminlogin():
    return render_template("adminlogin.html")


@app.route('/newvoter')
def newvoter():
    return render_template("newvoter.html")

@app.route('/adminviewvoters')
def adminviewvoters():
    lines = []
    with open(voterfilename) as f:
        lines = f.readlines()
    return render_template("adminviewvoters.html", rows=lines)

@app.route('/adminvoterdeletepage')
def voterdeletepage():
    lines = []
    with open(voterfilename) as f:
        lines = f.readlines()
    return render_template("adminvoterdeletepage.html", rows=lines)

@app.route('/admindeletevoterpage1', methods=['GET'])
def voterdeletepage1():
    args = request.args
    id = args.get("id")
    print("Id : ", id)
    lines = []
    with open(voterfilename) as f:
        lines = f.readlines()
    f.close();

    newlines=[]
    idlines=[]
    for line in lines:
        s=line.split(",")
        print(id,":", len(id), ":",  s[0],":", len(s[0]), ":", line)
        if(id!=s[0]):
            print("Not Equals")
            newlines.append(line)
            idlines.append(s[0]+"\n")

    print("New Lines : ")
    print(newlines)
    print("Id Lines : ")
    print(idlines)

    with open(voterfilename,'w') as f:
        for line in newlines:
            f.writelines(line)
    f.close();

    with open(idfilename, 'w') as f:
        for line in idlines:
            f.writelines(line)
    f.close();

    return render_template("adminvoterdeletepage.html", rows=newlines)

@app.route('/adminvotersearchpage')
def adminvotersearchpage():
    return render_template("adminvotersearchpage.html", rows=[])

@app.route('/adminvotersearchpage1', methods=['POST'])
def adminvotersearchpage1():
    msg="Not Found"
    if request.method == 'POST':
        id = request.form['id']
    lines = []
    with open(voterfilename) as f:
        lines = f.readlines()
    f.close();

    newlines=[]
    for line in lines:
        s=line.split(",")
        print(id,":", len(id), ":",  s[0],":", len(s[0]), ":", line)
        if(id==s[0]):
            newlines.append(line)
            msg="Found"

    return render_template("adminvotersearchpage.html", rows=newlines, msg=msg)


@app.route('/adminupdatevoterpage1', methods=['GET'])
def adminvoterupdatepage():
    args = request.args
    id = args.get("id")
    print("Id : ", id)
    lines = []
    with open(voterfilename) as f:
        lines = f.readlines()
    f.close();

    voterline=""
    for line in lines:
        s=line.split(",")
        print(id,":", len(id), ":",  s[0],":", len(s[0]), ":", line)
        if(id==s[0]):
            voterline = line

    f.close();
    s=voterline.split(",")
    return render_template("adminupdatevoterpage1.html", id=s[0], fname=s[1], lname=s[2], gender=s[3], dob=s[4])

@app.route('/adminvoterupdatepage')
def voterupdatepage():
    lines = []
    with open(voterfilename) as f:
        lines = f.readlines()
    return render_template("adminvoterupdatepage.html", rows=lines)

@app.route('/opennotepad', methods=['POST'])
def opennotepad():
    if request.method == 'POST':
        choice = request.form['choice']

    if(choice=="Voters"):
        os.system("voter.txt")
    elif (choice == "Id"):
        os.system("id.txt")
    else:
        os.system("traversalfile.txt")

    print("Choice : ", choice)
    lines = []
    with open(voterfilename) as f:
        lines = f.readlines()
    return render_template("adminviewvoters.html", rows=lines)

@app.route('/adminlogincheck', methods=['POST'])
def adminlogincheck():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']
    print("Uname : ", uname, " Pwd : ", pwd);
    if uname == "admin" and pwd == "admin":
        return render_template("adminmainpage.html")
    else:
        return render_template("adminlogin.html", msg="UserName/Password is Invalid")


@app.route('/adminupdatevoterpage2', methods=['POST'])
def adminupdatevoterpage2():
    print("Add New VoterId Function")
    if request.method == 'POST':
        id = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        dob = request.form['dob']

        s = str(id) + "," + firstname + "," + lastname + "," + gender + "," + dob;
        lines = []
        with open(voterfilename) as f:
            lines = f.readlines()

        newlines = []
        for line in lines:
            print(f'line : {line}')
            x = line.split(",")
            if(x[0]==id):
                newlines.append(s+"\n")
            else:
                newlines.append(line)
        f.close();

        print("NewLines : ", newlines)

        with open(voterfilename, 'w') as f:
            for line in newlines:
                f.writelines(line)

        f.close();
        return render_template("adminviewvoters.html", rows=newlines);


@app.route('/addnewvoter', methods=['POST'])
def addnewvoter():
    print("Add New VoterId Function")
    if request.method == 'POST':
        id = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        dob = request.form['dob']

        file_exists = os.path.exists('voter.txt')

        print("File Exists : ", file_exists)

        if (file_exists == False):
            file = open(voterfilename, "w")
            file.close();

        file_exists = os.path.exists(idfilename)

        print("File Exists : ", file_exists)

        if (file_exists == False):
            file = open(voterfilename, "w")
            file.close();

        lines = []
        with open(voterfilename) as f:
            lines = f.readlines()

        voterid = 0
        flag=True
        for line in lines:
            print(f'line : {line}')
            x = line.split(",")
            if(id == x[0]):
                flag=False
                break

        f.close();

        if(flag):
            s = str(id) + "," + firstname + "," + lastname + "," + gender + "," + dob;
            print(s)
            with open(voterfilename, 'a') as f:
                f.writelines(s+"\n")

            f.close();

            with open(idfilename, 'a') as f:
                f.writelines(id+"\n")
            f.writelines("\n\n\n")

            #f.close();

            return render_template("newvoter.html", msg="Voter Details Inserted Successfully!!");
        else:
            return render_template("newvoter.html", msg="VoterId Already Exists !!");




@app.route('/userlogincheck', methods=['POST'])
def userlogincheck():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']
    print("Uname : ", uname, " Pwd : ", pwd);
    if uname == "user" and pwd == "user":
        return render_template("usermainpage.html")
    else:
        return render_template("userlogin.html", msg="UserName/Password is Invalid")

global rows
@app.route('/adminviewtraversalpage')
def adminviewtraversalpage():
    global rows
    btree1.vlist()
    #btree1.BTree.insert()
    #btree1.B.print_tree()
    lines = []

    with open(traversalfile) as f:
        lines = f.readlines()

    print(lines)
    return render_template("adminviewtraversalpage.html", rows=lines)

@app.route('/userlogin')
def userlogin():
    return render_template("userlogin.html")


@app.route('/adminmainpage')
def adminmainpage():
    return render_template("adminmainpage.html")


if __name__ == "__main__":
    app.run(debug=True)
#See PyCharm help at https://www.jetbrains.com/help/pycharm/

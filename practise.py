import module1
import mysql.connector

# This file for practise only

""" This is a example to run any function at the time of loading file

print 'Hello, this is demo file'

def showmessage():
    print 'This is showing message inner function'

if __name__ == '__main__':
    print 'I am in under main function and calling other function at initialization time'
    showmessage()

"""

""" __init__ function works as constructor for class 

num1 = 2
num2 = 4


sum =  Calculator.Add(self,num1,num2)
print "Sum of 2 number " + sum

"""

num1 = 2
num2 = 4

def calculate():
    cal1 = module1.Calculator()
    sum  =  cal1.Add(num1,num2)
    print "Sum of two number: %s " % sum
    print "User Name: " + cal1.name

def connectwithDb():
    mydb = mysql.connector.connect(
        host = "192.168.6.51",
        user = "tushar",
        passwd = "tushar12",
        database = "hiringbull_20190524"
    )
    
    mycursor = mydb.cursor()
    
    mycursor.execute("Select * from Candidate where CompanyId = 1")
    candidates = mycursor.fetchall()
    for item in candidates:
        print "{},{}".format(item[1], item[2])


if __name__ == "__main__":
    connectwithDb() 



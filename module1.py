print 'Hello, this is demo file'

def showmessage():
    print 'This is showing message inner function'

def main():
    print 'This is call when we will trying to import this file'

if __name__ == '__main__':
    print 'I am in under main function and calling other function at initialization time'
    showmessage()

class Calculator:

    name = ""

    def __init__(self):
        self.name = "Deependra Singh"

    """ 
    # Adding the two numbers

    """
    def Add(self, num1, num2):
        return num1 + num2

    """ 
    # Subtract the two numbers

    """
    def Subtract(self, num1, num2):
        return num1 - num2

    """ 
    # Multiply the two numbers

    """
    def Multiply(self, num1, num2):
        return num1 * num2

    """ 
    # Deviding the two numbers

    """
    def devide(self, num1, num2):
        if num2 == 0:
            return 0
        
        return num1 / num2
    


    
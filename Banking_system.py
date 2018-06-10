###CONNECTION WITH LOCAL SERVER###

import psycopg2
conn = psycopg2.connect(database = 'mydb',user = 'postgres',password = '*******',port = '5432',host = '127.0.0.1')
cur = conn.cursor()



def fetch(temp_pass,temp_accno):
    cur.execute('''SELECT id, name, acc_no, ph_no,address, email,balance
               FROM accounts
               WHERE id = %s and acc_no = %s''',
            (str(temp_pass), str(temp_accno)));
    row = cur.fetchall()
    #print(row[0][6])
    return row

def fetchtrans(temptrans_accno):
    cur.execute("SELECT id,name,acc_no,ph_no,address,email,balance FROM accounts WHERE acc_no = %s" , (temptrans_accno,))
    row1 = cur.fetchall();
    print(row1)
    return row1



###########################################################################################################################################################################

###CLASSES###


class accounts(object):
    def __init__(self,name,ph_no,address,email,acc_no,balance):
        self.name = name
        self.ph_no = ph_no
        self.address = address
        self.email = email
        self.acc_no = acc_no
        self.balance = balance
        #self.amt = amt

    def debit(self,amt,temp_accno):
        if (amt > self.balance):
            return 'Sorry Insufficient Balance'
        else:
            self.balance -= amt
            cur.execute("UPDATE accounts set balance = (%s) where acc_no = %s",(self.balance,temp_accno))
            conn.commit();
            print('Account Number: ',temp_accno,'\n','Balance: ',self.balance)

    def credit(self,amt,temp_accno):
        self.balance += amt
        cur.execute(
            "UPDATE accounts set balance = %s where acc_no = %s",(self.balance,temp_accno)
            )
        conn.commit();
        print('Account Number: ',temp_accno,'\n','Balance: ',self.balance)

    def delete(self,temp_accno,temp_pass):
        cur.execute('''DELETE FROM accounts
                   WHERE id = %s and acc_no = %s''',
                (str(temp_pass), str(temp_accno)));
        conn.commit()
        print('Account deleted successfully')

######################################################################################################################################################################################################

###FUNCTIONS###

def create():
    name1 = input('Enter your fullname:* ')
    acc_no1 = int(input('Enter your account number:* '))
    ph_no1 = int(input('Enter your Phone number:* '))
    address1 = input('Enter your address:* ')
    email1 = input('Enter your Email address: ')
    id1 = int(input('please enter 4 digit pin passcode for your account:* '))
    bal = float(input('Please enter your inetial amount to deposit: '))
    cur.execute("INSERT INTO ACCOUNTS (ID,ADDRESS,BALANCE,ACC_NO,NAME,PH_NO,EMAIL) \
      VALUES (%s,%s,%s,%s,%s,%s,%s)", (id1,address1,bal,acc_no1,name1,ph_no1,email1));
    conn.commit()
    print('Account created successfully')

def deposit():
    #temp_accno = int(input('Please enter your Account Number: '))
    #temp_pass = int(input('Please enter your 4 digit pass code: '))
    temp_amt = int(input('How much do you want to deposit: '))
    #info = fetch(temp_pass,temp_accno)
    #new_trans = accounts(info[0][1],info[0][3],info[0][4],info[0][5],info[0][2],info[0][6])
    new_trans.credit(temp_amt,temp_accno)


def withdraw():
    #temp_accno = int(input('Please enter your Account Number: '))
    #temp_pass = int(input('Please enter your 4 digit pass code: '))
    temp_amt = float(input('How much do you want to Withdraw: '))
    #info = fetch(temp_pass,temp_accno)
    #new_trans = accounts(info[0][1],info[0][3],info[0][4],info[0][5],info[0][2],info[0][6])
    new_trans.debit(temp_amt,temp_accno)

def transfer():
    #temp_accno = int(input('Please enter your Account Number: '))
    #temp_pass = int(input('Please enter your 4 digit pass code: '))
    temp_amt = float(input('How much do you want to Withdraw: '))
    temptrans_accno = int(input('Enter the Account number you want to transfer: '))
    #info = fetch(temp_pass,temp_accno)
    info1 = fetchtrans(temptrans_accno)
    #new_trans = accounts(info[0][1],info[0][3],info[0][4],info[0][5],info[0][2],info[0][6])
    new_trans1 = accounts(info1[0][1],info1[0][3],info1[0][4],info1[0][5],info1[0][2],info1[0][6])
    new_trans.debit(temp_amt,temp_accno)
    new_trans1.credit(temp_amt,temptrans_accno)

def delete():
    delt = True
    while(delt):
        #temp_accno = int(input('Please enter your Account Number: '))
        #temp_pass = int(input('Please enter your 4 digit pass code: '))
        confirm = input('Are you sure you want to delete your account? (YES/NO): ')
        if confirm.lower() == 'yes':
            info = fetch(temp_pass,temp_accno)
            new_trans = accounts(info[0][1],info[0][3],info[0][4],info[0][5],info[0][2],info[0][6])
            new_trans.delete(temp_accno,temp_pass)
            delt = False
        else:
            if confirm.lower() == 'no':
                continue
                delt = False
            else:
                print('Sorry wrong response, try again')


##############################################################################################################################################################################################

###EXECUTION###

now = True
while(now):
    while (True):
        import os
        os.system('clear')
        #print('Below are the services we offer: \n1) Create a new account\n2) Deposit money in your account\n3) Withdraw money from our account\n4) Transfer money\n5) Delete your account\n6) EXIT')
        #print('Select: \n1) Exixsting user.\n2) Create new account.')
        option = int(input('Enter 1 if you want to create new account.\nEnter 2 if you already have an account\nEnter 3 to EXIT.'))

        while(True):
            import os
            os.system('clear')
            if (option == 1) :
                create()
                break
            if (option == 2):
                choice = int(input('Below are the services we offer: \n1) Deposit money in your account\n2) Withdraw money from our account\n3) Transfer money\n4) Delete your account\n5) EXIT'))
                if choice == 5:
                    break
                temp_accno = int(input('Please enter your Account Number: '))
                temp_pass = int(input('Please enter your 4 digit pass code: '))
                #choice = int(input('Below are the services we offer: \n1) Deposit money in your account\n2) Withdraw money from our account\n3) Transfer money\n4) Delete your account\n5) EXIT'))
                info = fetch(temp_pass,temp_accno)
                new_trans = accounts(info[0][1],info[0][3],info[0][4],info[0][5],info[0][2],info[0][6])
                if (choice == 1) :
                    deposit()
                if choice == 2 :
                    withdraw()
                if choice == 3:
                    transfer()
                if choice == 4:
                    delete()
                if choice == 5:
        if option == 3:
                break

    cont = input('Do you want to continue banking? (YES/NO)')
    if cont.lower() == 'yes':
        now = True
    else:
        now = False


conn.close()

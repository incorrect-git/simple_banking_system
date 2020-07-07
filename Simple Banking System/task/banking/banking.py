import sqlite3
import random
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
# cur.execute("drop table card")
# conn.commit()
cur.execute('create table IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0 )')
conn.commit()


class SQL:
    conn = None
    cur = None

    def __init__(self):
        self.conn = conn
        # self.conn = sqlite3.connect('../card.s3db')
        self.cur = self.conn.cursor()

    def insert(self, sql):
        self.cur.execute(sql)
        self.conn.commit()

    def update(self, sql):
        self.cur.execute(sql)
        self.conn.commit()

    def select_all(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def select_one(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchone()

    def delete(self, sql):
        self.cur.execute(sql)
        self.conn.commit()


class OtherFunc:
    @staticmethod
    def gen_rand_number(numb):
        return ''.join(['{}'.format(random.randint(0, 9)) for num in range(0, numb)])

    @staticmethod
    def check_lua(card):
        i = 1
        sumDigits = 0
        for digit in card:
            digitOne = int(digit)
            if i % 2 != 0:
                digitOne = int(digit) * 2
            if digitOne > 9:
                digitOne -= 9

            sumDigits += digitOne

            # cardCash += str(digitOne)
            i += 1

        return True if sumDigits % 10 == 0 else False
        # CHECK_SUM = 10 - SUM_DG if SUM_DG > 0 else 0

    @staticmethod
    def gen_card(genMII, genIIN):
        accountGen = OtherFunc.gen_rand_number(9)
        CHECK_SUM = 0
        card = "{}{}{}".format(genMII, genIIN, accountGen)
        i = 1
        sumDigits = 0
        for digit in card:
            digitOne = int(digit)
            if i % 2 != 0:
                digitOne = int(digit) * 2
            if digitOne > 9:
                digitOne -= 9

            sumDigits += digitOne

            # cardCash += str(digitOne)
            i += 1

        SUM_DG = (sumDigits % 10)
        CHECK_SUM = 10 - SUM_DG if SUM_DG > 0 else 0
        # CHECK_SUM = 10 - (sumDigits % 10)
        # print("test", sumDigits)
        # print("test", (10 - (sumDigits % 10)))
        return "{}{}{}{}".format(genMII, genIIN, accountGen, CHECK_SUM)
        pass


# Write your code here
class BankSystem:
    MII = "4"
    IIN = "00000"
    card = None
    PIN = None
    status = "off"
    login_info_account = None

    def __init__(self):
        pass

    def create_account(self):
        random.seed()
        self.PIN = OtherFunc.gen_rand_number(4)
        # self.account = OtherFunc.gen_rand_number(9)
        # self.card = "{}{}{}{}".format(self.MII, self.IIN, self.account, self.CHECK_SUM)
        self.card = OtherFunc.gen_card(self.MII, self.IIN)

        sql = SQL()
        sql.insert("insert into card (number, pin) values ({}, {})".format(self.card, self.PIN))
        # self.db[self.card] = Client(self.card, self.PIN).get_info()
        print("Your card has been created")
        print("Your card number:\n{}".format(self.card))
        print('Your card PIN:\n{}'.format(self.PIN))
        # return "{}{}{}{}".format(self.MMI, self.IIN, self.account, self.CHECK_SUM)

    def delete_account(self):
        sql = SQL()
        sql.delete("delete from card where number = {}".format(self.login_info_account))
        print("The account has been closed!")
        self.login_info_account = None
        pass

    def transfer(self):
        print("Transfer")
        card_transfer = input("Enter card number:\n> ")
        if OtherFunc.check_lua(card_transfer) is False:
            print("Probably you made mistake in the card number. Please try again!")
        numb_transfer = input("Enter how much money you want to transfer:\n> ")

        sql = SQL()
        find_account = sql.select_one("select * from card where number = {}".format(card_transfer))
        if find_account is not None:
            balance_check = sql.select_one("select * from card where number = {} and balance >= {}".format(self.login_info_account, numb_transfer))
            if balance_check is not None:
                sql.update("update card set balance = balance + {} where number = {}".format(numb_transfer, card_transfer))
                sql.update("update card set balance = balance - {} where number ={}".format(numb_transfer, self.login_info_account))
                print("Success!")
            else:
                print("Not enough money!")
        else:
            print("Such a card does not exist.")

        # print(OtherFunc.check_lua(card_transfer))



        pass

    def login_account(self):
        card = input("Your card number:\n")
        pin = input("Your card PIN:\n")
        sql = SQL()
        result = sql.select_one("select * from card where number = {} and pin = {}".format(card, pin))

        if result is not None:
            print("You have successfully logged in!")
            print(result)
            self.login_info_account = result[1]
        else:
            print("Wrong card number or PIN!")
        # if len(self.db) != 0 and card in self.db and self.db[card]['PIN'] == pin:
        #     print("You have successfully logged in!")
        #     self.login_info_account = card
        # else:
        #     print("Wrong card number or PIN!")

    def add_income(self):
        input_income = int(input("Enter income:\n> "))
        sql = SQL()
        sql.update("update card set balance = balance + {} where number = {}".format(input_income, self.login_info_account))
        print("Income was added!")
        pass

    def logout(self):
        print("You have successfully logged out!")
        self.login_info_account = None

    def account_check(self):
        sql = SQL()
        result = sql.select_one("select * from card where number = {}".format(self.login_info_account))
        print("Balance: {}".format(result[3]))
        # print(self.db[self.login_info_account]['account'])


class Client:

    account = 0

    def __init__(self, card, pin):
        self.card = card
        self.pin = pin
        pass

    def get_info(self):
        return {'PIN': self.pin, 'account': self.account, 'card': self.card}
    # def __repr__(self):
    #     return {self.pin, self.account, self.card}


bank = BankSystem()
# bank.create_account()
# bank.login_account()

while True:
    if bank.login_info_account is not None:
        bank.action = input("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out 
0. Exit
> """)
        if bank.action == '1':
            bank.account_check()
        elif bank.action == '2':
            bank.add_income()
        elif bank.action == '3':
            bank.transfer()
        elif bank.action == '4':
            bank.delete_account()
        elif bank.action == '5':
            bank.logout()
        elif bank.action == '0':
            break
    else:
        bank.action = input("""1. Create an account
2. Log into account
0. Exit
> """)
        if bank.action == '1':
            bank.create_account()
        elif bank.action == '2':
            bank.login_account()
        elif bank.action == '0':
            print("Bye!")
            break

# This is a sample Python script.
import datetime
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import psycopg2
import time
import random

init = """CREATE Table customer (
	cID serial PRIMARY KEY,
	FirstName varchar(255),
	LastName varchar(255),
	isMember bool
);

CREATE Table address (
	addrID serial PRIMARY KEY,
	street varchar(255) UNIQUE,
	city varchar(255),
	zipCode char(5)
);
	
CREATE Table business (
	bID serial PRIMARY KEY,
	BusinessName varchar(255)
);

CREATE Table videogame (
	videogameID serial PRIMARY KEY,
	genre varchar(255),
	ageRating varchar(3), --thingslike 3-10, 13+, etc
	playerCount int,
	expectedTickets int, --can be 0 if doesn't give tickets
	isCompetitive bool, 
	reviewScore int --out of 5 stars	
);
	
Create Table craneGame (
	cranegameID serial PRIMARY KEY,
	craneSize varchar(6), --small, medium, large
	gripChance DECIMAL(3,2), --crane games actually have random chance to fully grip
	CHECK (gripChance > 0 AND gripChance <= 1)
);

CREATE Table game (
	gameID serial PRIMARY KEY,
	gameName TEXT,
	dayPrice int,
	widthDim DECIMAL(5, 2), 
	lengthDim DECIMAL(5, 2),
	heightDim DECIMAL(5, 2),
	releaseDate DATE,
	powerUsage int,
	videogameID int REFERENCES videogame, --Disjoint, can only be one
	cranegameID int REFERENCES cranegame
);

CREATE Table machine (
	gameID int REFERENCES game,
	machineID int,  --Weak entity set, since multiple machines exist for same game
	working bool, --is it broken?
	PRIMARY KEY (gameID, machineID)
);


CREATE Table prizes (
	prizeID serial PRIMARY KEY,
	prizeName varchar(255),
	shipmentCost DECIMAL(5,2),
	shipmentStock int,
	numberInShipment int,
	prizeSize varchar(6), --small, medium, large
	CHECK (shipmentCost > 0)
);

CREATE Table owners (
	customerID int REFERENCES customer, --can only be one, disjoint
	businessID int REFERENCES Business, --if one, other is null
	accountemail TEXT PRIMARY KEY,
	accountPassword TEXT,
	phoneNumber varchar(10), --allow only one, but not necessarily unique, like family phone	
	UNIQUE(customerID,businessID)
);

CREATE Table payInfo (
	payInfoID serial PRIMARY KEY,
	creditCardNum varchar(16), --can be 15 or 16
	expirationDate char(5), --not like standard date, xx/xx
	securityCode int
);


Create Table orderStatus (
	orderID serial PRIMARY KEY,
	orderDate DATE,
	overdueDate DATE, --after this, late fees applied
	status varchar(12) --4 statuses: SHIPPED, DELIVERED, PICKUP, RETURNING
);

--RELATIONS 

CREATE Table machineOrder (
	orderID int REFERENCES orderStatus, 
	machineID int,
	gameID int,
	FOREIGN KEY (gameID,machineID) REFERENCES machine(gameID,machineID),
    Primary Key(orderID)
);

CREATE Table orderOwner (
	orderId int REFERENCES orderStatus,
	ownerEmail TEXT REFERENCES owners,
	PRIMARY KEY (orderID)
);

CREATE Table cranePrize (
	prizeID int REFERENCES prizes, --different machines can use same prize
	craneGameID int REFERENCES craneGame, --and different prizes in same machine
	PRIMARY KEY(prizeID, craneGameID)
);

CREATE Table machineAddr (
	gameID int,
	machineID int,
	addrID int REFERENCES address, --null if in middle of delivery, else at location or storage
	FOREIGN KEY (gameID,machineID) REFERENCES machine(gameID,machineID),
	PRIMARY KEY (gameID,machineID)
);

CREATE Table ownerPay (
	ownerEmail TEXT REFERENCES owners,
	payInfoID int REFERENCES payInfo, --different users can have same payment method, like family card
    PRIMARY KEY (ownerEmail)
);

CREATE table ownerAddr(
	ownerEmail TEXT REFERENCES owners PRIMARY KEY,
	addrID int REFERENCES address
);

	
CREATE Table auction (
	gameID int,
	machineID int,
	highestBidder TEXT REFERENCES owners,
	bidAmount DECIMAL(9,2),
	FOREIGN KEY (machineID,gameID) REFERENCES machine(gameID, machineID),
	PRIMARY KEY(gameID, machineID)
);	
"""
clear = """DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS address CASCADE;
DROP TABLE IF EXISTS business CASCADE;
DROP TABLE IF EXISTS videogame CASCADE;
DROP TABLE IF EXISTS craneGame CASCADE;
DROP TABLE IF EXISTS game CASCADE;
DROP TABLE IF EXISTS machine CASCADE;
DROP TABLE IF EXISTS prizes CASCADE;
DROP TABLE IF EXISTS owners CASCADE;
DROP TABLE IF EXISTS payInfo CASCADE;
DROP TABLE IF EXISTS orderStatus CASCADE;
DROP TABLE IF EXISTS machineOrder CASCADE;
DROP TABLE IF EXISTS orderOwner CASCADE;
DROP TABLE IF EXISTS cranePrize CASCADE;
DROP TABLE IF EXISTS machineAddr CASCADE;
DROP TABLE IF EXISTS ownerPay CASCADE;
DROP TABLE IF EXISTS ownerAddr CASCADE;
DROP TABLE IF EXISTS auction CASCADE;"""
example = """
INSERT INTO videoGame (genre, ageRating, playerCount, expectedTickets, isCompetitive, reviewScore)
VALUES 
('Fighting', '13+', 2, 0, true, 5), --1
('Platformer', '5+', 1, 20, false, 4) --2
;

INSERT INTO craneGame (craneSize, gripChance)
VALUES ('Large', 0.3) --1
;

--text, int, decimal, decimal, decimal, Date, int, int, int
INSERT INTO game (gameName, dayPrice, widthDim, lengthDim, heightDim, releaseDate, powerUsage, videogameId, cranegameId)
VALUES 
('StreetFighter 2', 30, 0.5,0.5,0.5, '1991-02-01', 1000, 1, Null),  --1 
('Donkey Kong', 20, 0.75,0.5,0.5, '1981-07-15', 300, 2, Null), --2
('Plush Mega-Crane', 30, 0.75, 0.75, 0.75, '2000-05-25', 1250, Null, 1) --3   
;

INSERT INTO machine (gameId, machineId, working) --4
VALUES 
(1,1,True),
(1,2,False),
(1,3,False),
(2,1,True),
(3,1,True)
; 

INSERT INTO prizes (shipmentCost, shipmentStock, numberInShipment, prizeSize, prizeName)
VALUES (20, 5, 5, 'Small', 'Bunny Plush') --1
; 

INSERT INTO cranePrize (prizeID, craneGameId)
VALUES (1,1)
;

INSERT INTO customer (FirstName, LastName, isMember)
VALUES ('Bob', 'Smith', True) --1
;

INSERT INTO business (businessName)
VALUES ('BigCorp Inc.') --1
;

INSERT INTO owners (accountEmail, accountPassword, phoneNumber, customerId, businessId)
VALUES 
('bobbyboy@gmail.com', 'smithMan7', '5557654321', 1, Null),
('bigcorp@gmail.com', 'SupplyandDemand', '1115671234', Null, 1)
;

INSERT INTO payInfo (creditCardNum, expirationDate, securityCode)
VALUES 
('1111333355557777', '07/35', 123), --1
('1212343456567878', '03/29', 234) --2
;

INSERT INTO ownerPay (ownerEmail, payInfoID)
VALUES
('bobbyboy@gmail.com', 1),
('bigcorp@gmail.com', 2)
;

INSERT INTO address (street, city, zipCode)
VALUES
('123 S. Bark St', 'Chicago', '12345'), --1
('6700 Sponge Ave', 'Detroit', '56789'), --2
('56 Arcade St', 'Springfield', '11998')  --3
;

INSERT INTO ownerAddr (ownerEmail, addrId)
VALUES 
('bobbyboy@gmail.com', 1),
('bigcorp@gmail.com', 2)
;

INSERT INTO machineAddr (gameId, machineId, addrId)
VALUES 
(1, 1, 3),
(1, 2, 3),
(2, 1, 3)
;

INSERT INTO auction (gameId, machineId, highestbidder, bidAmount)
VALUES (1, 2, 'bobbyboy@gmail.com', 350)
;

INSERT INTO orderStatus (orderDate, overdueDate, status)
VALUES ('2023-01-01', '2023-01-015', 'Delivered') --1
;

INSERT INTO orderOwner (orderID, ownerEmail)
VALUES (1, 'bobbyboy@gmail.com')
;

INSERT INTO machineOrder (orderID, machineID, gameID)
VALUES (1, 1, 1)
;

"""
create = """CREATE DATABASE CS425ProjectArcade"""

debug = False

class menu:

    def __init__(self):
        self.email = None
        print("""This program requires postgresql server access.
              Please ensure you have it installed and enter the following
              to establish a connection.""")
        user = input("postgresql user: ")
        password = input("postgresql password: ")
        try:
            self.program = dataHandler(user, password)
        except:
            print("Connection Failed, Either input incorrect or requirements not met")
            time.sleep(2)
            exit()
        self.program.create()
        self.program.clear()
        self.program.start()
        self.program.populate()
        self.signScreen()

    def signScreen(self):
        print("Would you like to sign in or create an account (S: sign in, C: Create, X: Exit, I: Login Info)")
        cmd = input()
        while not self.validAnswer(cmd, 1):
            print("Input Error, please retry")
            print("Would you like to sign in or create an account (S: sign in, C: Create, X: Exit, I: Account Info)")
            cmd = input()
        cmd = cmd.lower()
        if cmd == "s":
            if self.signIn():
                print("\nHello, " + self.email)
                self.menuScreen()
            else:
                self.signScreen()
                self.program.close()
                exit()
        if cmd == "c":
            self.createAccount()
            print("\nHello, " + self.email)
            self.menuScreen()
        if cmd == "i":
            print("Here are existing accounts to try out: (Email, Password)")
            print(self.program.grab(("owners",),("accountEmail", "accountPassword")))
            self.signScreen()
        if cmd == "x":
            self.program.close()
            exit()

    def menuScreen(self):
        print("What would you like to do? (m:See/Rent Machines, a:See Auctions, i:See Account Info, o: See current renting, x: Exit)")
        ans = input()
        while not self.validAnswer(ans, 4):
            print("Error in Input. Please try again")
            print("What would you like to do? (m:See/Rent Machines, a:See Auctions, i:See Account Info, o: See current renting, x: Exit)")
            ans = input()
        ans = ans.lower()
        if ans == "x":
            self.program.close()
            exit()
        if ans == "m":
            self.seeGames()
        if ans == "a":
            self.seeAuctions()
        if ans == "o":
            self.orderHistory()
        if ans == "i":
            self.seeInfo()

    def validAnswer(self, input : str, mode : int, num = 0):
        answ = input.lower()
        # mode 1 is initial screen
        if mode == 1:
            if answ == "s" or answ == "c" or answ == "x" or answ == "i":
                return True
            return False
        if mode == 2:
            if "@" in answ and "." in answ:
                return True
            return False
        if mode == 3:
            if answ.isdigit():
                if int(input) > 0 and int(input) < num + 1:
                    return True
            elif answ == "x":
                return True
            return False
        if mode == 4:
            if answ == "m" or answ == "a" or answ == "i" or answ == "o" or answ == "x":
                return True
            return False
        if mode == 5:
            if answ == "y" or answ == "n":
                return True
            return False
        if mode == 6:
            if answ.isdecimal():
                if int(answ) > 0 and int(answ) < 10000000:
                    return True
                else:
                    return False
            return False
        if mode == 7:
            if len(answ) == 10 and answ.isdigit():
                return True
            return False
        if mode == 8:
            if len(answ) == 5 and answ.isdigit():
                return True
            return False



    def signIn(self):
        print("Insert Email (Case sensitive): ")
        cmd = input()
        while not self.validAnswer(cmd, 2):
            print("Input Error, email requires @ and . characters")
            print("Insert Email: ")
            cmd = input()
        email = cmd
        print("Insert Password (Case sensitive): ")
        passwordIn = input()
        account = self.program.grab(("owners",), ("accountEmail",), "accountEmail = '" + email + "' AND accountPassword = '" + passwordIn + "'")
        if not isEmpty(account):
            self.email = account[0][0]
            return True
        else:
            print("No Account with that email/password exist")
            return False

    def accountAddress(self):
        print("Insert Address, Street: ")
        addr = input()
        print("Insert City: ")
        city = input()
        print("Insert Zip Code (5 digits): ")
        zip = input()
        while not self.validAnswer(zip, 8):
            print("Input Error, zip code must be 5 digits")
            print("Insert Zip Code (5 digits): ")
            zip = input()
        adrId = self.program.addAddress(addr, city, zip)[0] #need ID
        self.program.attachAddress(adrId, self.email)

    def createAccount(self):
        print("Insert Email: ")
        cmd = input()
        while not self.validAnswer(cmd, 2):
            print("Input Error, email requires @ and . characters")
            print("Insert Email: ")
            cmd = input()
        email = cmd
        print("Insert Password: ")
        passwordIn = input()
        print("Insert First Name: ")
        fname = input()
        print("Insert Last Name: ")
        lname = input()
        print("Insert Phone Number (No dashes, 10 characters) Ex: 1234567890: ")
        phone = input()
        while not self.validAnswer(phone, 7):
            print("Phone Number Input Error")
            print("Insert Phone Number (No dashes, 10 characters) Ex: 1234567890: ")
            phone = input()
        self.program.addUser(fname, lname, False, email, passwordIn, phone)
        self.program.generatePayInfo(email)
        self.email = email
        self.accountAddress()

    def space(self):
        print("\n{--- --- --- --- --- --- --- --- --- ---}\n")

    def seeGames(self):
        games = self.program.grab(("game",),("*",))
        for i in range(0, len(games)):
            type = " (Video Game)"
            if games[i][9] is not None:
                type = " (Crane Game)"
            print(str(i+1) + ": " + games[i][1] + type) # 1 index is the name
        print("Which Game Would you like to see/Rent?: (x to exit) ")
        ans = input()
        while not self.validAnswer(ans, 3, len(games)):
            print("Input error: Please enter a number in range")
            print("Which Game Would you like to see/Rent?: (x to exit) ")
            ans = input()
        ans = ans.lower()
        if ans == "x":
            self.program.close()
            exit()
        else:
            self.viewGame(games[int(ans)-1])

    def viewGame(self, gameTuple):
        print("About " + str(gameTuple[1]))
        print("Price Per Day: $" + str(gameTuple[2]))
        print("Dimensions: " + "w-" + str(gameTuple[3]) + "m, l-" + str(gameTuple[4]) + "m, h-" + str(gameTuple[5]) + "m")
        print("Release Date: " + str(gameTuple[6]))
        print("Power Usage: " + str(gameTuple[7]) + "W")
        if gameTuple[8] is not None: # is a video game, not a crane game
            videoGameTuple = self.program.grab(("videogame",),("*"),"""VideogameID = """ + str(gameTuple[8]))[0]
            print("Genre: " + videoGameTuple[1])
            print("ageRating: " + videoGameTuple[2])
            print("Number of Players: " + str(videoGameTuple[3]))
            print("Expected Number of Tickets: " + str(videoGameTuple[4]))
            print("Is the Game Competitive: " + str(videoGameTuple[5]))
            print("Review Score: " + str(videoGameTuple[6]) + "/5")
        else:
            craneGameTuple = self.program.grab(("cranegame",),("*"),"""cranegameId = """ + str(gameTuple[9]))[0]
            print("craneSize: " + craneGameTuple[1])
            print("gripChange: " + str(craneGameTuple[2]))
            print("This Crane Game comes with the following prize(s)")
            table = """(SELECT prizeID FROM cranePrize WHERE craneGameID = """ + str(gameTuple[9]) + ")"
            prizes = self.program.grab((table + "NATURAL JOIN prizes",),("*",))
            for prize in prizes:
                print("--------------------")
                print("Prize Name: " + prize[1])
                print("Number in Shipment: " + str(prize[4]))
                print("Prize Size: " + prize[5])

        table = "game NATURAL JOIN machine"
        query = """((gameID,machineID) NOT IN (SELECT gameId, machineID FROM machineOrder)) 
         AND ((gameID,machineID) NOT IN (SELECT gameId, machineID FROM auction))
         AND gameID = """ + str(gameTuple[0])
        rentables = self.program.grab(("machine",),("*",), query) # index 1 is machineID, next is gameID
        if isEmpty(rentables):
            print("Unfortunately, all machines of this game are being rented/auctioned. Please check again later")
        else:
            print("A machine for this game is available to rent. Would you like to do so? y/n")
            rentAns = input()
            while not self.validAnswer(rentAns, 5):
                print("Input Error, please reinput")
                print("A machine for this game is available to rent. Would you like to do so? y/n")
                rentAns = input()
            rentAns = rentAns.lower()
            if rentAns == "y":
                gameID = rentables[0][0]
                machineID = rentables[0][1]
                print(gameID)
                self.program.rentAMachine(self.email, machineID, gameID)
                print("You have now rented this machine. It will be on its way. Find it in your 'currently renting' section")
        self.menuScreen()

    def seeAuctions(self):
        Featuredauction = self.program.grab(("auction",),("*",))[0] # first is tuple
        winner = Featuredauction[2]
        gameId = Featuredauction[0]
        machineID = Featuredauction[1]
        bid = Featuredauction[3]
        gameName = self.program.grab(("game",),("gameName",),"gameID = " + str(gameId))[0][0]
        print("Todays Featured Auction is a " + gameName + " Machine")
        if winner == self.email:
            print("The winning bidder is you (" + winner + "), with a winning bid of $" + str(bid))
            print("You cannot increase a bid as a current winner")
        else:
            print("The winning bidder is " + winner + ", with a winning bid of $" + str(bid))
            print("Would you like to place a bid? y/n")
            ans = input()
            while not self.validAnswer(ans, 5):
                print("Input Error")
                print("Would you like to place a bid? y/n")
                ans = input()
            ans = ans.lower()
            if ans == "y":
                print("How much would you like to bid? (Integer Between 1 and 10000000)")
                b = input()
                while not self.validAnswer(b, 6):
                    print("Bid input Error")
                    print("How much would you like to bid? (Integer Between 1 and 10000000)")
                    b = input()
                if self.program.setAuctionWinner(machineID, gameId, self.email, int(b)):
                    print("You have set the bid to $" + str(b))
                else:
                    print("The bid did not exceed the current bid")
        self.menuScreen()

    def orderHistory(self):
        userOrderTable = "(SELECT orderID FROM orderOwner WHERE ownerEmail = " + quotes(self.email) + ")"
        userMachineTables = "machineOrder NATURAL JOIN " + userOrderTable
        fullOrderTable = "orderStatus NATURAL JOIN (" + userMachineTables + ")"
        userOrders = self.program.grab((fullOrderTable,),("orderID", "machineID", "gameID", "orderDate", "overdueDate"))
        i = 0
        if isEmpty(userOrders):
            print("You have no machines currently rented"
                  "")
        for machine in userOrders:
            i += 1
            gameId = machine[2]
            rentDate = machine[3]
            dueDate = machine[4]
            gameName = self.program.grab(("game",), ("gameName",), "gameID = " + str(gameId))[0][0]
            print("Game " + str(i) + ":" + gameName)
            print("-Rented on " + str(rentDate))
            print("-Return by " + str(dueDate))
        self.menuScreen()

    def seeInfo(self):
        userPayInfoTable = """SELECT * FROM ownerPay WHERE ownerEmail = """ + quotes(self.email)
        payInfoTable = """payInfo NATURAL JOIN (""" + userPayInfoTable + ")"
        payInfo = self.program.grab((payInfoTable,),("creditCardNum","expirationDate","securityCode"))[0]
        ccNum = payInfo[0]
        eD = payInfo[1]
        secCode = str(payInfo[2])
        userAddressTable = """SELECT * FROM ownerAddr WHERE ownerEmail = """ + quotes(self.email)
        userAddress = """address NATURAL JOIN (""" + userAddressTable + ")"
        addrInfo = self.program.grab((userAddress,), ("street", "city", "zipCode"))[0]
        street = addrInfo[0]
        city = addrInfo[1]
        zip = addrInfo[2]

        print("Payment Info (Randomly Generated for Security Purposes)")
        print("Credit Card Num: " + ccNum)
        print("Expiration Date: " + eD)
        print("Security Code: " + secCode)

        print("Address Info")
        print("Street: " + street)
        print("City: " + city)
        print("Zip: " + zip)
        self.menuScreen()


class dataHandler:


    def __init__(self, user, password):
        self.conn = psycopg2.connect(host="localhost", user=user, password=password)
        self.cur = self.conn.cursor()
        self.conn.autocommit = True

    def create(self):
        try:
            exists = self.cur.execute('DROP DATABASE IF EXISTS cs425projectarcade')
            self.cur.execute(create)
            self.conn.commit()
        except:
            print("Error Another Program is using this database, could not clear out")
            time.sleep(3)
            self.close()
            exit()

    def clear(self):
        self.cur.execute(clear)
        self.conn.commit()

    def start(self):
        self.cur.execute(init)
        self.conn.commit()

    def populate(self):
        self.cur.execute(example)

    def exec(self,string):
        returnQ = self.cur.execute(string)
        self.conn.commit()
        return  returnQ

    def close(self):
        self.cur.close()
        self.conn.close()

    def insert(self, table, areas : tuple, values: tuple):
        # inserts and returns tuple (including id/serial)
        if debug:
            if len(areas) != len(values):
                print("Error, insert area and values different length")
        stringQuery = """INSERT INTO """ + table + "("
        for i in range(0,len(areas)):
            stringQuery += areas[i]
            if i != len(areas) - 1:
                stringQuery += ","
        stringQuery += ")\n"
        stringQuery += "VALUES ("
        for i in range(0, len(values)):
            if isinstance(values[i], str):
                stringQuery += "'" + values[i] + "'"
            else:
                stringQuery += str(values[i])
            if i != len(areas) - 1:
                stringQuery += ","
        stringQuery += ");\n"
        if debug: print(stringQuery)
        self.exec(stringQuery)
        self.conn.commit()
        query = ""
        for i in range(0, len(areas)):
            query += areas[i] + " = "
            if isinstance(values[i], str):
                query += "'" + values[i] + "'"
            else:
                query += str(values[i])
            if i != len(areas) - 1:
                query += " AND "
        item = self.grab((table,),("*"), query)
        if len(item) > 1:
            max = -1 # get biggest Id
            maxHolder = None
            for x in item:
                if x[0] > max:
                    max = x[0]
                    maxHolder = x
            return maxHolder
        return item[0] # tuple in list

    def update(self, table, areas: tuple, values: tuple, condition = None):
        if debug:
            if len(areas) != len(values):
                print("Error, insert area and values different length")
        stringQuery = """UPDATE """ + table + "\n SET "
        for i in range(0,len(areas)):
            stringQuery += areas[i] + " = " + quotes(values[i])
            if i != len(areas) - 1:
                stringQuery += ","
        stringQuery += "\n"
        if condition is not None:
            stringQuery += "WHERE " + condition
        stringQuery += ";\n"
        if debug: print("update query: \n" + stringQuery)
        self.exec(stringQuery)
        self.conn.commit()

    def grab(self, tables : tuple, columns : tuple, conditionString = None):
        stringQuery = """SELECT """
        for i in range(0, len(columns)):
            stringQuery += columns[i]
            if i != len(columns) - 1:
                stringQuery += ","
        stringQuery += "\n"
        stringQuery += "FROM "
        for i in range(0, len(tables)):
            stringQuery += tables[i]
            if i != len(tables) - 1:
                stringQuery += ","
        stringQuery += "\n"
        if conditionString is not None:
            stringQuery += "WHERE " + conditionString
        stringQuery += ";\n"
        if debug: print(stringQuery)
        self.cur.execute(stringQuery)
        return self.cur.fetchall()

    def seeIfExist(self, table: str, columns: tuple, values: tuple):
        # returns True if exist and false is not
        if debug:
            if len(columns) != len(values):
                print("Error-Exists, values and values different length")
        query = ""
        for i in range (0,len(columns)):
            query += columns[i] + " = "
            if isinstance(values[i], str):
                query += "'" + values[i] + "'"
            else:
                query += str(values[i])
            if i != len(columns) - 1:
                query += " AND "
        print("exists query" + query)
        grabbedItem = self.grab((table,),columns,query)
        return not isEmpty(grabbedItem)

    def addCustomer(self, fname, lname, isMember):
        self.insert("customer", ("FirstName", "LastName", "isMember"), (fname,lname,isMember))

    def attachAddress(self, addrId, ownerEmail):
        self.insert("ownerAddr", ("ownerEmail","addrId"), (ownerEmail, addrId))

    def addAddress(self, street, city, zipCode):
        # returns Id if created or already existing
        return self.insert("address", ("street","city","zipCode"),(street, city, zipCode))

    def addUser(self, fName, lName, isMember, email, password, phone):
        self.addCustomer(fName,lName,isMember)
        id = self.grab(("customer",), ("MAX(cId)",))[0][0] #first of list and of first tuple in list is ID
        # automatically converted to int
        # self.insert()
        self.insert("owners", ("customerId", "accountEmail","accountPassword","phoneNumber"), (id, email, password, phone))

    def createOrder(self, machineId, gameId):
        today = datetime.date.today()
        returntime = today + datetime.timedelta(weeks=2)
        id = self.insert("orderStatus", ("orderDate","overdueDate", "status"), (str(today),str(returntime),"Shipped"))[0] # 1st index is id
        return id

    def rentAMachine(self, ownerEmail, machineId, gameId):
        # returns true if is rentable and false if not
        orderId = self.createOrder(machineId, gameId)
        self.insert("orderOwner", ("ownerEmail","orderId"),(ownerEmail,orderId))
        self.insert("machineOrder", ("orderId", "machineId", "gameId"), (orderId, machineId, gameId))

    def setAuctionWinner(self, machineId, gameId, winnerCandidate, amount):
        # returns true if changed to newOwner and false if Not
        bidAmount = self.getBid(machineId, gameId)
        if bidAmount is None:
            if debug:
                print("No auction exists")
                return False
        if amount <= bidAmount:
            return False
        condition = "machineId = " + quotes(machineId) + " AND gameId = " + quotes(gameId)
        self.update("auction", ("highestBidder","bidAmount"), (winnerCandidate,amount), condition)
        return True

    def getBid(self, machineId, gameId):
        returnVal = None # returns none if no auction exists for machine
        ifState = "machineId = " + str(machineId) + " AND gameID = " + str(gameId)
        returnVal = self.grab(("auction",),("bidAmount",),ifState)[0][0]
        if debug: print("Bid Return Val: " + str(returnVal))
        return returnVal

    def getGames(self):
        videoGames = self.grab(("game NATURAL JOIN videogame"), ("*"))
        craneGames = self.grab(("game NATURAL JOIN craneGame"), ("*"))
        return [videoGames, craneGames]

    def generatePayInfo(self, email):
        randomCard = str(random.randint(100000000000000,9999999999999999))
        expirationDate1 = str(random.randint(1,12))
        expirationDate2 = str(random.randint(1,12))
        if len(expirationDate1) == 1: expirationDate1 = "0" + expirationDate1
        if len(expirationDate2) == 1: expirationDate2 = "0" + expirationDate2
        finalDate = expirationDate1 + "/" + expirationDate2
        secCode = random.randint(100,999) # remember to stay an int
        infoID = self.insert("payInfo", ("creditCardNum","expirationDate","securityCode"), (randomCard, finalDate,secCode))[0] # need ID
        self.insert("ownerPay", ("ownerEmail","payInfoID"), (email, infoID))
    # def generateAddress(self, email):

    def getAuctions(self):
        return self.grab(("auction",),("*"))

    def getPrizes(self, craneId):
        return self.grab(("""(SELECT prizeID FROM cranePrize WHERE prizeId = """ + str(craneId) + ")"), ("*"))

def isEmpty(l : list):
    if l == []:
        return True
    else: return False

def quotes(item):
    if isinstance(item, str):
        return "'" + item + "'"
    else:
        return str(item)

main = menu()
#main = None
#try:
#    main = menu()
#except:
#    if main is not None:
#        if main.program is not None:
#            main.program.close()

# system.clear()
# system.start()
# system.populate()
# system.insert("customer", ("FirstName", "LastName", "isMember"), ("Bob", "Smith", True))
# print(system.seeIfExist("customer", ("FirstName",), ("Bob",)))

# print(system.grab(("customer",), ("MAX(cId)",))[0][0])

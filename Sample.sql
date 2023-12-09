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
CREATE Table customer (
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
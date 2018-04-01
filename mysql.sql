DROP DATABASE marktplaats;
CREATE DATABASE `marktplaats`;
USE marktplaats;
CREATE TABLE `Search` (
  `searchID` INT AUTO_INCREMENT NOT NULL,
  `query` VARCHAR(50) NOT NULL,
  `maxPrice` DECIMAL NOT NULL,
  `minPrice` DECIMAL NOT NULL,
  `maxBidPrice` DECIMAL NOT NULL,
  `distance` INT NOT NULL,
  `zipCode` VARCHAR(8) NOT NULL,
  `link` VARCHAR(500) NOT NULL,
  PRIMARY KEY (`searchID`)
);

CREATE TABLE `Advert` (
  `advertID` INT AUTO_INCREMENT NOT NULL,
  `searchID` INT NOT NULL,
  `title` VARCHAR(65) NOT NULL,
  `date` DATE NOT NULL,
  `description` VARCHAR(350),
  `priceNumber` DECIMAL,
  priceString VARCHAR(30),
  isPriceString BOOLEAN,
  isBidding BOOLEAN,
  `city` VARCHAR(150),
  `link` VARCHAR(500) NOT NULL,
  photoLink VARCHAR(500),
  PRIMARY KEY (`advertID`),
  FOREIGN KEY (searchID) REFERENCES Search(searchID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `Included` (
  `includedID` INT AUTO_INCREMENT NOT NULL,
  `include` VARCHAR(100) NOT NULL,
	PRIMARY KEY (`includedID`)
);

CREATE TABLE `Excluded` (
  `excludedID` INT AUTO_INCREMENT,
  `exclude` VARCHAR(100),
  PRIMARY KEY (`excludedID`)
);

CREATE TABLE `SearchIncluded` (
  `SearchIncludedID` INT AUTO_INCREMENT,
  `searchID` INT,
  `includedID` INT,
  PRIMARY KEY (`SearchIncludedID`),
  FOREIGN KEY (searchID) REFERENCES Search(searchID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (includedID) REFERENCES Included(includedID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `SearchExcluded` (
  `searchExcludedID` INT AUTO_INCREMENT,
  `searchID` INT,
  `excludedID` INT,
  PRIMARY KEY (`searchExcludedID`),
  FOREIGN KEY (searchID) REFERENCES Search(searchID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (excludedID) REFERENCES Excluded(excludedID) ON DELETE CASCADE ON UPDATE CASCADE
);



USE marktplaats;
INSERT INTO Search (query, maxPrice, minPrice, maxBidPrice, distance, zipCode, link)
VALUES ("iphone 7", 300, 200, 300, 15000, "3445TA","https://www.marktplaats.nl/z/telecommunicatie/mobiele-telefoons-apple-iphone/iphone-7.html?query=iphone%207&categoryId=1953"), ("iphone 6", 100, 50, 100 ,15000, "3445TA","https://www.marktplaats.nl/z/telecommunicatie/mobiele-telefoons-apple-iphone/iphone-6.html?query=iphone%206&categoryId=1953");

INSERT INTO Included(include)
VALUES("barst");

INSERT INTO Included(include)
VALUES("Barst");

INSERT INTO Included(include)
VALUES("scherm");

INSERT INTO Included(include)
VALUES("Scherm");

INSERT INTO Included(include)
VALUES("accu");

INSERT INTO Included(include)
VALUES("Accu");

INSERT INTO Included(include)
VALUES("camera");

INSERT INTO Included(include)
VALUES("Camera");

INSERT INTO Included(include)
VALUES("defect");

INSERT INTO Included(include)
VALUES("Defect");

INSERT INTO Included(include)
VALUES("speaker");

INSERT INTO Included(include)
VALUES("Speaker");

INSERT INTO Included(include)
VALUES("home");

INSERT INTO Included(include)
VALUES("Home");

INSERT INTO Included(include)
VALUES("button");

INSERT INTO Included(include)
VALUES("Button");


INSERT INTO Excluded(exclude)
VALUES("Gezocht");

INSERT INTO Excluded(exclude)
VALUES("gezocht");

INSERT INTO Excluded(exclude)
VALUES("NU");

INSERT INTO Excluded(exclude)
VALUES("ACTIE!!");

INSERT INTO Excluded(exclude)
VALUES("ruilen");

INSERT INTO Excluded(exclude)
VALUES("Afgeprijsd!");

INSERT INTO Excluded(exclude)
VALUES("Aktie!");

INSERT INTO Excluded(exclude)
VALUES("Refurbished");

INSERT INTO Excluded(exclude)
VALUES("gegarandeerd");

INSERT INTO Excluded(exclude)
VALUES("trixon.nl");

INSERT INTO Excluded(exclude)
VALUES("KPN");

INSERT INTO Excluded(exclude)
VALUES("GARANTIE!");

INSERT INTO Excluded(exclude)
VALUES("Phonestuff");

INSERT INTO Excluded(exclude)
VALUES("inruil");

INSERT INTO Excluded(exclude)
VALUES("garantie");

INSERT INTO Excluded(exclude)
VALUES("Garantie");

INSERT INTO Excluded(exclude)
VALUES("Informatie");

INSERT INTO Excluded(exclude)
VALUES("moederbord");

INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,1);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,2);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,3);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,4);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,5);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,6);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,7);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,8);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,9);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,10);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,11);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,12);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,13);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,14);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,15);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (1,16);


INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,1);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,2);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,3);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,4);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,5);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,6);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,7);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,8);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,9);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,10);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,11);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,12);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,13);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,14);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,15);
INSERT INTO SearchIncluded(searchID, includedID)
VALUES (2,16);


INSERT INTO SearchExcluded(searchID, excludedID)
VALUES(1,1);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,2);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,3);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,4);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,5);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,6);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,7);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,8);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,9);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,10);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,11);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,12);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,13);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,14);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,15);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,16);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,17);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (1,18);

INSERT INTO SearchExcluded(searchID, excludedID)
VALUES(2,1);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,2);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,3);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,4);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,5);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,6);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,7);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,8);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,9);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,10);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,11);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,12);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,13);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,14);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,15);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,16);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,17);
INSERT INTO SearchExcluded(searchID, excludedID)
VALUES (2,18);

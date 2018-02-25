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
  `city` VARCHAR(150),
  `link` VARCHAR(500) NOT NULL,
  PRIMARY KEY (`advertID`),
  FOREIGN KEY (searchID) REFERENCES Search(searchID)
);


USE marktplaats;
INSERT INTO Search (query, maxPrice, minPrice, maxBidPrice, distance, zipCode, link)
VALUES ("iphone 7", 300, 200, 300, 15000, "3445TA","https://www.marktplaats.nl/z/telecommunicatie/mobiele-telefoons-apple-iphone/iphone-7.html?query=iphone%207&categoryId=1953&distance=15000"), ("iphone 6", 100, 50, 100 ,15000, "3445TA","https://www.marktplaats.nl/z/telecommunicatie/mobiele-telefoons-apple-iphone/iphone-6.html?query=iphone%206&categoryId=1953&distance=15000");

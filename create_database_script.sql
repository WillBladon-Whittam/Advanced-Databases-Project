PRAGMA foreign_keys = ON;

-- Drop tables if they exists --
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Billing;
DROP TABLE IF EXISTS Shipping;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Basket_Contents;
DROP TABLE IF EXISTS Customer_Basket;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Suppliers;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Customers;


-- Create tables --
CREATE TABLE Customers
(Customer_ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
Customer_Firstname TEXT NOT NULL,
Customer_Surname TEXT NOT NULL,
Customer_Gender TEXT NOT NULL,
Customer_Email TEXT NOT NULL,
Customer_Username TEXT UNIQUE NOT NULL,
Customer_Password BLOB NOT NULL,
CONSTRAINT Customer_Gender CHECK (Customer_Gender IN ('Male', 'Female'))
);

CREATE TABLE Category
(Category_ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
Category_Name TEXT NOT NULL
);

CREATE TABLE Suppliers
(Supplier_ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
Supplier_Name TEXT NOT NULL,
Supplier_Email TEXT NOT NULL,
Supplier_Phone TEXT NOT NULL,
Supplier_HQ_Street_Number INTEGER NOT NULL,
Supplier_HQ_Street TEXT NOT NULL,
Supplier_HQ_Postcode TEXT NOT NULL
);

CREATE TABLE Products
(Product_ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
Product_Name TEXT NOT NULL,
Category_ID INTEGER NOT NULL,
Price INTEGER NOT NULL,
Stock_Level INTEGER NOT NULL,
Supplier_ID INTEGER NOT NULL,
Product_Image BLOB,
CONSTRAINT Category_ID_fk FOREIGN KEY (Category_ID)
REFERENCES Category(Category_ID)
CONSTRAINT Supplier_ID_fk FOREIGN KEY (Supplier_ID)
REFERENCES Suppliers(Supplier_ID)
);

CREATE TABLE Billing
(Billing_ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
Customer_ID INTEGER NOT NULL,
Billing_Address_Street_Number INTEGER NOT NULL,
Billing_Address_Street TEXT NOT NULL,
Billing_Address_Postcode TEXT NOT NULL,
Card_Number TEXT NOT NULL,
Card_Expiry TEXT NOT NULL,
Name_on_Card TEXT NOT NULL,
CVC TEXT NOT NULL,
CONSTRAINT Customer_ID_fk FOREIGN KEY (Customer_ID)
REFERENCES Customers(Customer_ID)
);

CREATE TABLE Shipping
(Shipping_ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
Customer_ID INTEGER NOT NULL,
Shipping_Address_Street_Number INTEGER NOT NULL,
Shipping_Address_Street TEXT NOT NULL,
Shipping_Address_Postcode TEXT NOT NULL,
Delivery_Date TEXT,
CONSTRAINT Customer_ID_fk FOREIGN KEY (Customer_ID)
REFERENCES Customers(Customer_ID)
);

CREATE TABLE Orders
(Order_ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
Order_Date TEXT NOT NULL,
Customer_ID INTEGER NOT NULL,
Product_ID INTEGER NOT NULL,
Shipping_ID INTEGER NOT NULL,
Billing_ID INTEGER NOT NULL,
Order_Quantity INTEGER NOT NULL,
Order_Status TEXT NOT NULL,
CONSTRAINT Customer_ID_fk FOREIGN KEY (Customer_ID)
REFERENCES Customers(Customer_ID)
CONSTRAINT Product_ID_fk FOREIGN KEY (Product_ID)
REFERENCES Products(Product_ID)
CONSTRAINT Shipping_ID_fk FOREIGN KEY (Shipping_ID)
REFERENCES Shipping(Shipping_ID)
CONSTRAINT Billing_ID_fk FOREIGN KEY (Billing_ID)
REFERENCES Billing(Billing_ID)
);

CREATE TABLE Customer_Basket
(Basket_ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
Customer_ID INTEGER NOT NULL,
Basket_Created_Date INTEGER NOT NULL,
CONSTRAINT Customer_ID_fk FOREIGN KEY (Customer_ID)
REFERENCES Customers(Customer_ID)
);

CREATE TABLE Basket_Contents
(Basket_ID INTEGER NOT NULL,
Product_ID INTEGER NOT NULL,
Quantity INTEGER NOT NULL,
PRIMARY KEY (Basket_ID, Product_ID)
CONSTRAINT Basket_ID_fk FOREIGN KEY (Basket_ID)
REFERENCES Customer_Basket(Basket_ID)
CONSTRAINT Product_ID_fk FOREIGN KEY (Product_ID)
REFERENCES Products(Product_ID)
);

CREATE TABLE Reviews
(Review_ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
Customer_ID INTEGER NOT NULL,
Product_ID INTEGER NOT NULL,
Review_Stars INTEGER NOT NULL,
Review_Comment TEXT,
Review_Date TEXT NOT NULL,
CONSTRAINT Customer_ID_fk FOREIGN KEY (Customer_ID)
REFERENCES Customers(Customer_ID)
CONSTRAINT Product_ID_fk FOREIGN KEY (Product_ID)
REFERENCES Products(Product_ID)
);

-- Insert Data --
INSERT INTO Customers (Customer_Firstname, Customer_Surname, Customer_Gender, Customer_Email, Customer_Username, Customer_Password) VALUES
('John', 'Doe', 'Male', 'john.doe@gmail.com', 'johndoe123', X'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'),
('Jane', 'Smith', 'Female', 'jane.smith@yahoo.com', 'janesmith456', X'415858d6b1a389558e5fd3b0b661c223bcee5825b6e75e13e2e9de4e5611d0c2'),
('Tom', 'Lee', 'Male', 'tom.lee@hotmail.com', 'tomlee789', X'e507bfe86e34891933615adb4bc9410b3fe248d8ab3afe5e2139b067e9472152'),
('Sara', 'White', 'Female', 'sara.white@icloud.com', 'sarawhite001', X'4e5fc404f1160bffb766a81a5e99535a388f625d73d02cd8dd3eda10357a4c68'),
('Emily', 'Brown', 'Female', 'emily.brown@outlook.com', 'emilybrown234', X'81ba08b0f0b41718c2aa1754201ae7a8dd2c4b977a5e1d57937386b767ed6586'),
('Michael', 'Green', 'Male', 'michael.green@gmail.com', 'mikegreen321', X'a0819e036a25f7606ca46cb898c72f6dc9510a2e1b37122b6ca4e86f9a0fdd7a'),
('Linda', 'Black', 'Female', 'linda.black@yahoo.com', 'lindablack789', X'369d18dbc516f16bf850735f146e5ad81fb71c99c4f0d6592b763ccfbe7b7bdf'),
('Chris', 'Blue', 'Male', 'chris.blue@hotmail.com', 'chrisblue001', X'4cce974ef92ba61455ed43a82342970066782ab88ab55433f889c97ce067c10f'),
('Robert', 'Grey', 'Male', 'robert.grey@icloud.com', 'robertgrey456', X'110c92056a8063f96fed7d3a43fc80dda08edcf7c4f8aaa57cdcec68452c118c'),
('Alice', 'Silver', 'Female', 'alice.silver@outlook.com', 'alicesilver789', X'94ba66de49d23c80e0ccfd952f1b283c5dda5324a54429b97c7fb6c4b3d0501a'),
('Harry', 'King', 'Male', 'harry.king@gmail.com', 'harryking123', X'f3f05636b35c80735c1fac5b5b79eca737035200322af82ac541f349811fbe92'),
('Paula', 'Pink', 'Female', 'paula.pink@icloud.com', 'paulapink456', X'de94bae412fa577ed2e13a1b7cf51de6d26951b16d9c08cb963f871929a46619'),
('George', 'Brown', 'Male', 'george.brown@gmail.com', 'georgebrown789', X'c4e15e47cf0964209a0af9591cd8f78413411621d9e2c869d5a4265c71fb65dc'),
('James', 'White', 'Male', 'james.white@outlook.com', 'jameswhite123', X'00878b2e6228332481ed9f8e4de7ba04c01925e9f48d46ac98209f0d2704c083'),
('Laura', 'Grey', 'Female', 'laura.grey@gmail.com', 'lauragrey789', X'e6f98324abc73148038a0b7ec077c1f203c5e8e32e13979cf6b42b78c53807b2'),
('Peter', 'Silver', 'Male', 'peter.silver@gmail.com', 'petersilver456', X'999edc7b7420fe149da92864847e59aba9585eacc5a7aafc137cc781f7406474'),
('Bella', 'Gold', 'Female', 'bella.gold@gmail.com', 'bellagold123', X'807aaa394bcc5a7feaf3f956b275e6e510b6dd06ed67e3370ca0f7b9694c5e30');

INSERT INTO Category (Category_Name) VALUES
('Laptops'),
('Desktops'),
('Keyboards'),
('Mice'),
('Components'),
('Monitors'),
('Storage'),
('Cooling'),
('Components'),
('Processors'),
('Laptops'),
('Audio'),
('Accessories'),
('Printers'),
('Cameras'),
('Storage'),
('Furniture');

INSERT INTO Suppliers (Supplier_Name, Supplier_Email, Supplier_Phone, Supplier_HQ_Street_Number, Supplier_HQ_Street, Supplier_HQ_Postcode)
VALUES
('TechSupplies Ltd.', 'supplier@techsupplies.co.uk', '+44 20 7946 0958', 12, 'Silicon Ave', 'WC2N 5DU'),
('CompHardware Ltd.', 'supplier@comphardware.co.uk', '+44 20 7946 0959', 45, 'Hardware St', 'M1 4FN'),
('KeyTech Ltd.', 'supplier@keytech.co.uk', '+44 20 7946 0960', 23, 'Input Ln', 'LS1 2HT'),
('MouseMasters Ltd.', 'supplier@mousemasters.co.uk', '+44 20 7946 0961', 16, 'Click St', 'B2 4QA'),
('GraphicPlus Ltd.', 'supplier@graphicplus.co.uk', '+44 20 7946 0962', 99, 'Render Rd', 'S1 4GF'),
('MonitorWorld Ltd.', 'supplier@monitorworld.co.uk', '+44 20 7946 0963', 55, 'View St', 'G2 4NQ'),
('StorageXpert Ltd.', 'supplier@storagexpert.co.uk', '+44 20 7946 0964', 88, 'Flash Ln', 'L1 8JU'),
('CoolingPro Ltd.', 'supplier@coolingpro.co.uk', '+44 20 7946 0965', 77, 'Chill St', 'BS1 5DJ'),
('MotherTech Ltd.', 'supplier@mothertech.co.uk', '+44 20 7946 0966', 66, 'Mainboard St', 'CF1 6LJ'),
('ChipMakers Ltd.', 'supplier@chipmakers.co.uk', '+44 20 7946 0967', 11, 'Silicon St', 'EH1 2NG'),
('TechSupplies Ltd.', 'supplier@techsupplies.co.uk', '+44 20 7946 0958', 12, 'Silicon Ave', 'WC2N 5DU'),
('SoundTech Ltd.', 'supplier@soundtech.co.uk', '+44 20 7946 0968', 33, 'Sound Ln', 'NE1 4GN'),
('HubMasters Ltd.', 'supplier@hubmasters.co.uk', '+44 20 7946 0969', 44, 'USB Ln', 'OX1 2DJ'),
('PrintWorld Ltd.', 'supplier@printworld.co.uk', '+44 20 7946 0970', 55, 'Print Ln', 'CB2 1PX'),
('CameraPlus Ltd.', 'supplier@cameraplus.co.uk', '+44 20 7946 0971', 66, 'Lens St', 'BA1 5DF'),
('StorageMasters Ltd.', 'supplier@storagemasters.co.uk', '+44 20 7946 0972', 77, 'Disk St', 'CH1 3DN'),
('ChairMasters Ltd.', 'supplier@chairmasters.co.uk', '+44 20 7946 0973', 99, 'Sit Ln', 'NG1 6DF');

INSERT INTO Products (Product_Name, Category_ID, Price, Stock_Level, Supplier_ID, Product_Image) VALUES
('Gaming Laptop', 1, 1500, 50, 1, NULL),
('Desktop Computer', 2, 1200, 30, 2, NULL),
('Mechanical Keyboard', 3, 100, 100, 3, NULL),
('Wireless Mouse', 4, 50, 150, 4, NULL),
('Graphics Card', 5, 400, 80, 5, NULL),
('Gaming Monitor', 6, 300, 40, 6, NULL),
('External SSD', 7, 150, 60, 7, NULL),
('Cooling Fan', 8, 30, 200, 8, NULL),
('Motherboard', 9, 250, 70, 9, NULL),
('Processor', 10, 500, 40, 10, NULL),
('Headset', 12, 100, 120, 12, NULL),
('USB Hub', 13, 20, 500, 13, NULL),
('Printer', 14, 200, 60, 14, NULL),
('Web Camera', 15, 80, 150, 15, NULL),
('External Hard Drive', 16, 100, 75, 16, NULL),
('Gaming Chair', 17, 150, 100, 17, NULL);

INSERT INTO Shipping (Customer_ID, Shipping_Address_Street_Number, Shipping_Address_Street, Shipping_Address_Postcode, Delivery_Date)
VALUES
(1, 123, 'Main St', 'SW1A 1AA', '2024-01-13'),
(2, 456, 'Elm St', 'M1 4FL', '2024-02-17'),
(3, 789, 'Oak St', 'LS1 2HU', NULL),
(4, 321, 'Maple St', 'B2 4QA', '2024-02-17'),
(5, 654, 'Pine St', 'S1 4GE', '2024-05-08'),
(6, 987, 'Cedar St', 'G2 4NU', NULL),
(7, 743, 'Oak St', 'H1 8JX', '2024-07-20'),
(8, 876, 'Walnut St', 'BS1 5DX', NULL),
(9, 543, 'Ash St', 'CF1 6LM', '2024-09-20'),
(10, 210, 'Spruce St', 'EH1 2NH', '2024-10-05'),
(11, 321, 'Cedar St', 'SW1A 2AB', '2024-01-18'),
(12, 987, 'Elm St', 'NE1 4GP', '2024-02-20'),
(13, 654, 'Pine St', 'OX1 2DF', NULL),
(14, 210, 'Ash St', 'CB2 1PY', '2024-04-18'),
(15, 876, 'Oak St', 'BA1 5DG', NULL),
(16, 432, 'Maple St', 'CH1 3DP', '2024-06-10'),
(17, 210, 'Elm St', 'NG1 6DG', NULL);

INSERT INTO Billing (Customer_ID, Billing_Address_Street_Number, Billing_Address_Street, Billing_Address_Postcode, Card_Number, Card_Expiry, Name_on_Card, CVC)
VALUES
(1, 123, 'Main St', 'SW1A 1AA', '1234 5678 9101 1123', 'Dec-25', 'MrJohn V Doe', 123),
(2, 456, 'Elm St', 'M1 4FL', '4321 5678 9101 1213', 'Nov-26', 'Mrs Jane G Smith', 456),
(3, 789, 'Oak St', 'LS1 2HU', '9876 1234 5678 4321', 'Oct-24', 'Mr Tom L Lee', 789),
(4, 321, 'Maple St', 'B2 4QA', '1111 2222 3333 4444', 'Sep-24', 'Ms Sara T White', 987),
(5, 654, 'Pine St', 'S1 4GE', '5555 6666 7777 8888', 'Aug-26', 'Dr Emily O Brown', 321),
(6, 987, 'Cedar St', 'G2 4NU', '6666 7777 8888 9999', 'May-27', 'Mr Chris P Green', 654),
(7, 743, 'Oak St', 'H1 8JX', '7777 8888 9999 0000', 'Apr-27', 'Lady Anne B Grey', 987),
(8, 876, 'Walnut St', 'BS1 5DX', '1111 2222 3333 4444', 'Mar-24', 'Mr Richard K Black', 432),
(9, 543, 'Ash St', 'CF1 6LM', '2222 3333 4444 5555', 'Feb-25', 'Mr George W White', 543),
(10, 210, 'Spruce St', 'EH1 2NH', '3333 4444 5555 6666', 'Jan-26', 'Ms Linda F Brown', 654),
(11, 321, 'Cedar St', 'SW1A 2AB', '4444 5555 6666 7777', 'Dec-25', 'Mr Kevin G Purple', 765),
(12, 987, 'Elm St', 'NE1 4GP', '5555 6666 7777 8888', 'Nov-26', 'Mrs Olivia Q Pink', 987),
(13, 654, 'Pine St', 'OX1 2DF', '6666 7777 8888 9999', 'Oct-24', 'Dr David P Yellow', 432),
(14, 210, 'Ash St', 'CB2 1PY', '7777 8888 9999 0000', 'Sep-25', 'Sir Robert L Blue', 765),
(15, 876, 'Oak St', 'BA1 5DG', '8888 9999 0000 1111', 'Aug-27', 'Lady Margaret J Cyan', 987),
(16, 432, 'Maple St', 'CH1 3DP', '9999 0000 1111 2222', 'Jul-26', 'Ms Patricia R Indigo', 543),
(17, 210, 'Elm St', 'NG1 6DG', '0000 1111 2222 3333', 'Jun-25', 'Mr Paul M Violet', 876);

INSERT INTO Orders (Order_Date, Customer_ID, Product_ID, Shipping_ID, Billing_ID, Order_Quantity, Order_Status)
VALUES
('2024-01-13', 1, 1, 1, 1, 1, 'Delivered'),
('2024-02-15', 2, 2, 2, 2, 2, 'Delivered'),
('2024-03-19', 3, 3, 1, 3, 3, 'Dispatched'),
('2024-04-25', 4, 4, 1, 4, 4, 'Delivered'),
('2024-05-03', 5, 5, 2, 5, 5, 'Delivered'),
('2024-06-13', 6, 6, 4, 6, 6, 'Out for delivery'),
('2024-07-15', 7, 7, 1, 7, 7, 'Delivered'),
('2024-08-21', 8, 8, 1, 8, 8, 'Dispatched'),
('2024-09-17', 9, 9, 2, 9, 9, 'Delivered'),
('2024-10-02', 10, 10, 3, 10, 10, 'Delivered'),
('2024-01-14', 11, 1, 1, 11, 11, 'Delivered'),
('2024-02-14', 12, 11, 2, 12, 12, 'Delivered'),
('2024-03-19', 13, 12, 1, 13, 13, 'Dispatched'),
('2024-04-13', 14, 13, 4, 14, 14, 'Delivered'),
('2024-05-22', 15, 14, 3, 15, 15, 'Out for delivery'),
('2024-06-05', 16, 15, 1, 16, 16, 'Delivered'),
('2024-07-27', 17, 16, 1, 17, 17, 'Out for delivery');

INSERT INTO Reviews (Customer_ID, Product_ID, Review_Stars, Review_Comment, Review_Date)
VALUES
(1, 1, 5, 'Excellent product!', '14/01/2024'),
(2, 2, 4, 'Works well, fast delivery.', '18/02/2024'),
(5, 5, 5, 'Amazing graphics, love it!', '09/05/2024'),
(7, 7, 5, 'SSD is very fast, highly recommend.', '21/07/2024'),
(9, 9, 4, 'Motherboard worked as expected.', '22/09/2024'),
(10, 10, 5, 'Fast processor, no issues so far.', '06/10/2024'),
(11, 1, 4, 'Excellent laptop, a bit pricey.', '19/01/2024'),
(12, 12, 5, 'Great sound quality, comfortable.', '21/02/2024'),
(14, 14, 5, 'Printer works perfectly, no issues.', '19/04/2024'),
(16, 16, 5, 'Fast hard drive, highly recommend.', '11/06/2024');

-- Create triggers --
DROP TRIGGER IF EXISTS Trigger1;
DROP TRIGGER IF EXISTS Trigger2;
DROP TRIGGER IF EXISTS Trigger3;

-- Check when adding an item to the basket that there is enough stock --
CREATE TRIGGER Trigger1
BEFORE INSERT ON Basket_Contents
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT Stock_Level
              FROM Products
              WHERE Product_ID = NEW.Product_ID) <
             (NEW.Quantity +
              IFNULL((SELECT SUM(Quantity)
                      FROM Basket_Contents
                      WHERE Basket_ID = NEW.Basket_ID AND Product_ID = NEW.Product_ID), 0))
        THEN RAISE(ABORT, 'Not enough stock available to add this quantity to the basket.')
    END;
END;

-- Check when adding an item to the basket that there is enough stock --
CREATE TRIGGER Trigger2
BEFORE UPDATE ON Basket_Contents
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT Stock_Level
              FROM Products
              WHERE Product_ID = NEW.Product_ID) <
             (NEW.Quantity +
              IFNULL((SELECT SUM(Quantity)
                      FROM Basket_Contents
                      WHERE Basket_ID = NEW.Basket_ID AND Product_ID = NEW.Product_ID), 0) - OLD.Quantity)
        THEN RAISE(ABORT, 'Not enough stock available to add this quantity to the basket.')
    END;
END;

-- Update the stock when an order is placed --
CREATE TRIGGER Trigger3
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
    UPDATE Products
    SET Stock_Level = Stock_Level - NEW.Order_Quantity
    WHERE Product_ID = NEW.Product_ID;
END;

-- Create Views --
DROP View IF EXISTS BestSellingProducts;
DROP View IF EXISTS CustomerBasketValue;

CREATE VIEW BestSellingProducts AS
SELECT 
    p.Product_ID AS Product_ID,
    p.Product_Name AS Product_Name,
    p.Category_ID AS Category_ID,
    p.Price AS Price,
    p.Stock_Level AS Stock_Level,
    p.Supplier_ID AS Supplier_ID,
    p.Product_Image AS Product_Image,
SUM(o.Order_Quantity) AS Total_Ordered
FROM Orders AS o
INNER JOIN Products AS p ON o.Product_ID = p.Product_ID
GROUP BY p.Product_ID
HAVING  Total_Ordered > 0
ORDER BY Total_Ordered DESC
LIMIT 6;
    
CREATE VIEW CustomerBasketValue AS
SELECT 
    cb.Basket_ID AS Basket_ID,
    c.Customer_ID AS Customer_ID,
    SUM(p.Price * bc.Quantity) AS Total_Basket_Value
FROM Customer_Basket AS cb
INNER JOIN Customers AS c ON cb.Customer_ID = c.Customer_ID
INNER JOIN Basket_Contents AS bc ON cb.Basket_ID = bc.Basket_ID
INNER JOIN Products AS p ON bc.Product_ID = p.Product_ID
GROUP BY cb.Basket_ID;

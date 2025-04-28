
Create Table Manager(
    ssn Int, 
    name text,
    email text,
    Primary Key (ssn)
);

Create Table Car(
    carId Int,
    Brand text,
    Primary Key (carId)
);

Create Table Client(
    name text,
    email text,
    Primary Key (email)
);

Create Table Address(
    roadName text,
    addressNumber Int,
    city text,
    Primary Key (roadName, addressNumber, city)
);

Create Table Model(
    color text,
    constructionYear Int, 
    transmission text, 
    modelId Int,
    carId Int,
    Primary Key (modelId, carId),
    Foreign Key (carID) References Car
);

Create Table Driver( 
    name text,
    Primary Key (name),
    addressNumber Int Not Null,
    roadName text Not Null, 
    city text Not Null,
    Foreign Key (roadName, addressNumber, city) References Address
);

Create Table Rent( 
    rentId Int,
    date date,
    Primary Key (rentId),
    modelId Int Not NUll, 
	carId Int Not NUll,
    Foreign Key (modelId, carId) References Model,
    name text Not NULL, 
    Foreign Key (name) References Driver,
    email text Not NULL,
    Foreign Key (email) References Client
);

Create Table CreditCard( 
    creditCardNumber int,
    Primary Key (creditCardNumber),
    email text Not NULL,
    Foreign Key (email) References Client,
    addressNumber Int Not Null,
    roadName text Not Null, 
    city text Not Null,
    Foreign Key (roadName, addressNumber, city) References Address
);


Create Table Review(
    reviewId Int, 
    name text,
    rating Int, 
    message text,
    Primary Key (reviewId, name),
    Foreign Key (name) References Driver,
    email text Not NULL,
    Foreign Key (email) References Client
);

Create Table drives(
    name text,
    modelId Int,
    carId Int,
    Primary Key (name, modelId, carId),
    Foreign Key (modelId, carId) References Model,
    Foreign Key (name) References Driver
);

Create Table staysAt(
    roadName text, 
    addressNumber Int,
    city text,
    email text,
    Primary Key (roadName, addressNumber, city, email),
    Foreign Key (roadName, addressNumber, city) References Address,
    Foreign Key (email) References Client
);

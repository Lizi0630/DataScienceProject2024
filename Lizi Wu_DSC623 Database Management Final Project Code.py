import sqlite3

# Connect to the SQLite database
db_connect = sqlite3.connect('pawsome_pets_final.db')
cursor = db_connect.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clinic (
        clinicNo INTEGER PRIMARY KEY,
        cName TEXT NOT NULL CHECK (length(cName) <= 100),
        cAddress TEXT NOT NULL CHECK (length(cAddress) <= 200),
        cPhone TEXT NOT NULL CHECK (length(cPhone) = 10 AND cPhone GLOB '[0-9]*'),
        staffNo INTEGER UNIQUE,
        FOREIGN KEY (staffNo) REFERENCES Staff(staffNo)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Staff (
        staffNo INTEGER PRIMARY KEY,
        sName TEXT NOT NULL CHECK (length(sName) <= 100),
        sAddress TEXT NOT NULL CHECK (length(sAddress) <= 200),
        sPhone TEXT NOT NULL CHECK (length(sPhone) = 10 AND sPhone GLOB '[0-9]*'),
        sDOB DATE NOT NULL,
        position TEXT NOT NULL CHECK (length(position) <= 50),
        salary REAL NOT NULL CHECK (salary > 0),
        clinicNo INTEGER NOT NULL,
        FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Owner (
        ownerNo INTEGER PRIMARY KEY,
        oName TEXT NOT NULL CHECK (length(oName) <= 100),
        oAddress TEXT NOT NULL CHECK (length(oAddress) <= 200),
        oPhone TEXT NOT NULL CHECK (length(oPhone) = 10 AND oPhone GLOB '[0-9]*')
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pet (
        petNo INTEGER PRIMARY KEY,
        pName TEXT NOT NULL CHECK (length(pName) <= 100),
        pDOB DATE NOT NULL,
        species TEXT NOT NULL CHECK (length(species) <= 50),
        breed TEXT NOT NULL CHECK (length(breed) <= 50),
        color TEXT NOT NULL CHECK (length(color) <= 50),
        ownerNo INTEGER NOT NULL,
        clinicNo INTEGER NOT NULL,
        FOREIGN KEY (ownerNo) REFERENCES Owner(ownerNo),
        FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Examination (
        examNo INTEGER PRIMARY KEY,
        complaint TEXT NOT NULL CHECK (length(complaint) <= 500),
        description TEXT NOT NULL CHECK (length(description) <= 1000),
        date DATE NOT NULL,
        action TEXT NOT NULL CHECK (length(action) <= 500),
        petNo INTEGER NOT NULL,
        staffNo INTEGER NOT NULL,
        FOREIGN KEY (petNo) REFERENCES Pet(petNo),
        FOREIGN KEY (staffNo) REFERENCES Staff(staffNo)
    );
''')

print("Tables created successfully.")

# Insert sample data
cursor.execute('''
    INSERT OR IGNORE INTO Clinic (clinicNo, cName, cAddress, cPhone) VALUES
    (6, 'Paws Miami', '101 Ocean Dr, Miami, FL', '3051234567'),
    (7, 'Pet Paradise', '202 Beach Ave, Miami, FL', '3052345678'),
    (8, 'Miami Paw Care', '303 Biscayne Blvd, Miami, FL', '3053456789'),
    (9, 'Happy Pets Miami', '404 Sunset Rd, Miami, FL', '3054567890'),
    (10, 'VetCare Miami', '505 Brickell Ave, Miami, FL', '3055678901');
''')

cursor.execute('''
    INSERT OR IGNORE INTO Staff (staffNo, sName, sAddress, sPhone, sDOB, position, salary, clinicNo) VALUES
    (6, 'Carlos Mendez', '123 Ocean Dr, Miami, FL', '3051234567', '1980-11-10', 'Veterinarian', 85000, 6),
    (7, 'Sofia Martinez', '234 Beach Ave, Miami, FL', '3052345678', '1992-06-15', 'Receptionist', 40000, 7),
    (8, 'Daniela Garcia', '345 Biscayne Blvd, Miami, FL', '3053456789', '1995-03-05', 'Technician', 50000, 8),
    (9, 'Ricardo Lopez', '456 Sunset Rd, Miami, FL', '3054567890', '1987-09-25', 'Veterinarian', 80000, 9),
    (10, 'Maria Perez', '567 Brickell Ave, Miami, FL', '3055678901', '1990-01-18', 'Technician', 55000, 10);
''')

cursor.execute('''
    INSERT OR IGNORE INTO Owner (ownerNo, oName, oAddress, oPhone) VALUES
    (6, 'Ana Rodriguez', '789 Bay Rd, Miami, FL', '7861234567'),
    (7, 'Juan Torres', '890 Coral Way, Miami, FL', '7862345678'),
    (8, 'Luis Alvarez', '567 Flagler St, Miami, FL', '7863456789'),
    (9, 'Elena Sanchez', '345 Little Havana, Miami, FL', '7864567890'),
    (10, 'Miguel Diaz', '123 Coconut Grove, Miami, FL', '7865678901');
''')

cursor.execute('''
    INSERT OR IGNORE INTO Pet (petNo, pName, pDOB, species, breed, color, ownerNo, clinicNo) VALUES
    (6, 'Rocky', '2018-12-10', 'Dog', 'Bulldog', 'Brown', 6, 6),
    (7, 'Luna', '2019-04-22', 'Cat', 'Sphynx', 'Beige', 7, 7),
    (8, 'Max', '2021-08-05', 'Dog', 'Beagle', 'Tri-color', 8, 8),
    (9, 'Milo', '2020-01-15', 'Rabbit', 'Holland Lop', 'White', 9, 9),
    (10, 'Chloe', '2022-02-28', 'Bird', 'Parrot', 'Green', 10, 10);
''')

cursor.execute('''
    INSERT OR IGNORE INTO Examination (examNo, complaint, description, date, action, petNo, staffNo) VALUES
    (6, 'Limping', 'Checked leg; no fracture found', '2023-01-15', 'Prescribed rest and pain relief', 6, 6),
    (7, 'Hair Loss', 'Examined skin and conducted allergy test', '2023-02-10', 'Prescribed special shampoo', 7, 7),
    (8, 'Coughing', 'Checked throat and chest X-ray', '2023-03-20', 'Prescribed antibiotics', 8, 8),
    (9, 'Weight Loss', 'Blood tests and physical examination', '2023-04-25', 'Prescribed vitamins and diet plan', 9, 9),
    (10, 'Broken Wing', 'X-ray and bandage applied', '2023-05-15', 'Scheduled follow-up', 10, 10);
''')

# Create triggers for date validation
cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_check_sDOB
    BEFORE INSERT ON Staff
    FOR EACH ROW
    BEGIN
        SELECT CASE
            WHEN NEW.sDOB >= DATE('now') THEN
                RAISE(ABORT, 'sDOB must be a valid date in the past.')
        END;
    END;
''')

cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_check_pDOB
    BEFORE INSERT ON Pet
    FOR EACH ROW
    BEGIN
        SELECT CASE
            WHEN NEW.pDOB >= DATE('now') THEN
                RAISE(ABORT, 'pDOB must be a valid date in the past.')
        END;
    END;
''')

cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_check_exam_date
    BEFORE INSERT ON Examination
    FOR EACH ROW
    BEGIN
        SELECT CASE
            WHEN NEW.date > DATE('now') THEN
                RAISE(ABORT, 'Examination date must be in the past or current date.')
        END;
    END;
''')

print("Triggers created successfully.")


db_connect.commit()
print("Sample data inserted successfully.")

# Display all data
table_names = ["Clinic", "Staff", "Owner", "Pet", "Examination"]
for table_name in table_names:
    print(f"\nData from {table_name}:")
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Close database connection
db_connect.close()

import sqlite3

# Connect to the SQLite database
db_connect = sqlite3.connect('pawsome_pets_final.db')
cursor = db_connect.cursor()

# Transaction 1: Add a New Pet
cursor.execute('''
    INSERT INTO Pet (petNo, pName, pDOB, species, breed, color, ownerNo, clinicNo)
    VALUES (11, 'Simba', '2021-06-10', 'Dog', 'Shih Tzu', 'Brown', 6, 6);
''')
print("New pet added successfully.")

# Transaction 2: Record an Examination
cursor.execute('''
    INSERT INTO Examination (examNo, complaint, description, date, action, petNo, staffNo)
    VALUES (11, 'Skin Rash', 'Applied ointment and prescribed medication', '2023-11-28', 'Follow-up in 2 weeks', 6, 6);
''')
print("New examination recorded successfully.")

# Transaction 3: Assign a Staff Member to a Clinic
cursor.execute('''
    INSERT INTO Staff (staffNo, sName, sAddress, sPhone, sDOB, position, salary, clinicNo)
    VALUES (11, 'Gabriela Flores', '890 Brickell Ave, Miami, FL', '3056789012', '1993-12-15', 'Technician', 45000, 10);
''')
print("New staff member assigned to a clinic successfully.")

# Transaction 4: Change Clinic Staff
cursor.execute('''
    UPDATE Clinic
    SET staffNo = 7
    WHERE clinicNo = 7;
''')
print("Clinic staff changed successfully.")

# Transaction 5: Retrieve a Pet’s Examination History
cursor.execute('''
    SELECT Examination.examNo, Examination.complaint, Examination.description, Examination.date, Examination.action
    FROM Examination
    INNER JOIN Pet ON Examination.petNo = Pet.petNo
    WHERE Pet.petNo = 6;
''')
rows = cursor.fetchall()
print("\nExamination history for Pet 6:")
for row in rows:
    print(row)

# Commit changes and close the connection
db_connect.commit()
db_connect.close()
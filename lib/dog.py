import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    all = []
    def __init__(self, name,  breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
              CREATE TABLE IF NOT EXISTS dogs
                (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
                )
           
              """
        CURSOR.execute(sql)
        CONN.commit()    

    @classmethod
    def drop_table(cls):
        query = """DROP TABLE IF EXISTS dogs"""
        CURSOR.execute(query)        
        CONN.commit()
       

    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
      
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]  
        return dog

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """

        all = CURSOR.execute(sql).fetchall()

        cls.all = [cls.new_from_db(row) for row in all] 
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        dog = CURSOR.execute(sql, (name,)).fetchone()

        if(dog):
            return cls.new_from_db(dog)
        else:
            return None

        # return cls.new_from_db(dog)
     
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        dog = CURSOR.execute(sql, (id,)).fetchone()

        return cls.new_from_db(dog) 
    
    @classmethod
  
    def find_or_create_by(cls, name, breed):
        query = """SELECT id FROM dogs WHERE name = ? AND breed = ?"""
        CURSOR.execute(query, (name, breed))
        existing_row = CURSOR.fetchone()

        if existing_row:
            dog_id = existing_row[0]
            return f"Dog with name '{name}' and breed '{breed}' already exists with ID {dog_id}"
            
        else:
            dog = Dog(name, breed)
            dog.save()
            return dog
        
    def update(self):
        sql = """UPDATE dogs SET name = ?, breed = ? WHERE id = ?"""
        val = (self.name, self.breed, self.id)
        
        CURSOR.execute(sql, val)
        CONN.commit()



# dog = Dog.create_table()
# dog = Dog.create("Test2", "200")
# dog.save()
# dog.name = 'Test3'
# dog.update()
# dog = Dog("GT", "26")
# dog = dog.find_or_create_by("GT", "27")
# dog = Dog.find_by_id("1")
dog = Dog.find_by_name("joseph")
if dog:
    dog.name = "john"
    dog.update()
    print("Dog updated successfully.")
else:
    print("Dog not found.")



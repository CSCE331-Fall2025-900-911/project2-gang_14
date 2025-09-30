import psycopg2
from schema import create_schema, drop_schema
from seed import seed_data

def main():
    conn = psycopg2.connect(
        host="csce-315-db.engr.tamu.edu",
        database="gang_14_db",
        user="gang_14",
        password="gang_14"
    )
    cursor = conn.cursor()

    # Drop and recreate tables
    drop_schema(cursor)
    print("droped schema")
    create_schema(cursor)
    print("made schema")

    # Populate tables
    seed_data(cursor)
    print("populated database")

    conn.commit()
    cursor.close()
    conn.close()
    print("Database reset and seeded successfully!")

if __name__ == "__main__":
    main()

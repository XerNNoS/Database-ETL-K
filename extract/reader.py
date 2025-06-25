def read_table_in_batches(cursor, table_name, batch_size=1000, offset=0):
    while True:
        query = f"SELECT * FROM {table_name} LIMIT %s OFFSET %s"
        cursor.execute(query, (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

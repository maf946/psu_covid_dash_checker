import sqlite3

def create_connection():
    try:
        conn = sqlite3.connect('psu_covid_dash_checker.sqlite3')
        return conn
    except:
        print ("error connecting to db")


def update_database(dataDictionary):
    conn = create_connection()
    cur = conn.cursor()

    table='covid_data'
    columns_string= '('+','.join(dataDictionary.keys())+')'
    values_string = '('+','.join(map(str,dataDictionary.values()))+')'
    sql = """INSERT INTO %s %s VALUES %s"""%(table, columns_string,values_string)
    cur.execute(sql)
    conn.commit()
    cur.close()

def get_last_recorded_overall_total_positive():
    # create a database connection
    conn = create_connection()
    cur = conn.cursor()
    query_string = "select overall_total_positive from covid_data order by update_time desc limit 1"
    last_recorded_overall_total_positive = int(cur.execute(query_string).fetchone()[0])
    conn.commit()
    cur.close()
    return last_recorded_overall_total_positive

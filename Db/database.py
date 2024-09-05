import sqlite3

### CONFIGURATION
sqlite_db_file = "aid.db"
sqlite_table_name = "software"

def init_db():
    connection = sqlite3.connect(sqlite_db_file)
    cursor = connection.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS """ + sqlite_table_name + """(
	"app_name"	TEXT NOT NULL,
	"app_version"	TEXT NOT NULL,
	"app_platform"	TEXT NOT NULL,
	"url_bin"	TEXT NOT NULL,
	"url_sha256"	TEXT,
	"url_asc"	TEXT,
	"last_found"	TEXT NOT NULL,
	"last_download"	TEXT,
	PRIMARY KEY("app_name","app_version","app_platform")
);
                   """)
    connection.commit()

def append_software(list_software_dict):
    for software in list_software_dict:
        app_name = software['app_name']
        app_version = software['app_version']
        last_found = software['last_found']
        last_download = software['last_download']
        for download in software['downloads']:
            connection = sqlite3.connect(sqlite_db_file)
            cursor = connection.cursor()
            #print(app_name, app_version, download['app_platform'], download['url_bin'], download['url_sha256'], download['url_asc'], last_found, last_download )
            cursor.execute("SELECT app_version FROM " + sqlite_table_name + " WHERE app_name=? AND app_platform=?", (app_name,download['app_platform']))
            entry = cursor.fetchone()
            if entry:
                version = entry[0]
                if version == app_version:
                    print(f"App {app_name} in version {app_version} already exists.")
                    continue
            print(f"Inserting App {app_name} in version {app_version}.")
            cursor.execute("INSERT INTO " + sqlite_table_name + "(app_name, app_version, app_platform, url_bin, url_sha256, url_asc, last_found, last_download) VALUES (?,?,?,?,?,?,?,?)", (app_name, app_version, download['app_platform'], download['url_bin'], download['url_sha256'], download['url_asc'], last_found, last_download ))

            # SQLs = "INSERT INTO " + sqlite_table_name + " VALUES (" + app_name + "," + app_version + "," + download['platform']+ "," + download['url_bin'] + a")"
            # print(SQLs)
            # cursor.execute(SQLs)
            connection.commit()

def insert_dummy_data():
    connection = sqlite3.connect(sqlite_db_file)
    cursor = connection.cursor()
    SQLs = "INSERT INTO " + sqlite_table_name + " VALUES ('stunnel','5.4','linux','https://www.stunnel.org/download.html','','','','')"
    print(SQLs)
    cursor.execute(SQLs)
    connection.commit()

if __name__ == "__main__":
    sqlite_db_file = "../" + sqlite_db_file
    print(sqlite_db_file)
    init_db()
    #insert_dummy_data()
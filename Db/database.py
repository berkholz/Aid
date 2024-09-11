import os.path
import sqlite3
from platform import platform

### CONFIGURATION
cwd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(cwd_dir)
sqlite_db_file = os.path.join(cwd_dir, 'aid.db')
# print(sqlite_db_file)
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
	"hash_type"	TEXT,
	"hash_res"	TEXT,
	"sig_type"	TEXT,
	"sig_res"	TEXT,
	"url_pub_key"	TEXT,
	"last_found"	TEXT NOT NULL,
	"last_download"	TEXT,
	"verified_version"	TEXT,
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
            # print(app_name, app_version, download['app_platform'], download['url_bin'], download['url_sha256'], download['url_asc'], last_found, last_download )
            cursor.execute("SELECT app_version FROM " + sqlite_table_name + " WHERE app_name=? AND app_platform=?",
                           (app_name, download['app_platform']))
            entry = cursor.fetchall()

            if entry:
                version = entry[0][0]
                if version == app_version:
                    print(f"App {app_name} in version {app_version} already exists.")
                    continue
                else:
                    print(f"Updating App {app_name} to version {app_version}.")
                    cursor.execute(
                        f"UPDATE '{sqlite_table_name}' SET app_version='{app_version}', url_bin='{download['url_bin']}',"
                        f"hash_type = '{download['hash_type']}', hash_res = '{download['hash_res']}',"
                        f"sig_type = '{download['sig_type']}', sig_res = '{download['sig_res']}',"
                        f"url_pub_key = '{download['url_pub_key']}', last_found = '{last_found}' WHERE app_name='{app_name} and app_platform='{download['app_platform']}'",
                    )
            else:
                print(f"Inserting App {app_name} in version {app_version}.")
                cursor.execute(
                    "INSERT INTO " + sqlite_table_name + "(app_name, app_version, app_platform, url_bin, hash_type,"
                                                         " hash_res, sig_type, sig_res, url_pub_key, last_found,"
                                                         " last_download, verified_version) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (app_name, app_version, download['app_platform'], download['url_bin'],
                     download['hash_type'], download['hash_res'], download['sig_type'], download['sig_res'],
                     download['url_pub_key'], last_found, last_download, None))
            connection.commit()


def get_software_link(app_name, platform):
    connection = sqlite3.connect(sqlite_db_file)
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT url_bin , app_version FROM {sqlite_table_name} WHERE app_name=\"{app_name}\" AND app_platform=\"{platform}\"")
    entry = cursor.fetchone()

    return entry


def get_checksum_link(platform, app_name, version):
    connection = sqlite3.connect(sqlite_db_file)
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT url_bin, hash_type, hash_res, sig_type, sig_res, url_pub_key FROM {sqlite_table_name} WHERE app_platform=\"{platform}\" AND app_name=\"{app_name}\" AND app_version=\"{version}\""
    )
    entry = cursor.fetchone()
    print(entry)
    if entry:
        return entry
    else:
        return None


def get_sw_list_for_platform(platform):
    connection = sqlite3.connect(sqlite_db_file)
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT app_name FROM {sqlite_table_name} WHERE app_platform=\"{platform}\""
    )
    entries = cursor.fetchall()
    ret_sw = []
    for entry in entries:
        ret_sw.append(entry[0])
    return ret_sw


def set_verified_version(software, platform, version):
    connection = sqlite3.connect(sqlite_db_file)
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE " + sqlite_table_name + " SET verified_version=? WHERE app_name=? AND app_platform=?",
        (version, software, platform)
    )
    connection.commit()
    connection.close()

def get_verified_version(software, platform):
    connection = sqlite3.connect(sqlite_db_file)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT verified_version FROM " + sqlite_table_name + " WHERE app_name=? AND app_platform=?", (software, platform)
    )
    entry = cursor.fetchone()
    if entry:
        return entry[0]
    else:
        return None

def insert_dummy_data():
    connection = sqlite3.connect(sqlite_db_file)
    print(sqlite_db_file)
    cursor = connection.cursor()
    SQLs = "INSERT INTO " + sqlite_table_name + " VALUES ('stunnel','5.4','linux','https://www.stunnel.org/download.html','','','','','','','')"
    print(SQLs)
    cursor.execute(SQLs)
    connection.commit()


if __name__ == "__main__":
    sqlite_db_file = sqlite_db_file
    print(sqlite_db_file)
    init_db()
    # insert_dummy_data()

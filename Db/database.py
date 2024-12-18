# import errno
# from os import error
import os.path
import sqlite3
import logging # import lib for LOGGING
import settings # import global settings

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOGLEVEL)
# logging.basicConfig(level=logging.DEBUG)

cwd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGGER.debug(" current working dir: %s", cwd_dir)

sqlite_db_file = os.path.join(cwd_dir, 'aid.db')
sqlite_table_name = "software"
# product_table_name = "products"

################################### FUNCTIONS

def init_db():
    """
    Inititalize the database schema.
    """
    connection = sqlite3.connect(sqlite_db_file)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS """ + sqlite_table_name + """(
        "app_name"	TEXT NOT NULL,
        "app_version"	TEXT NOT NULL,
        "app_platform"	TEXT NOT NULL,
        "full_name"	TEXT NOT NULL,
        "download" INTEGER DEFAULT 0,
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
    connection.close()


def append_software(list_software_dict):
    """adds a software-versions to the database if it doesn't exist'"""
    global LOGGER
    connection = sqlite3.connect(sqlite_db_file)
    cursor = connection.cursor()

    for software in list_software_dict:
        app_name = software['app_name']
        app_version = software['app_version']
        full_name = software['full_name']
        last_found = software['last_found']
        last_download = software['last_download']
        LOGGER.debug("Actual software: %s %s %s %s %s", app_name, app_version, full_name, last_found, last_download)

        for download in software['downloads']:
            cursor.execute(
                "SELECT app_version FROM " + sqlite_table_name + " WHERE app_name=? AND app_platform=? AND app_version=?",
                (app_name, download['app_platform'], app_version))
            entry = cursor.fetchall()

            if entry and entry[0][0] == app_version:
                LOGGER.info("App %s in version %s already exists, updating last_found.", app_name, app_version)
                update_query = f"UPDATE {sqlite_table_name} SET last_found = \"{last_found}\" WHERE app_name = \"{app_name}\" AND app_version = \"{app_version}\""
                cursor = connection.cursor()
                LOGGER.info("Executing SQL: %s", update_query)
                cursor.execute(update_query)
            else:
                LOGGER.info("Inserting App %s  in version %s.", app_name, app_version)
                insert_query = f"INSERT INTO {sqlite_table_name} (app_name, app_version, app_platform, full_name, url_bin, hash_type, hash_res, sig_type, sig_res, url_pub_key, last_found, last_download, verified_version) VALUES ('{app_name}', '{app_version}', '{download['app_platform']}', '{full_name}', '{download['url_bin']}', '{download['hash_type']}', '{download['hash_res']}', '{download['sig_type']}', '{download['sig_res']}', '{download['url_pub_key']}', '{last_found}', '{last_download}', 'None')"
                LOGGER.debug("SQL execute: %s", insert_query)
                cursor.execute(insert_query)
            connection.commit()
    connection.close()


def activate_download_for_latest_found():
    """Activate the download flag in database for the software that what was latest found"""
    LOGGER.info("Entering function activate_download_for_latest_found")
    connection = sqlite3.connect(sqlite_db_file)
    LOGGER.info("Using sqlite file %s", sqlite_db_file)
    update_query = f"UPDATE {sqlite_table_name} SET download = 1 WHERE last_found = (SELECT MAX(last_found) FROM {sqlite_table_name})"
    cursor = connection.cursor()
    LOGGER.info("Executing SQL: %s", update_query)
    cursor.execute(update_query)
    connection.commit()
    LOGGER.info("Exiting function activate_download_for_latest_found")
    connection.close()


def activate_download_for_latest_found_by_architecture(architecture):
    """Activate the download flag in database for the software that what was latest found and with given architecture.

    @param architecture: specify the architecture for which the software download should be activated. Valid archs are: mac, mac_arm, win32, win64, linux, linux-x86_64, android
    """
    valid_architectures = ['mac', 'mac_arm', 'win32', 'win64', 'linux', 'linux-x86_64', 'android']
    LOGGER.debug("Valid architectures: %s", str(valid_architectures))
    LOGGER.info("Entering function activate_download_for_latest_found")
    connection = sqlite3.connect(sqlite_db_file)
    LOGGER.info("Using sqlite file %s", sqlite_db_file)
    if (architecture in valid_architectures):
        LOGGER.debug("Given architecture (%s) is valid.", architecture)
        update_query = f"UPDATE {sqlite_table_name} SET download = 1 WHERE app_platform = {architecture} AND last_found = (SELECT MAX(last_found) FROM {sqlite_table_name})"
        cursor = connection.cursor()
        LOGGER.info("Executing SQL: %s", update_query)
        cursor.execute(update_query)
        connection.commit()
        LOGGER.info("Exiting function activate_download_for_latest_found")
        connection.close()
    else:
        LOGGER.error("Given architecture (%s) is NOT valid.", architecture)

def reset_download_flag_for_all():
    """Reset the download flag in database for all software."""
    LOGGER.info("Entering function reset_download_flag_for_all")
    connection = sqlite3.connect(sqlite_db_file)
    LOGGER.info("Using sqlite file %s", sqlite_db_file)
    update_query = f"UPDATE {sqlite_table_name} SET download = 0"
    cursor = connection.cursor()
    LOGGER.info("Executing SQL: %s", update_query)
    cursor.execute(update_query)
    connection.commit()
    LOGGER.info("Exiting function reset_download_flag_for_all")
    connection.close()

def get_checksum_link(platform, app_name, version):
    """
    Returns the verification sources for an application with app_name,
    version and platform from the database.

    @param platform: platform of the application to find
    @param app_name: name of the application to find
    @param version: version of the application to find
    """
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

def get_url_bin_of_software_to_download():
    """
    Returns all software with download = true OR >0 and generates a list with dictionaries of every software to download.

    Dictionary contains the followong entries:
    [
        {
            'app_name': "value",
            'app_version': "value",
            'app_platform': "value",
            'url_bin' : "value",
            'last_found': "value",
            'hash_type': "value",
            'hash_res': "value",
            'sig_type': "value",
            'sig_res': "value",
            'url_pub_key': "value"
        }
    ]
    """
    connection = sqlite3.connect(sqlite_db_file)
    cursor = connection.cursor()
    query = f"""
        SELECT app_name, app_version, app_platform, url_bin, last_found, hash_type, hash_res, sig_type, sig_res, url_pub_key,
	        (SELECT MAX(last_found) FROM {sqlite_table_name} t2 WHERE t2.app_name = t1.app_name) AS max_last_found
        FROM {sqlite_table_name} t1
        WHERE download >0;
    """
    cursor.execute(query)
    sofware_list = []

    # iterate over all software marked for download with MAX_LAST_FOUND
    for row in cursor.fetchall():
        # store result in variables
        app_name, app_version, app_platform, url_bin, last_found, hash_type, hash_res, sig_type, sig_res, url_pub_key, max_last_found = row

        # create a dictionary for inserting it into list
        entry = {
                'app_name': app_name,
                'app_version': app_version,
                'app_platform': app_platform,
                'url_bin' : url_bin,
                'last_found': max_last_found,
                'hash_type': hash_type,
                'hash_res': hash_res,
                'sig_type': sig_type,
                'sig_res': sig_res,
                'url_pub_key': url_pub_key
            }
        # add software do sfotware_list which should be downloaded
        sofware_list.append(entry)
    return sofware_list

if __name__ == "__main__":
    sqlite_db_file = sqlite_db_file
    init_db()
    LOGGER.info(get_url_bin_of_software_to_download())
    # insert_dummy_data()

import os.path
import sqlite3
import logging # import lib for LOGGING
import settings # import global settings

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LogLevel)
cwd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGGER.info(" current workoing dir: " + cwd_dir)

sqlite_db_file = os.path.join(cwd_dir, 'aid.db')
sqlite_table_name = "software"
# product_table_name = "products"

################################### FUNCTIONS

def init_db():
    """Inititalize the database schema"""
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
        LOGGER.debug(f"Actual software: {app_name} {app_version} {full_name} {last_found} {last_download}")

        for download in software['downloads']:
            # print(app_name, app_version, download['app_platform'], download['url_bin'], download['url_sha256'], download['url_asc'], last_found, last_download )
            cursor.execute(
                "SELECT app_version FROM " + sqlite_table_name + " WHERE app_name=? AND app_platform=? AND app_version=?",
                (app_name, download['app_platform'], app_version))
            entry = cursor.fetchall()

            if entry and entry[0][0] == app_version:
                LOGGER.info(f"App {app_name} in version {app_version} already exists, skipping.")
            else:
                LOGGER.info(f"Inserting App {app_name} in version {app_version}.")
                insert_query = f"INSERT INTO {sqlite_table_name} (app_name, app_version, app_platform, full_name, url_bin, hash_type, hash_res, sig_type, sig_res, url_pub_key, last_found, last_download, verified_version) VALUES ('{app_name}', '{app_version}', '{download['app_platform']}', '{full_name}', '{download['url_bin']}', '{download['hash_type']}', '{download['hash_res']}', '{download['sig_type']}', '{download['sig_res']}', '{download['url_pub_key']}', '{last_found}', '{last_download}', 'None')"
                LOGGER.debug("SQL execute: " + insert_query)
                cursor.execute(insert_query)
            connection.commit()
    connection.close()


def activate_download_for_latest_found():
    """Activate the download flag in database for the software that what was latest found"""
    LOGGER.info("Entering function activate_download_for_latest_found")
    connection = sqlite3.connect(sqlite_db_file)
    LOGGER.info("Using sqlite file " + sqlite_db_file)
    update_query = f"UPDATE {sqlite_table_name} SET download = 1 WHERE last_found = (SELECT MAX(last_found) FROM {sqlite_table_name})"
    cursor = connection.cursor()
    LOGGER.info("Executing SQL: " + update_query)
    cursor.execute(update_query)
    connection.commit()
    LOGGER.info("Exiting function activate_download_for_latest_found")
    connection.close()


def activate_download_for_latest_found_by_architecture(architecture):
    """Activate the download flag in database for the software that what was latest found and with given architecture.

    @param architecture: specify the architecture for which the software download should be activated. Valid archs are: mac, mac_arm, win32, win64, linux, linux-x86_64, android
    """
    valid_architectures = ['mac', 'mac_arm', 'win32', 'win64', 'linux', 'linux-x86_64', 'android']
    LOGGER.debug("Valid architectures: " + str(valid_architectures)
    LOGGER.info("Entering function activate_download_for_latest_found")
    connection = sqlite3.connect(sqlite_db_file)
    LOGGER.info("Using sqlite file " + sqlite_db_file)
    if (architecture in valid_architectures):
        LOGGER.debug("Given architecture ("+ architecture + ") is valid.")
        update_query = f"UPDATE {sqlite_table_name} SET download = 1 WHERE app_platform = {architecture} AND last_found = (SELECT MAX(last_found) FROM {sqlite_table_name})"
        cursor = connection.cursor()
        LOGGER.info("Executing SQL: " + update_query)
        cursor.execute(update_query)
        connection.commit()
        LOGGER.info("Exiting function activate_download_for_latest_found")
        connection.close()
    else:
        LOGGER.error("Given architecture (" + architecture + ") is NOT valid.")

def reset_download_flag_for_all():
    """Reset the download flag in database for all software."""
    LOGGER.info("Entering function activate_download_for_latest_found")
    connection = sqlite3.connect(sqlite_db_file)
    LOGGER.info("Using sqlite file " + sqlite_db_file)
    update_query = f"UPDATE {sqlite_table_name} SET download = 0"
    cursor = connection.cursor()
    LOGGER.info("Executing SQL: " + update_query)
    cursor.execute(update_query)
    connection.commit()
    LOGGER.info("Exiting function activate_download_for_latest_found")
    connection.close()

def get_checksum_link(platform, app_name, version):
    """provides verification  source for an application from the database"""
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
        app_name, app_version, app_platform, url_bin, last_found, max_last_found = row

        # create a dictionary for inserting it into list
        entry = {
                'app_name': app_name,
                'app_version': app_version,
                'app_platform': app_platform,
                'url_bin' : url_bin,
                'last_found': max_last_found
            }
        # add software do sfotware_list which should be downloaded
        sofware_list.append(entry)
    return sofware_list


# def get_available_software():
#     """returns all available software and generates a dictionary for table view"""
#     connection = sqlite3.connect(sqlite_db_file)
#     cursor = connection.cursor()
#     query = f"""
#     SELECT app_name, app_version, app_platform, last_found,
#            (SELECT MAX(last_found) FROM {sqlite_table_name} t2 WHERE t2.app_name = t1.app_name) AS max_last_found
#     FROM {sqlite_table_name} t1;
#     """

#     cursor.execute(query)

#     program_data = {}

#     for row in cursor.fetchall():
#         app_name, app_version, app_platform, last_found, max_last_found = row
#         platform = app_platform

#         connection2 = sqlite3.connect(sqlite_db_file)
#         cursor2 = connection2.cursor()
#         query2 = "SELECT default_download FROM " + product_table_name + " WHERE app_name = ?"
#         cursor2.execute(query2, (app_name,))
#         default = cursor2.fetchone()[0]

#         if app_name not in program_data:
#             program_data[app_name] = []

#         #  check for version existence in list
#         version_exists = None
#         for version_data in program_data[app_name]:
#             if version_data['version'] == app_version:
#                 version_exists = True
#                 version_data[platform] = True if platform in default and last_found == max_last_found else False
#                 break

#         # When not existent add version to list
#         if not version_exists:
#             version_data = {
#                 'version': app_version,
#                 'win64': None if platform != 'win64' else (
#                     True if 'win64' in default and last_found == max_last_found else False),
#                 'linux': None if platform != 'linux' else (
#                     True if 'linux' in default and last_found == max_last_found else False),
#                 'android': None if platform != 'android' else (
#                     True if 'android' in default and last_found == max_last_found else False)
#             }
#             program_data[app_name].append(version_data)

#     return program_data


# def get_sw_list_for_platform(platform):
#     """lists all available apps for a platform"""
#     connection = sqlite3.connect(sqlite_db_file)
#     cursor = connection.cursor()
#     cursor.execute(
#         f"SELECT app_name FROM {sqlite_table_name} WHERE app_platform=\"{platform}\""
#     )
#     entries = cursor.fetchall()
#     ret_sw = []
#     for entry in entries:
#         ret_sw.append(entry[0])
#     return ret_sw


if __name__ == "__main__":
    sqlite_db_file = sqlite_db_file
    init_db()
    LOGGER.info(get_url_bin_of_software_to_download())
    # insert_dummy_data()

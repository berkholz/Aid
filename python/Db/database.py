import os
import psycopg2
import logging
import settings

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOGLEVEL)

cwd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGGER.debug("Current working dir: %s", cwd_dir)

postgres_db_config = settings.DB_CONNECTION
postgres_table_name = "software"

################################### FUNCTIONS

def init_db():
    """
    Initialize the database schema.
    """
    connection = psycopg2.connect(**postgres_db_config)
    cursor = connection.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {postgres_table_name} (
        app_name TEXT NOT NULL,
        app_version TEXT NOT NULL,
        app_platform TEXT NOT NULL,
        full_name TEXT NOT NULL,
        download INTEGER DEFAULT 0,
        url_bin TEXT NOT NULL,
        hash_type TEXT,
        hash_res TEXT,
        sig_type TEXT,
        sig_res TEXT,
        url_pub_key TEXT,
        last_found TEXT NOT NULL,
        last_download TEXT,
        verified_version TEXT,
        PRIMARY KEY (app_name, app_version, app_platform)
        );
    """)
    connection.commit()
    connection.close()


def append_software(list_software_dict):
    """Adds software versions to the database if they don't exist."""
    global LOGGER
    connection = psycopg2.connect(**postgres_db_config)
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
                f"SELECT app_version FROM {postgres_table_name} WHERE app_name=%s AND app_platform=%s AND app_version=%s",
                (app_name, download['app_platform'], app_version))
            entry = cursor.fetchall()

            if entry and entry[0][0] == app_version:
                LOGGER.info("App %s in version %s already exists, updating last_found.", app_name, app_version)
                update_query = f"UPDATE {postgres_table_name} SET last_found = %s WHERE app_name = %s AND app_version = %s"
                cursor.execute(update_query, (last_found, app_name, app_version))
            else:
                LOGGER.info("Inserting App %s in version %s.", app_name, app_version)
                insert_query = f"""
                    INSERT INTO {postgres_table_name} 
                    (app_name, app_version, app_platform, full_name, url_bin, hash_type, hash_res, sig_type, sig_res, url_pub_key, last_found, last_download, verified_version) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    app_name, app_version, download['app_platform'], full_name, download['url_bin'], 
                    download['hash_type'], download['hash_res'], download['sig_type'], download['sig_res'], 
                    download['url_pub_key'], last_found, last_download, 'None'))
            connection.commit()
    connection.close()


def activate_download_for_latest_found():
    """Activate the download flag in the database for the software that was latest found."""
    LOGGER.info("Entering function activate_download_for_latest_found")
    connection = psycopg2.connect(**postgres_db_config)
    LOGGER.info("Using PostgreSQL database")
    update_query = f"""
        UPDATE {postgres_table_name} 
        SET download = 1 
        WHERE last_found = (SELECT MAX(last_found) FROM {postgres_table_name})
    """
    cursor = connection.cursor()
    LOGGER.info("Executing SQL: %s", update_query)
    cursor.execute(update_query)
    connection.commit()
    LOGGER.info("Exiting function activate_download_for_latest_found")
    connection.close()


def reset_download_flag_for_all():
    """Reset the download flag in the database for all software."""
    LOGGER.info("Entering function reset_download_flag_for_all")
    connection = psycopg2.connect(**postgres_db_config)
    LOGGER.info("Using PostgreSQL database")
    update_query = f"UPDATE {postgres_table_name} SET download = 0"
    cursor = connection.cursor()
    LOGGER.info("Executing SQL: %s", update_query)
    cursor.execute(update_query)
    connection.commit()
    LOGGER.info("Exiting function reset_download_flag_for_all")
    connection.close()


def get_checksum_link(platform, app_name, version):
    """
    Returns the verification sources for an application with app_name,
    version, and platform from the database.
    """
    connection = psycopg2.connect(**postgres_db_config)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT url_bin, hash_type, hash_res, sig_type, sig_res, url_pub_key 
        FROM {postgres_table_name} 
        WHERE app_platform=%s AND app_name=%s AND app_version=%s
        """, (platform, app_name, version))
    entry = cursor.fetchone()
    print(entry)
    if entry:
        return entry
    else:
        return None


def get_url_bin_of_software_to_download():
    """
    Returns all software with download > 0 and generates a list with dictionaries of every software to download.
    """
    connection = psycopg2.connect(**postgres_db_config)
    cursor = connection.cursor()
    query = f"""
        SELECT app_name, app_version, app_platform, url_bin, last_found, hash_type, hash_res, sig_type, sig_res, url_pub_key,
         (SELECT MAX(last_found) FROM {postgres_table_name} t2 WHERE t2.app_name = t1.app_name) AS max_last_found
        FROM {postgres_table_name} t1
        WHERE download > 0;
    """
    cursor.execute(query)
    software_list = []

    for row in cursor.fetchall():
        app_name, app_version, app_platform, url_bin, last_found, hash_type, hash_res, sig_type, sig_res, url_pub_key, max_last_found = row
        entry = {
            'app_name': app_name,
            'app_version': app_version,
            'app_platform': app_platform,
            'url_bin': url_bin,
            'last_found': max_last_found,
            'hash_type': hash_type,
            'hash_res': hash_res,
            'sig_type': sig_type,
            'sig_res': sig_res,
            'url_pub_key': url_pub_key
        }
        software_list.append(entry)
    return software_list


if __name__ == "__main__":
    init_db()
    LOGGER.info(get_url_bin_of_software_to_download())
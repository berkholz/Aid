from os import path
from posixpath import basename
from tkinter import NO
import gnupg # import for GNUPG actions
import requests # import for requesting http ressources
import logging # import for logging
import os # for quarentine files
import urllib # import urllib for parsing urls
# from Downloader.utils import DOWNLOAD_PATH
from Downloader.downloader import download_file
import settings # import global settings
import validators # validate urls
import hashlib # for generating sha256 sum

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LogLevel)


################################### FUNCTIONS

def import_keys(list_of_key_urls):
    """
    Mapper function for importing vendor public keys from a list of dicts with URL.
    Expected dictionary:
    [
        {'url_pub_key': 'scheme://netloc/path;parameters?query#fragment'},
        {'url_pub_key': 'scheme://netloc/path;parameters?query#fragment'},
        {'url_pub_key': 'scheme://netloc/path;parameters?query#fragment'}
    ]

    @param: List of dict with url_pub_key to import url.
    """
    # importing public keys from vendors
    for software in list_of_key_urls:
        import_key_from_url(software['url_pub_key'])

def import_key_from_url(key_url):
    """Import a public key from a URL.

    @param: URL of key file to import.
    """
    gpg = gnupg.GPG()

    if validators.url(key_url):
        LOGGER.debug("Key URL " + key_url + " is valid.")
        try:
            retry = 0
            response = requests.get(key_url, timeout=300)
            while response.status_code == 502 and retry < 5:
                response = requests.get(key_url, timeout=300)
                retry += 1

            LOGGER.info(response.status_code)
            key_data = response.text
            import_result = gpg.import_keys(key_data)
            if import_result.count == 0:
                LOGGER.info("Error: No key was imported.")
                return False
            LOGGER.info(f"Key imported successfully. Fingerprint: {import_result.fingerprints[0]}")
            return True
        except requests.RequestException as e:
            LOGGER.error(f"Error downloading or importing the key: {e}")
            return False
    else:
        LOGGER.warning("Key URL <" + key_url + "> is not valid, skipping import.")

def calculate_hash(hash_algorithm, hashfile):
    """
    Function to calculate the hash sum with given algorithm (hash_alroithm). For valid hash algorithms see hashlib.algorithms_available().

    @param hash_algorithm: a hash algorithm representation of hashlib.
    @param hashfile: absolute path including file name of the file for which the hash should be generated.
    """

    # TODO: Check if file exists
    with open(hashfile,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
    return readable_hash

    # generated_hash = hashlib.sha256
    # # open hash file
    # with open(hashfile,"rb") as f:
    #     # reading file in 4K blocks
    #     for byte_block in iter(lambda: f.read(4096),b""):
    #         generated_hash.update(byte_block)
    # return generated_hash.hexdigest()

def get_absolute_filename(url_bin, basedir):
    """
    Function to generate the absoulte path for the download file. The URL (url_bin) is taken to extract the basename.
    The basename is concatenated with the basedir (basedir) to generate the absolute file name including the fuill path.

    @param url_bin: URL fo downloaded binary in DB.
    @param basedir: Download directory where the downloaded software was saved.
    """
    LOGGER.debug("Begin function get_absolute_filename()...")

    parsed_url = urllib.parse.urlsplit(url_bin)
    LOGGER.debug("parsed url: " + str(parsed_url))

    quoted_file_name = str(parsed_url.path).split('/')[-1]
    LOGGER.debug("quoted_file_name: " + quoted_file_name)

    # remove url special quoting characters, e.g. %20
    file_name = urllib.parse.unquote(quoted_file_name, encoding='utf-8', errors='replace')
    LOGGER.debug("file_name: " + file_name)

    LOGGER.debug("...end function get_absolute_filename()")
    return basedir + file_name

def quarentine_file(absolute_filename):
    """
    Rename a file with a prefix QUARENTINED_ to mark file as invalid (hash is not correct).

    @param absolute_filename: Absolute path and name of file to quarentine.
    """
    basedir = os.path.dirname(absolute_filename)
    filename = os.path.basename(absolute_filename)

    if (os.path.isfile(absolute_filename)):
        os_name = os.uname()
        # check OS so that we take the correct path seperator
        if (os_name.sysname == "Windows"):
            old_filename = absolute_filename
            new_filename = basedir + "\\QUARENTINED_" + filename
            os.rename(old_filename, new_filename)
        elif (os_name.sysname == "Linux" or os.system() == "Darwin"):
            old_filename = absolute_filename
            new_filename = basedir + "/QUARENTINED_" + filename
            LOGGER.debug("Move " + old_filename + " to " + new_filename)
            os.rename(old_filename, new_filename)
        else:
            LOGGER.error("OS " + os.system() + " not supported. File " + absolute_filename + " is NOT quarentined.")
    else:
        LOGGER.error("File " + absolute_filename + " does not exist and could not be quarentined.")

def check_signature_of_hash_file(signature_type, signature_filename, hash_filename):
    """
    Check the signature of the hash file by using the signature file on disk.

    @param signature_type: Type of the signature.
    @param signature_filename: Local filename of the signature.
    @param hash_filename: Local file name of the hash file.
    """
    if signature_type == "sig_file":
        LOGGER.debug("signature_type is " + signature_type)
    elif signature_type == "gpg_file":
        LOGGER.debug("signature_type is " + signature_type)
    elif signature_type == "asc_file":
        LOGGER.debug("signature_type is " + signature_type)
    else:
        LOGGER.error("unknown signature type")


def get_hash_type(hash_typ_in_db):
    """
    Converts the hash_type from the db to a hash type of hashlib:
    * hashlib.sha256
    * hashlib.sha1

    @param hash_typ_in_db: The hash type that is stored in the db.
    """
    if (hash_typ_in_db == "sha256_multi" or hash_typ_in_db == "sha256_single"):
        return hashlib.sha256
    elif (hash_typ_in_db == "sha1_string"):
        return hashlib.sha1
    elif (hash_typ_in_db == "string"):
        return hashlib.sha256
    else:
        return hashlib.sha256


def verify(list_of_software):
    """

    @param list_of_software: list of dictionaries with software entries.
    """
    LOGGER.info("In function verify...")
    for software_entry in list_of_software:
        # assigning values to temporary variables for logging and better readability
        tmp_hash_type = software_entry['hash_type']
        LOGGER.debug("hash_type: " + tmp_hash_type)
        tmp_hash_res = software_entry['hash_res']
        LOGGER.debug("hash_res: " + tmp_hash_res)
        tmp_sig_type = software_entry['sig_type']
        tmp_sig_res = software_entry['sig_res']
        tmp_app_name = software_entry['app_name']
        tmp_app_version = software_entry['app_version']
        tmp_app_platform = software_entry['app_platform']
        path_to_download_file = get_absolute_filename(software_entry['url_bin'], settings.DOWNLOAD_PATH + tmp_app_name + '/' + tmp_app_version + '/' + tmp_app_platform + '/')

        # no hash_res given
        if (tmp_hash_type == 'None' or tmp_hash_res == 'None'):
            LOGGER.debug("No hash file given.")
            hash = calculate_hash(hashlib.sha256, path_to_download_file)
            LOGGER.info("Calculated hash for file " + path_to_download_file + ": " + hash)

            LOGGER.info(f"update hash_res for {tmp_app_name}({tmp_app_version} - arch {tmp_app_platform}) in database to {hash}.")
            # TODO: implement
            LOGGER.info(f"update hash_type for {tmp_app_name}({tmp_app_version} - arch {tmp_app_platform}) in database to manual_sha256")
            # TODO: implement
        # hash_res in db specified
        else:
            LOGGER.debug("Hash file in DB specified for " + tmp_app_name + "(" + tmp_app_version + "|" + tmp_app_platform + ").")
            # hash_type was genereated manually
            if (tmp_hash_type == "manual_sha256"):
                LOGGER.debug("Calculating hash of downloaded file: " + path_to_download_file)
                control_hash = calculate_hash(hashlib.sha256, path_to_download_file)
                LOGGER.info("calculated hash (" + str(hashlib.sha256) + "):" + control_hash)
                # check if hash in DB is equal to calculated hash
                if (tmp_hash_res == control_hash):
                    LOGGER.info("Hash in DB (" + tmp_hash_res + ") is equal to calculated hash (" + control_hash + ").")
                else:
                    LOGGER.info("Hash is not correct.")
                    quarentine_file()
            # hash was given by vendor or URL
            else:
                LOGGER.info("Downloading hash file (" + tmp_hash_res + ")...")
                destination_hash_file_name = get_absolute_filename(tmp_hash_res, os.path.dirname(path_to_download_file))
                download_file(tmp_hash_res, destination_hash_file_name)

                LOGGER.info("Check if signature is given in DB")
                # signature for hash file in DB found
                if (tmp_sig_type != None and tmp_sig_res != None):
                    destination_sig_file_name = get_absolute_filename(tmp_sig_res, os.path.dirname(path_to_download_file))
                    download_file(tmp_sig_res, destination_sig_file_name)
                    LOGGER.debug(f"downloading signature file from {tmp_sig_res} to local file {destination_sig_file_name}.")

                    check_signature_of_hash_file(tmp_sig_type, destination_sig_file_name, destination_hash_file_name)
                # no signature found
                else:
                    control_hash = calculate_hash(get_hash_type(tmp_hash_type), path_to_download_file)
                    hash_res_sum = "" # get_hash(hash_type, hash_res, app_name, app_platform, app_version)

                    if control_hash == hash_res_sum:
                        LOGGER.info("success: hash validated successful")
                    else:
                        LOGGER.error("failure: hash of file not valid")
                        quarentine_file(path_to_download_file)
    LOGGER.info("Exiting function verify...")

if __name__ == '__main__':
    LOGGER.info("Starting verifier.")
    unix_filename = "/home/user/test.txt"
    # windows_filename = 'C:\Users\USER\test.txt'
    quarentine_file(unix_filename)
import hashlib
import os
from functools import reduce

import gnupg
import requests

from Db.database import get_checksum_link


def verify(path):
    file_name = path.split('/')[-1]
    platform = path.split('/')[-2].split('-')[0]
    software = file_name.split('-')[0]
    i=-1
    if file_name.split('.')[-2]=='tar':
        i = -2
    software_version = ".".join(file_name.split('-')[1].split('.')[:i])

    res = get_checksum_link(platform, software, software_version)

    hash_verify_status = verify_hash(path, software, res)

    sig_verify_status = verify_signature(path, res)

    if hash_verify_status == False or sig_verify_status == False:
        return False
    else:
        return True


def verify_hash(path, software, res):
    dwl_link = res[0]
    cs_type = res[1]
    cs_link = res[2]

    if cs_link:
        if cs_type == 'sha256_single':
            online_sha256 = get_single_line_file_hash(link=cs_link)
        elif cs_type == 'sha256_multi':
            online_sha256 = get_multi_line_file_hash(cs_link, dwl_link)
        elif cs_type == 'string':
            online_sha256 = cs_link
        else:
            return True

        with open(path, 'rb') as f:
            bytes = f.read()
            file_sha256 = hashlib.sha256(bytes).hexdigest()

        print(f'Verifying hash of {software}:\n'
              f'local:\t{file_sha256}\n'
              f'online:\t{online_sha256}')

        return file_sha256 == online_sha256

    else:
        return None


def download_file(url, local_filename):
    """Download a file from a URL and save it locally."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        # print(response.content)
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        # print(f"Downloaded: {local_filename}")
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False
    return True


def import_key_from_url(key_url):
    """Import a public key from a URL."""
    gpg = gnupg.GPG()
    try:
        retry = 0
        response = requests.get(key_url, timeout=300)
        while response.status_code == 502 and retry < 5:
            response = requests.get(key_url, timeout=300)
            retry += 1

        # print(response.status_code)
        key_data = response.text
        import_result = gpg.import_keys(key_data)
        if import_result.count == 0:
            print("Error: No key was imported.")
            return False
        # print(f"Key imported successfully. Fingerprint: {import_result.fingerprints[0]}")
        return True
    except requests.RequestException as e:
        print(f"Error downloading or importing the key: {e}")
        return False


def verify_signature(file_path, res):
    """Verify a local file against its PGP signature downloaded from a URL."""
    signature_type = res[3]
    signature_url = res[4]
    key_url = res[5]

    if signature_type in ['asc_file', 'sig_file']:
        if not import_key_from_url(key_url):
            return False
        gpg = gnupg.GPG()

        # Check if the local file exists
        if not os.path.exists(file_path):
            print(f"Error: The file {file_path} does not exist.")
            return False

        # Download the signature file
        if signature_type == 'sig_file':
            signature_filename = "signature.sig"
        else:
            signature_filename = "signature.asc"

        if not download_file(signature_url, signature_filename):
            return False


        # Verify the signature
        with open(signature_filename, 'rb') as sig_file:
            verified = gpg.verify_file(sig_file, file_path)

        os.remove(signature_filename)

        if verified:
            print("Signature verified successfully.")
            print(f"Signed by: {verified.username}")
            return True
        else:
            print("Signature verification failed.")
            print(f"Status: {verified.problems}")
            return False


    elif signature_type is None:
        return True


def get_single_line_file_hash(link):
    hash_file = requests.get(link)
    return hash_file.content.decode('utf-8').split('  ')[0]


def get_multi_line_file_hash(cs_link, file_link):
    tmp = "/".join(file_link.split('/')[-3:])
    print(tmp)

    hash_file = requests.get(cs_link)
    lines = hash_file.content.decode('utf-8')
    for line in lines.split('\n'):
        if tmp in line:
            return line.split('  ')[0]
    return None


if __name__ == '__main__':
    if verify('C:/Users/***REMOVED***/PycharmProjects/Aid/downloads/09_09_2024/win64-6/notepad++-v8.6.9.exe'):
        print('VERIFIED')
    else:
        print('NOT VERIFIED')

import os
import hashlib

import gnupg

def verify_pkg_path(path):
    files = os.listdir(path)
    filenames = [file for file in files if file not in ['sha256sum.txt', 'sha256sum.txt.asc']]

    result = verify_sha256_checksums(path, filenames)
    return result

def calculate_sha256(filename):
    """calculates the sha256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def verify_sha256_checksums(path, filenames):
    """verifies the sha256 hash of a file using the sha256.txt file"""
    sums_file = os.path.join(path, "sha256sum.txt")

    # Verify GPG signature first
    signature_result = verify_gpg_signature(path)
    if "Error" in signature_result:
        return signature_result


    # Read the sha256sum.txt file
    try:
        with open(sums_file, "r") as f:
            expected_checksums = dict(line.strip().split("  ")[::-1] for line in f if line.strip())
    except FileNotFoundError:
        return "Error: sha256sum.txt file not found"

    # Verify checksums for each file
    for filename in filenames:
        full_path = os.path.join(path, filename)
        try:
            calculated_checksum = calculate_sha256(full_path)
        except FileNotFoundError:
            return f"Error: File not found - {filename}"

        if filename not in expected_checksums:
            return f"Error: Checksum not found for file - {filename}"

        if calculated_checksum != expected_checksums[filename]:
            return f"Error: Checksum mismatch for file - {filename}"

    return "All checksums verified successfully"


def verify_gpg_signature(path):
    """verifies the gpg signature of our sha256sum.txt file"""
    gpg = gnupg.GPG()
    signature_file = os.path.join(path, "sha256sum.txt.asc")
    sums_file = os.path.join(path, "sha256sum.txt")

    if not os.path.isfile(signature_file):
        return "Error: GPG signature file (sha256sum.txt.asc) not found"

    with open(signature_file, 'rb') as f:
        verified = gpg.verify_file(f, sums_file)

    if verified:
        return "GPG signature verified successfully"
    else:
        return f"Error: GPG signature verification failed - {verified.status}"


if __name__ == "__main__":
    path = "C:/Users/***REMOVED***/Desktop/tmp_package/AID_PACKAGE-24_09_17-blupp/"

    print(verify_pkg_path(path))

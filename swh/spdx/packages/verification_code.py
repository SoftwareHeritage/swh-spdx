import hashlib

from spdx_tools.spdx.model import PackageVerificationCode


def generate_verification_code(files_list: list) -> PackageVerificationCode:
    """
    Generates the Package verification code using the
    algorithm specified by SPDX specification

    Args:
        files_list (list): List of file objects contained by package
        maybe Directory or Content object

    Returns:
        PackageVerificationCode(value)
    """
    list_of_file_hashes = []
    for file in files_list:
        file_checksum_value = file.checksums["sha1"]
        list_of_file_hashes.append(file_checksum_value)
    list_of_file_hashes.sort()
    hasher = hashlib.new("sha1")
    hasher.update("".join(list_of_file_hashes).encode("utf-8"))
    value = hasher.hexdigest()
    return PackageVerificationCode(value)

#!/usr/bin/env python

import shutil
import zmq
import zmq.auth
from pathlib import Path
from typing import Union


def generate_certificates(base_dir: Union[str, Path]) -> None:
    """Generate client and server CURVE certificate files"""
    base_dir = Path(base_dir).resolve()

    # Directories for certificates, public keys, and private keys
    keys_dir = base_dir / "certificates"
    public_keys_dir = keys_dir / "public_keys"
    secret_keys_dir = keys_dir / "private_keys"

    # Create directories for certificates, remove old content if necessary
    for directory in [keys_dir, public_keys_dir, secret_keys_dir]:
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)

    # Create new keys in certificates dir
    server_public_file, server_secret_file = zmq.auth.create_certificates(
        keys_dir, "server"
    )
    client_public_file, client_secret_file = zmq.auth.create_certificates(
        keys_dir, "client"
    )

    # Define file suffixes for public and secret keys
    public_suffix = ".key"
    private_suffix = ".secret"

    # Move and rename keys to the appropriate directories
    for key_file in keys_dir.iterdir():
        if key_file.suffix == ".key":
            new_location = public_keys_dir / key_file.name.replace(
                ".key", public_suffix
            )
            shutil.move(key_file, new_location)

        elif key_file.suffix == ".key_secret":
            new_location = secret_keys_dir / key_file.name.replace(
                ".key_secret", private_suffix
            )
            shutil.move(key_file, new_location)


if __name__ == "__main__":
    if zmq.zmq_version_info() < (4, 0):
        raise RuntimeError(
            f"Security is not supported in libzmq version < 4.0. libzmq version {zmq.zmq_version()}"
        )

    generate_certificates(Path(__file__).resolve().parent)

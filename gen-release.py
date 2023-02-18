# Helper script to generate a release for a debian package repository.
# The script first generates a Packages file for the repository that contains the list of packages.
# Then, it generates a Release file that contains the checksums of the Packages file.
# The Release file is signed with the GPG key of the repository.

import os
import sys

# Get the current date.
current_date = os.popen("date -Ru").read().strip()

### Clean up ###
# Delete the Packages, Packages.gz, Release, Release.gpg and InRelease files if they exist.
def delete_existing_files():
    print("Deleting old build files...")
    print("--------------------------------------------------")
    os.system("rm -f dists/stable/main/binary-amd64/Packages")
    os.system("rm -f dists/stable/main/binary-amd64/Packages.gz")
    os.system("rm -f dists/stable/Release")
    os.system("rm -f dists/stable/Release.gpg")
    os.system("rm -f dists/stable/InRelease")

delete_existing_files()

### Packages file generation ###
# Function to generate the Packages file.
def generate_packages_file():
    print("Generating Packages file...")
    print("--------------------------------------------------")
    os.system("dpkg-scanpackages --multiversion pool/ > dists/stable/main/binary-amd64/Packages")
    # Zip the Packages file.
    os.system("gzip -k -f dists/stable/main/binary-amd64/Packages > dists/stable/main/binary-amd64/Packages.gz")

generate_packages_file()

### Release file generation ###
# Append repo information to the Release file.
def append_repo_info_to_release_file():
    print("Appending repo information to Release file...")
    print("--------------------------------------------------")
    with open("dists/stable/Release", "a") as release_file:
        release_file.write("Origin: Numigi repository\n")
        release_file.write("Label: numigi-apt-repo\n")
        release_file.write("Suite: stable\n")
        release_file.write("Codename: stable\n")
        release_file.write("Version: 1.0\n")
        release_file.write("Architectures: amd64 arm64 arm7\n")
        release_file.write("Components: main\n")
        release_file.write("Description: Numigi custom packages repository\n")
        release_file.write(f"Date: {current_date}\n")

append_repo_info_to_release_file()

# Append checksums to the Release file.
def append_checksums_to_release_file():
    print("Appending checksums to Release file...")
    print("--------------------------------------------------")
    os.system("apt-ftparchive release dists/stable >> dists/stable/Release")

append_checksums_to_release_file()

# Function to sign the Release file.
def sign_release_file():
    print("Signing Release file...")
    print("--------------------------------------------------")
    os.system("gpg --default-key \"joliveau.loan@gmail.com\" -abs -o - dists/stable/Release > dists/stable/Release.gpg")

sign_release_file()

# Function to create the InRelease file.
def create_in_release_file():
    print("Creating InRelease file...")
    print("--------------------------------------------------")
    os.system("gpg --default-key \"joliveau.loan@gmail.com\" --clearsign -o - dists/stable/Release > dists/stable/InRelease")

create_in_release_file()

# Helper script to generate a release for a debian package repository.
# The script first generates a Packages file for the repository that contains the list of packages.
# Then, it generates a Release file that contains the checksums of the Packages file.
# The Release file is signed with the GPG key of the repository.

import os

# Generate a new release
def generate_release():
    # Verify if the KEY.asc file is present. If not, list the user's gpg secret keys and ask them to choose one.
    # Then, export the chosen key to the KEY.asc file.
    def verify_key_file():
        if not os.path.isfile("KEY.asc"):
            print("No GPG key found. Please choose one from the list below:")
            print("--------------------------------------------------")
            os.system("gpg --list-secret-keys --keyid-format=long")
            print("--------------------------------------------------")
            key_id = input("Enter the ID of the key you want to use: ")
            os.system(f"gpg --armor --export {key_id} > KEY.asc")
            print("--------------------------------------------------")
            print("Public GPG key exported to KEY.asc file.")
            print("--------------------------------------------------")

    verify_key_file()

    # Delete old release files.
    def delete_existing_files():
        print("Deleting old build files...")
        print("--------------------------------------------------")
        os.system("rm -f dists/stable/main/binary-amd64/Packages")
        os.system("rm -f dists/stable/main/binary-amd64/Packages.gz")
        os.system("rm -f dists/stable/Release")
        os.system("rm -f dists/stable/Release.gpg")
        os.system("rm -f dists/stable/InRelease")

    delete_existing_files()

    ### Generate release files ###
    def generate_release_files():
        # Packages file generation.
        def packages_file():
            print("Generating Packages file...")
            print("--------------------------------------------------")
            os.system("dpkg-scanpackages --multiversion pool/ > dists/stable/main/binary-amd64/Packages")
            # Zip the Packages file.
            os.system("gzip -k -f dists/stable/main/binary-amd64/Packages > dists/stable/main/binary-amd64/Packages.gz")

        packages_file()

        # Append repo information to the Release file.
        def release_file():
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
                
        release_file()
        
        # Append checksums to the Release file.
        def release_checksums():
            print("Appending checksums to Release file...")
            print("--------------------------------------------------")
            os.system("apt-ftparchive release dists/stable >> dists/stable/Release")
            
        release_checksums()
        
        # Sign the Release file.
        def sign_release():
            print("Signing Release file...")
            print("--------------------------------------------------")
            os.system('gpg --default-key "joliveau.loan@gmail.com" -abs -o - dists/stable/Release > dists/stable/Release.gpg')
            
        sign_release()
        
        # Create the InRelease file.
        def add_in_release():
            print("Creating InRelease file...")
            print("--------------------------------------------------")
            os.system('gpg --default-key "joliveau.loan@gmail.com" --clearsign -o - dists/stable/Release > dists/stable/InRelease')
            
        add_in_release()
    
    generate_release_files()

generate_release()

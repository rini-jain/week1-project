import requests
import hashlib

# ✅ Cloudsmith API Key and Repository Details
API_KEY = "b4036026bca68503496476c742b23da50c3542f5"  # Replace with actual API Key
OWNER = "rini-jain-RNYE"  # Your Cloudsmith organization name
REPO_NAME = "rini"  # Your Cloudsmith repository name
PACKAGE_FILE = "npm-package-upload-1.0.0.tgz"  # Replace with your actual package file

# ✅ Step 1: Generate SHA-256 Checksum of the Package
def generate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

checksum = generate_sha256(PACKAGE_FILE)
print(f"✅ SHA-256 Checksum: {checksum}")

# ✅ Step 2: Upload the Package File (PUT Request)
upload_url = f"https://upload.cloudsmith.io/{OWNER}/{REPO_NAME}/{PACKAGE_FILE}"
headers = {
    "Content-Sha256": checksum,
    "X-Api-Key": API_KEY
}

with open(PACKAGE_FILE, "rb") as f:
    response = requests.put(upload_url, headers=headers, data=f)

if response.status_code == 200:
    identifier = response.json().get("identifier")
    print(f"✅ Package uploaded successfully! Identifier: {identifier}")
else:
    print(f"❌ Error uploading package: {response.text}")
    exit()

# ✅ Step 3: Complete the Upload (POST Request)
complete_url = f"https://api.cloudsmith.io/v1/packages/{OWNER}/{REPO_NAME}/upload/npm/"
payload = {
    "package_file": identifier,
    "npm_dist_tag": "latest"
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Api-Key": API_KEY
}

response = requests.post(complete_url, json=payload, headers=headers)

if response.status_code == 201:
    print(f"✅ Package upload completed successfully!")
else:
    print(f"❌ Error completing package upload: {response.text}")

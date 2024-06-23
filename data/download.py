import requests
import zipfile
import io

url = "https://download.inep.gov.br/microdados/microdados_enem_2023.zip"
print("Downloading file")
response = requests.get(url)
if response.status_code == 200:
    print("Download complete")
    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        thezip.extractall("microdados_enem_2023")
    print("Extraction complete")
else:
    print("Failed to download file")

import pyinstaller_versionfile

pyinstaller_versionfile.create_versionfile(
    output_file="versionfile.txt",
    version="0.3",
    company_name="Bob",
    file_description="Screen ruler",
    internal_name="Screen ruler",
    legal_copyright="© 2022",
    original_filename="screenruler.exe",
    product_name="Screenruler"
)
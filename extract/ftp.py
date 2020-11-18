import re

import ftplib

DATASUS_HOST = "ftp.datasus.gov.br"
CNES_DIR = "cnes"
FTP_CNES_FILE = r'(BASE_DE_DADOS_CNES_)(\d{6})(\.ZIP)'


def download_latest_cnes_dataset(temp_dir):
    with ftplib.FTP(DATASUS_HOST) as ftp:
        ftp.login()
        ftp.cwd(CNES_DIR)

        latest_file = [None, 0, None]
        file_list = ftp.nlst()
        for line in file_list:
            match = re.search(FTP_CNES_FILE, line)
            if match is not None:
                n = match.group(1)
                v = int(match.group(2))
                f = match.group(3)

                latest_file[0] = n if latest_file[0] is None else latest_file[0]
                latest_file[1] = v if v > latest_file[1] else latest_file[1]
                latest_file[2] = f if latest_file[2] is None else latest_file[2]

        latest_file[1] = str(latest_file[1])
        version = latest_file[1]
        latest_file_str = "".join(latest_file)

        handler_func = open(temp_dir + latest_file_str, 'wb').write
        try:
            ftp.retrbinary("RETR " + latest_file_str, handler_func)
        except Exception as e:
            raise Exception("retrieving archived CNES dataset: " + str(e))

        return temp_dir + latest_file_str, version

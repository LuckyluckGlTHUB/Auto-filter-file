from ftplib import FTP, error_perm

common_config = {
    'server': 'your_ip',
    'id': 'your_user',
    'passwd': 'your_passwd',
    'extension': '.txt',
}

folders = ['a', 'b', 'c']

for folder in folders:
    config = common_config.copy()
    
    config['path_ftp'] = f'your_ftp_file_path{folder}'

    ftp = FTP()

    try:
        ftp.connect(config['server'])
        ftp.login(config['id'], config['passwd'])
        ftp.set_pasv(0)
        print(f"Connected to FTP server {config['server']} - Folder: {folder}")

        ftp.cwd(config['path_ftp'])

        file_list = [file[0] for file in ftp.mlsd() if file[1]['type'] == 'file']

        files_with_size = []

        for file in file_list:
            try:
                file_size = ftp.size(file)

                if file_size == 0:
                    print(f"Ignore file {file} (0 bytes)")
                    continue

                if not file.endswith(config['extension']):
                    print(f"Ignore file {file} (invalid extension)")
                    continue

                files_with_size.append((file, file_size))

            except Exception as e:
                print(f"Error getting file size for {file}: {e}")

        if files_with_size:
            files_with_size.sort(key=lambda x: x[1], reverse=False)
            file_to_keep = files_with_size[0][0]
            print(f"Keep file with the largest size: {file_to_keep}")

            non_empty_txt_files = [file[0] for file in files_with_size if file[1] > 0]
            if len(non_empty_txt_files) > 1:
                for file in file_list:
                    if file == file_to_keep:
                        ftp.delete(file)
                        print(f"The file {file} has been deleted")
            else:
                print(f"There is only one non-empty .txt file on {config['server']} - Folder: {folder}. Do not delete.")
    except error_perm as e_perm:
        print(f"Permission error on {config['server']} - Folder: {folder}: {e_perm}")
    except Exception as e:
        print(f"An unexpected error occurred on {config['server']} - Folder: {folder}: {e}")
    finally:
        print(f'Disconnected from FTP server {config["server"]} - Folder: {folder}')
        ftp.quit()

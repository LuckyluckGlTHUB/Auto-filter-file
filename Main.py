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
        print(f"Connecté au FTP de {config['server']} - Dossier : {folder}")

        ftp.cwd(config['path_ftp'])

        liste_fichiers = [fichier[0] for fichier in ftp.mlsd() if fichier[1]['type'] == 'file']

        fichiers_avec_taille = []

        for fichier in liste_fichiers:
            try:
                taille_fichier = ftp.size(fichier)

                if taille_fichier == 0:
                    print(f"Ignorer le fichier {fichier} (0 octet)")
                    continue

                if not fichier.endswith(config['extension']):
                    print(f"Ignorer le fichier {fichier} (extension non valide)")
                    continue

                fichiers_avec_taille.append((fichier, taille_fichier))

            except Exception as e:
                print(f"Erreur lors de la récupération de la taille du fichier {fichier}: {e}")

        if fichiers_avec_taille:
            fichiers_avec_taille.sort(key=lambda x: x[1], reverse=False)
            fichier_a_garder = fichiers_avec_taille[0][0]
            print(f"Conserver le fichier avec la plus grande taille : {fichier_a_garder}")

            fichiers_txt_non_nuls = [fichier[0] for fichier in fichiers_avec_taille if fichier[1] > 0]
            if len(fichiers_txt_non_nuls) > 1:
                for fichier in liste_fichiers:
                    if fichier == fichier_a_garder:
                        ftp.delete(fichier)
                        print(f"Le fichier {fichier} a été supprimé")
            else:
                print(f"Il ne reste qu'un seul fichier .txt (non à 0 octet) sur {config['serveur']} - Dossier : {folder}. Ne pas supprimer.")
    except error_perm as e_perm:
        print(f"Erreur de permission sur {config['server']} - Dossier : {folder}: {e_perm}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite sur {config['server']} - Dossier : {folder}: {e}")
    finally:
        print(f'Déconnexion au FTP de {config["server"]} - Dossier : {folder}')
        ftp.quit()

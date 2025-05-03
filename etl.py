import pandas as pd
import os #Manipular o sistema operacional
import glob #Manipular diretorios e arquivos em massa

#caminho para ler os arquivos
folder_path = r'C:\Users\Tacio14\OneDrive\Documentos\Netflix ETL Python\src\data\raw'

# lista todos os arquivos
excel_files = glob.glob(os.path.join(folder_path, '*.xlsx'))

if not excel_files:
    print("Nenhum arquivo encontrado")
else:
    print(excel_files)

    #dataframe = tabela na memoria para guardar os conteudos dos arquivos
    dfs = []

    for excel_files in excel_files:
        try:
            # leio o arquivo excel
            df_temp = pd.read_excel(excel_files)

            #capturo o nome dos arquivos
            file_name = os.path.basename(excel_files)

            df_temp['filename'] = file_name

            #criando nova coluna chamada 'location'
            if 'brasil' in file_name.lower():
                df_temp['location'] = 'br'
            elif 'france' in file_name.lower():
                df_temp['location'] = 'fr'
            elif 'italian' in file_name.lower():
                df_temp['location'] = 'it'

            #criando nova coluna chamada campaign
            df_temp['campaign'] = df_temp['utm_link'].str.extract(r'utm_campaign=(.*)')

            #guarda todos os dados tratados em um dataframe
            dfs.append(df_temp)

        except Exception as e:
            print(f"Error {excel_files}")

    if dfs:

        #concatena todas as tabelas salvas no dfs em uma unica tabela
        result = pd.concat(dfs, ignore_index=True)
        #caminho de saida
        output_file = os.path.join(r'C:\Users\Tacio14\OneDrive\Documentos\Netflix ETL Python\src\data\ready\clean.xlsx')
        #configura o motor de escrita
        writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
        #leva os dados a serem escritos no motor de excel ocnfigurado
        result.to_excel(writer, index=False)
        #salva o arquivo excel
        writer._save()
    else:
        print("Nenhum dado para ser salvo")
import shutil
import os
from prefect import task, flow

# Definir una tarea que copie archivos de una carpeta a otra
@task
def copy_files(source_dir, target_dir):
    #file_names = []
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Copiar archivos
        

        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)
            if os.path.isfile(file_path):
                shutil.copy(file_path, target_dir)
                #file_names.append(filename)
                print(f"Archivo {filename} copiado a {target_dir}")

    except Exception as e:
        print(f"Error al copiar archivos: {str(e)}")
    
    #return '\n'.join(str(file) for file in file_names) 



# Definir el flujo
@flow(name = "backup flow")
def copy_files_flow():
    # Especificar las rutas de origen y destino
    source_directory = "C:\\Users\\kim_j\\OneDrive\\Escritorio\\CTF\\Origin"
    target_directory = "C:\\Users\\kim_j\\OneDrive\\Escritorio\\CTF\\Dest"
    
    # Llamar a la tarea de copiar archivos
    copy_files(source_directory, target_directory)


#copy_files_flow()
if __name__ == '__main__':
    copy_files_flow()
    
    
    
    
    #copy_files_flow.serve(name='copy-files-deployment')
import pandas as pd

def File_loader(path):
    #Funcion utilizada para probar la ruta del archivo provista
    loc = path

    try:
        data = pd.read_excel(loc)
    except FileNotFoundError:
        return "Error, nombre de archivo equivocado o archivo no encontrado en la ubicacion provista."
    except OSError:
        return "Error, ruta de archivo equivocada."
    except AssertionError:
        return "Error, ninguna ruta de archivo provista"
    except ValueError:
        return "Error, extension no reconocida"

    data = data.convert_dtypes()

    #Este resumen se imprime a la consola
    print("Resumen de la data proporcionada por el usario")
    print("----------------------------------------------")
    print(data)
    print("----------------------------------------------")

    return data


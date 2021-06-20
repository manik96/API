import pandas as pd

def File_loader(path):
    loc = path

    try:
        data = pd.read_excel(loc)
    except FileNotFoundError:
        return "Error, nombre de archivo equivocado o archivo no encontrado en la ubicacion provista."
    except OSError:
        return "Error, ruta de archivo equivocada."
    except AssertionError:
        return "Error, ninguna ruta de archivo provista"

    data = data.convert_dtypes()

    print("Resumen de la data proporcionada por el usario")
    print("----------------------------------------------")
    print(data)
    print("----------------------------------------------")

    return data

#data.to_excel("nuevo_datos.xlsx", sheet_name="datos", index=False)

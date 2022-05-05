import random
from re import A
import string
import sqlite3


def main():
   
    action = input("¿Qué desea hacer? Consultar/Generar/Modificar: ")

    if (action == "consultar" or action == "generar" or action == "modificar"):
        print("Se procede a realizar la acción seleccionada")
    else:
        print("Por favor, escriba en minúsculas la acción")
        action= input("consultar, generar o modificar: ")
        print("Se procede a realizar la acción seleccionada")

    if (action == "consultar"): consultar()
    if (action == "generar"): generar()
    if (action == "modificar"): modificar()    

def generar():
    
    def Caracts ():
        nums = string.digits
        letras = string.ascii_letters
        caract = string.punctuation

        return (nums+letras+caract)

    concat = Caracts()

    i = input("Longitud de la contraseña: ")

    contrasena = []

    while len(contrasena) < int(i):
        caracter = str(random.choice(concat))
        contrasena.append(caracter)
        if len(contrasena) > int(i): 
            print("Se ha producido un error")
            break
        continue

 
    StrContrasena="".join(contrasena)
    print("Su nueva contraseña es: ", StrContrasena)

    guardar =input("¿Desea guardarla en la base de datos? Y/N: ")

    if (guardar == "Y"):
        
        usuario = input ("¿A qué usuario pertenece esta contraseña?: ")
        plataforma = input ("¿A qué plataforma pertenece esta contraseña?: ")

        cur.executescript('''
            CREATE TABLE IF NOT EXISTS Contrasenas(
            plataforma TEXT,
            usuario TEXT,
            contrasena TEXT,
            aux int primary key
        )''')
        cur.execute('''INSERT INTO Contrasenas (plataforma, usuario, contrasena) 
        VALUES ( ?, ?, ? )''', ( plataforma, usuario, StrContrasena ) )
        conn.commit() 
    else:
        print("No se guardará en Base de Datos")   

def modificar():
   
    plataforma = input("Introduzca la PLATAFORMA de la que quiere modificar la contraseña: ")
    usuario = input("Introduzca el USUARIO para el que quiere cambiar la contraseña : ")
    contrasena_anti = input("Introduzca la contraseña antigua: ")    
    cur.execute('SELECT contrasena FROM Contrasenas WHERE usuario = ? and plataforma = ? ', (usuario, plataforma))
    contrasena_bbdd = cur.fetchone()[0]
    
    if (contrasena_anti != contrasena_bbdd): print("[ERROR]: La contraseña no coincide")
    else:
        contrasena_nueva = input("Introduzca la contraseña nueva: ")
        print("**** Esto puede llevar unos segundos ****")
        cur.execute('UPDATE Contrasenas set contrasena = ? WHERE usuario = ? and plataforma = ? ', (contrasena_nueva, usuario, plataforma))
        conn.commit()
        print("Se ha actualizado correctamente la contraseña")

def consultar():

    usuario = input("Introduzca el usuario que desea consultar: ")
    plataforma = input("Introduzca la plataforma de la que desea conocer la contraseña: ")
    
    cur.execute('SELECT contrasena FROM Contrasenas WHERE usuario = ? and plataforma = ? ', (usuario, plataforma))
    contrasena_bbdd = cur.fetchone()[0]

    print("La contraseña del usuario "+usuario + " para la plataforma "+plataforma+" es: "+contrasena_bbdd)


conn = sqlite3.connect('contrasenas.sqlite')
cur = conn.cursor()
main()






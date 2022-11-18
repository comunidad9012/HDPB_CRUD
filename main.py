from tkinter import *
from tkinter import ttk
from conexion import * #Importa la DB
#Ventana raiz
ventana=Tk()
#Indica Titulo y tamaño de la ventana
ventana.title("CRUD MySql Tkinter")
ventana.geometry("600x500")
#----------------------------------------------------
#VARIABLES
db=DataBase() #Instancia de la DB
modificar= False
dni=StringVar()
sexo=StringVar()
nombres=StringVar()
apellidos=StringVar()
def sele(event):
    id=tvEstudiantes.selection()[0]
    if int(id)>0:
        dni.set(tvEstudiantes.item(id, "values")[1])
        sexo.set(tvEstudiantes.item(id, "values")[2])
        nombres.set(tvEstudiantes.item(id, "values")[3])
        apellidos.set(tvEstudiantes.item(id, "values")[4])
#----------------------------------------------------
#frame o marco del formulario.
marco = LabelFrame(ventana,text="Formulario de gestion de estudiantes") #Indica el titulo del frame.
marco.place(x=50,y=50,width=500,height=400) #Indica ubicacion y tamaño del frane
#----------------------------------------------------
#Labels / Entries
                #Label-entry: DNI
lblDni=Label(marco, text="DNI").grid(column=0,row=0,padx=5,pady=5)
txtDni=Entry(marco, textvariable = dni)
txtDni.grid(column=1,row=0)
                #Label-entry: Sexo
lblSexo=Label(marco, text="Sexo").grid(column=0,row=1,padx=5,pady=5)
txtSexo=ttk.Combobox(marco, values=["M","F"], textvariable = sexo)
txtSexo.grid(column=1,row=1)
txtSexo.current(0)
                #Label-entry: Nombres
lblNombres=Label(marco, text="Nombres").grid(column=2,row=0,padx=5,pady=5)
txtombres=Entry(marco, textvariable = nombres)
txtombres.grid(column=3,row=0)
                #Label-entry: Apellidos
lblApellidos=Label(marco, text="Apellidos").grid(column=2,row=1,padx=5,pady=5)
txtApellidos=Entry(marco, textvariable = apellidos)
txtApellidos.grid(column=3,row=1)
                #Label: Mensajes de estado
lblMensaje=Label(marco,text="Esperando Accion",fg="green")
lblMensaje.grid(column=0,row=2,columnspan=4)
#----------------------------------------------------
#Tabla de estudiantes
tvEstudiantes=ttk.Treeview(marco, selectmode=NONE)
tvEstudiantes.grid(column=0,row=3,columnspan=4,padx=5)
tvEstudiantes["columns"]=("ID","DNI","Sexo","Nombres","Apellidos")
tvEstudiantes.column("#0",width=0,stretch=NO)
tvEstudiantes.column("ID",width=50,anchor=CENTER)
tvEstudiantes.column("DNI",width=50,anchor=CENTER)
tvEstudiantes.column("Sexo",width=50,anchor=CENTER)
tvEstudiantes.column("Nombres",width=100,anchor=CENTER)
tvEstudiantes.column("Apellidos",width=100,anchor=CENTER)
#Encabezados de columnas
tvEstudiantes.heading("#0",text="")
tvEstudiantes.heading("ID", text="ID",anchor=CENTER)
tvEstudiantes.heading("DNI", text="DNI",anchor=CENTER)
tvEstudiantes.heading("Sexo", text="Sexo",anchor=CENTER)
tvEstudiantes.heading("Nombres", text="Nombres",anchor=CENTER)
tvEstudiantes.heading("Apellidos", text="Apellidos",anchor=CENTER)
tvEstudiantes.bind("<<TreeviewSelect>>", sele)
#----------------------------------------------------
#Botones de accion
btnEliminar=Button(marco,text="Eliminar",command=lambda:eliminar())
btnEliminar.grid(column=1,row=4)

btnNuevo=Button(marco,text="Guardar",command=lambda:nuevo())
btnNuevo.grid(column=2,row=4)

btnModificar=Button(marco,text="Seleccionar",command=lambda:actualizar())
btnModificar.grid(column=3,row=4)
#----------------------------------------------------
#Funcionmes
                #ModificarFalse y modificarTrue se usan para manipular las acciones de Guardar. Seleccionar, Nuevo y modificar.
def modificarFalse():
    global modificar
    modificar = False
    tvEstudiantes.config(selectmode=NONE)
    btnNuevo.config(text="Guardar")
    btnModificar.config(text="Seleccionar")
    btnEliminar.config(state=DISABLED)
def modificarTrue():
    global modificar
    modificar = True
    tvEstudiantes.config(selectmode=BROWSE)
    btnNuevo.config(text="Nuevo")
    btnModificar.config(text="Modificar")
    btnEliminar.config(state=NORMAL)
                #Validacion de estado de Entries
def validar():
    return len(dni.get()) and len(nombres.get()) and  len(apellidos.get())
                #Limpia los Entries
def limpiar():
    dni.set("")
    nombres.set("")
    apellidos.set("")
                #
def vaciar_tabla():
    filas=tvEstudiantes.get_children() #Devuelve todas las filas
    for fila in filas:
        tvEstudiantes.delete(fila)
                #Muestra los datos ingresados en la db
def llenar_tabla():
    vaciar_tabla()
    sql="select * from estudiantes"
    db.cursor.execute(sql)
    filas=db.cursor.fetchall()
    for fila in filas:
        id = fila[0]
        tvEstudiantes.insert("", END, id, text=id, value=fila)
                #Elimina el registro seleccionado
def eliminar():
    id= tvEstudiantes.selection()[0]
    if int(id)>0:
        sql="delete from estudiantes where id ="+id
        db.cursor.execute(sql)
        db.connection.commit()
        tvEstudiantes.delete(id)
        lblMensaje.config(text="Se a eliminado el registro correctamente")
        limpiar()
    else:
        lblMensaje.config(text="Seleccione un registro para eliminar")
                #Agrega un nuevo registro a la tabla
def nuevo():
    if modificar==False:
        if validar():
            val=(dni.get(),sexo.get(),nombres.get(),apellidos.get())
            sql="insert into estudiantes (dni, sexo, nombres, apellidos) values(%s,%s,%s,%s)"
            db.cursor.execute(sql,val)
            db.connection.commit()
            lblMensaje.config(text="se ha guardado un registro correctamente",fg="green")
            llenar_tabla()
            limpiar()
        else:
            lblMensaje.config(text="los campos no deben estar vacios", fg="red")
    else:
        modificarFalse()
                #Modifica un registro de la tabla
def actualizar():
    if modificar == True:
        if validar():
            id =tvEstudiantes.selection()[0]
            val=(dni.get(),sexo.get(),nombres.get(),apellidos.get())
            sql="update estudiantes set dni=%s, sexo=%s, nombres=%s, apellidos=%s where id="+id
            db.cursor.execute(sql,val)
            db.connection.commit()
            lblMensaje.config(text="se ha actualizado un registro correctamente",fg="green")
            llenar_tabla()
            limpiar()
        else:
            lblMensaje.config(text="los campos no deben estar vacios", fg="red")
    else:
        modificarTrue()

llenar_tabla()
ventana.mainloop()
import csv
SUPERMERCADOS="supermercados.csv"
PRODUCTOS="productos.csv"
PRECIOS="precios.csv"
INFLACION_POR_SUPERMERCADO=1
INFLACION_POR_PRODUCTO=2
INFLACION_GENERAL_PROMEDIO=3
MEJOR_PRECIO_PARA_UN_PRODUCTO=4
SALIR=5
def mostrar_menu():
	'''Funcion que muestra el menu principal del programa'''
	print()
	print('        Menu principal\n''------------------------------\n')
	print('1. Inflación por supermercado\n2. Inflación por producto')
	print('3. Inflación general promedio\n4. Mejor precio para un producto\n5. Salir\n')
	
def abrir_archivo_precios(ruta):
	'''Funcion que recibe una ruta de un archivo de formato csv con 4 campos, lo lee y devuelve un diccionario
	con claves tuplas y valor lista de tuplas'''
	diccionario={}
	try:
		with open (ruta) as archivo:
			archivo_csv=csv.reader(archivo)
			referencias=next(archivo_csv)
			while True:
				try:
					for ind_sup,ind_prod,fecha,precio in archivo_csv:
						clave=(ind_sup,ind_prod)
						if clave in diccionario:
							diccionario[clave].append((fecha,precio))
							continue
						diccionario[clave]=[(fecha,precio)]
					return diccionario
				except:
					next(archivo_csv)
	except IOError:
		print("Se ha producido un error al buscar/leer el archivo ")
		
def abrir_archivo_super_produ(ruta):
	'''Funcion que recibe una ruta de un archivo de formato csv, lo lee y devuelve un diccionario donde la clave
	es el indice y el valor es el producto o supermercado asociado a ese indice.'''
	dicc_super={}
	dicc_produ={}
	try:
		with open (ruta) as archivo:
			archivo_csv=csv.reader(archivo)
			referencias=next(archivo_csv)
			while True:
				try:
					for num,item in archivo_csv:
						indice=int(num)
						if(ruta==SUPERMERCADOS):
							dicc_super[num]=item.lower()
						elif(ruta==PRODUCTOS):
							dicc_produ[num]=item.lower()
					if(ruta==SUPERMERCADOS):
						return dicc_super
					return dicc_produ			
				except:
					next(archivo_csv)
	except IOError:
		print("Se ha producido un error al buscar/leer el archivo ")
		
def pedir_eleccion(mensaje):
	'''Funcion que le pide al usuario que elija una opcion de las mostradas en pantalla y la devuelve'''
	opcion=input('Escoja {} que desee: '.format(mensaje))
	return opcion
	
def validar_eleccion(mensaje):
	'''Funcion que verifica la opcion ingresada y la devuelve en caso de ser valida, de lo contrario la vuelve a pedir'''
	opcion=pedir_eleccion(mensaje)
	while True:
		for numero in range(1,6):
			if opcion!=str(numero):
				continue
			return int(opcion)
		print('La opcion ingresada no es correcta')
		opcion=pedir_eleccion(mensaje)

def pedir_fecha(momento):
	'''Funcion que pide la fecha al usuario y la devuelve'''
	mes=input('Ingrese el numero del mes {} (ejemplo: 06):  '.format(momento))
	año=input('Ingrese el numero del año {} (ejemplo: 2015):  '.format(momento))
	return año,mes

def validar_fecha(dicci_prec,momento):
	'''Funcion que verifica que la fecha ingresada por el usuario sea valida y la devuelve, si no lo es vuelve a pedirla'''
	año,mes=pedir_fecha(momento)
	while True:
		if len(mes)==1:
			mes='0'+mes
		fecha=año+mes
		for elemento in range(12):
			if fecha!=dicci_prec[('1','1')][elemento][0]:
				continue
			return fecha
		print('El periodo escogido no es correcto, revise el formato o los datos (solo contemplado 2015/2016')
		año,mes=pedir_fecha(momento)
		
def pedir_producto():
	'''Funcion que le pide el nombre del producto al usuario y lo devuelve'''
	return input('Ingrese el nombre del producto: ').lower()
	
def validar_producto(produ):
	'''Funcion que recibe el diccionario de productos,crea una lista de los posibles productos que
	quiere el usuario y los devuelve, si no encuentra posibles productos vuelve a pedir alguna referencia'''
	lista_productos_posibles=[]
	producto=pedir_producto()
	while True:
		for x in range (1,len(produ)+1):
			try:
				if producto in produ[str(x)]:
						lista_productos_posibles.append(produ[str(x)])
			except:
				continue
		if lista_productos_posibles!=[]:
			return lista_productos_posibles
		print('No se encontró ningún producto con nombre {} '.format(producto))
		producto=pedir_producto()
		
def imprimir_productos_posibles(lista):
	'''Funcion que imprime en pantalla los productos que posiblemente quiere el usuario'''
	for x in range(len(lista)):
		print('{}. {}'.format(x+1,lista[x]))
	
def validar_eleccion_producto(productos,mensaje):
	'''Funcion que recibe una lista de productos posibles, le pide al usuario que elija el producto que
	desee, si la eleccion es correcta devuelve el indice que tiene el producto'''
	indice_producto=pedir_eleccion(mensaje)
	while True:
		for numero in range(1,len(productos)+1):
			if indice_producto!=str(numero):
				continue
			return indice_producto
		print('La opcion ingresada no es correcta')
		indice_producto=pedir_eleccion(mensaje)
		
def validar_periodo(dicci_prec):
	'''Funcion que pide dos fechas al usuario, verifica que no sean iguales y las devuelve'''
	while True:
		fecha_ini=validar_fecha(dicci_prec,"inicial")
		fecha_fin=validar_fecha(dicci_prec,"final")
		if fecha_ini>fecha_fin:
			fecha_ini,fecha_fin=fecha_fin,fecha_ini
			return fecha_ini,fecha_fin
		if fecha_ini==fecha_fin:
			print('Las fechas no pueden ser iguales\n')
			continue
		return fecha_ini,fecha_fin
		
def calcular_inflacion(precio_final,precio_inicial):
	'''Funcion que recibe un precio final y uno inicial, calcula la inflacion y la devuelve'''
	return 100*((precio_final-precio_inicial)/precio_inicial)
	
def imprimir_inflacion_por_supermercado(dicci_prec):
	'''Funcion que recibe el diccionario de productos creado e imprime 
	en pantalla la inflacion general de cada supermercado'''
	fecha_ini,fecha_fin=validar_periodo(dicci_prec)
	infla_sup1,infla_sup2,infla_sup3=calcular_inflacion_super(dicci_prec,fecha_ini,fecha_fin)
	print("La inflacion en el supermercado Coto en el periodo indicado fue: {:.3}%".format(infla_sup1))
	print("La inflacion en el supermercado Jumbo en el periodo indicado fue: {:.3}%".format(infla_sup2))
	print("La inflacion en el supermercado Carrefour en el periodo indicado fue: {:.3}%".format(infla_sup3))
	
def calcular_inflacion_super(dicci_prec,fecha_ini,fecha_fin):
	'''Funcion que recibe el diccionario de productos con sus precios en cada fecha en cada supermercado
	 y un periodo, calcula la inflacion de cada supermercado y la devuelve''' 
	suma_precio_ini_1=0
	suma_precio_fin_1=0
	suma_precio_ini_2=0
	suma_precio_fin_2=0
	suma_precio_ini_3=0
	suma_precio_fin_3=0
	for clave in dicci_prec:
		for x in range(len(dicci_prec[clave])):
			if dicci_prec[clave][x][0]==fecha_ini:
				if clave[0]=="1":
					suma_precio_ini_1+=float(dicci_prec[clave][x][1])
				elif clave[0]=="2":
					suma_precio_ini_2+=float(dicci_prec[clave][x][1])
				elif clave[0]=="3":
					suma_precio_ini_3+=float(dicci_prec[clave][x][1])
			elif dicci_prec[clave][x][0]==fecha_fin:
				if clave[0]=="1":
					suma_precio_fin_1+=float(dicci_prec[clave][x][1])
				elif clave[0]=="2":
					suma_precio_fin_2+=float(dicci_prec[clave][x][1])
				elif clave[0]=="3":
					suma_precio_fin_3+=float(dicci_prec[clave][x][1])
	inflacion_total_super_1=calcular_inflacion(suma_precio_fin_1,suma_precio_ini_1)
	inflacion_total_super_2=calcular_inflacion(suma_precio_fin_2,suma_precio_ini_2)
	inflacion_total_super_3=calcular_inflacion(suma_precio_fin_3,suma_precio_ini_3)
	return inflacion_total_super_1,inflacion_total_super_2,inflacion_total_super_3
	
def inflacion_por_producto(dicc_super,dicc_produ,dicci_prec):
	'''Funcion que recibe un diccionario de supermercados,uno de productos y otro de productos con precios en
	en cada fecha y en cada supermercado, calcula la inflacion para un producto pedido al usuario en determinado
	periodo y la imprime en pantalla.'''
	producto=elegir_producto_en_lista_posibles(dicc_super,dicc_produ)
	for valor in range(len(dicc_produ)):
		if (producto==dicc_produ[str(valor+1)]):
			indice_prod_dicc_produ=valor+1
			break
	fecha_ini,fecha_fin=validar_periodo(dicci_prec)
	for x in range(1,len(dicc_super)+1):
		precio_inicial,precio_final=precio_ini_fin(str(x),dicci_prec,indice_prod_dicc_produ,fecha_ini,fecha_fin)
		inflacion_sup=calcular_inflacion(precio_final,precio_inicial)
		print("La inflacion de {} en el supermercado {} fue: {:.3}%".format(producto,dicc_super[str(x)],inflacion_sup))
		
def precio_ini_fin(sup,dicci_prec,indice_prod_dicc_produ,fecha_ini,fecha_fin):
	'''Funcion que recibe el indice de un supermercado,la lista de productos con su precio en los
	determinados super y fechas,el indice de un producto y el periodo; y devuelve los precios, de ese 
	producto en el supermercado indicado, en el inicio del periodo y al final del periodo.''' 
	for clave in dicci_prec:
		if clave[0]==sup:
			if int(clave[1])==indice_prod_dicc_produ:
				for x in range(len(dicci_prec[clave])):
					if dicci_prec[clave][x][0]==fecha_ini:
						precio_ini_sup=float(dicci_prec[clave][x][1])
					elif dicci_prec[clave][x][0]==fecha_fin:
						precio_fin_sup=float(dicci_prec[clave][x][1])
	return precio_ini_sup,precio_fin_sup
	
def inflacion_general_promedio(dicc_super,dicc_produ,dicci_prec):
	'''Funcion que recibe un diccionario de supermercados, otro de productos y el de precios
	de productos segun el supermercado y fecha, calcula la inflacion general promedio y la imprime.'''
	fecha_ini,fecha_fin=validar_periodo(dicci_prec)
	suma_precio_ini=0
	suma_precio_fin=0
	for clave in dicci_prec:
		for x in range(len(dicci_prec[clave])):
			if dicci_prec[clave][x][0]==fecha_ini:
				suma_precio_ini+=float(dicci_prec[clave][x][1])
			elif dicci_prec[clave][x][0]==fecha_fin:
				suma_precio_fin+=float(dicci_prec[clave][x][1])
	infl_gral_promedio=calcular_inflacion(suma_precio_fin,suma_precio_ini)
	print("La inflacion general promedio de los tres sumermercados fue: {:.3}%".format(infl_gral_promedio))
	
def mejor_precio_para_un_producto(dicc_super,dicc_produ,dicci_prec):
	'''Funcion pide al usuario un producto y una fecha, se fija en el diccionario de precios 
	cual supermercado tiene ese producto mas barato en esa fecha y lo imprime en pantalla'''
	supermercado=0
	producto=elegir_producto_en_lista_posibles(dicc_super,dicc_produ)
	for i in range(len(dicc_produ)):
		if (producto==dicc_produ[str(i+1)]):
			indice_prod_dicc_produ=i
			break
	fecha=validar_fecha(dicci_prec,"")
	for clave in dicci_prec:
		if int(clave[1])==indice_prod_dicc_produ:
			for x in range(len(dicci_prec[clave])):
				if dicci_prec[clave][x][0]==fecha:
					if int(clave[0])==1:
						precio=float(dicci_prec[clave][x][1])
						supermercado=1
					elif int(clave[0])==2:
						precio=float(dicci_prec[clave][x][1])
						supermercado=2
					elif int(clave[0])==3:
						precio=float(dicci_prec[clave][x][1])
						supermercado=3
	if supermercado==1:
		print("El mejor precio de {} lo tiene el supermercado Coto a {}$".format(producto,precio))
	elif supermercado==2 :
		print("El mejor precio de {} lo tiene el supermercado Jumbo a {}$".format(producto,precio))
	elif supermercado==3 :
		print("El mejor precio de {} lo tiene el supermercado Carrefour a {}$".format(producto,precio))
	else:
		print("error")
		
def elegir_producto_en_lista_posibles(dicc_super,dicc_produ):
	'''Funcion que pide al usuario un producto, genera una lista con los productos posibles y le pregunta
	al usuario cual desea, verifica la eleccion y lo devuelve, en caso contrario vuelve a pedir'''
	lista_prod_posibles=validar_producto(dicc_produ)
	imprimir_productos_posibles(lista_prod_posibles)
	indice_prod_lista_posibles=validar_eleccion_producto(lista_prod_posibles,"el numero de producto")
	producto=lista_prod_posibles[int(indice_prod_lista_posibles)-1]
	while True:
		print("El producto elegido es: {}".format(producto))
		es_correcto=input("Es el producto deseado(s/n):").lower()
		if(es_correcto=="s"):
			return producto
		elif(es_correcto=="n"):
			indice_prod_lista_posibles=validar_eleccion_producto(lista_prod_posibles,"el numero de producto")
			producto=lista_prod_posibles[int(indice_prod_lista_posibles)-1]
		print('Responda por si o por no con s/n')
		
def ciclo_eleccion(dicc_super,dicc_produ,dicci_prec,opcion):
	'''Funcion que recibe la opcion que eligio el usuario y 
	entra a la opcion del menu que corresponda.'''
	if(opcion==INFLACION_POR_SUPERMERCADO):
			imprimir_inflacion_por_supermercado(dicci_prec)
	elif(opcion==INFLACION_POR_PRODUCTO):
			inflacion_por_producto(dicc_super,dicc_produ,dicci_prec)
	elif(opcion==INFLACION_GENERAL_PROMEDIO):
			inflacion_general_promedio(dicc_super,dicc_produ,dicci_prec)
	elif(opcion==MEJOR_PRECIO_PARA_UN_PRODUCTO):
			mejor_precio_para_un_producto(dicc_super,dicc_produ,dicci_prec)
	elif(opcion==SALIR):
		print("Usted ha salido del sistema de analisis de precios...\nGracias por su visita ;)")
		return 0
		
def main():
	'''Funcion principal del programa, crea los diccionarios correspondientes,
	muestra el menu principal y ejecuta la opcion que el usuario desee'''
	dicc_super=abrir_archivo_super_produ(SUPERMERCADOS)
	dicci_prec=abrir_archivo_precios(PRECIOS)
	dicc_produ=abrir_archivo_super_produ(PRODUCTOS)
	while True:
		mostrar_menu()
		opcion=validar_eleccion("la opcion")
		if ciclo_eleccion(dicc_super,dicc_produ,dicci_prec,opcion)==0:
			break
main()
	

	

		

		

			
		

		
		
	


		
	
	


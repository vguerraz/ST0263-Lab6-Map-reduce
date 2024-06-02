# ST0263-Lab6-Map/Reduce en Python con MRJOB

**Estudiante:** Valeria Guerra Zapata

## Despliegue de cluster EMR
Para crear el cluster EMR se usó AWS CLI por la consola AWS CLoud Shell se debe crear el key-pair y el bucket S3 con los siguientes comandos:

``` bash
#Crea el key-pair
aws ec2 create-key-pair --key-name lab-mapreduce --key-type rsa --key-format pem --query "KeyMaterial" --output text > lab-mapreduce.pem

#Crea el bucket S3
aws ec2 create-bucket --bucket map-reduce-vguerraz --region us-east-1
```

Estos comandos generarán la siguiente salida: 

![Captura de pantalla 2024-06-01 223502](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/bde89ad2-5c03-4be0-a1d5-774bc8ce1374)

Se evidencia en la consola de AWS la creación del bucket:

![Captura de pantalla 2024-06-01 223630](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/c0ab1e49-63db-4732-b877-3759a96643be)

Luego se crea el cluster EMR con el comando:

``` bash
aws emr create-cluster --release-label "emr-7.1.0" --name "vguerraz-lab-map" --applications Name=Spark Name=Hadoop Name=Pig Name=Hive --ec2-attributes KeyName=lab-mapreduce --instance-type m4.large --instance-count 3 --use-default-roles --no-auto-terminate --log-uri "s3://map-reduce-vguerraz/logs" 
```

Y obtendremos un resultado como el siguiente:

![Captura de pantalla 2024-06-01 223919](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/5e217965-651e-45a1-bcc9-5737aa970568)

También se debería entrar a la consola de AWS y buscar el servicio de EMR, donde se evidenciará el cluster recién creado, se deben esperar unos minutos para que esté disponible.

En este punto ya podemos conectarnos al nodo master del cluster, para esto hay que moverse en la terminal a la carpeta donde esté el key-pair, y ejecutar un comando como el siguiente:

``` bash
ssh -i lab-mapreduce.pem hadoop@ec2-###-###-###-###.compute-1.amazonaws.com
```

Una vez conectados al master, procedemos a instalar git y MRJob para clonar el repositorio de los datasets y la dependencia necesaria para trabajar Map/Reduce

``` bash
sudo apt-get update
sudo yum install git
sudo yum install python3-pip
sudo pip3 install mrjob
```

## Pruebas wordcount-local.py
Se hicieron pruebas del wordcount con el archivo data1.txt. Se utilizó el comando:

``` bash
#Desde la carpeta raíz se navega hasta la carpeta wordcount
cd st0263-20241/Laboratorio\N6-MapReduce/wordcount
python wordcount-local.py ./data1.txt
```

Y obtendremos el siguiente resultado en pantalla:

![Captura de pantalla 2024-06-01 230754](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/21f2a773-197d-485a-8241-68d9d2b1e0c4)

## Pruebas wordcount-mr.py
Se hicieron las pruebas tanto con el archivo data1.txt como con el dataset *gutenberg-small*. A continuación se mostrarán los comandos (ejecutados desde la carpeta wordcount) y sus respectivas salidas:

``` bash
 python wordcount-mr.py ./data1.txt
```

![Captura de pantalla 2024-06-01 230843](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/22cf6633-6390-40e8-9477-cee4e626df3c)

``` bash
 python wordcount-mr.py ../../datasets/gutenberg-small/*.txt
```

![Captura de pantalla 2024-06-01 230927](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/fbe4f869-3c34-4b41-a546-6ab1c355d20e)

## Pruebas wordcount-mr.py en Hadoop
En este paso, debemos llevar nuestros datasets a Hadoop, esto lo podemos lograr creando un directorio en Hadoop para almacenarlos, y luego copiar los datasets a dicho directorio:

``` bash
hdfs dfs -mkdir -p /user/hadoop/datasets/gutenberg-small/
hdfs dfs -copyFromLocal ../../datasets/gutenberg-small/*.txt /user/hadoop/datasets/gutenberg-small/
```

Una vez se han pasado los datasets a Hadoop, ejecutamos el comando:

``` bash
python wordcount-mr.py hdfs:///user/hadoop/datasets/gutenberg-small/*.txt -r hadoop --output-dir hdfs:///user/hadoop/output/Resul.txt -D mapred.reduce.tasks=10
```
![Captura de pantalla 2024-06-02 030706](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/ba4ae2e1-fefe-441f-a887-2711d2a04bac)

De ese modo, el resultado de la ejecución se almacenará en el archivo Resul.txt, cuyo contenido es:

![Captura de pantalla 2024-06-02 030740c](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/5c400a45-45ea-4518-8b6e-5f98d65e7bb3)
Donde los "part" se dividen las líneas del resultado.

## Reto de programación en Map/Reduce
Para resolver los retos planteados, primero se pasaron los datasets a Hadoop (creando su correspondiente carpeta), ejecutando el siguiente comando:

``` bash
# Se crea la carpeta en hdfs
hdfs dfs -mkdir -p /user/hadoop/datasets/otros/

# Estando en la carpeta wordcount, se ejecuta
hdfs dfs -copyFromLocal ../../datasets/otros/*.txt /user/hadoop/datasets/otros/
```

![Captura de pantalla 2024-06-02 001904](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/34ed7dd0-89d4-4730-ba06-1b7624e82eb0)


Una vez estén los dataset en hdfs, procedemos a ejecutar los programas creados para resolver los retos. Se encuentran en las carpetas [Acciones](/Acciones), [Empleados](/Empleados) y [Peliculas](/Peliculas).
A continuación se verán las evidencias (capturas de pantalla) de los ejercicios en ejecución. La primera imagen corresponde al comando ejecutado sin hdfs, la segunda ya será con Hadoop y hdfs y corresponderá al comando ejecutado y las primeras lineas de su salida (ya que es una salida muy extensa), y la tercera imagen correponde al final de su salida y el comando para visualizar el resultado.

### 1. Empleados y sectores. Reporte de la DIAN
#### Ejercicio A

Datos locales:

![Captura de pantalla 2024-06-02 000903](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/881423a5-b39c-45a8-a75f-ca387409e7a5)

Datos hdfs:

``` bash
python EmpleadosA.py hdfs:///user/hadoop/datasets/otros/dataempleados.txt -r hadoop --output-dir hdfs:///user/hadoop/output/EmpleadosResA2.txt -D mapred.reduce.tasks=10
```

![Captura de pantalla 2024-06-02 004122](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/3e6c2587-d7b0-4a70-b3ea-4cba8338e2bb)

``` bash
hdfs dfs -ls /user/hadoop/output/EmpleadosResA2.txt
```

![Captura de pantalla 2024-06-02 004312](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/48ba3df6-d93c-47b4-a1f1-2fc52c6a5394)

![Captura de pantalla 2024-06-02 004552](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/0a6f0d00-86b9-4ccd-9802-edb64dcec931)


#### Ejercicio B

Datos locales:

![Captura de pantalla 2024-06-02 001038](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/99f37778-433a-4937-8be6-d23826515c8b)

Datos hdfs:

``` bash
python EmpleadosB.py hdfs:///user/hadoop/datasets/otros/dataempleados.txt -r hadoop --output-dir hdfs:///user/hadoop/output/EmpleadosResB.txt -D mapred.reduce.tasks=10
```

![Captura de pantalla 2024-06-02 005114](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/86bbd43f-7f72-4b18-9e47-e5e2e3dd19ce)

``` bash
hdfs dfs -ls /user/hadoop/output/EmpleadosResB.txt
```

![Captura de pantalla 2024-06-02 010731](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/5a7bb52e-9998-41de-b680-66650eb52009)


#### Ejercicio C

Datos locales:

![Captura de pantalla 2024-06-02 001102](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/dc2828e6-e3c8-40e8-9be4-26154467037b)

Datos hdfs:

``` bash
python EmpleadosC.py hdfs:///user/hadoop/datasets/otros/dataempleados.txt -r hadoop --output-dir hdfs:///user/hadoop/output/EmpleadosResC.txt -D mapred.reduce.tasks=10
```

![Captura de pantalla 2024-06-02 011026](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/afa7b450-f94f-4c8a-8523-869e744bc016)

``` bash
hdfs dfs -ls /user/hadoop/output/EmpleadosResC.txt
```

![Captura de pantalla 2024-06-02 011054](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/518b60cb-3b43-4e5a-8220-df94017cade8)


### 2. Acciones de bolsa
#### Ejercicio A

Datos locales:

![Captura de pantalla 2024-06-02 001141](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/b0cf0cd0-d370-4093-a3b3-42d8dcef35fe)

Datos hdfs:

``` bash
python AccionesA.py hdfs:///user/hadoop/datasets/otros/dataempresas.txt -r hadoop --output-dir hdfs:///user/hadoop/output/AccionesResA.txt -D mapred.reduce.tasks=10
```

![Captura de pantalla 2024-06-02 011319](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/f71ddfd4-4a1d-4fb6-9e4b-6b5fa9f97860)

``` bash
hdfs dfs -ls /user/hadoop/output/AccionesResA.txt
```

![Captura de pantalla 2024-06-02 011503](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/7caaefb8-313f-4a20-95ec-8a2aa6ec7054)


#### Ejercicio B

Datos locales:

![Captura de pantalla 2024-06-02 001206](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/cf38bab8-e5ec-4cee-8eb3-16fe5c9dd90e)

Datos hdfs:

``` bash
python AccionesB.py hdfs:///user/hadoop/datasets/otros/dataempresas.txt -r hadoop --output-dir hdfs:///user/hadoop/output/AccionesResB.txt -D mapred.reduce.tasks=10
```

![Captura de pantalla 2024-06-02 011715](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/a0308ece-2e69-4584-abc9-72a97dfc8554)

``` bash
hdfs dfs -ls /user/hadoop/output/AccionesResB.txt
```

![Captura de pantalla 2024-06-02 011745](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/951e8303-85ab-4fb2-b595-f9681f1312e9)


#### Ejercicio C

Datos locales:

![Captura de pantalla 2024-06-02 001240](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/f0cb3e75-5727-400b-91d5-d15f88ea910a)

Datos hdfs:

``` bash
python AccionesC.py hdfs:///user/hadoop/datasets/otros/dataempresas.txt -r hadoop --output-dir hdfs:///user/hadoop/output/AccionesResC.txt -D mapred.reduce.tasks=10
```

![Captura de pantalla 2024-06-02 014134](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/27c69ba3-3b96-4f5b-a8e2-903c07042ab0)

``` bash
hdfs dfs -ls /user/hadoop/output/AccionesResC.txt
```

![Captura de pantalla 2024-06-02 014602](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/27192369-5115-4301-9915-c7d8e5cea666)


### 3. Peliculas
#### Ejercicio A

Datos locales:

![Captura de pantalla 2024-06-02 001337](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/bc2b15c7-ef90-4d75-9bee-5564da36b66b)

Datos hdfs:

``` bash
python PeliculasA.py hdfs:///user/hadoop/datasets/otros/datapeliculas.txt -r hadoop --output-dir hdfs:///user/hadoop/output/PeliculasResA.txt -D mapred.reduce.tasks=10
```

![Captura de pantalla 2024-06-02 014832](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/c95402bd-70b4-47ef-9d5b-d2d0e4ac85e4)

``` bash
hdfs dfs -ls /user/hadoop/output/PeliculasResA.txt
```

![Captura de pantalla 2024-06-02 014907](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/0b8cab79-5aa9-4386-85da-231d24d381ac)


#### Ejercicios B y C

Datos locales:

![Captura de pantalla 2024-06-02 001414](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/9f56bb72-5ebd-4309-bb2c-7e3355cc6627)

Datos hdfs:

``` bash
python PeliculasBC.py hdfs:///user/hadoop/datasets/otros/datapeliculas.txt -r hadoop --output-dir hdfs:///user/hadoop/output/PeliculasResBC.txt -D mapred.reduce.tasks=10
```

![Captura de pantalla 2024-06-02 015137](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/74276474-c104-4a07-bd70-84b622f954d8)

``` bash
hdfs dfs -ls /user/hadoop/output/PeliculasResBC.txt
```

![Captura de pantalla 2024-06-02 015333](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/1b54e9c3-5269-45ee-8c95-d9aef4776dd2)


#### Ejercicio D

Datos locales:

![Captura de pantalla 2024-06-02 001438](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/91dcba26-5784-4555-a4be-f1e7344df0d0)

Datos hdfs:

``` bash
python PeliculasD.py hdfs:///user/hadoop/datasets/otros/datapeliculas.txt -r hadoop --output-dir hdfs:///user/hadoop/output/PeliculasResD.txt -D mapred.reduce.tasks=10
```

![Captura de pantalla 2024-06-02 015541](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/2b124acb-7089-458e-a55a-7934b9dd3fd7)

``` bash
hdfs dfs -ls /user/hadoop/output/PeliculasResD.txt
```

![Captura de pantalla 2024-06-02 015616](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/77fac36b-9ddb-4c13-b643-f6b5eeb0aab0)


#### Ejercicios E y F

Datos locales:

![Captura de pantalla 2024-06-02 001503](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/53d62fca-98c9-4019-8de0-26a3b9f71fa4)

Datos hdfs:

``` bash
python PeliculasEF.py hdfs:///user/hadoop/datasets/otros/datapeliculas.txt -r hadoop --output-dir hdfs:///user/hadoop/output/PeliculasResEF.txt -D mapred.reduce.tasks=10
```

![Captura de pantalla 2024-06-02 015859](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/e9619017-7ed7-4775-8615-c0ce2d4efb04)

``` bash
hdfs dfs -ls /user/hadoop/output/PeliculasResEF.txt
```

![Captura de pantalla 2024-06-02 020006](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/3c729018-51f0-4ff6-8483-a9ca3e0dab06)


#### Ejercicio G

Datos locales:

![Captura de pantalla 2024-06-02 001529](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/356dcdb4-64d0-4504-978b-0ad418ebc46d)

Datos hdfs:

``` bash
python PeliculasG.py hdfs:///user/hadoop/datasets/otros/datapeliculas.txt -r hadoop --output-dir hdfs:///user/hadoop/output/PeliculasResG.txt -D mapred.reduce.tasks=10
```

![Captura de pantalla 2024-06-02 015901](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/6f13a2de-ba3a-4a6e-8308-eaff10882fe9)

``` bash
hdfs dfs -ls /user/hadoop/output/PeliculasResG.txt
```

![Captura de pantalla 2024-06-02 020404](https://github.com/vguerraz/ST0263-Lab6-Map-reduce/assets/84991036/7164cfa6-681d-469b-a1df-f21e635cd822)

## Video sustentación
[Video](https://youtu.be/Ke6ODP3T38o)

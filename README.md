# SimanJob

- El proyecto consiste en un ETL de los datos de la tienda siman (https://gt.siman.com/).

- Para ejecutar el proyecto debes tener instalada la libreria scrapy de python, selenium y talend open studio, estos son los pasos para ejecutar el proyecto:

  1. Ejecutar: scrapy crawl siman (Tomar en consideración que el scraper demora aproximadamente 24 horas en terminar)
  2. Una vez finalizado el scraper, ejecutar el job de talend abriéndolo desde la herramienta (cambiar variables de contexto)
  3. Por último para ejecutar la parte de pyspark, se debe exportar el notebook hacía zeppelin u otra herramienta deseada para poder correr la limpieza.
  
- Este proyecto fue realizado utilizando el servicio de hortonworks de cloudera. Abajo se dejará una breve explicación del proyecto:

  - Primeramente se creo el scraper para la tienda siman utilizando selenium y el framework de python scrapy:
  
    ![Screenshot from 2023-03-28 02-43-31](https://user-images.githubusercontent.com/61527863/235328686-586a0104-1de0-40cc-9407-c25e9a9128ae.png)
    
  - La extracción de datos y subida a hdfs se ejecutó desde Talend Open Studio, un par de screenshots de los jobs ejecutándose:
  
    ![Screenshot from 2023-04-03 22-15-22](https://user-images.githubusercontent.com/61527863/235328700-e66b153e-5045-4993-b53b-9e988a5d602a.png)
    
    ![Screenshot from 2023-04-06 13-30-38](https://user-images.githubusercontent.com/61527863/235328717-e271e2ba-a5b7-4c11-8846-33bb4aee46eb.png)

    ![Screenshot from 2023-04-07 21-21-57](https://user-images.githubusercontent.com/61527863/235328729-fa6f7378-f1be-456f-ad97-b2716eb0bb04.png)

    ![Screenshot from 2023-04-07 21-54-35](https://user-images.githubusercontent.com/61527863/235328736-d62b96d5-3038-487e-b854-77c9b9b76e3f.png)

  - Una vez subida la data a hdfs, se puede visualizar utilizando hdfs o ambari, el archivo se ve de la siguiente manera:
  
    ![Screenshot from 2023-04-07 21-55-43](https://user-images.githubusercontent.com/61527863/235328777-a9c21924-030b-43fc-ab89-6e718f7ac71a.png)
    
  - Estos son los datos que contiene en el csv:
  
    ![Screenshot from 2023-04-06 13-30-31](https://user-images.githubusercontent.com/61527863/235328788-f9d1f50c-0acd-4fac-a9be-88b9b7c541c4.png)

  - Para el proceso de limpieza de datos se utilizo pyspark desde apache zeppelin para poder trabajar con los datos crudos extraidos de la web de siman.
  
    ![Screenshot from 2023-04-07 22-19-27](https://user-images.githubusercontent.com/61527863/235328822-3bb22b86-d3b3-4ebf-976b-cddb33967dae.png)
    
    ![Screenshot from 2023-04-08 13-38-05](https://user-images.githubusercontent.com/61527863/235328823-1fdb57f4-fa80-498f-a32e-fb37bf1a83f7.png)
    
    ![Screenshot from 2023-04-08 14-59-27](https://user-images.githubusercontent.com/61527863/235328825-22cbd863-90c6-4223-b8ea-ecf1b96949d6.png)
    
    ![Screenshot from 2023-04-08 14-59-38](https://user-images.githubusercontent.com/61527863/235328826-2f07ff53-3e78-48ae-b0de-97f06151d6fb.png)
    
  - Una vez limpios los datos de siman, se procedió a almacenarlos en hive.
    
![Screenshot from 2023-04-08 15-58-02](https://user-images.githubusercontent.com/61527863/235328902-74275c79-9cee-4df4-a86f-2bdf04dd0a55.png)

![Screenshot from 2023-04-08 15-56-02](https://user-images.githubusercontent.com/61527863/235328904-06e868e6-e766-474b-acf9-d19193f8502c.png)

  - Las visualizaciones fueron hechas utilizando tableau. Aquí hay unos screenshots de ejemplo:
  
  ![Screenshot from 2023-05-01 18-27-43](https://user-images.githubusercontent.com/61527863/235554704-26ba30c8-db15-4d17-992b-bd1934253a80.png)

![Screenshot from 2023-05-01 18-27-58](https://user-images.githubusercontent.com/61527863/235554734-dce3f890-61eb-40e3-a82e-daad9d228228.png)

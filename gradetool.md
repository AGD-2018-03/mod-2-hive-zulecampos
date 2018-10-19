# Instrucciones para la evaluación automática del notebook

Para realizar la evaluación automática del notebook usando `gradetol`:

* Salve el notebook que desea evaluar.
* Abra un Terminal.
* Verifique que está en la misma carpeta que contiene el notebook.
* Verifique que existe un archivo con el mismo nombre del notebook,
  pero con extensión `.json`.
* Ejecute el siguiente comando, cambiando `<<notebook>>` por el
  nombre del notebook que desea evaluar:

      ./gradetool <<notebook>>.ipynb

* Para las evaluaciones, suba el
  notebook al correspondiente repositorio de GitHub.

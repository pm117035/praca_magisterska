# Databricks notebook source
# MAGIC %md
# MAGIC Wyświetlenie dostępnych plików znajdujących się na HDFS (DBFS):

# COMMAND ----------

# MAGIC %fs
# MAGIC ls /FileStore/tables

# COMMAND ----------

# MAGIC %md
# MAGIC Załadowanie danych do ramki danych o nazwie 'd1':

# COMMAND ----------

d1 = spark.read\
       .format("csv")\
       .options(
          inferSchema="false", 
          header="true", 
          delimiter=";")\
       .load("/FileStore/tables/Dane.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC Wyświetlenie danych znajdujących się w 'd1':

# COMMAND ----------

display(d1)

# COMMAND ----------

# MAGIC %md
# MAGIC Zaimportowanie paczki z funkcjami:

# COMMAND ----------

import pyspark.sql.functions as f

# COMMAND ----------

# MAGIC %md
# MAGIC Pogrupowanie danych po zmiennej 'Dzien' wraz z liczbą pomiarów dla danej grupy dla ramki danych 'd1':

# COMMAND ----------

d1.groupBy("Dzien").count().display()

# COMMAND ----------

# MAGIC %md
# MAGIC Usunięcie rekordów, w któych wartość temperatury wynosiła ponad 10°C, w celu dokładniejszej analizy:

# COMMAND ----------

d2 = d1.filter("Temperatura < 10")

# COMMAND ----------

# MAGIC %md
# MAGIC Wyświetlenie danych znajdujących się w 'd2':

# COMMAND ----------

d2.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Pogrupowanie danych po zmiennej 'Dzien' wraz z liczbą pomiarów dla danej grupy dla ramki danych 'd2':

# COMMAND ----------

d2.groupBy("Dzien").count().display()

# COMMAND ----------

# MAGIC %md
# MAGIC Wyświetlenie temperatury minimalnej, maksymalnej oraz średniej (zaokrąglonej do 2 miejsc po przecinku) dla pogrupowanych danych po zmiennej 'Dzien' dla ramki danych 'd2':

# COMMAND ----------

d2.groupBy('Dzien').agg(f.min('Temperatura').alias("Min T"), f.max('Temperatura').alias("MAX T"), f.round(f.avg('Temperatura'),2).alias("AVG T")).display()

# COMMAND ----------

# MAGIC %md
# MAGIC Stworzenie tabeli tymczasowej o nazwie 'd2sql' na podstawie ramki danych 'd2':

# COMMAND ----------

d2.createOrReplaceTempView("d2sql")

# COMMAND ----------

# MAGIC %md
# MAGIC Wypisanie dnia, minimalnej, maksymalnej oraz oraz średniej (zaokrąglonej do 2 miejsc po przecinku) dla pogrupowanych danych po zmiennej 'Dzien' dla tabeli 'd2sql' w języku SQL:

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT Dzien, MIN(Temperatura) as MIN_T, MAX(Temperatura) as MAX_T, ROUND(AVG(Temperatura),2) as AVG_T
# MAGIC FROM d2sql
# MAGIC GROUP BY Dzien

# COMMAND ----------

# MAGIC %md
# MAGIC Pogrupowanie danych po zmiennej 'Godzina' wraz z liczbą pomiarów dla danej grupy dla ramki danych 'd2':

# COMMAND ----------

d2.groupBy("Godzina").count().display()

# COMMAND ----------

# MAGIC %md
# MAGIC Wyświetlenie temperatury minimalnej, maksymalnej oraz średniej (zaokrąglonej do 2 miejsc po przecinku) dla pogrupowanych danych po zmiennej 'Godzina' dla ramki danych 'd2':

# COMMAND ----------

d2.groupBy("Godzina").agg(f.min("Temperatura").alias("MIN T"), f.max("Temperatura").alias("MAX T"), f.round(f.avg("Temperatura"),2).alias("AVG T")).display()

# COMMAND ----------

# MAGIC %md
# MAGIC Wypisanie godziny, minimalnej, maksymalnej oraz oraz średniej (zaokrąglonej do 2 miejsc po przecinku) dla pogrupowanych danych po zmiennej 'Godzina' dla tabeli 'd2sql' w języku SQL:

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT Godzina, MIN(Temperatura) as MIN_T, MAX(Temperatura) as MAX_T, ROUND(AVG(Temperatura),2) as AVG_T
# MAGIC FROM d2sql
# MAGIC GROUP BY Godzina

# COMMAND ----------

# MAGIC %md
# MAGIC Pogrupowanie danych w przedziały po jednej godzinie (24 przedziałów) i zapisanie ich do ramki danych 'd3':

# COMMAND ----------

d3 = d2.withColumn("Godziny_po_1", f.when((d2.Godzina >= "00:00") & (d2.Godzina < "01:00"),"00:00-01:00").when((d2.Godzina >= "01:00") & (d2.Godzina < "02:00"),"01:00-02:00").when((d2.Godzina >= "02:00") & (d2.Godzina < "03:00"),"02:00-03:00").when((d2.Godzina >= "03:00") & (d2.Godzina < "04:00"),"03:00-04:00").when((d2.Godzina >= "04:00") & (d2.Godzina < "05:00"),"04:00-05:00").when((d2.Godzina >= "05:00") & (d2.Godzina < "06:00"),"05:00-06:00").when((d2.Godzina >= "06:00") & (d2.Godzina < "07:00"),"06:00-07:00").when((d2.Godzina >= "07:00") & (d2.Godzina < "08:00"),"07:00-08:00").when((d2.Godzina >= "08:00") & (d2.Godzina < "09:00"),"08:00-09:00").when((d2.Godzina >= "09:00") & (d2.Godzina < "10:00"),"09:00-10:00").when((d2.Godzina >= "10:00") & (d2.Godzina < "11:00"),"10:00-11:00").when((d2.Godzina >= "11:00") & (d2.Godzina < "12:00"),"11:00-12:00").when((d2.Godzina >= "12:00") & (d2.Godzina < "13:00"),"12:00-13:00").when((d2.Godzina >= "13:00") & (d2.Godzina < "14:00"),"13:00-14:00").when((d2.Godzina >= "14:00") & (d2.Godzina < "15:00"),"14:00-15:00").when((d2.Godzina >= "15:00") & (d2.Godzina < "16:00"),"15:00-16:00").when((d2.Godzina >= "16:00") & (d2.Godzina < "17:00"),"16:00-17:00").when((d2.Godzina >= "17:00") & (d2.Godzina < "18:00"),"17:00-18:00").when((d2.Godzina >= "18:00") & (d2.Godzina < "19:00"),"18:00-19:00").when((d2.Godzina >= "19:00") & (d2.Godzina < "20:00"),"19:00-20:00").when((d2.Godzina >= "20:00") & (d2.Godzina < "21:00"),"20:00-21:00").when((d2.Godzina >= "21:00") & (d2.Godzina < "22:00"),"21:00-22:00").when((d2.Godzina >= "22:00") & (d2.Godzina < "23:00"),"22:00-23:00").otherwise("23:00-00:00"))

# COMMAND ----------

# MAGIC %md
# MAGIC Pogrupowanie danych po zmiennej 'Godziny_po_1' wraz z liczbą pomiarów dla danej grupy dla ramki danych 'd3', posortowanych rosnąco:

# COMMAND ----------

d3.groupBy("Godziny_po_1").count().sort("Godziny_po_1").display()

# COMMAND ----------

# MAGIC %md
# MAGIC Wyświetlenie temperatury minimalnej, maksymalnej oraz średniej (zaokrąglonej do 2 miejsc po przecinku) dla pogrupowanych danych po zmiennej 'Godziny_po_1' dla ramki danych 'd3':

# COMMAND ----------

d3.groupBy("Godziny_po_1").agg(f.min("Temperatura").alias("MIN T"), f.max("Temperatura").alias("MAX T"), f.round(f.avg("Temperatura"),2).alias("AVG T")).display()

# COMMAND ----------

# MAGIC %md
# MAGIC Pogrupowanie danych w przedziały po sześć godzin (4 przedziały) i zapisanie ich do ramki danych 'd4':

# COMMAND ----------

d4 = d2.withColumn("Godziny_po_6", f.when((d2.Godzina >= "04:00") & (d2.Godzina < "10:00"),"04:00-10:00").when((d2.Godzina >= "10:00") & (d2.Godzina < "16:00"),"10:00-16:00").when((d2.Godzina >= "16:00") & (d2.Godzina < "22:00"),"16:00-22:00").otherwise("22:00-04:00"))

# COMMAND ----------

# MAGIC %md
# MAGIC Pogrupowanie danych po zmiennej 'Godziny_po_6' wraz z liczbą pomiarów dla danej grupy dla ramki danych 'd4', posortowanych rosnąco:

# COMMAND ----------

d4.groupBy("Godziny_po_6").count().sort("Godziny_po_6").display()

# COMMAND ----------

# MAGIC %md
# MAGIC Wyświetlenie temperatury minimalnej, maksymalnej oraz średniej (zaokrąglonej do 2 miejsc po przecinku) dla pogrupowanych danych po zmiennej 'Godziny_po_6' dla ramki danych 'd4':

# COMMAND ----------

d4.groupBy("Godziny_po_6").agg(f.min("Temperatura").alias("MIN T"), f.max("Temperatura").alias("MAX T"), f.round(f.avg("Temperatura"),2).alias("AVG T")).display()

# COMMAND ----------

# MAGIC %md
# MAGIC Pogrupowanie danych w przedziały po osiem godzin (3 przedziały) i zapisanie ich do ramki danych 'd5':

# COMMAND ----------

d5 = d2.withColumn("Godziny_po_8", f.when((d2.Godzina >= "06:00") & (d2.Godzina < "14:00"),"06:00-14:00").when((d2.Godzina >= "14:00") & (d2.Godzina < "22:00"),"14:00-22:00").otherwise("22:00-06:00"))

# COMMAND ----------

# MAGIC %md
# MAGIC Pogrupowanie danych po zmiennej 'Godziny_po_8' wraz z liczbą pomiarów dla danej grupy dla ramki danych 'd5', posortowanych rosnąco:

# COMMAND ----------

d5.groupBy("Godziny_po_8").count().sort("Godziny_po_8").display()

# COMMAND ----------

# MAGIC %md
# MAGIC Wyświetlenie temperatury minimalnej, maksymalnej oraz średniej (zaokrąglonej do 2 miejsc po przecinku) dla pogrupowanych danych po zmiennej 'Godziny_po_8' dla ramki danych 'd5':

# COMMAND ----------

d5.groupBy("Godziny_po_8").agg(f.min("Temperatura").alias("MIN T"), f.max("Temperatura").alias("MAX T"), f.round(f.avg("Temperatura"),2).alias("AVG T")).display()

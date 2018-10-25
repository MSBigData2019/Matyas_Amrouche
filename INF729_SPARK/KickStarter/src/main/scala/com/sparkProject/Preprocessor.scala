package com.sparkProject

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.udf

object Preprocessor {

  def main(args: Array[String]): Unit = {

    // Des réglages optionels du job spark. Les réglages par défaut fonctionnent très bien pour ce TP
    // on vous donne un exemple de setting quand même
    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12"
    ))

    // Initialisation de la SparkSession qui est le point d'entrée vers Spark SQL (donne accès aux dataframes, aux RDD,
    // création de tables temporaires, etc et donc aux mécanismes de distribution des calculs.)
    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP_spark")
      .getOrCreate()


    /*******************************************************************************
      *
      *       TP 2
      *
      *       - Charger un fichier csv dans un dataFrame
      *       - Pre-processing: cleaning, filters, feature engineering => filter, select, drop, na.fill, join, udf, distinct, count, describe, collect
      *       - Sauver le dataframe au format parquet
      *
      *       if problems with unimported modules => sbt plugins update
      *
      ********************************************************************************/

//    println("hello world ! from Preprocessor")


    // Load the csv file
    val df = spark.read
      .format("csv")
      .option("header", "true") //reading the headers
      .load("/Users/matyasamrouche/Downloads/train_clean.csv")

    // Number of lines
    val nbLines = df.count()

    // Number of columns
    val nbColumns = df.columns.size

    // Show the schema of DF (column : type)
    df.printSchema()

    // Cast to Int proper columns
    val newDF = df.withColumn("goal", df("goal").cast("Int"))
      .withColumn("backers_count", df("backers_count").cast("Int"))
      .withColumn("deadline", df("deadline").cast("Int"))
      .withColumn("state_changed_at", df("state_changed_at").cast("Int"))
      .withColumn("created_at", df("created_at").cast("Int"))
      .withColumn("launched_at", df("launched_at").cast("Int"))
      .withColumn("final_status", df("final_status").cast("Int"))

    newDF.printSchema()

    // Show statistiques sur les colonnes sélectionnées
    newDF.select("goal","backers_count", "final_status").describe().show()

    // drop column
    val df2 =  newDF.drop("disable_communication")


    def udfCountry = udf{(country: String, currency: String) =>
      if (country == "False")
        currency
      else
        country //: ((String, String) => String)  pour éventuellement spécifier le type
    }

    def udfCurrency = udf{(currency: String) =>
      if ( currency != null && currency.length != 3 )
        null
      else
        currency //: ((String, String) => String)  pour éventuellement spécifier le type
    }


    val dfCountry = df2.withColumn("country2", udfCountry($"country", $"currency"))
      .withColumn("currency2", udfCurrency($"currency"))
      .drop("country", "currency")

  }

}

package com.sparkProject

import org.apache.spark.SparkConf
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.ml.feature._
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.evaluation.{MulticlassClassificationEvaluator, RegressionEvaluator}
import org.apache.spark.ml.tuning.{ParamGridBuilder, TrainValidationSplit}

object Trainer {

  def main(args: Array[String]): Unit = {

    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12",
      "spark.driver.maxResultSize" -> "2g"
    ))

    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP_spark")
      .getOrCreate()


    /*******************************************************************************
      *
      *       TP 3
      *
      *       - lire le fichier sauvegarder précédemment
      *       - construire les Stages du pipeline, puis les assembler
      *       - trouver les meilleurs hyperparamètres pour l'entraînement du pipeline avec une grid-search
      *       - Sauvegarder le pipeline entraîné
      *
      *       if problems with unimported modules => sbt plugins update
      *
      ********************************************************************************/

    //println("hello world ! from Trainer")

    /**
      * 1) Chargement du dataset
      *
      */
    val df = spark.read.parquet("/Users/matyasamrouche/Downloads/prepared_trainingset")
    //parquetFileDF.show(10)


    /**
      * 2) Numérisation des données textuelles
      *
      */

    // Split du texte en tokens (en mots)
    val tokenizer = new RegexTokenizer()
      .setPattern("\\W+")
      .setGaps(true)
      .setInputCol("text")
      .setOutputCol("tokens")

    // Filtre les tokens ayant peu d'importance (mots de liaison...)
    val remover = new StopWordsRemover()
      .setInputCol("tokens")
      .setOutputCol("filtered")

    // TF = Term Frequency -> on wordcount les mots on transforme nos documents en vecteurs de mots
    val count_vectorizer = new CountVectorizer()
      .setInputCol("filtered")
      .setOutputCol("vectorized_texts")
      //.setMinDF(2)
      //.setVocabSize(3)


    // IDF = Inverse Document Frequency -> si le mot est présent dans plusieurs documents alors il perd de l'importance
    // i.e le mot n'est pas propre à l'identification du "sujet" du document
    val tfidf = new IDF().setInputCol(count_vectorizer.getOutputCol).setOutputCol("tfidf")


    /**
      * 3) Numérisation des données catégorielles
      *
      */

    // Transforme un string (ici un pays 'USA') en indice numérique
    // Les indices sont choisies en fonction de la fréquence décroissante du string dans la colonne
    val country_indexer = new StringIndexer()
      .setInputCol("country2")
      .setOutputCol("country_indexed")

    // Idem pour currency
    val currency_indexer = new StringIndexer()
      .setInputCol("currency2")
      .setOutputCol("currency_indexed")

    // A la différence du StringIndexer le one-hot encoding créer une colonne de booléen pour chaque label de la colonne à numériser
    // Cela permet de rester cohérent (index1>index2 -> $>€ : pas de sens) en particulier pour les arbres de décision
    val hot_encoder_country = new OneHotEncoder()
      .setInputCol("country_indexed")
      .setOutputCol("country_onehot")

    val hot_encoder_currency = new OneHotEncoder()
      .setInputCol("currency_indexed")
      .setOutputCol("currency_onehot")

    /**
      * 4) Préparation des données pour Spark.ml et création de la Pipeline
      *
      */

    // Assemble les colonnes en une colonne de vecteurs contenant les valeurs des colonnes précédentes
    val assembler = new VectorAssembler()
      .setInputCols(Array("tfidf", "days_campaign", "hours_prepa", "goal", "country_onehot", "currency_onehot"))
      .setOutputCol("features")

    // Modèle de Régression Logistiqe utilisé
    val lr = new LogisticRegression()
      .setElasticNetParam(0.0)
      .setFitIntercept(true)
      .setFeaturesCol("features")
      .setLabelCol("final_status")
      .setStandardization(true)
      .setPredictionCol("predictions")
      .setRawPredictionCol("raw_predictions")
      .setThresholds(Array(0.7, 0.3))
      .setTol(1.0e-6)
      .setMaxIter(300)

    // Application de notre pipeline
    val pipeline = new Pipeline()
      .setStages(Array(tokenizer, remover, count_vectorizer, tfidf, country_indexer, currency_indexer
        , hot_encoder_country, hot_encoder_currency, assembler, lr))

    /**
      * 5) Entraînement et tuning du modèle
      *
      */

    // Train = 90% & Test = 10%
    val Array(training, test) = df.randomSplit(Array[Double](0.9, 0.1), 18)

    // Trouvons les Hyper-paramètres optimals avec grid-search
    // Ici les hyper-paramètres sont :
    // minDF = permet de prendre en compte les mots apparaissant dans au moins minDF documents
    // regParam = paramètre de régularisation pour la régression logistique
    val paramGrid = new ParamGridBuilder()
      .addGrid(count_vectorizer.minDF,  Array(55.0, 75.0, 95.0))
      .addGrid(lr.regParam, Array(10e-8, 10e-6, 10e-4, 10e-2))
      .build()

    //
    val evaluator = new MulticlassClassificationEvaluator()
      .setLabelCol("final_status")
      .setPredictionCol("predictions")
      .setMetricName("f1")

    // On
    val trainValidationSplit = new TrainValidationSplit()
      .setEstimator(pipeline)
      .setEvaluator(evaluator)
      .setEstimatorParamMaps(paramGrid)
      .setTrainRatio(0.7)

    val model = trainValidationSplit.fit(training)

    // On regarde les prédictions de notre modèle sur le test set
    val dfPrediction = model
      .transform(test)
      .select("features","final_status", "predictions", "raw_predictions")

    // f1-score
    val metrics = evaluator.evaluate(dfPrediction)
    println("f1-score du modèle sur les données du Test set : " + metrics)

    // Affiche les predictions
    dfPrediction.groupBy("final_status","predictions").count.show()

  }
}

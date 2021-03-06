from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession, Row
import seaborn as sns
import matplotlib.pyplot as plt
import time

KEY_WORD = 'football'
TCP_IP = "localhost"
TCP_PORT = 9876

def spark(TCP_IP,TCP_PORT,KEY_WORD):
    sc=SparkContext(appName="TwitterStreamming")
    sc.setLogLevel("ERROR")
    ssc=StreamingContext(sc,30)
    
    socket_stream = ssc.socketTextStream(TCP_IP,TCP_PORT)
    
    lines=socket_stream.window(300)
    df=lines.flatMap(lambda x:x.split(" "))  \
            .filter(lambda x:x.startswith("#"))  \
            .filter(lambda x:x!='#%s'%KEY_WORD)  
    
    def process(rdd):
        spark=SparkSession \
                .builder \
                .config(conf=rdd.context.getConf()) \
                .getOrCreate()
    
        rowRdd = rdd.map(lambda x: Row(word=x))
        wordsDataFrame = spark.createDataFrame(rowRdd)
    
        wordsDataFrame.createOrReplaceTempView("words")
        wordCountsDataFrame = spark.sql("select word, count(*) as total from words group by word order by 2 desc")       
        pd_df=wordCountsDataFrame.toPandas()
        
        plt.figure( figsize = ( 10, 8 ) )
        sns.barplot( x="total", y="word", data=pd_df.head(20))
        plt.show()
        
    df.foreachRDD(process)
    
    ssc.start()
    time.sleep(900)
    ssc.stop(stopSparkContext=True)
 
if __name__=="__main__":
    spark(TCP_IP,TCP_PORT,KEY_WORD)
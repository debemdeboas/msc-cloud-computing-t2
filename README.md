# Setting up an EMR cluster and running a Spark job

First, create and populate an S3 bucket to store the input data, the output data, and the script that will be run on the EMR cluster:

```shell
$ python3.11 download_books.py
$ aws s3 cp word_count.py s3://myemrclusterdata/
$ aws s3 cp --recursive books s3://myemrclusterdata/books
```

Then run the following command to add a step to the EMR cluster (replace `j-1PCXVXE5P57VM` with the ID of your cluster):

```shell
$ aws emr add-steps \
    --cluster-id j-1PCXVXE5P57VM \
    --steps Type=Spark,\
Name="Spark Word Count",\
ActionOnFailure=CONTINUE,\
Args=[--deploy-mode,cluster,s3://myemrclusterdata/word_count.py,--input,s3://myemrclusterdata/books,--output,s3://myemrclusterdata/output]
```

To download the output files and process them, run the following commands:

```shell
$ aws s3 cp --recursive s3://myemrclusterdata/output output
$ python3.11 process_output.py 
```


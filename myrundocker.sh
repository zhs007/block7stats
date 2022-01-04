docker stop block7stats
docker rm block7stats
docker run -d --name block7stats -v $PWD/output:/src/block7stats/output -v $PWD/cfg:/src/block7stats/cfg block7stats
cp -rf $PWD/output/* ../jupyternotebook.demo/home/block7/ 

const express = require('express')
const path = require('path')
const hbs = require('hbs')
const elastic = require("./elastic");
const bodyParser = require('body-parser');
var http = require('follow-redirects').http;
var httpProxy = require('http-proxy');

// Proxy for separately hosted Elastic
httpProxy.createProxyServer({target:'http://206.189.137.227:9200/'}).listen(9200);


async function ready_elastic(){
    const isElasticReady = await elastic.checkConnection();
    if (isElasticReady) {
        const elasticIndex = await elastic.esclient.indices.exists({index: elastic.index});
        console.log(elasticIndex.body)
        if (!elasticIndex.body) {
            await elastic.createIndex(elastic.index);
            await elastic.setFlagMapping(); 
        }else{
            await elastic.esclient.indices.delete({
              index: elastic.index
            })
        }

        await elastic.esclient.index({  
                  index: elastic.index,
                  type: elastic.type,
                  body: {   
                    "flag": "batpwn{elasticsearch_is_hella_awesome}"
                  }
                },function(err,resp,status) {
                    console.log(resp);
                });
    }
}
ready_elastic()


const app = express()
const publicDir = path.join(__dirname, './public')
const viewsDir = path.join(__dirname, './views')

app.set('view engine', 'hbs')
app.set('views', viewsDir)

app.use(express.static(publicDir))
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) =>{
    res.render('index')
})

app.get('/gallery', (req, res) =>{
    res.render('gallery')
})

app.get('/redirect', (req, res) =>{
    res.redirect(req.query.next)
})

app.post('/', (req, res) =>{

    try{

        var url = 'http://127.0.0.1:3001/img/' + req.body.id + '.png'

        console.log(url)
        http.get(url, (resp) => {
            resp.setEncoding('base64');
            body = "data:" + resp.headers["content-type"] + ";base64,";
            resp.on('data', (data) => { body += data});
            resp.on('end', () => {
                req.body.url = body
                res.render('id', req.body)
            });
        }).on('error', (e) => {
            req.body.url = ""
            res.render('id', req.body)
        });
    }catch{
        req.body.url = "504 Gateway Timeout"
        res.render('id', req.body)
    }
})

app.get('*', (req, res) => {
    res.send('404')
})

const port = process.env.PORT || 3001

app.listen(port, () => {
    console.log('challege: elastic is up and runnig on port: '+ port)
})


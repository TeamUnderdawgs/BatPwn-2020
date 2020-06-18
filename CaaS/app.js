const express = require('express')
const path = require('path')
const hbs = require('hbs')
const bodyParser = require('body-parser');
const fs = require('fs');
const temp = require('temp')
const exec = require('child_process').exec;

temp.track();

const app = express()
const viewsDir = path.join(__dirname, './views')


app.set('view engine', 'hbs')
app.set('views', viewsDir)

app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) =>{
    res.render('index')
})

app.post('/', (req, res) =>{

    code = req.body.code

    temp.open({suffix: '.cpp'}, function(err, info) {
      if (!err) {
        fs.write(info.fd, code, (err) => {
            if(err){
                res.send({error: "Internal Error"})
            }else{
                fs.close(info.fd, function(err) {
                    if(err){
                        res.send({error: "Internal Closing Error"})
                    }else{
                        exec("g++ '" + info.path + "' -o " + info.path + ".out", function(err, stdout) {
                            if(err){
                                res.send({error: "Code Compilation error"})
                            }else{
                                res.download(info.path + ".out")
                            }
                        });
                    }
                });
            }
        });

      }else{
        res.send({error: "Internal temp Error"})
      }

    });
})

app.get('*', (req, res) => {
    res.send('404')
})

const port = process.env.PORT || 3000

app.listen(port, () => {
    console.log('challenge: compiler is up and runnig on port: '+ port)
})


var express  = require('express');
var app = express();
var server = require('http').Server(app);
var socketio = require('socket.io')(server);
var shell = require('shelljs')
var fs = require('fs');
const summaryFolder = './summary';
var util = require('util');
var https = require('https');
var subscriptionKey = '21d8913e64854ab48f0496758210fdb5';
var request_params;

app.get('/', function(req, res){
	res.sendFile(__dirname + '/index.html');
});

socketio.on('connection', function(socket){
	console.log("A new connection is being made");
	
	function web_search(term){

		var host = 'api.cognitive.microsoft.com';
		var path = '/bing/v7.0/images/search';
		var response_handler = function (response) {
	    	var body = '';
	    	response.on('data', function (d) {
	        	body += d;
	    	});
	    	response.on('end', function () {
		        console.log('\nRelevant Headers:\n');
		        for (var header in response.headers)
		            // header keys are lower-cased by Node.js
		            if (header.startsWith("bingapis-") || header.startsWith("x-msedge-"))
		                 console.log(header + ": " + response.headers[header]);
		        console.log('\nJSON Response:\n');
		        body = JSON.parse(body);
		        var a = body.value[0].contentUrl;
		        sendImageURL(a);
	    	});
	    	response.on('error', function (e) {
	        	console.log('Error: ' + e.message);
	    	});
		};

		var bing_image_search = function (search) {
		  	console.log('Searching images for: ' + term);
		  	request_params = {
		        method : 'GET',
		        hostname : host,
		        path : path + '?q=' + encodeURIComponent(search),
		        headers : {
		            'Ocp-Apim-Subscription-Key' : subscriptionKey,
		        }
		    };

    	var req = https.request(request_params, response_handler);
    	req.end();
    	}
    	bing_image_search(term);
	}

	function sendImageURL(url){
		socketio.emit("send_url", a);
		console.log("sending url");
	}


	socket.on('fetch_data', function(){
		console.log('Trying to fetch data');
		shell.exec('bash ./setup.sh');
		console.log("Bash script ran completely");
		console.log("Trying to read data");

		fs.readdirSync('./output').forEach(file => {
			fs.readFile(summaryFolder + '/' + file, "utf8", function(err, data){
				console.log(data);
				web_search(data);
			})
		}


		fs.readdirSync(summaryFolder).forEach(file => {
			fs.readFile(summaryFolder + '/' + file, "utf8", function(err, data) {
				console.log(data);
				sendData(data);
			});
			console.log(file);
		})
	});

	function sendData(file){
		socketio.emit("senddata", file);
		console.log("data sent");
	}
});

var port = process.env.PORT || 1337;
server.listen(port, function(){
	console.log("Server running at http://localhost:%d", port);
});

console.log("Server running at http://localhost:%d", port);

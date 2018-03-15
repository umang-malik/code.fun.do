var express  = require('express');
var app = express();
var server = require('http').Server(app);
var socketio = require('socket.io')(server);
var shell = require('shelljs')
var fs = require('fs');
const summaryFolder = './summary';

app.get('/', function(req, res){
	res.sendFile(__dirname + '/index.html');
});

socketio.on('connection', function(socket){
	console.log("A new connection is being made");

	socket.on('fetch_data', function(){
		console.log('Trying to fetch data');
		shell.exec('bash ./setup.sh');
		console.log("Bash script ran completely");
		console.log("Trying to read data");
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

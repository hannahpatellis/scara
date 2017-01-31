// This is the ScARA Server application. Execute node server.js to run it
// Code in your API intigrations in here to be sent to the Panels
// Written by Hannah A. Patellis - hannahap.com - @hannahpatellis

var config = require('./config');

// Sets up and creates a websocket server to recieve commands
var WebSocketServer = require('websocket').server;
var http = require('http');

var server = http.createServer(function(request, response) {
    console.log((new Date()) + ' Received request for ' + request.url);
    response.writeHead(404);
    response.end();
});
server.listen(8080, function() {
    console.log((new Date()) + ' Server is listening on port 8080');
});
 
wsServer = new WebSocketServer({httpServer: server,autoAcceptConnections:false});

wsServer.on('request', function(request) {
    
    var connection = request.accept('echo-protocol', request.origin);
    console.log((new Date()) + ' Connection accepted.');
    
    // If a message comes in, console log it
    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            console.log('Received UTF Message: ' + message.utf8Data);
            //if(message.utf8Data == 'hello'){
	        //    connection.sendUTF('whatup');
            //}
        }
        // If a binary message comes in, console log it and send it back
        else if (message.type === 'binary') {
            console.log('Received Binary Message of ' + message.binaryData.length + ' bytes');
            connection.sendBytes(message.binaryData);
        }
    });
    
    // Sending messages at varying intervals assures the Panels don't recieve two messages strung together
    setInterval(function() {
	    // Add a list of any functions to call on a regular interval
	    getAlmondClientList(function(message) {console.log("BROADCAST: almondClientList"+message);connection.sendUTF("almondClientList"+message)});
    }, 30000);
    setInterval(function() {
	    // Add a list of any functions to call on a regular interval
	    getAlmondSceneList(function(message) {console.log("BROADCAST: almondSceneList"+message);connection.sendUTF("almondSceneList"+message)});
    }, 45000);
    setInterval(function() {
	    // Add a list of any functions to call on a regular interval
	    getExternalWeather(function(message) {console.log("BROADCAST: weather"+message);connection.sendUTF("weather"+message)});
    }, 60000);
    
    connection.on('close', function(reasonCode, description) {
        console.log((new Date()) + ' Peer ' + connection.remoteAddress + ' disconnected.');
    });
});


// Write your connection functions here. They should all have callbacks formatted to be understood by the Panels
function getAlmondClientList(callback) {
  	var WebSocketClient = require('websocket').client;
	var almond = new WebSocketClient();
	
	almond.on('connectFailed', function(error) {
	    callback('Almond Error');
	});

	almond.on('connect', function(connection) {
		
	    connection.on('error', function(error) {
		    callback('Almond Error');
	    });
	    connection.on('close', function() {});
	    connection.sendUTF('{"CommandType":"ClientList","MobileInternalIndex":"getClientList"}');
	    connection.on('message', function(message) {
	        if (message.type === 'utf8') {
		        data = JSON.parse(message.utf8Data);
		        var clientList = [];
		        if(data.MobileInternalIndex == 'getClientList'){
			        for(var x in data.Clients){
				        if(data.Clients[x]['Active'] == 'true'){
					        clientList.push({name:data.Clients[x]['Name'], ip:data.Clients[x]['LastKnownIP']});
				        }
			        }
			        clientList = JSON.stringify(clientList);
			        callback(clientList);
			        connection.close();
		        }
	        }
	    });
	});
	almond.connect(config.almondAddress);
}
function getAlmondSceneList(callback) {
  	var WebSocketClient = require('websocket').client;
	var almond = new WebSocketClient();
	
	almond.on('connectFailed', function(error) {
	    callback('Almond Error');
	});

	almond.on('connect', function(connection) {
		
	    connection.on('error', function(error) {
		    callback('Almond Error');
	    });
	    connection.on('close', function() {});
	    connection.sendUTF('{"CommandType":"DynamicSceneList","MobileInternalIndex":"getAlmondSceneList"}');
	    connection.on('message', function(message) {
	        if (message.type === 'utf8') {
		        data = JSON.parse(message.utf8Data);
		        var sceneList = [];
		        if(data.MobileInternalIndex == 'getAlmondSceneList'){
			        for(var x in data.Scenes){
				    	sceneList.push({name:data.Scenes[x]['Name'], id:data.Scenes[x]['ID'], active:data.Scenes[x]['Active']});
			        }
			        sceneList = JSON.stringify(sceneList);
			        callback(sceneList);
			        connection.close();
		        }
	        }
	    });
	});
	almond.connect(config.almondAddress);
}
function getExternalWeather(callback) {
  	var request = require('request');
	request('http://api.wunderground.com/api/'+config.wuAPI+'/conditions/q/GA/Savannah.json', function (error, response, body) {
	  if (!error && response.statusCode == 200) {
	    data = JSON.parse(body);
	    if (typeof data.current_observation.feelslike_f !== 'undefined') {
		    callback(data.current_observation.feelslike_f);
		}
	  }
	})
}
# scara
A central hub for home automation

Sapphic Citadel Automated Residency Application (ScARA) Project

Preface: Hi all! My name is Hannah Patellis and bottom line, I'm a huge nerd. Home automation has always been an interest of mine and I really enjoy learning various languages and creating projects so thus ScARA was born. ScARA is a suite of applications that run on Raspberry Pis to be used as wall panels in a "smart house" and control the "smart" aspects of the house. It's a really fancy light switch. That being said, ScARA is a project and one that is in its early stages of development. I wanted to release all the code and guides so other people could build similar systems but please understand this is not something with a super simple GUI setup. You will have to hand code functionality into it to be used with your specific devices. But please enjoy, make suggestions, alter the code to fit your home, et cetera.

*~~*

ScARA is in early early development and does not work 100% yet

*~~*

ScARA currently includes support for:
	•	Security Almond router/smart home hub via websocket API
	⁃		Get and set Almond scenes
	⁃		Get Almond modes
	⁃		Get Almond connected clients
	•	Raspberry Pi

ScARA works with four components. The server, the panels, a website, and "extras". Extras can include other small scripts to help around the house. I've included my extras just for fun.

ScARA Server is written primarily in Node.js and handles the communications between external smart home devices and the ScARA Panels. It keeps all the Panels up to date using websockets.

ScARA Panel is written primarily in Python 3.5 and PyQt5 (Qt framework). The job of the panel is to be mounted on the wall and offer a friendly, modern, easy interface to alter smart devices in the house. Think of it as a very fancy light switch.

ScARA Online is written primarily in Javascript (after HTML, CSS, jQuery, and Bootstrap) with some help from PHP. The job of ScARA Online is to get control of your house from anywhere. Everything accessible on the Panels is accessible using ScARA Online, too.

	Online <--->
	Panel <---> Server <--> Smart devices
	Panel <--->

ScARA can interface with theoretically anything with an API.

*~~*

I've been developing this for my current house and what it offers, but in the future I plan to expand it more for more flexibility and fun.

Future plans:
	•	Get it to actually work
	•	Make some videos about it
	•	Control a Sensi Thermostat via a Wink Hub and Wink's API
	•	Install a small camera on each Panel and have it record security footage based on Almond "Modes"
	•	Add on a voice command system based on the Amazon Alexa API

*~~*

If you have suggestions, found bugs, want to help, send me an e-mail! If you want to see this project go further, you can also think about donating: paypal.me/hannahpatellis

Hannah A. Patellis
hannahap.com
go.hannahap.com/scara
hannahpatellis@outlook.com
@hannahpatellis

Updated 3 Nov 2016

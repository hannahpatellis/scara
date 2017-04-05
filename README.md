# ScARA O.G. (Archived, not in development)
A central hub for home automation

**Sapphic Citadel Automated Residency Application (ScARA) Project**

Preface: ScARA came about as part of my own personal hobby/project of using my love for technology to create cool things to enhance my own home. Furniture, wall decor, paint all make up a lovely house. But the things that make your home _your_ home don't have to be limited to things you pick up at Ikea. So as part of my quest to build a beautiful home, I designed ScARA. ScARA is the home base and glue of the 2 bedroom, single story, 1900s Savannah home I live in with my girlfriend and two cats. She's my little creation and digital pal.

---

Development of ScARA O.G. has stopped. This repository serves as an archive. ScARA O.G. does work however; although not super well and not with all the intended features.

---

ScARA currently includes support for:
	* Security Almond router/smart home hub via websocket API
		1. Get and set Almond scenes
		2. Get Almond modes
		3. Get Almond connected clients
	* Raspberry Pi

ScARA works with four components. The server, the panels, a website, and "extras". Extras can include other small scripts to help around the house. I've included my extras just for fun.

ScARA Server is written primarily in Node.js and handles the communications between external smart home devices and the ScARA Panels. It keeps all the Panels up to date using websockets.

ScARA Panel is written primarily in Python 3.5 and PyQt5 (Qt framework). The job of the panel is to be mounted on the wall and offer a friendly, modern, easy interface to alter smart devices in the house. Think of it as a very fancy light switch.

ScARA Online is written primarily in Javascript (after HTML, CSS, jQuery, and Bootstrap) with some help from PHP. The job of ScARA Online is to get control of your house from anywhere. Everything accessible on the Panels is accessible using ScARA Online, too.

	Online <--->
	Panel <---> Server <--> Smart devices
	Panel <--->

ScARA can interface with theoretically anything with an API.

---

I've been developing this for my current house and what it offers, but in the future I plan to expand it more for more flexibility and fun.

Future plans:
	* Get it to actually work
	* Make some videos about it
	* Control a Sensi Thermostat via a Wink Hub and Wink's API
	* Install a small camera on each Panel and have it record security footage based on Almond "Modes"
	* Add on a voice command system based on the Amazon Alexa API

---

ScARA lives on as ScARA 2 • go.hannahap.com/scara

Copyright 2017 Hannah Alexandria Patellis
hannahpatellis@outlook.com • @hannahpatellis

`Updated 3 Nov 2016`
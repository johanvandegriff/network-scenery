## Inspiration
I wanted to show people what devices are on the network in a way that would be interactive, fun, and give a little more awareness of what the network looks like from the computer's perspective.

## What it does
Scan the Space runs periodic scans for devices on the network, then displays the data on a web server. Users can visit the web server, look at graphs of the network data over time, and have the option to assign their device a nickname. Scan the Space is useful for makerspaces, to log how many people visit throughout the day/week (or year!), how long each individual spends there, and to give the users some insight into the network. Another use case could be a company that runs a chain restaurant or store, to identify repeat customers to different locations.

## How I built it
The whole thing runs on a raspberry pi with a pi sense hat. It connects to MongoDB Atlas running on Google's Cloud Platform (GCP). The web server is made with a Flask Python backend, and Vue.js for the frontend.

## Challenges I ran into
We had some trouble connecting to MongoDB from the pi (it worked on the laptop). We ended up solving it by connecting another wifi dongle and conecting to a network that didn't block certain types of packets. In the process, we now dual-wield wifi dongles so we can now scan 2 networks at once!

## Accomplishments that I'm proud of
You can even assign multiple devices to your nickname, without anyone being able to steal the name (with a clever authentication method).

## What I learned
How to use MongoDB!

## What's next for scan-the.space
A global dashboard that connects to multiple devices
More charts!
A more visual representation of the devices 
A leaderboard of total time connected

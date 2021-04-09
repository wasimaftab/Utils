/* get the network table */
const path = require('path');
const Clustergrammer = require('clustergrammer');
const fs = require('fs'); 

/* load data for heatmap */
var network_data = fs.readFileSync(path.join(__dirname, "../data/small_mat.json"), {
    encoding: 'utf8',
    flag: 'r'
});

network_data = JSON.parse(network_data);
// console.log("network_data.mat.length = " + network_data.mat.length);

// args must contain root of container and the visualization JSON
var args = {
    'root': '#cy',
    'network_data': 'network_data'
  }

// Clustergrammer returns a Clustergrammer object in addition to making the visualization
var cgm = Clustergrammer(args); 



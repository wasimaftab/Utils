    'use strict'
    const path = require("path");
    const which = require("which");
    
    const isDev = require('electron-is-dev');
    if (isDev) {
        console.log('Running in development');
    } else {
        console.log('Running in production');
    }
    
    which("Rscript", function (er, RscriptPath) {
        console.log('RscriptPath = ' + RscriptPath);
    })

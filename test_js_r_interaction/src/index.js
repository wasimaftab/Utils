'use strict'
const path = require("path");

const child_process = require('child_process');

const RSCRIPT = 'Rscript';

const defaultOptions = {
    verboseResult: false
}

function parseStdout(output) {
    try {
        output = output.substr(output.indexOf('"{'), output.lastIndexOf('}"'));
        return JSON.parse(JSON.parse(output));
    } catch (err) {
        return err;
    }
}

function callSync(script, args, options) {
    options = options || defaultOptions;

    const result = args ?
        child_process.spawnSync(RSCRIPT, [script, JSON.stringify(args)]) :
        child_process.spawnSync(RSCRIPT, [script]);

    if (result.status == 0) {
        const ret = parseStdout(result.stdout.toString());
        if (!(ret instanceof Error)) {
            if (options.verboseResult) {
                return {
                    pid: result.pid,
                    result: ret
                };
            } else {
                return ret;
            };
        } else {
            return {
                pid: result.pid,
                error: ret.message
            };
        }
    } else if (result.status == 1) {
        return {
            pid: result.pid,
            error: result.stderr.toString()
        };
    } else {
        return {
            pid: result.pid,
            error: result.stderr.toString()
            //error: result.stdout.toString()
        };
    }
}

const isDev = require('electron-is-dev');

if (isDev) {
    console.log('Running in development');
    var R_path = path.join(__dirname, "../r_codes");
    console.log('R_path = ' + R_path);
} else {
    console.log('Running in production');
    var R_path = path.join(process.resourcesPath, 'r_codes');
    console.log('R_path = ' + R_path);
}

var button = document.getElementById('butt');
button.addEventListener('click', function (e) {
    var a = parseInt(document.getElementById('a').value);
    var b = parseInt(document.getElementById('b').value);
    const result = callSync(path.join(R_path, "exp_sum.R"), {
        a: a,
        b: b
    }, {
        "verboseResult": true
    });

    document.getElementById("result").innerHTML = "Exp sum = " + result.result.exp_sum;
    document.getElementById("r_version").innerHTML = "Computed using R version = " + result.result.R_version;

    console.log(result.result);
});

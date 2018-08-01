'use strict'

window.$ = window.jQuery = require('jquery')
window.Tether = require('tether')
window.Bootstrap = require('bootstrap')
window.Dialogs = require('dialogs')
const {spawn} = require('child_process');

var loaded_data_id = 0;

var myScatterChart;

function init() {
    //load the scatter data
    myScatterChart = new dhtmlXChart({
        view: "scatter",
        container: "scatter_here",
        value: "#risk#",
        xValue: "#cost#",
        yAxis: {
            title: "risk"
        },
        xAxis: {
            title: "cost"
        },
        tooltip: {
            template: "#risk# - #cost#"
        },
        item: {
            radius: 5,
            borderColor: "#f38f00",
            borderWidth: 1,
            color: "#ff9600",
            type: "d",
            shadow: true
        }
    });
    myScatterChart.attachEvent("onItemClick", function(id) {
        loadData(id);
        return true;
    })
    myScatterChart.load("data/optimization_result.json", "json");

    //load gannt
    gantt.config.readonly = true;
    gantt.config.xml_date = "%Y-%m-%d %H:%i:%s";

    gantt.config.columns = [{
            name: "text",
            label: "Task",
            width: 200,
            tree: true
        }, //use * for complete width
        //{name:"start_date", label:"Start time", align:"center" },
        //{name:"duration",   label:"Duration",   align:"center" },
        {
            name: "add",
            label: "",
            width: 44
        }
    ];

    var date_to_str = gantt.date.date_to_str(gantt.config.task_date);

    var id = gantt.addMarker({
        start_date: new Date(),
        css: "today",
        title: date_to_str(new Date())
    });
    setInterval(function() {
        var today = gantt.getMarker(id);
        today.start_date = new Date();
        today.title = date_to_str(today.start_date);
        gantt.updateMarker(id);
    }, 1000 * 60);

    gantt.init("gantt_here");
}

window.onresize = function(event) {
    var h = window.innerHeight;
    $("#gantt_here").height(h - 120 + "px");
    console.log("resize");
};

function dayview() {
    $("#gantt_here").show();
    $("#optimizationView").hide();
    gantt.config.scale_unit = "day";
    gantt.config.date_scale = "%d %M";
    gantt.init("gantt_here");
}

function weekview() {
    $("#gantt_here").show();
    $("#optimizationView").hide();
    gantt.config.scale_unit = "week";
    gantt.config.date_scale = "Week #%W";
    gantt.init("gantt_here");
}

function monthview() {
    $("#gantt_here").show();
    $("#optimizationView").hide();
    gantt.config.scale_unit = "month";
    gantt.config.date_scale = "%F, %Y";
    gantt.init("gantt_here");
}

function optimizeView() {
    $("#gantt_here").hide();
    $("#optimizationView").show();
}

function loadData(id) {
    loaded_data_id = id;
    gantt.clearAll();
    gantt.load("data/data" + loaded_data_id + ".json");
    dayview();
}

function reload() {
    gantt.clearAll();
    gantt.load("data/data" + loaded_data_id + ".json");
    myScatterChart.clearAll();
    myScatterChart.load("data/optimization_result.json", "json");
    var dialogs = Dialogs();
    dialogs.alert('New data loaded.', function(ok) {
        console.log('alert', ok)
    })
}

var process_running = false;

function executeProcess() {
    if (process_running == false) {
        const ls = spawn('sh', ['./app/program.sh'], {
            shell: true
        });
        process_running = true;

        //<i class="fas fa-circle-notch fa-spin"></i>
        $("#runbutton").html('<i class="fas fa-circle-notch fa-spin"></i> Running..');

        ls.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });

        ls.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });

        ls.on('close', (code) => {
            console.log(`child process exited with code ${code}`);
            process_running = false;
            $("#runbutton").html('(Re)start optimization');
            reload();
        });
    } else {
        dialogs.alert('Optimization still running.', function(ok) {
            console.log('alert', ok)
        });
    }
}
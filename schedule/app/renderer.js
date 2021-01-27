'use strict'

window.$ = window.jQuery = require('jquery')
window.Tether = require('tether')
window.Bootstrap = require('bootstrap')
window.Dialogs = require('dialogs')
const {spawn} = require('child_process');
const { platform } = require('os')
const {dialog} = require('electron').remote;

var loaded_data_id = 1;
var selected_directory = "data";
var myScatterChart;
var server = null;
var dialogs = Dialogs();
var optimization_config = '';

var json_config = '';

function init() {
    //load the scatter data
    myScatterChart = new dhtmlXChart({
        view: "scatter",
        container: "scatter_here",
        value: "#time#",
        xValue: "#cost#",
        yAxis: {
            title: "time"
        },
        xAxis: {
            title: "cost"
        },
        tooltip: {
            template: "#id#: Time:#time# - Cost:#cost# - Defects:#defectnum#"
        },
        item: {
            radius: 5,
            borderColor: "#000000",
            borderWidth: 1,
            color:function(obj){
               if (obj.defectnum < 10) return "#00ff00";
               if (obj.defectnum < 20) return "#44ff00";
               if (obj.defectnum < 30) return "#88ff00";
               if (obj.defectnum < 40) return "#aaaa00";
               if (obj.defectnum < 50) return "#ff8800";
               if (obj.defectnum < 60) return "#ff4400";
               return "#ff0000";
            },
            type: "d",
            shadow: true
        }
    });
    myScatterChart.attachEvent("onItemClick", function(id) {
        loadData(id);
        return true;
    })
    myScatterChart.load(selected_directory+DS+"optimization_result.json", "json");

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

    setTimeout(function(){ reload(); }, 1000);
}

window.onresize = function(event) {
    var h = window.innerHeight;
    $("#gantt_here").height(h - 120 + "px");
    $("#iframe").height(h + "px");
    console.log("resize");
};

function dayview() {
    $('.nav-item').removeClass("active");
    $("#nav-item3").addClass("active");
    $(".gantt").show();
    $(".visualisation").hide();
    $("#optimizationView").hide();
    gantt.config.scale_unit = "day";
    gantt.config.date_scale = "%d %M";
    gantt.init("gantt_here");
}

function weekview() {
    $('.nav-item').removeClass("active");
    $("#nav-item3").addClass("active");
    $(".gantt").show();
    $(".visualisation").hide();
    $("#optimizationView").hide();
    gantt.config.scale_unit = "week";
    gantt.config.date_scale = "Week #%W";
    gantt.init("gantt_here");
}

function monthview() {
    $('.nav-item').removeClass("active");
    $("#nav-item3").addClass("active");
    $(".gantt").show();
    $(".visualisation").hide();
    $("#optimizationView").hide();
    gantt.config.scale_unit = "month";
    gantt.config.date_scale = "%F, %Y";
    gantt.init("gantt_here");
}

function resetView(){
    $('.nav-item').removeClass("active");
    $(".gantt").hide();
    $("#optimizationView").hide();
    $(".visualisation").hide();
    $(".modeling").hide();
    $("#statusfooter").hide();
}

function yearview() {
    resetView()
    $("#nav-item3").addClass("active");
    $(".gantt").show();
    gantt.config.scale_unit = "year";
    gantt.config.date_scale = "%M, %Y";
    gantt.init("gantt_here");
}

function optimizeView() {
    resetView()
    $("#nav-item2").addClass("active");
    $("#optimizationView").show();
    $(window).trigger('resize');
}

function analyseView(){
    resetView()
    $("#nav-item1").addClass("active");
    $(".visualisation").show();
    $(window).trigger('resize');
}

function modelView(){
    resetView()
    $("#nav-model").addClass("active");
    $(".modeling").show();
    $(window).trigger('resize');
}

function loadData(id) {
    loaded_data_id = id;
    gantt.clearAll();
    gantt.load(selected_directory+"/data" + loaded_data_id + ".json");
    monthview();
}

function reload() {
    gantt.clearAll();
    //load config
    $.getJSON("../config.json", function(json) {
        console.log(json); // this will show the info it in firebug console
        //visualisation, optimization, project
        $("#projectname").text(json.project);

        if (json.server_script){ //only support on linux/mac for now.
            if (server != null){
                server.kill('SIGHUP');
                server = null;
            }
            console.log('sh '+json.server_script);
            server = spawn('sh',[json.server_script], {
                shell: true
            });
            $(".loader").show();
            $("#iframe").hide();
            setTimeout(function(){ $("#iframe").attr("src",json.server_output); }, 5000);
            document.getElementById('iframe').onload = function() {
              $(".loader").hide();
              $("#iframe").show();
            };
            analyseView();
            $(".analysis-menu").show();
        }else if (json.visualisation != ""){
            $("#iframe").attr("src",json.visualisation);
            analyseView();
            $(".analysis-menu").show();
        }else{
            $(".analysis-menu").hide();
        }
        json_config = json;
        if (json.optimization == "yes"){
            optimization_config = json.optimization_config;
            gantt.load(json.optimization_output +DS +"data" + loaded_data_id + ".json");
            myScatterChart.clearAll();
            myScatterChart.load(selected_directory +DS+"optimization_result.json", "json");
            $(".optimization-menu").show();
            optimizeView();
        }else{
            $(".optimization-menu").hide();
        }
    });
}

function loadFolder() {
    dialog.showOpenDialog({
        properties: ['openDirectory']
    }, function (files) {
        if (files !== undefined) {
            // handle files
            console.log(files[0]);
            selected_directory = files[0]+"/";
            $.getJSON(selected_directory+"config.json", function(json) {
                console.log(json); // this will show the info it in firebug console
                //visualisation, optimization, project
                $("#projectname").text(json.project);

                if (json.server_script){
                    if (server != null){
                        server.kill('SIGHUP');
                        server = null;
                    }
                    console.log('sh '+selected_directory+json.server_script);
                    server = spawn('sh',[selected_directory+json.server_script], {
                        shell: true
                    });
                    $(".loader").show();
                    $("#iframe").hide();
                    setTimeout(function(){ $("#iframe").attr("src",json.server_output); }, 5000);
                    document.getElementById('iframe').onload = function() {
                      $(".loader").hide();
                      $("#iframe").show();
                    };
                    analyseView();
                    $(".analysis-menu").show();
                }else if (json.visualisation != ""){
                    $("#iframe").attr("src",selected_directory+json.visualisation);
                    analyseView();
                    $(".analysis-menu").show();
                }else{
                    $(".analysis-menu").hide();
                }
                if (json.optimization == "yes"){
                    gantt.load(files[0] + "/data" + loaded_data_id + ".json");
                    myScatterChart.clearAll();
                    myScatterChart.load(selected_directory +"/optimization_result.json", "json");
                    
                    dialogs.alert('New data loaded.', function(ok) {
                        console.log('alert', ok)
                    })
                    $(".optimization-menu").show();
                    optimizeView();
                }else{
                    $(".optimization-menu").hide();
                }
            });
            
        }
    });
}

var process_running = false;

/**
 * Run the optimizer
 */
function executeProcess() {
    var budget = $("#budgetInput").val();
    if (process_running == false) {
        if (currentPlatform == platforms.WINDOWS){
            const ls = spawn(__dirname+DS+'run-optimizer.bat', [__dirname, __dirname+DS+optimization_config, budget], {
                shell: true
            });
            process_running = true;
    
            //<i class="fas fa-circle-notch fa-spin"></i>
            $("#runbutton").html('<i class="fas fa-circle-notch fa-spin"></i> Optimization in progress..');
    
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
            const ls = spawn('sh', ['./app/run-optimizer.sh', optimization_config, budget], {
                shell: true
            });
            process_running = true;
    
            //<i class="fas fa-circle-notch fa-spin"></i>
            $("#runbutton").html('<i class="fas fa-circle-notch fa-spin"></i> Optimization in progress..');
    
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
        }
        
    } else {
        dialogs.alert('Optimization still running.', function(ok) {
            console.log('alert', ok)
        });
    }
}

/**
 * Set progressbar.
 * @param {string} msg Message with percentage in it
 */
function setProgress(msg){
    var percentage = msg.match(/\d+\%/g);
    if (percentage){
        $("#progressbar").css("width", percentage[0]);
    } else {
        $("#progressbar").css("width", "0%");
    }
}

var logger = document.getElementById('modeling_log');
function logmsg(message) {
    if (typeof message == 'object') {
        logger.innerHTML += (JSON && JSON.stringify ? JSON.stringify(message) : message);
    } else {
        var percpos = message.indexOf("%");
        if (percpos > 0){
            logger.innerHTML = message.substr(0, percpos+1);
        } else {
            logger.innerHTML = message;
        }
        
    }
}
var training_in_progress = false;
/**
 * Run the model training
 */
function trainModel() {
    $("#statusfooter").show();
    $("#progressbar").show();
    if (training_in_progress == false) {
        if (currentPlatform == platforms.WINDOWS){
            const ls = spawn(__dirname+DS+'run-modeling.bat', 
                [__dirname+DS+"modeling", 3,1,25,__dirname+DS+json_config.training_input, __dirname+DS+json_config.training_output, __dirname+DS+json_config.training_features], {
                shell: true
            });
            training_in_progress = true;
            $("#trainbutton").html('<i class="fas fa-circle-notch fa-spin"></i> Training in progress..');  
            ls.stdout.on('data', (data) => {
                logmsg(`${data}`);
                setProgress(`${data}`);
            });
    
            ls.stderr.on('data', (data) => {
                logmsg(`${data}`);
                setProgress(`${data}`);
            });
    
            ls.on('close', (code) => {
                logmsg(`Done`);
                training_in_progress = false;
                $("#progressbar").fadeOut(500);
                $("#trainbutton").html('(Re)start model training');
            });
        } else {
            const ls = spawn('sh', ['./app/run-modeling.sh', 
                3,1,25,__dirname+DS+json_config.training_input, __dirname+DS+json_config.training_output, __dirname+DS+json_config.training_features], {
                shell: true
            });
            training_in_progress = true;
            $("#trainbutton").html('<i class="fas fa-circle-notch fa-spin"></i> Training in progress..');
    
            ls.stdout.on('data', (data) => {
                logmsg(`${data}`);
                setProgress(`${data}`);
            });
    
            ls.stderr.on('data', (data) => {
                logmsg(`${data}`);
                setProgress(`${data}`);
            });
    
            ls.on('close', (code) => {
                logmsg(`Done`);
                training_in_progress = false;
                $("#progressbar").fadeOut(500);
                $("#trainbutton").html('(Re)start model training');
            });
        }
        
    } else {
        dialogs.alert('Model still training.', function(ok) {
            console.log('alert', ok)
        });
    }
}
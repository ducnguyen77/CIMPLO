'use strict'

window.$ = window.jQuery = require('jquery')
window.Tether = require('tether')
window.Bootstrap = require('bootstrap')
window.Dialogs = require('dialogs')

 window.onresize = function(event) {
  var h = window.innerHeight;
  $("#gantt_here").height(h-120 + "px");
};

function dayview(){
  gantt.config.scale_unit = "day"; 
  gantt.config.date_scale = "%d %M";
  gantt.init("gantt_here");
}

function weekview(){
  gantt.config.scale_unit = "week"; 
  gantt.config.date_scale = "Week #%W";
  gantt.init("gantt_here");
}

function monthview(){
  gantt.config.scale_unit = "month";
  gantt.config.date_scale = "%F, %Y";
  gantt.init("gantt_here");
}

function reload(){
  gantt.load("data.json");
  var dialogs = Dialogs();
  dialogs.alert('New data loaded.', function(ok) {
  	console.log('alert', ok)
  })
}

# CIMPLO electron based app to view optimization output.

Can view schedules from json format.

How to setup:

- Clone repository
- `cd schedule`
- run `npm install`
- make sure you have electron installed globally `npm install -g electron`
- run `npm start`
- package `npm run-script package-win`



## Configuration file

The platform uses one main configuration file and several configuration files per module.

The main config file looks like this

    {
        "project":"Sample project",
        "visualisation":"Path to HTML file for visualisation (can also be a website)",
        "optimization":"yes",                                           // or "no" to turn on or off the optimization module,
        "optimization_output": "path to store data files",
        "optimization_config":"path to config file (folder where it is located)",
        "server_script":"start.sh",                                      // to start a background service if needed
        "server_output":"http://localhost:5006/CIMPLO_sensor_viz"        // To view the server output (analysis section)
    }

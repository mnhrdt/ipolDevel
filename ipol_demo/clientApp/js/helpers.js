'use strict'

var clientApp = clientApp || {};
var helpers = helpers || {};
clientApp.helpers = helpers;

clientApp.helpers.getFromAPI = function(module, method, parameters, funct){
    var url = "/api/" + module + "/" + method + "?" + parameters;
    $.get(url).done(funct);
};

clientApp.helpers.getJSON = function(json){
    return jQuery.parseJSON(json);
};


jQuery(function($){
	"use strict";
	var $ya_sk_id = ya_circle_skillbar.sk_id;
	$(function() {
		jQuery('.ya-skill-circle').waypoint(function() {
				$(this).circliful();
			}, {
				triggerOnce: true,
				offset: 'bottom-in-view'
			});	
    })
           
});
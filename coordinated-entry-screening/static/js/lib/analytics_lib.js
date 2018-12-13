/*!
 * Google Analytics Library v2
 * Upgraded for Universal Analytics
 *
 * Copyright 2016, Derek Eder of DataMade
 * Licensed under the MIT license.
 * Based on Google Analytics Library by Nick Rougeaux and Derek Eder from Open City
 *
 * Date: 4/19/2016
 *
 */

var analyticsTrackingCode = 'UA-XXXXXXXX-1'; //enter your tracking code here

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', analyticsTrackingCode, 'auto');
ga('set', 'forceSSL', true);
ga('send', 'pageview');

function handleOutboundLinkClicks(href) {
  ga('send', 'event', {
    eventCategory: 'Outbound Link',
    eventAction: 'click',
    eventLabel: href,
    transport: 'beacon'
  });
}

function _trackClickEventWithGA(category, action, label) {
  ga('send', {
	  hitType: 'event',
	  eventCategory: category,
	  eventAction: action,
	  eventLabel: label
	});
}

jQuery(function () {

	jQuery('a').click(function () {
		var $a = jQuery(this);
		var href = $a.attr("href");

		//links going to outside sites
		if (href.match(/^http/i) && !href.match(document.domain)) {
			handleOutboundLinkClicks(href);
		}

		//direct links to files
		if (href.match(/\.(avi|css|doc|docx|exe|gif|js|jpg|mov|mp3|pdf|png|ppt|pptx|rar|txt|vsd|vxd|wma|wmv|xls|xlsx|zip)$/i)) {
			_trackClickEventWithGA("Downloads", "Click", href);
		}

		//email links
		if (href.match(/^mailto:/i)) {
			_trackClickEventWithGA("Emails", "Click", href);
		}
	});
});

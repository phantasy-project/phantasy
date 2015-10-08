/*
 * Copyright (c) 2015, Facility for Rare Isotope Beams
 *
 */

/*
 * Common utilities for the Lattice Model web application.
 *
 * Dependencies: jQuery
 *
 */
var latticemodel = (function() {

	var exports = {};

	var config = {};

	exports.config = config;

	exports.data = {}

	// Request list of Lattice names matching the specified query.
	function find_lattice_names(query, callback) {
		if( !config.lattice_names_url ) {
			console.log('LatticeModel: missing configuration: "lattice_names_url"');
			return;
		}
		jQuery.ajax(config.lattice_names_url, {
			method:'POST',
			dataType:'json',
			data:{
				query:query
			},
			success:function(data) {
				callback(data);
			}
		});
	};

	exports.data.find_lattice_names = find_lattice_names;

	return exports;
})();

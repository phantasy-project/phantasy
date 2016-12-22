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

	function ajax_post(url, data, callback) {
		jQuery.ajax(url, {
			method:'POST',
			dataType:'json',
			data: data,
			success:function(data) {
				callback(data);
			}
		});
	};

	// Request list of Lattice names matching the specified query.
	function find_lattice_names(query, callback) {
		if( !config.lattice_names_url ) {
			console.log('LatticeModel: missing configuration: "lattice_names_url"');
			return;
		}
		ajax_post(config.lattice_names_url, {query:query}, callback);
	};
	exports.data.find_lattice_names = find_lattice_names;

	// Request list of Lattice branches matching the specified query.
	function find_lattice_branches(query, callback) {
		if( !config.lattice_branches_url ) {
			console.log('LatticeModel: missing configuration: "lattice_branches_url"');
			return;
		}
		ajax_post(config.lattice_branches_url, {query:query}, callback);
	};
	exports.data.find_lattice_branches = find_lattice_branches;

	// Request list of Model names matching the specified query.
	function find_model_names(query, callback) {
		if( !config.model_names_url ) {
			console.log('LatticeModel: missing configuration: "model_names_url"');
			return;
		}
		ajax_post(config.model_names_url, {query:query}, callback);
	};
	exports.data.find_model_names = find_model_names;


	function find_model_elements_property_values(model_id, name, callback) {
		if( !config.model_elements_property_values_url ) {
			console.log('LatticeModel: missing configuration: "model_elements_property_values_url"');
			return;
		}
		var data = { model_id:model_id, name:name };
		ajax_post(config.model_elements_property_values_url, data, callback)
	};
	exports.data.find_model_elements_property_values = find_model_elements_property_values

	return exports;
})();

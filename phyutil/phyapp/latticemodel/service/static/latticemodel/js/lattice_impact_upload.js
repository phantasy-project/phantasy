/*
 * Copyright (c) 2015, Facility for Rare Isotope Beams
 *
 */

$('#lattice_name').typeahead({}, {
	source:function(query, syncResults, asyncResults) {
		latticemodel.data.find_lattice_names(query, asyncResults);
	}
});


/*
 * Copyright (c) 2015, Facility for Rare Isotope Beams
 *
 */

$('#lattice_name').typeahead({hint:false}, {
	source:function(query, syncResults, asyncResults) {
		latticemodel.data.find_lattice_names(query, asyncResults);
	},
	limit:10
});

$('#lattice_branch').typeahead({hint:false}, {
	source:function(query, syncResults, asyncResults) {
		latticemodel.data.find_lattice_branches(query, asyncResults);
	},
	limit:10
});

$('#lattice_autoversion').on('change', function() {
	$('#lattice_version').val('').prop('disabled', this.checked);
});


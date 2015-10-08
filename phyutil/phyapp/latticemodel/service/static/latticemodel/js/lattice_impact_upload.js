/*
 * Copyright (c) 2015, Facility for Rare Isotope Beams
 *
 */

$('#lattice_name').typeahead({}, {
	source:function(query, syncResults, asyncResults) {
		latticemodel.data.find_lattice_names(query, asyncResults);
	}
});

$('#lattice_branch').typeahead({}, {
	source:function(query, syncResults, asyncResults) {
		latticemodel.data.find_lattice_branches(query, asyncResults);
	}
});

$('#lattice_autoversion').on('change', function() {
	$('#lattice_version').val('').prop('disabled', this.checked);
});


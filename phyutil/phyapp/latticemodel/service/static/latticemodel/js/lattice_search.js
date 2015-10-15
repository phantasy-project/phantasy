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

$('.compare-checkbox').on("change", function() {
	var checked = $('.compare-checkbox:checked').length;
	if( checked < 2) {
		$('.compare-button').addClass('hidden');
	} else if( checked == 2 ) {
		$('.compare-button').removeClass('hidden');
	} else if( checked == 3) {
		$(this).prop("checked", false);
		alert("Only two Lattice can be compared.");
	}
});

$('.compare-button').on('click', function() {
	$('.compare-form').submit();
});


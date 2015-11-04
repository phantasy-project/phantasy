/*
 * Copyright (c) 2015, Facility for Rare Isotope Beams
 *
 */

(function() {

	function hideCompareButton() {
		$('.compare-button').addClass('hidden');
	};

	function showCompareButton() {
		$('.compare-button').removeClass('hidden');
	};

	function toggleCompareButton() {
		var checked = $('.compare-checkbox:checked').length;
		if( checked < 2) {
			hideCompareButton();
		} else if( checked == 2 ) {
			showCompareButton();
		} else if( checked == 3) {
			$(this).prop("checked", false);
			alert("Only two Models can be compared.");
		}
	};

	$('#model_name').typeahead({hint:false}, {
		source:function(query, syncResults, asyncResults) {
			latticemodel.data.find_model_names(query, asyncResults);
		},
		limit:10
	});

	$('.compare-checkbox').on("change", toggleCompareButton);

	$('a[href="#results"]')
		.on('show.bs.tab', toggleCompareButton)
		.on('hide.bs.tab', hideCompareButton);

	$('.compare-button').on('click', function() {
		$('.compare-form').submit();
	});

	// Initialize compare button because of possible autocomplete.
	toggleCompareButton();

})();




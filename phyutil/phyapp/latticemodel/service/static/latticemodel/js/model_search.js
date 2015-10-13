/*
 * Copyright (c) 2015, Facility for Rare Isotope Beams
 *
 */

$('#model_name').typeahead({hint:false}, {
	source:function(query, syncResults, asyncResults) {
		latticemodel.data.find_model_names(query, asyncResults);
	},
	limit:10
});

/*
 * Copyright (c) 2015, Facility for Rare Isotope Beams
 *
 */


(function () {

	var selected = null;
	var modeldata = [];

	function colorByNumber(n) {
		// The basic algorithm for this method has
		// been adopted from Flot library internals.

		// Default color scheme copied from Flot.
		var colors = ["#edc240", "#55aff6", "#cb4b4b", "#4da74d", "#9440ed"],
		variations = [ 0, -0.2, +0.2, -0.4, +0.4, -0.6, +0.6 ],
		color = null, vidx = 0;

		n = Math.abs(n);
		color = $.color.parse(colors[n % colors.length] || "#666");
		vidx = Math.floor(n / colors.length) % variations.length;
		color.scale('rgb', 1 + variations[vidx])
		return color.toString();
	};

	function redrawModelData() {
		if( modeldata.length === 0 ) {
			$('.model-element-data-hint').removeClass('hidden');
			$('.model-element-data-label').addClass('hidden');
			$('.model-element-data-plot').addClass('hidden');
		} else {
			$('.model-element-data-hint').addClass('hidden');
			$('.model-element-data-label').removeClass('hidden');
			$('.model-element-data-plot').removeClass('hidden');
			$('.model-element-data-plot').plot(modeldata, { legend:{ show:true } });
		}
	}

	$('.model-element-property-controls').each(function(idx, control) {

		var property_colors = [
			colorByNumber(idx),
			colorByNumber(idx+2)
		];

		$(control).children('input[type="checkbox"]').on('change', function() {

			var property_name = $(this).prop("value"),
				rawdata = [];

			var process_rawdata = function() {
				var idx = 0;
				if( rawdata[0] && rawdata[1] ) {
					modeldata = [];
					$.each(rawdata, function(n, data) {
						var idx = 0, points = [], npoints = 0;
						if( data[property_name] ) {
							data = data[property_name];
							npoints = data.values.length;
							for( idx=0; idx<npoints; idx+=1 ) {
								points.push([data.positions[idx], data.values[idx]]);
							}
							modeldata.push({
								label:"Model " + (n+1),
								color:property_colors[n],
								data:points
							});
						}
					});
					redrawModelData();
				}
			};

			if( $(this).prop('checked') ) {
				if( selected ) {
					$(selected).parent().css('background-color', '');
					$(selected).prop('checked', false);
				}

				$(this).parent().css('background-color', property_colors[0]);
				selected = this;
				modeldata = [];
				redrawModelData();

				latticemodel.data.find_model_elements_property_values(
								model1, $(this).prop("value"), function(data) {
									rawdata[0] = data;
									process_rawdata();
								});

				latticemodel.data.find_model_elements_property_values(
								model2, $(this).prop("value"), function(data) {
									rawdata[1] = data;
									process_rawdata();
								});
			} else {
				$(this).parent().css('background-color', '');
				selected = null;
				modeldata = [];
				redrawModelData();
			}
		});
	});
})();


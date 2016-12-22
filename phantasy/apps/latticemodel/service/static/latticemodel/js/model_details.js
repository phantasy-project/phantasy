/*
 * Copyright (c) 2015, Facility for Rare Isotope Beams
 *
 */

var updateModelDataPlot = (function() {

	var cache = {}

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

	function retrieveModelData() {
		$('.model-element-property-controls').each(function(idx) {
			var property_name = $(this).find('.model-element-property-name').text(),
				property_scale = $(this).find('.model-element-property-scale').prop("value"),
				property_enabled = $(this).find('.model-element-property-enabled').prop("checked"),
				property_color = '';

			var process_data = function(data) {
				var idx = 0, points = [], npoints = 0;
				if( data[property_name] ) {
					data = data[property_name];
					npoints = data.values.length;
					for( idx=0; idx<npoints; idx+=1 ) {
						points.push([data.positions[idx], data.values[idx]]);
					}
					cache[property_name] = {
						label:property_name,
						color:property_color,
						data:points
					};
					redrawModelData();
				}
			};

			if( property_enabled === true ) {
				property_color = colorByNumber(idx);
				$(this).css('background-color', property_color)

				if( !cache[property_name] ) {
					latticemodel.data.find_model_elements_property_values(
										model_id, property_name, process_data);
				}
			} else {
				$(this).css('background-color', property_color);

				if( cache[property_name] ) {
					delete cache[property_name];
					redrawModelData();
				}
			}
		});
	}

	function redrawModelData() {
		var data = [], yaxes = [];
		$.each(cache, function(name, value) {
			value.yaxis = yaxes.length+1;
			yaxes.push({ color:value.color, tickColor:'rgb(0,0,0,0.15)' });
			data.push(value);
		});

		if( data.length === 0 ) {
			$('.model-element-data-hint').removeClass('hidden');
			$('.model-element-data-label').addClass('hidden');
			$('.model-element-data-plot').addClass('hidden');
		} else {
			$('.model-element-data-hint').addClass('hidden');
			$('.model-element-data-label').removeClass('hidden');
			$('.model-element-data-plot').removeClass('hidden');
			$('.model-element-data-plot').plot(data, { yaxes:yaxes, legend:{ show:false } });
		}
	}

	return retrieveModelData;
})();


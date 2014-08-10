/*
  fund distribution function
*/

function loadFundDistribution(data){
    var plot1 = jQuery.jqplot ('pie_chart', [data],
			       {
				   seriesDefaults: {
				       // Make this a pie chart.
				       renderer: jQuery.jqplot.PieRenderer,
				       rendererOptions: {
					   // Put data labels on the pie slices.
					   // By default, labels show the percentage of the slice.
					   showDataLabels: true
				       }
				   },
				   legend: { show:true, location: 'e' }
			       }
			      );
    
}

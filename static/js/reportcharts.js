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

function loadPieChart(id, data){
    var plot1 = jQuery.jqplot (id, [data],
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
				   legend: { show:true,
					     location:'e',
					     placement:'insideGrid' }
			       }
			      );
    
}

/*
  this funtion requires to load th ff. js files
    <script type="text/javascript" src="/static/jquery.jqplot.1.0.8/plugins/jqplot.dateAxisRenderer.min.js"></script>
    <script type="text/javascript" src="/static/jquery.jqplot.1.0.8/plugins/jqplot.canvasTextRenderer.min.js"></script>
    <script type="text/javascript" src="/static/jquery.jqplot.1.0.8/plugins/jqplot.canvasAxisTickRenderer.min.js"></script>
    <script type="text/javascript" src="/static/jquery.jqplot.1.0.8/plugins/jqplot.categoryAxisRenderer.min.js"></script>
    <script type="text/javascript" src="/static/jquery.jqplot.1.0.8/plugins/jqplot.barRenderer.min.js"></script>
    
*/

function loadBarChart(id, data){
    var plot1 = $.jqplot(id, [data], {
    title: 'Fund distribution by Allocation',
    series:[{renderer:$.jqplot.BarRenderer}],
    axesDefaults: {
        tickRenderer: $.jqplot.CanvasAxisTickRenderer ,
        tickOptions: {
          angle: -30,
          fontSize: '10pt'
        }
    },
    axes: {
      xaxis: {
        renderer: $.jqplot.CategoryAxisRenderer
      }
    }
  });
}

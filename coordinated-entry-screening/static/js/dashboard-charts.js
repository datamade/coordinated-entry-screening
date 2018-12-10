var basic_config = {  
        chart: {
            type: 'bar',
            borderColor: '#e7e7e7',
            borderWidth: 2,
            style: {
                fontFamily: 'Libre Franklin', 
            },
        },
        title: {
            text: null
        },
        subtitle: {
            text: null
        },
        credits: {
            enabled: false
        },
    };

function barHelper(container, prepped_data, data_map){
    custom_config = {
        xAxis: {
            type: 'category',
            labels: {
                formatter: function () {
                   return data_map[this.value];
                },
            },
        },
        yAxis: {
            title: {
                text: 'Number of times B.E.N recommended each resource'
            },
            allowDecimals: false
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
            }
        },
        tooltip: {
            useHTML: true,
            headerFormat: '',
            pointFormat:  '<h6><strong>{point.y} recommendations</strong></h6><p>{point.name}</p>',
            shadow: false,
            borderColor: '#3B4B5C',
        },
        series: [
            {
                "name": "Number of users",
                "colorByPoint": true,
                "data": prepped_data
            }
        ]
    };

    config = $.extend(basic_config, custom_config);

    Highcharts.chart(container, config);
}

function stackedBarHelper(container, prepped_data, data_map){
    custom_config = {
        xAxis: {
          labels: {
            enabled: false
          },
          tickWidth: 0
        },
        yAxis: {
            title: {
                text: 'Percent of users'
            },
            allowDecimals: false,
        },
        legend: {
            enabled: true,
            labelFormatter: function () {
                return data_map[this.name];
            },
        },
        plotOptions: {
            series: {
              stacking: 'percent',
              dataLabels: {
                enabled: true,
                format: '{y:,.0f}%',
                color: '#fff',
                style: {
                  textShadow: 'none',
                  opacity: 0.8,
                  fontWeight: 'bold'
                }
              }
            }
        },
        tooltip: {
            useHTML: true,
            headerFormat: '',
            pointFormat:  '<h6><strong>{point.y}% of users</strong></h6><p>{point.series.name}</p>',
            shadow: false,
            borderColor: '#3B4B5C',
        },
        series: prepped_data
    };

    config = $.extend(basic_config, custom_config);

    Highcharts.chart(container, config);
}

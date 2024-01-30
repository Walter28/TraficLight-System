var options = {
    series: [30, 23, 21, 17, 15, 10, 12],
    labels: ["Total", "Total Fille", "Total Garcons", "Total travailleurs", "Total fille employée" ,
                "Totat auto-employé", "Total fille auto-employée"],
    chart: {
    type: 'polarArea',
  },
  stroke: {
    colors: ['#fff']
  },
  fill: {
    opacity: 0.8
  },
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: 200
      },
      legend: {
        position: 'bottom'
      }
    }
  }]
  };

  var chart = new ApexCharts(document.querySelector("#summury"), options);
  chart.render();
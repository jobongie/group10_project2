function init() {
    
  // Grab a reference to the dropdown select element
  var selection = d3.select("#selDataset");
  d3.csv("merge.csv").then(function(data){
    console.log(data)
  //Added for ease of conversion  JB
  dataset.forEach(function(data){
// data.Industry = +data.Industry;
//data.employment_b =+data.employment_b;
//data.industries_b = +data.industries_b;
//data.employment_s = +data.employment_s
//data.industries_s =+data.industries_s
})  

// get the YEAR data to the dropdwown menu
  var sampleYEAR = data.map(d => d.YEAR);
  var usedNames = []
      sampleYEAR.forEach((year) => {
        if (usedNames.indexOf(year) == -1) {
        selection
          .append("option")
          .text(year)
          .property("value", year);usedNames.push(year);
        }
      })
      buildCharts(usedNames[0]);
    })
  };
  function optionChanged(newYEAR) {
    // Fetch new data each time a new sample is selected
    buildCharts(newYEAR);
  }
  // Initialize 
  init();
  //function when sample id is changed 
  function buildCharts(sampleYEAR) {
    //update demographic info area
    d3.csv("merge.csv").then((data) => {
    var employment_b = findings_b_y.map(d => d.EMPLOYMENT)
    var industries_b = findings_b_y.map(d => d.INDUSTRY)
    var employment_s = findings_s_y.map(d => d.EMPLOYMENT)
    var industries_s = findings_s_y.map(d => d.INDUSTRY)
//       var findings = data.filter(d => d.YEAR == sampleYEAR)
//       var payroll = findings.map(d => d.ANNUAL_PAYROLL)
//       var employment = findings.map(d => d.EMPLOYMENT)
//       var firms = findings.map(d => d.FIRMS_log)
//       var industries = findings.map(d => d.INDUSTRY)
//       var sector = findings.map(d => d.SECTOR)
//       var findings_b = data.filter(d => d.BUSINESS_CLASSIFICATION == "Large Business")
//       var findings_b_y = findings_b.filter(d => d.YEAR == sampleYEAR)
//       var payroll_b = findings_b_y.map(d => d.ANNUAL_PAYROLL)
//       var firms_b = findings_b_y.map(d => d.FIRMS_log)
//       var sector_b = findings_b_y.map(d => d.SECTOR)
//       var findings_s = data.filter(d => d.BUSINESS_CLASSIFICATION == "Small Business")
//       var findings_s_y = findings_s.filter(d => d.YEAR == sampleYEAR)
//       var payrolls = findings_s_y.map(d => d.ANNUAL_PAYROLL)
//       var firms_s = findings_s_y.map(d => d.FIRMS_log)
//       var sector_s = findings_s_y.map(d => d.SECTOR)
        //console.log(findings_b);              
         //  Build bar Chart        
         var trace1 =
          {
            y:employment_b,
            x:industries_b,
            name: 'Large Business',
            text:industries_b,
            type:"bar",
            marker: {
              color: '#08519c'
            }
          };            
          var trace2 ={
            y:employment_s,
            x:industries_s,
            name: 'Small Business',
            text:industries_s,
            type:"bar",
            marker: {color: '#993404'    
              }
        };
        var data = [trace1, trace2];
        var layout = {
          barmode: 'group',
          title: "EMPLOYMENT BY INDUSTRY",
        };
        Plotly.newPlot("bar", data, layout);
        //create bubble chart
        var trace2 = {
          x: employment,
          y: payroll,
        //   text: text,
          mode: "markers",
          text: industries,
          marker: {
            color: employment,
            colorscale: "Greens",
            size: firms,
            colorbar: {
                thickness: 20,
                y: 0.5,
                ypad: 0,
                titleside: 'bottom',
                outlinewidth: 1,
                outlinecolor: 'black'
            }}};
        var data = [trace2];
        var layout = {
          showlegend: false,
          margin: { t: 0 },
          xaxis: { title: "TOTAL EMPLOYMENT (PEOPLE)" },
          yaxis: { title: "TOTAL PAYROLL ($)" },
          hovermode: "closest",
          };
        Plotly.newPlot('bubble', data, layout);
    });
  };


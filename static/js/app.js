function init() {
  // Grab a reference to the dropdown select element
  var selection = d3.select("#selDataset");

  d3.json("/linechart").then(function(data){
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
 
  
  d3.json("/linechart").then((data) => {

      
      var findings = data.filter(d => d.YEAR == sampleYEAR)
      
      var payroll = findings.map(d => d.ANNUAL_PAYROLL)
      var employment = findings.map(d => d.EMPLOYMENT)
      var firms = findings.map(d => d.FIRMS_log)
      var industries = findings.map(d => d.INDUSTRY)
      var sector = findings.map(d => d.SECTOR)

      var findings_b = data.filter(d => d.BUSINESS_CLASSIFICATION == "Large Business")
      var findings_b_y = findings_b.filter(d => d.YEAR == sampleYEAR)
     
      var payrollb = findings_b_y.map(d => d.ANNUAL_PAYROLL)
      var employment_b = findings_b_y.map(d => d.EMPLOYMENT)
      var firms_b = findings_b_y.map(d => d.FIRMS_log)
      var industries_b = findings_b_y.map(d => d.INDUSTRY)
      var sector_b = findings_b_y.map(d => d.SECTOR)


      var findings_s = data.filter(d => d.BUSINESS_CLASSIFICATION == "Small Business")
      var findings_s_y = findings_s.filter(d => d.YEAR == sampleYEAR)
     
      var payrolls = findings_s_y.map(d => d.ANNUAL_PAYROLL)
      var employment_s = findings_s_y.map(d => d.EMPLOYMENT)
      var firms_s = findings_s_y.map(d => d.FIRMS_log)
      var industries_s = findings_s_y.map(d => d.INDUSTRY)
      var sector_s = findings_s_y.map(d => d.SECTOR)
      
      
         
    
       //  Build bar Chart
      
       var trace1 =
        {
          y:employment_b,
          x:industries_b,
          name: 'Large Business',
          text:industries_b,
          type:"bar",
          // orientation: "h",
          
          marker: {
            color: 'blue'
          },
        
          
        };
          

        var trace2 ={
          y:employment_s,
          x:industries_s,
          name: 'Small Business',
          text:industries_s,
          type:"bar",
          // orientation: "h",
       
        
          marker: {
            color: 'orange'
          
  
        }
      };
     
      var data = [trace1, trace2];
      
      var layout = {
        barmode: 'group',
        title: "EMPLOYMENT BY INDUSTRY",
        yaxis: {
          automargin: true
        },
        height:400,
        width: 1100,
        
      };
      
      Plotly.newPlot("bar", data, layout);

      //create bubble chart
      var trace3 = {
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
          }
      }
      };

     

      var data = [trace3];

      var layout = {
        
        // showlegend: true,
        // margin: { t: 0 },
        xaxis: { title: "TOTAL EMPLOYMENT (PEOPLE)" },
        yaxis: { title: "TOTAL PAYROLL ($)" },
        hovermode: "closest",
        height: 400,
        width: 1100

        };

      //   var layout_2 = {
      //     xaxis:{title: "OTU ID"},
      //     yaxis: {title:"sample values"},
      //     height: 600,
      //     width: 1000
      // };

      


      Plotly.newPlot('bubble', data, layout);
  });
};


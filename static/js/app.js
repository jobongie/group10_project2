function init() {
  // Grab a reference to the dropdown select element
  var selection = d3.select("#selDataset");

  d3.json("/scatter").then(function(data){
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
 
  d3.json("/scatter").then((data) => {
    
  
      
      var findings = data.filter(d => d.YEAR == sampleYEAR)

      var payroll = findings.map(d => d.ANNUAL_PAYROLL)
      var employment = findings.map(d => d.EMPLOYMENT)
      // var firms = findings.map(d => d.FIRMS_log)
      var industries = findings.map(d => d.INDUSTRY)
      var code = findings.map(d => d.NAICS_CODE)

      var findings_b = data.filter(d => d.BUSINESS_CLASSIFICATION == "Large Business")
      var findings_b_y = findings_b.filter(d => d.YEAR == sampleYEAR)
     
      var payrollb = findings_b_y.map(d => d.ANNUAL_PAYROLL)
      var employment_b = findings_b_y.map(d => d.EMPLOYMENT)
      var firms_b = findings_b_y.map(d => d.FIRMS_log)
      var industries_b = findings_b_y.map(d => d.INDUSTRY)
      var code_b = findings_b_y.map(d => d.NAICS_CODE)
      var code_bb = code_b.toString()

      console.log(code_b)

      var findings_s = data.filter(d => d.BUSINESS_CLASSIFICATION == "Small Business")
      var findings_s_y = findings_s.filter(d => d.YEAR == sampleYEAR)
     
      var payrolls = findings_s_y.map(d => d.ANNUAL_PAYROLL)
      var employment_s = findings_s_y.map(d => d.EMPLOYMENT)
      var firms_s = findings_s_y.map(d => d.FIRMS_log)
      var industries_s = findings_s_y.map(d => d.INDUSTRY)
      var code_s = findings_s_y.map(d => d.NAICS_CODE)
      var code_ss = code_s.toString()
      
      
      console.log(findings_b);
            
    
       //  Build bar Chart
      
       var trace1 =
        {
          y: employment_b,
          x: industries_b,
          name: 'Large Business',
          text: industries_b,
          type: "bar",
          marker: {
            color: '#Steel blue'
          }
        };
          

        var trace2 ={
          y: employment_s,
          x: industries_s,
          name: 'Small Business',
          text: industries_s,
          type: "bar",
          marker: {
            color: 'Orange'
          
  
        }
      };
     
      var data = [trace1, trace2];

      var layout = {
        autosize: false,
        width: 900,
        height: 700,
        margin: {
          l: 50,
          r: 50,
          b: 100,
          t: 100,
          pad: 4,
        },
        xaxis: {
          tickangle: 45,
          automargin: true
        },
        yaxis: {
          automargin: true
        },
        
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
          size: 20,
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


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
        
        
        console.log(findings_b);
              
      
         //  Build bar Chart
        
         var trace1 =
          {
            y:employment_b,
            x:industries_b,
            name: 'Large Business',
            text:industries_b,
            type:"bar",
            marker: {
              color: 'rgb(142,124,195)'
            }
          };
            

          var trace2 ={
            y:employment_s,
            x:industries_s,
            name: 'Small Business',
            text:industries_s,
            type:"bar",
            marker: {
              color: 'rgb(142,124,100)'
            
    
          }
        };
       
        var data = [trace1, trace2];
        
        var layout = {
          barmode: 'group',
          title: "EMPLOYMENT BY INDUSTRY",
          
        };
    
        Plotly.newPlot("bar", data, layout);
  
        // var trace1 = {
        //   x: ['giraffes', 'orangutans', 'monkeys'],
        //   y: [20, 14, 23],
        //   name: 'SF Zoo',
        //   type: 'bar'
        // };
        
        // var trace2 = {
        //   x: ['giraffes', 'orangutans', 'monkeys'],
        //   y: [12, 18, 29],
        //   name: 'LA Zoo',
        //   type: 'bar'
        // };
        
        // var data = [trace1, trace2];
        
        // var layout = {barmode: 'group'};







 
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
                title: 'EMPLOYMENT #',
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
          xaxis: { title: "TOTAL EMPLOYMENT" },
          yaxis: { title: "TOTAL PAYROLL ($)" },
          hovermode: "closest",
          };
  
          // var frames = [];
          // for (i = 0; i < years.length; i++) {
          //   frames.push({
          //     name: years[i],
          //     data: industries.map(function (industry) {
          //       return getData(years[i], industry);
          //     })
          //   })
          // }
        
          //   // Now create slider steps, one for each frame. The slider
          // // executes a plotly.js API command (here, Plotly.animate).
          // // In this example, we'll animate to one of the named frames
          // // created in the above loop.
          // var sliderSteps = [];
          // for (i = 0; i < years.length; i++) {
          //   sliderSteps.push({
          //     method: 'animate',
          //     label: years[i],
          //     args: [[years[i]], {
          //       mode: 'immediate',
          //       transition: {duration: 300},
          //       frame: {duration: 300, redraw: false},
          //     }]
          //   });
          // }
          // console.log(sliderSteps)
          // var layout = {
          //   xaxis: {
          //     title: 'EMPLOYMENT',
              
          //   },
          //   yaxis: {
          //     title: 'ANNUAL PAYROLL',
          //     type: 'log'
          //   },
          //   hovermode: 'closest',
          //  // We'll use updatemenus (whose functionality includes menus as
          //  // well as buttons) to create a play button and a pause button.
          //  // The play button works by passing `null`, which indicates that
          //  // Plotly should animate all frames. The pause button works by
          //  // passing `[null]`, which indicates we'd like to interrupt any
          //  // currently running animations with a new list of frames. Here
          //  // The new list of frames is empty, so it halts the animation.
          //   updatemenus: [{
          //     x: 0,
          //     y: 0,
          //     yanchor: 'top',
          //     xanchor: 'left',
          //     showactive: false,
          //     direction: 'left',
          //     type: 'buttons',
          //     pad: {t: 87, r: 10},
          //     buttons: [{
          //       method: 'animate',
          //       args: [null, {
          //         mode: 'immediate',
          //         fromcurrent: true,
          //         transition: {duration: 300},
          //         frame: {duration: 500, redraw: false}
          //       }],
          //       label: 'Play'
          //     }, {
          //       method: 'animate',
          //       args: [[null], {
          //         mode: 'immediate',
          //         transition: {duration: 0},
          //         frame: {duration: 0, redraw: false}
          //       }],
          //       label: 'Pause'
          //     }]
          //   }],
          //  // Finally, add the slider and use `pad` to position it
          //  // nicely next to the buttons.
          //   sliders: [{
          //     pad: {l: 130, t: 55},
          //     currentvalue: {
          //       visible: true,
          //       prefix: 'Year:',
          //       xanchor: 'right',
          //       font: {size: 20, color: '#666'}
          //     },
          //     steps: sliderSteps
          //   }]
          // };




        Plotly.newPlot('bubble', data, layout);
    });
  };































// var dataVisuals = function (metadata, otuValues, sampleValues, hoverText, xValues, yValues, labels) {

//     var panel = d3.select("#sample-metadata");
//     panel.html("");
//      Object.entries(metadata).forEach(([key, value]) => {
//        panel.append("h6").text(`${key}: ${value}`);
//      });
         
//   //creating bar graph     
//        var trace1 = {
//            x: data.map(d => d.YEAR),
//            y: data.map(d => d.ANNUAL_PAYROLL_B),
//            text: hoverText,
//            marker: {
//            color: 'olive'},
//            type:"bar",
//            orientation: "h",
//        };
 
//        var data = [trace1];
     
           
//      var layout = {
//          title: "Top 10 OTU",
 
//          margin: {
//            l: 150,
//            r: 50,
//            b: 50,
//            t: 30,
          
//          },
                
//              };
     
//      Plotly.newPlot("bar", data, layout);
     
//      //creating bubble plot
//      var trace2 = {
     
     
//        x: xValues,
//        y: yValues,
//        mode: "markers",
//        marker:{
//            size: yValues,
//            color: xValues,
//            colorbar: {
//              thickness: 20,
//              y: 0.5,
//              ypad: 0,
//              title: 'OTU IDs',
//              titleside: 'bottom',
//              outlinewidth: 1,
//              outlinecolor: 'black'
//            }
           
//        },
//        text:  labels
 
//    };
   
//            // set the layout for the bubble plot
//            var layout_2 = {
//                xaxis:{title: "OTU ID"},
//                yaxis: {title:"sample values"},
//                height: 600,
//                width: 1000
//            };
   
//            // creating data variable 
//            var data1 = [trace2];
   
//        // create the bubble plot
//        Plotly.newPlot("bubble", data1, layout_2); 
 
//    };

// //filtering  metadata and plots
// var optionChanged = function(newYear){

//     d3.json("/linechart").then(function(data){
    
//     var yearFiltered = data["YEAR"].filter(function(year){
//       return year ==newYear;
//     })


//     var metadataFiltered = data["metadata"].filter(function(metadata){
//       return metadata.id ==newSample;

//     });

//     otu = sampleFiltered[0]["otu_ids"].slice(0, 10).reverse();

//     otuValues = otu.map(d => "OTU " + d);
    
//     sampleValues =  sampleFiltered[0]["sample_values"].slice(0,10).reverse();
  
//     hoverText =  sampleFiltered[0]["otu_labels"].slice(0,10); 

//     xValues = sampleFiltered[0]["otu_ids"]
//     yValues = sampleFiltered[0]["sample_values"]
//     labels = sampleFiltered[0]["otu_labels"]
//     dataVisuals(metadataFiltered[0], otuValues, sampleValues, hoverText, xValues, yValues, labels)
//     });

//   }


// function init() {
//   // select dropdown menu 
//   var dropdown = d3.select("#selDataset");
  
//  // read the data   
// d3.json("/linechart").then(function(data){
//     // console.log(data)

//       // get the YEAR data to the dropdwown menu
//       data.YEAR.forEach(function(date) {
//         dropdown.append("option").text(date).property("value");
//     });

//     //display the data and the plots to the page
//     otu = data["samples"][0]["otu_ids"].slice(0, 10).reverse();

//     otuValues = otu.map(d => "OTU " + d);
        
//     sampleValues =  data["ANNUAL_PAYROLL"].slice(0,10).reverse();
      
//     hoverText =  data["samples"][0]["otu_labels"].slice(0,10); 
    
    
//     xValues = data["samples"][0]["otu_ids"];
//     yValues = data["samples"][0]['sample_values']
//     labels = data["samples"][0]["otu_labels"]
//     metadata = data["metadata"][0];
//     dataVisuals(metadata, otuValues, sampleValues, hoverText, xValues, yValues, labels);
// });
// }

// init();


(function(){
  
  var width = 980;
  var height = 800;

  var margin = {
    top: 20,
    right: 40,
    bottom: 100,
    left: 100
  };
  var chart= d3.select("#chart")
    .append("div")
    .classed("chart", true)

  var svg =chart.append('svg')
    .attr("height", height)
    .attr("width", width)
    .append("g")
    .attr("transform", "translate(0.0)");


    var svg = d3.select("#my_dataviz")
    .append("svg")
      .attr("width", width)
      .attr("height", height)

   
  
  // The scale you use for bubble size
  var size = d3.scaleSqrt()
    .domain([14666, 101309])  // What's in the data, let's say it is percentage
    .range([10,40])  // Size in pixel
  
  // Add legend: circles
  var valuesToShow = [40000, 100000, 15000]
  var xCircle = 100
  var xLabel = 280
  var yCircle = 780
  var legerndcircleTitle =[{
    title: "Circles are sized according to the employee salary ($)"
  }];
  var titleSalaryX = 75
  var titleSalaryY = 680
  svg
    .selectAll("legend")
    .data(valuesToShow)
    .enter()
    .append("circle")
      .attr("cx", xCircle)
      .attr("cy", function(d){ return yCircle - size(d) } )
      .attr("r", function(d){ return size(d) })
      .style("fill", "none")
      .attr("stroke", "black")
  
  // Add legend: segments
  svg
    .selectAll("legend")
    .data(valuesToShow)
    .enter()
    .append("line")
      .attr('x1', function(d){ return xCircle + size(d) } )
      .attr('x2', xLabel)
      .attr('y1', function(d){ return yCircle - size(d) } )
      .attr('y2', function(d){ return yCircle - size(d) } )
      .attr('stroke', 'black')
      .style('stroke-dasharray', ('2,2'))
  
  // Add legend: labels
  svg
    .selectAll("legend")
    .data(valuesToShow)
    .enter()
    .append("text")
      .attr('x', xLabel)
      .attr('y', function(d){ return yCircle - size(d) } )
      .text( function(d){ return d } )
      .style("font-size", 12)
      .attr('alignment-baseline', 'middle') 
  
  svg
  .selectAll("legend")
  .data(legerndcircleTitle)
  .enter()
  .append("text")
    .attr('x', titleSalaryX)
    .attr('y',titleSalaryY)
    .attr('font-size', '15px')
    .text(function(d){return d.title});

  svg.append("circle").attr("cx",500).attr("cy",700).attr("r", 20).style("fill", "steelblue")
  svg.append("circle").attr("cx",500).attr("cy",750).attr("r", 20).style("fill", "orange")
  svg.append("text").attr("x", 540).attr("y", 700).text("Large Business").style("font-size", "20px").attr("alignment-baseline","middle")
  svg.append("text").attr("x", 540).attr("y", 750).text("Small Business").style("font-size", "20px").attr("alignment-baseline","middle")

 
  // var textTitle = ("Total Annual Payroll of $ 19.9 Trillion")
  // svg.append("text")
  //   .attr("x", 490)
  //   .attr("y",100)
  //   .classed("aText", true)
  //   .text(textTitle);
    
    // var textsalary = ("Employee salary > $50,000          Employee salary < $50,000")
    // svg.append("text")
    //   .attr("x", 490)
    //   .attr("y",100)
    //   .classed("aText", true)
    //   .text(textsalary );

    var allLabel = svg.append("text")
    .attr("x", 490)
    .attr("y",100)
    .classed("active", true)
    .classed("aText", true)
    .text("Total Annual Payroll of $ 19.9 Trillion");

    var textSeparate = svg.append("text")
    .attr("x", 490)
    .attr("y",130)
    .classed("inactive", true)
    .classed("aText", true)
    .text("Employee salary > $50,000          Employee salary < $50,000");




  var color = d3.scaleOrdinal().domain(["1", "2"]).range(["steelblue", "orange"])
  var radiusScale = d3.scaleSqrt().domain([14666, 101309]).range([5,40])

  var forceXSeparate = d3.forceX(function(d){
    if (d.Employee_salary >= 50000){
      return 300
    }
    else{
      return 700
    }
  }).strength(0.05)


  var forceYSeparate = d3.forceY(function(d){
    if (d.Employee_salary >= 50000){
      return 310
    }
    else{
      return 310
    }
  }).strength(0.05)





  var forceXIndustry = d3.forceX(function(d){
    if (d.Industry_number === 1){
      return 140
    }
    else if (d.Industry_number === 2){
      return 360
    }

    else if (d.Industry_number === 3){
      return 530
    }

    else if (d.Industry_number === 4){
      return 680
    }

    else if (d.Industry_number === 5){
      return 840
    }
    if (d.Industry_number === 6){
      return 140
    }
    else if (d.Industry_number === 7){
      return 360
    }

    else if (d.Industry_number === 8){
      return 530
    }

    else if (d.Industry_number === 9){
      return 680
    }

    else if (d.Industry_number === 10){
      return 840
    }
    if (d.Industry_number === 11){
      return 140
    }
    else if (d.Industry_number === 12){
      return 360
    }

    else if (d.Industry_number === 13){
      return 530
    }

    else if (d.Industry_number === 14){
      return 680
    }

    else if (d.Industry_number === 15){
      return 840
    }
    if (d.Industry_number === 16){
      return 140
    }
    else if (d.Industry_number === 17){
      return 360
    }

    else if (d.Industry_number === 18){
      return 530
    }

    else if (d.Industry_number === 19){
      return 680
    }

    else {
      return 840
    }


  })

  var forceYIndustry = d3.forceY(function(d){
    if (d.Industry_number === 1){
      return 140
    }
    else if (d.Industry_number === 2){
      return 140
    }

    else if (d.Industry_number === 3){
      return 140
    }

    else if (d.Industry_number === 4){
      return 140
    }

    else if (d.Industry_number === 5){
      return 140
    }
    if (d.Industry_number === 6){
      return 280
    }
    else if (d.Industry_number === 7){
      return 280
    }

    else if (d.Industry_number === 8){
      return 280
    }

    else if (d.Industry_number === 9){
      return 280
    }

    else if (d.Industry_number === 10){
      return 280
    }
    if (d.Industry_number === 11){
      return 420
    }
    else if (d.Industry_number === 12){
      return 420
    }

    else if (d.Industry_number === 13){
      return 420
    }

    else if (d.Industry_number === 14){
      return 420
    }

    else if (d.Industry_number === 15){
      return 420
    }
    if (d.Industry_number === 16){
      return 560
    }
    else if (d.Industry_number === 17){
      return 560
    }

    else if (d.Industry_number === 18){
      return 560
    }

    else if (d.Industry_number === 19){
      return 560
    }

    else {
      return 560
    }


  })
    

  var forceXCombine = d3.forceX(width/2).strength(0.05)
  var forceYCombine = d3.forceY(height/2).strength(0.05)

  // var forceXCombine = d3.forceX(width/2).strenght(0.05)
  var forceCollide = d3.forceCollide(function(d){
    return radiusScale(d.Employee_salary);
  })

  var simulation = d3.forceSimulation()
    .force("x", forceXCombine)
    .force("y", forceYCombine)
    .force("collide", forceCollide)

  // var simulation =d3.forceSimulation()
  //   .force("x", d3.forceX(width/2).strength(0.05))
  //   .force("y", d3.forceY(height/2).strength(0.05))
  //   .force("collide", d3.forceCollide(function(d){
  //     return radiusScale(d.Employee_salary);
  //   }))


d3.json("/api/data").then(function(dataset){
//d3.csv("/static/data/tablebusiness.csv").then(function(dataset){

  dataset.forEach(function(data){
    // data.Industry = +data.Industry;
    data.Business_class =+data.Business_class;
    data.Employee_salary = +data.Employee_salary;
    data.Sector= +data.Sector
    data.Industry_number =+data.Industry_number
  })
  // d3.queue()
  //   .defer(d3.csv, "tablebusiness.csv")
  //   .await(ready)
  
  
  // function ready (error, business){
    var circles = svg.selectAll(".Sector")
    .data(dataset)
    .enter()
    .append("circle")
    .attr("class", "Sector")
    .attr("r", function(d){
      return radiusScale(d.Employee_salary)
      
    })
    .attr("fill", function(d){
      return color(d.Business_class)     
    })

    .attr("stroke", function(d){ 
      return d3.rgb(color(d.Business_class)).darker(); 
    })
    .attr("stroke-width", 1)

    // circles.transition()
    // .duration(2000)
    // .attr('r', function (d) { return d.Employee_salary; });


    // .attr("cx", 500)
    // .attr("cy", 300)
  


    d3.select("#total").on('click', function(){
      simulation
        .force("x", forceXCombine)
        .force("y", forceYCombine)
        .alphaTarget(1)
        .restart()

       d3.select(this).attr("text");
      // if (simulation == forceXCombine && simulation == forceYCombine){

      // allLabel
      //   .classed("active", true)
      // textSeparate
      //   .classed("inactive", false)

      // }
     
    })

    d3.select("#split").on('click', function(){
      simulation
        .force("x", forceXSeparate)
        .force("y",forceYSeparate)
       
        .alphaTarget(1)
        .restart()
      // if (simulation == forceXSeparate && simulation == forceYSeparate){
      //     textSeparate
      //     .classed("active", true) 
      //     allLabel
      //     .classed("inactive", false)


      // }
      

    })

  
    d3.select("#more").on('click', function(){
      simulation
        .force("x", forceXIndustry)
        .force("y", forceYIndustry)
        .alphaTarget(1)
        .restart()
      

    })


   
    
    simulation.nodes(dataset)
      .on("tick", ticked)

    function ticked (){
      circles
        .attr("cx", function(d){
          return d.x
        })

        .attr ("cy", function (d){
          return d.y
        })
    }
    
    
  
  var toolTip = d3.tip()
    .attr("class", "tooltip")
    .offset([80, -20])
    .html(function(d) {
      return (`${d.Industry}<br> Salary: $ ${d.Employee_salary}`);
    });

    svg.call(toolTip);

    circles.on("mouseover", function(data) {
      toolTip.show(data, this);
    })
      // onmouseout event
      .on("mouseout", function(data, index) {
        toolTip.hide(data);
      });
  // }

      

    
  });

})();



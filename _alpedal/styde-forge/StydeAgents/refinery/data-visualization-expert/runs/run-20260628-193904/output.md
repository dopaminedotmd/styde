<html>
<head>
<meta charset="utf-8">
<title>D3 Visualization</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
<div id="chart" style="width:800px;height:500px;margin:auto;font-family:sans-serif;"></div>
<script>
const data = [
  {category:"Q1",value:42},{category:"Q2",value:58},{category:"Q3",value:35},{category:"Q4",value:71},
  {category:"Q5",value:64},{category:"Q6",value:49},{category:"Q7",value:53},{category:"Q8",value:67}
];
const width = 760, height = 420, margin = {top:40,right:20,bottom:50,left:60};
const svg = d3.select("#chart").append("svg").attr("width",width+margin.left+margin.right).attr("height",height+margin.top+margin.bottom)
  .append("g").attr("transform",`translate(${margin.left},${margin.top}`);
const x = d3.scaleBand().domain(data.map(d=>d.category)).range([0,width]).padding(0.3);
const y = d3.scaleLinear().domain([0,d3.max(data,d=>d.value)*1.1]).range([height,0]);
svg.append("g").call(d3.axisLeft(y));
svg.append("g").attr("transform",`translate(0,${height})`).call(d3.axisBottom(x));
svg.selectAll("rect").data(data).join("rect")
  .attr("x",d=>x(d.category)).attr("y",d=>y(d.value)).attr("width",x.bandwidth()).attr("height",d=>height-y(d.value))
  .attr("fill","#4e79a7").attr("alt",d=>`${d.category}: ${d.value}`);
svg.append("text").attr("x",width/2).attr("y",-10).attr("text-anchor","middle").style("font-size","16px").style("font-weight","bold")
  .text("Quarterly Metrics");
</script>
<p style="text-align:center;color:#555;font-size:12px;margin-top:8px;">Chart: Quarterly Metrics (synthetic data). Use keyboard Tab to navigate bars.</p>
</body>
</html>
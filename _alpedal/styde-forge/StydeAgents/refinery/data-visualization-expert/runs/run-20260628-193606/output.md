<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Synthetic Data Viz — D3.js Bar Chart</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
body { font-family: system-ui, sans-serif; margin: 2rem; background: #fafafa; }
svg { display: block; margin: 2rem auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.axis text { font-size: 11px; }
.axis path, .axis line { stroke: #ccc; }
.tooltip { position: absolute; background: #333; color: #fff; padding: 6px 10px; border-radius: 4px; font-size: 12px; pointer-events: none; opacity: 0; transition: opacity 0.15s; }
.bar:hover { opacity: 0.8; cursor: pointer; }
.caption { text-align: center; color: #666; font-size: 13px; margin-top: -1rem; }
</style>
</head>
<body>
<h2 style="text-align:center;color:#333;">Quarterly Revenue by Product Line (Synthetic)</h2>
<p class="caption">Generated on demand — no input provided</p>
<div id="chart" style="position:relative;"></div>
<script>
const data = [
  {product: 'Cloud', q1: 142, q2: 168, q3: 195, q4: 223},
  {product: 'Hardware', q1: 98, q2: 87, q3: 92, q4: 76},
  {product: 'Services', q1: 55, q2: 63, q3: 71, q4: 88},
  {product: 'Licensing', q1: 201, q2: 194, q3: 188, q4: 175},
  {product: 'Support', q1: 33, q2: 38, q3: 42, q4: 49}
];
const width = 720, height = 420, margin = {top: 30, right: 20, bottom: 60, left: 60};
const innerW = width - margin.left - margin.right;
const innerH = height - margin.top - margin.bottom;
const quarters = ['q1','q2','q3','q4'];
const quarterLabels = ['Q1','Q2','Q3','Q4'];
const color = d3.scaleOrdinal().domain(quarters).range(['#4e79a7','#f28e2b','#e15759','#76b7b2']);
const x0 = d3.scaleBand().domain(data.map(d => d.product)).range([0, innerW]).padding(0.2);
const x1 = d3.scaleBand().domain(quarters).range([0, x0.bandwidth()]).padding(0.08);
const yMax = d3.max(data, d => d3.max(quarters, q => d[q])) + 15;
const y = d3.scaleLinear().domain([0, yMax]).range([innerH, 0]);
const svg = d3.select('#chart').append('svg').attr('width', width).attr('height', height)
  .append('g').attr('transform', `translate(${margin.left},${margin.top})`);
const tooltip = d3.select('#chart').append('div').attr('class', 'tooltip');
svg.append('g').attr('class', 'axis').call(d3.axisLeft(y).ticks(6).tickFormat(d => '$'+d+'M'));
svg.append('g').attr('class', 'axis').attr('transform', `translate(0,${innerH})`)
  .call(d3.axisBottom(x0)).selectAll('text').attr('transform','rotate(-15)').style('text-anchor','end');
quarters.forEach((q, i) => {
  svg.selectAll('.bar-'+q)
    .data(data)
    .join('rect')
    .attr('class', 'bar')
    .attr('x', d => x0(d.product) + x1(q))
    .attr('y', d => y(d[q]))
    .attr('width', x1.bandwidth())
    .attr('height', d => innerH - y(d[q]))
    .attr('fill', color(q))
    .on('mouseover', (ev, d) => {
      tooltip.style('opacity', 1).html(`<strong>${d.product}</strong> ${quarterLabels[i]}: $${d[q]}M`);
    })
    .on('mousemove', ev => tooltip.style('left', (ev.offsetX+12)+'px').style('top', (ev.offsetY-24)+'px'))
    .on('mouseout', () => tooltip.style('opacity', 0));
});
const legendG = svg.append('g').attr('transform', `translate(${innerW - 180}, -6)`);
quarters.forEach((q, i) => {
  const lg = legendG.append('g').attr('transform', `translate(${i * 45}, 0)`);
  lg.append('rect').attr('width', 12).attr('height', 12).attr('fill', color(q));
  lg.append('text').attr('x', 16).attr('y', 10).text(quarterLabels[i]).style('font-size','11px').attr('fill','#555');
});
</script>
</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Data Visualization</title>
<style>
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; background: #f8f9fa; }
.container { max-width: 960px; margin: 0 auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); padding: 32px; }
h1 { font-size: 24px; color: #1a1a2e; margin-top: 0; }
.chart-wrapper { width: 100%; overflow-x: auto; }
.axis path, .axis line { stroke: #ccc; stroke-width: 1px; }
.axis text { font-size: 12px; fill: #666; }
.bar { transition: opacity 0.15s; }
.bar:hover { opacity: 0.7; }
.tooltip { position: absolute; background: rgba(0,0,0,0.85); color: #fff; padding: 8px 14px; border-radius: 6px; font-size: 13px; pointer-events: none; opacity: 0; transition: opacity 0.2s; }
footer { margin-top: 24px; font-size: 12px; color: #999; text-align: center; }
</style>
</head>
<body>
<div class="container">
<h1>Quarterly Revenue by Product Category (2025)</h1>
<div class="chart-wrapper">
<svg id="chart" width="880" height="480" aria-label="Bar chart showing quarterly revenue by product category for 2025" role="img"></svg>
</div>
<footer>Source: Generated synthetic data for demonstration</footer>
</div>
<div class="tooltip" id="tooltip"></div>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const data = [
  { category: 'Hardware', Q1: 420, Q2: 510, Q3: 485, Q4: 620 },
  { category: 'Software', Q1: 780, Q2: 820, Q3: 910, Q4: 1050 },
  { category: 'Services', Q1: 340, Q2: 390, Q3: 430, Q4: 510 },
  { category: 'Cloud',   Q1: 920, Q2: 1100, Q3: 1280, Q4: 1450 },
  { category: 'Data',    Q1: 210, Q2: 260, Q3: 310, Q4: 400 }
];
const quarters = ['Q1', 'Q2', 'Q3', 'Q4'];
const palette = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#b07aa1'];
const margin = { top: 20, right: 20, bottom: 60, left: 70 };
const width = 880 - margin.left - margin.right;
const height = 480 - margin.top - margin.bottom;
const groupWidth = width / 4;
const svg = d3.select('#chart')
  .append('g')
  .attr('transform', `translate(${margin.left},${margin.top})`);
const yMax = d3.max(data, d => d3.max(quarters, q => d[q])) * 1.1;
const xScale = d3.scaleBand()
  .domain(quarters)
  .range([0, width])
  .padding(0.4);
const yScale = d3.scaleLinear()
  .domain([0, yMax])
  .range([height, 0]);
const tooltip = d3.select('#tooltip');
quarters.forEach((q, qi) => {
  const xOff = xScale(q);
  const barWidth = xScale.bandwidth();
  const subBand = d3.scaleBand()
    .domain(data.map(d => d.category))
    .range([0, barWidth])
    .padding(0.1);
  data.forEach((d, di) => {
    const barH = height - yScale(d[q]);
    svg.append('rect')
      .attr('class', 'bar')
      .attr('x', xOff + subBand(d.category))
      .attr('y', yScale(d[q]))
      .attr('width', subBand.bandwidth())
      .attr('height', barH)
      .attr('fill', palette[di])
      .attr('data-category', d.category)
      .attr('data-quarter', q)
      .attr('data-value', d[q])
      .on('mouseenter', function() {
        const rect = this.getBoundingClientRect();
        tooltip
          .style('left', (rect.left + rect.width / 2) + 'px')
          .style('top', (rect.top - 10) + 'px')
          .style('opacity', 1)
          .html(`<strong>${d.category}</strong> — ${q}: $${d[q]}K`);
      })
      .on('mouseleave', () => tooltip.style('opacity', 0));
  });
});
const xAxis = d3.axisBottom(xScale);
svg.append('g')
  .attr('class', 'axis')
  .attr('transform', `translate(0,${height})`)
  .call(xAxis)
  .append('text')
  .attr('x', width / 2)
  .attr('y', 40)
  .attr('fill', '#333')
  .attr('font-size', 13)
  .attr('text-anchor', 'middle')
  .text('Quarter');
const yAxis = d3.axisLeft(yScale).tickFormat(d => '$' + d + 'K');
svg.append('g')
  .attr('class', 'axis')
  .call(yAxis)
  .append('text')
  .attr('x', -40)
  .attr('y', 12)
  .attr('fill', '#333')
  .attr('font-size', 13)
  .attr('text-anchor', 'end')
  .attr('transform', 'rotate(-90)')
  .text('Revenue (USD K)');
const legend = svg.append('g')
  .attr('transform', `translate(0, ${height + 50})`);
data.forEach((d, i) => {
  const lg = legend.append('g')
    .attr('transform', `translate(${i * 130}, 0)`);
  lg.append('rect')
    .attr('width', 12)
    .attr('height', 12)
    .attr('fill', palette[i]);
  lg.append('text')
    .attr('x', 18)
    .attr('y', 11)
    .attr('font-size', 11)
    .attr('fill', '#555')
    .text(d.category);
});
</script>
</body>
</html>
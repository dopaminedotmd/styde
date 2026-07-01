requires: chart input data — type, data source, intended visual structure — none provided
missing specification. provide ChartInput with at least type and data fields before chart generation can proceed.
example valid input:
type: score-history
data:
  labels: [epoch 1, epoch 2, epoch 3, epoch 4, epoch 5]
  datasets:
    - label: Alpha
      values: [45, 62, 78, 85, 91]
    - label: Beta
      values: [32, 48, 55, 67, 73]
options:
  width: 400
  height: 200
  theme: light
  showLegend: true
supply your data and i render the svg inline — no files, no markdown, no wrapping
A generative Lissajous weave with evolving parameters, color-cycled stroke weights, and mouse interactivity.
p5.js sketch — save as index.html, open in browser:
```
<!DOCTYPE html>
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.4/p5.min.js"></script>
<style>body{margin:0;overflow:hidden;background:#0a0a0f}</style>
</head>
<body>
<script>
let t = 0;
let phase = 0;
let freqPairs;
function setup() {
  createCanvas(windowWidth, windowHeight);
  colorMode(HSB, 360, 100, 100, 100);
  freqPairs = [];
  for (let i = 0; i < 5; i++) {
    freqPairs.push({
      ax: random(1, 4),
      ay: random(1, 4),
      bx: random(1, 4),
      by: random(1, 4),
      dx: random(TWO_PI),
      dy: random(TWO_PI)
    });
  }
}
function draw() {
  background(0, 0, 5, 3);
  translate(width / 2, height / 2);
  let scale = min(width, height) * 0.38;
  let layers = floor(map(mouseX, 0, width, 3, 10));
  if (layers < 2) layers = 2;
  for (let l = 0; l < layers; l++) {
    let hueVal = (l * 35 + phase * 20) % 360;
    let alpha = map(l, 0, layers, 12, 4);
    let sw = map(l, 0, layers - 1, 1.2, 0.3);
    push();
    let rot = sin(phase * 0.2 + l * 0.5) * 0.1;
    rotate(rot);
    scale(1 + l * 0.008);
    let fp = freqPairs[l % freqPairs.length];
    let res = 180;
    let speed = 0.003 + mouseY * 0.000005;
    noFill();
    stroke(hueVal, 70, 85, alpha);
    strokeWeight(sw);
    beginShape();
    for (let i = 0; i <= res; i++) {
      let u = i / res;
      let ang = u * TWO_PI * 4 + t * speed;
      let x = sin(ang * fp.ax + fp.dx + phase * 0.1) *
              cos(ang * fp.bx * 0.5 + phase * 0.05);
      let y = cos(ang * fp.ay + fp.dy) *
              sin(ang * fp.by * 0.5);
      let r = scale * (0.6 + 0.4 * sin(ang * 0.5 + l));
      vertex(x * r, y * r);
    }
    endShape();
    pop();
  }
  t++;
  phase += 0.002;
}
function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
</script>
</body>
</html>
```
What it does:
- Lissajous-like parametric curves stacked in layers
- Layer count tracks mouseX (3–10 layers)
- Speed tracks mouseY
- Each layer has unique frequency pairs, phase offsets, and hue rotation
- Fading background produces trailing motion-blur
- Window responsive
Save as index.html, double-click to open. Mouse left/right changes complexity, up/down changes speed.
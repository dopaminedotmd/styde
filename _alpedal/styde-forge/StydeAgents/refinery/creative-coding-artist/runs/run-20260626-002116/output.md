Lissajous-weaving generative sketch. Complete self-contained HTML with p5.js from CDN.
Animated knot pattern. Sine-wave driven hue rotation. MouseX controls harmonic ratio. MouseY controls phase offset.
```
<!DOCTYPE html>
<html>
<head>
<style>body{margin:0;overflow:hidden;background:#0a0a0f}</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
</head>
<body>
<script>
let t=0;
function setup(){createCanvas(windowWidth,windowHeight);colorMode(HSB,360,100,100,100)}
function draw(){
  background(0,0,5);
  translate(width/2,height/2);
  let a=map(mouseX,0,width,1,8);
  let b=map(mouseY,0,height,1,8);
  let d=5;
  let mult=map(mouseX,0,width,1,5);
  noFill();
  for(let i=0;i<500;i++){
    let n=map(i,0,499,0,TWO_PI*mult);
    let x=sin(n*a+sin(t*0.3)*0.5)*180;
    let y=cos(n*b+cos(t*0.2)*0.5)*180;
    let hu=(n*180/PI+i*0.5+t*0.2)%360;
    stroke(hu,80,90,40);
    strokeWeight(1.2);
    ellipse(x,y,d,d);
    d+=0.04;
  }
  t+=0.015;
}
function windowResized(){resizeCanvas(windowWidth,windowHeight)}
</script>
</body>
</html>
```
Harmonic weaving. 500 orbiting points trace evolving Lissajous loops. Rotating hue gradient. Frame-by-frame drift from t accumulator. Save as .html, open in browser. Mouse left-right changes frequency ratio. Mouse up-down changes harmonic multiplier.
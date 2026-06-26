Mobile-first responsive layout system for a product showcase page.
Core grid: 4-column minmax on desktop, collapses to 2 at tablet, 1 at phone. 
html
<div class="showcase">
  <header class="showcase-header">
    <h1>Products</h1>
  </header>
  <div class="showcase-grid">
    <article class="product-card"></article>
    <article class="product-card"></article>
    <article class="product-card"></article>
    <article class="product-card"></article>
  </div>
</div>
css
/* Mobile-first base */
.showcase-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: clamp(1rem, 4vw, 2rem);
  padding: clamp(1rem, 3vw, 3rem);
}
/* Tablet: 40em = 640px */
@media (min-width: 40em) {
  .showcase-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
/* Desktop: 64em = 1024px */
@media (min-width: 64em) {
  .showcase-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
.product-card {
  container-type: inline-size;
  container-name: card;
  display: flex;
  flex-direction: column;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
/* Container query: when card is wide, side-by-side layout */
@container card (min-width: 300px) {
  .product-card {
    flex-direction: row;
  }
  .product-card img {
    width: 40%;
    height: auto;
  }
  .product-card-body {
    width: 60%;
  }
}
/* Fluid typography */
h1 {
  font-size: clamp(1.5rem, 5vw, 2.5rem);
  line-height: 1.1;
}
.product-card h2 {
  font-size: clamp(1rem, 3vw, 1.25rem);
}
.product-card p {
  font-size: clamp(0.875rem, 2vw, 1rem);
}
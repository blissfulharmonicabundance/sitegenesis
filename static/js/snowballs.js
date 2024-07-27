// Get the SVG element
const starfield = document.getElementById('starfield');

// Define the star properties
const starCount = 100;
const starSize = 2;
const starColor = '#fff';
const starSpeed = 0.1;

// Create the stars
for (let i = 0; i < starCount; i++) {
  const star = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  star.setAttribute('cx', Math.random() * 100);
  star.setAttribute('cy', Math.random() * 100);
  star.setAttribute('r', starSize);
  star.setAttribute('fill', starColor);
  starfield.appendChild(star);
}

// Animate the stars
function animate() {
  for (let i = 0; i < starCount; i++) {
    const star = starfield.children[i];
    const x = parseFloat(star.getAttribute('cx')) + Math.random() * starSpeed;
    const y = parseFloat(star.getAttribute('cy')) + Math.random() * starSpeed;
    star.setAttribute('cx', x);
    star.setAttribute('cy', y);
  }
  requestAnimationFrame(animate);
}

animate();
const sections = document.querySelectorAll('.sections');

// Function to find the nearest section
function findNearestSection(scrollPosition) {
    let nearestSection = sections[0];
    let shortestDistance = Math.abs(scrollPosition - sections[0].offsetTop);

    sections.forEach(section => {
        const distance = Math.abs(scrollPosition - section.offsetTop);
        if (distance < shortestDistance) {
            shortestDistance = distance;
            nearestSection = section;
        }
    });

    return nearestSection;
}

// Smooth snap scrolling
function snapScroll() {
    const scrollPosition = window.scrollY;
    const nearestSection = findNearestSection(scrollPosition);
    nearestSection.scrollIntoView({ behavior: 'smooth' });
}

// Event listener for scroll
let isScrolling = false;

window.addEventListener('scroll', () => {
    if (!isScrolling) {
        isScrolling = true;
        snapScroll();
        setTimeout(() => {
            isScrolling = false;
        }, 100); // Adjust this value to control the delay between scrolls
    }
});

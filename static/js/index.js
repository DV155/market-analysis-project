const factorList = [];
const elementList = document.getElementsByClassName("toBeLookedThrough");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
for (element of elementList) {
    const values = parseFloat(element.dataset.value);
    if (reduceMotion) { // Show the final number straight away instead of counting up
        element.textContent = values.toFixed(2);
        continue;
    }
    const counter = new countUp.CountUp(element.id, values, { decimalPlaces: 2, duration: 1.2 });
    counter.start();
    
}
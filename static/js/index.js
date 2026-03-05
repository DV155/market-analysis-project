const factorList = [];
const elementList = document.getElementsByClassName("toBeLookedThrough");
for (element of elementList) {
    const values = parseFloat(element.dataset.value);
    const counter = new countUp.CountUp(element.id, values, { decimalPlaces: 2 });
    counter.start();
    
}
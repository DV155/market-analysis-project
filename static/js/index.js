const value1 = parseFloat(document.getElementById('foodCounter').dataset.value);
const food = new countUp.CountUp('foodCounter', value1, { decimalPlaces: 2 });
const value2 = parseFloat(document.getElementById('edCounter').dataset.value);
const edu = new countUp.CountUp('edCounter', value2, { decimalPlaces: 2 });
const value3 = parseFloat(document.getElementById('hpCounter').dataset.value);
const health = new countUp.CountUp('hpCounter', value3, { decimalPlaces: 2 });
factorList = [food, edu, health];
for (factor of factorList) {
    factor.start();
}
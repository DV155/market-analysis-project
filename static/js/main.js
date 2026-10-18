function save() {
    var inValue;
    inValue = document.getElementById("inValue").value;
    document.getElementById("inputVar").innerText = inValue;
    const priceFactor = parseFloat(document.getElementById("inValue").dataset.factor);
    const outValue = (inValue * priceFactor).toFixed(2);
    document.getElementById("outputVar").innerText = outValue;
}
function save() {
    var inValue;
    inValue = document.getElementById("inValue").value;
    document.getElementById("inputVar").innerText = inValue;
    outValue = (inValue * 1.387).toFixed(2);
    document.getElementById("outputVar").innerText = outValue;
}
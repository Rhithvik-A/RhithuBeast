function handleInput() {
    let selectOperation = document.querySelector('input[name="operation"]:checked');
    if (!selectOperation) {
        document.getElementById('final_output').innerText = "Please select an operation.";
        return;
    }

    let input1 = document.getElementById('num1').value;
    if (!input1) {
        document.getElementById('final_output').innerText = "Please enter the first number.";
        return;
    }

    let input2 = document.getElementById('num2').value;
    if (!input2) {
        document.getElementById('final_output').innerText = "Please enter the second number.";
        return;
    }

    let num1 = parseFloat(input1);
    let num2 = parseFloat(input2);

    let operation = selectOperation.value;
    let output;

    if (operation === "addition") {
        output = num1 + num2;
    } else if (operation === "subtraction") {
        output = num1 - num2;
    } else if (operation === "multiplication") {
        output = num1 * num2;
    } else {
        output = "Invalid operation.";
    }

    document.getElementById('final_output').innerText = `Result: ${output}`;
}

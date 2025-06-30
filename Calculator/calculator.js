function textgiver(num_op) {
    document.getElementById('text').value += num_op;
}

function evaluate_expression() {
    try {
        const expression = document.getElementById('text').value;
        const ans = eval(expression); 
        document.getElementById('text').value = ans;
    } catch (error) {
        alert("!33#wag$$+^*ERROR^ERROR");
        document.getElementById('text').value = "";
    }
}

function reset() {
    document.getElementById('text').value = "";
}

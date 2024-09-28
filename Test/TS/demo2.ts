function addNumbers(num1: number, num2: number): number {
    return num1 + num2;
}

let x = Math.random() * 100
let y = Math.random() * 100
let result = addNumbers(Math.floor(x), Math.floor(y));
console.log("The sum is:", result);
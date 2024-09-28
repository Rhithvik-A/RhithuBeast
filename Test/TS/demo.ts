let h: boolean = false;
let n1 = Math.random() * 100;

if (n1 >= 1 && n1 < 50) {
    h = true;
    console.log('The number is between 1 & 50');
} else {
    h = false;
    console.log('The number is between 50 & 100');
}

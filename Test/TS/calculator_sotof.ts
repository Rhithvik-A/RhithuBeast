let x = Math.floor(Math.random() * 100);
let z = Math.floor(Math.random() * 100);
let y = Math.floor(Math.random() * 3 + 1);
let ans: number;

if (y === 1) {
    ans = x + z;
    console.log(`${x} + ${z}`);
    setTimeout(() => {
        console.log(ans);
    }, 10000);
} else if (y === 2) {
    ans = x - z;
    console.log(`${x} - ${z}`);
    setTimeout(() => {
        console.log(ans);
    }, 10000);
} else if (y === 3) {
    ans = x * z;
    console.log(`${x} * ${z}`);
    setTimeout(() => {
        console.log(ans);
    }, 10000);
}
/************************************************FINISHED*****************************************************/

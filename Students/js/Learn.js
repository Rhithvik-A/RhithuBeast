let a = Math.floor(Math.random() * 100) + 1;
let b = Math.floor(Math.random() * 100) + 1;
let c = Math.floor(Math.random() * 3) + 1;
if (c === 1) {
   c = "+" ;
   let d = a + b;
}
if (c === 2) {
    c = "-";
    let d = a - b;
 }
 if (c === 3) {
    c = "*"; 
    let d = a * b;
 }
console.log(a);
console.log(c);
console.log(b);
setTimeout(function() {
    console.log();
  }, 2000);
  console.log(d);

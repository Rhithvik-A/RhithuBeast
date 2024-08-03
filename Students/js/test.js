/*let person = {
    name: 'rhithvik',
    age: 30
};
console.log(person);
*/
let person = ['Rhithvik', 'Ashok'];

console.log(person[0]);  // Output: Rhithvik (immediately)

setTimeout(() => {
  console.log(person[1]); // Output: Ashok (after 2 seconds)
}, 2000);

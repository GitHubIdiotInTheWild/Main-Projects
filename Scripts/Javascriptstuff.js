// Variables and Constants
let greeting = "Hello, World!";
const pi = 3.14159;

// Functions
function add(a, b) {
    return a + b;
}

function greet(name) {
    return `${greeting} My name is ${name}.`;
}

// Objects
let person = {
    firstName: "John",
    lastName: "Doe",
    age: 30,
    fullName: function() {
        return `${this.firstName} ${this.lastName}`;
    }
};

// Arrays
let fruits = ["Apple", "Banana", "Cherry"];
fruits.push("Date");

// Loops
for (let i = 0; i < fruits.length; i++) {
    console.log(fruits[i]);
}

fruits.forEach(function(fruit) {
    console.log(fruit);
});

for (let fruit of fruits) {
    console.log(fruit);
}

// Conditionals
if (person.age > 18) {
    console.log("Adult");
} else {
    console.log("Not an adult");
}

// ES6 Features
const arrowAdd = (a, b) => a + b;

let numbers = [1, 2, 3, 4, 5];
let squares = numbers.map(n => n * n);

// Promises and Async/Await
function asyncFunction() {
    return new Promise((resolve, reject) => {
        setTimeout(() => resolve("Async Function Result"), 1000);
    });
}

async function exampleAsync() {
    let result = await asyncFunction();
    console.log(result);
}

exampleAsync();

// Classes
class Animal {
    constructor(name) {
        this.name = name;
    }

    speak() {
        console.log(`${this.name} makes a noise.`);
    }
}

class Dog extends Animal {
    speak() {
        console.log(`${this.name} barks.`);
    }
}

let dog = new Dog("Rex");
dog.speak();

// DOM Manipulation
document.addEventListener("DOMContentLoaded", () => {
    let div = document.createElement("div");
    div.textContent = greet("John Doe");
    document.body.appendChild(div);

    let ul = document.createElement("ul");
    fruits.forEach(fruit => {
        let li = document.createElement("li");
        li.textContent = fruit;
        ul.appendChild(li);
    });
    document.body.appendChild(ul);
});

// Event Handling
document.addEventListener("click", () => {
    console.log("document was clicked");
});

// Fetch API
fetch("https://jsonplaceholder.typicode.com/posts")
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error("Error:", error));

// Local Storage
localStorage.setItem("greeting", greeting);
let storedGreeting = localStorage.getItem("greeting");
console.log(storedGreeting);

// Error Handling
try {
    throw new Error("something went wrong");
} catch (error) {
    console.error(error.message);
} finally {
    console.log("this will run regardless of the error");
}

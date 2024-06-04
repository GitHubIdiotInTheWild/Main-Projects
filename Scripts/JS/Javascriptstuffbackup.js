
let greeting = "Hello, World!";
const pi = 3.14159;


function add(a, b) {
    return a + b;
}

function greet(name) {
    return `${greeting} My name is ${name}.`;
}


let person = {
    firstName: "John",
    lastName: "Doe",
    age: 30,
    fullName: function() {
        return `${this.firstName} ${this.lastName}`;
    }
};


let fruits = ["Apple", "Banana", "Cherry"];
fruits.push("Date");


for (let i = 0; i < fruits.length; i++) {
    console.log(fruits[i]);
}

fruits.forEach(function(fruit) {
    console.log(fruit);
});

for (let fruit of fruits) {
    console.log(fruit);
}


if (person.age > 18) {
    console.log("Adult");
} else {
    console.log("Not an adult");
}


const arrowAdd = (a, b) => a + b;

let numbers = [1, 2, 3, 4, 5];
let squares = numbers.map(n => n * n);


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


class somethingeer {
    constructor(name) {
        this.name = name;
    }

    speak() {
        console.log(`${this.name} makes a noise.`);
    }
}

class somethingeer01 extends somethingeer {
    speak() {
        console.log(`${this.name} barks.`);
    }
}

let domeera = new somethingeer01("black");
domeera.speak();


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


document.addEventListener("click", () => {
    console.log("document was clicked");
});


fetch("https://jsonplaceholder.typicode.com/posts")
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error("Error:", error));


localStorage.setItem("greeting", greeting);
let storedGreeting = localStorage.getItem("greeting");
console.log(storedGreeting);


try {
    throw new Error("something went wrong");
} catch (error) {
    console.error(error.message);
} finally {
    console.log("this will run regardless of the error");
}

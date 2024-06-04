


class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    
    greet() {
        console.log(`Hello, my name is ${this.name} and I am ${this.age} years old.`);
    }
}


const person1 = new Person('Alice', 30);
const person2 = new Person('Bob', 25);


person1.greet();
person2.greet();


const { name, age } = person1;
console.log(`Destructuring assignment: Name - ${name}, Age - ${age}`);


const add = (a, b) => a + b;
console.log(`Arrow function result: ${add(5, 3)}`);


const product = 'Laptop';
const price = 999;
console.log(`Template literal: The price of ${product} is $${price}`);


async function fetchData() {
    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/posts/1');
        const data = await response.json();
        console.log('Async/await data:', data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

fetchData();


function fetchDataWithPromise() {
    return new Promise((resolve, reject) => {
        fetch('https://jsonplaceholder.typicode.com/posts/1')
            .then(response => response.json())
            .then(data => resolve(data))
            .catch(error => reject(error));
    });
}

fetchDataWithPromise()
    .then(data => console.log('promise data:', data))
    .catch(error => console.error('promise error:', error));


const map = new Map();
map.set('key1', 'value1');
map.set('key2', 'value2');
console.log('map example:', map.get('key1'));

// Use Set data structure
const set = new Set([1, 2, 3, 4, 5]);
console.log('set example:', set.has(3));


const immutableobject = Object.freeze({ prop1: 'value1', prop2: 'value2' });

immutableobject.prop1 = 'updatedvalue';
console.log('immutable object:', immutableobject);

// Use try-catch-finally for error handling
function divide(a, b) {
    try {
        if (b === 0) {
            throw new Error('division by zero');
        }
        return a / b;
    } catch (error) {
        console.error('error:', error.message);
    } finally {
        console.log('finally block executed');
    }
}

console.log('division result:', divide(10, 2));
console.log('division result:', divide(10, 0));

// Use generators
function* generatorFunction() {
    yield '01';
    yield '02';
    yield '03';
}

const generator = generatorFunction();
console.log('Generator example:', generator.next().value);

// Use Proxy for meta-programming
const handler = {
    get: function(target, prop) {
        return prop in target ? target[prop] : 'Property does not exist';
    }
};

const proxy = new Proxy({ prop1: 'value1' }, handler);
console.log('proxy example:', proxy.prop1);
console.log('proxy example:', proxy.prop2);

// Use BigInt for arbitrary precision integers
const bigintValue = 1234567890123456789012345678901234567890n;
console.log('bigint example:', bigIntValue);

// Use dynamic import for lazy loading modules
async function dynamicImportExample() {
    const module = await import('./module.js');
    module.default();
}

dynamicImportExample();


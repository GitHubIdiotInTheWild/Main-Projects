
class Utility<T extends number | string> {
    private data: Map<string, T[]> = new Map();

    public addData(key: string, values: T[]): void {
        if (!this.data.has(key)) {
            this.data.set(key, []);
        }
        const dataList = this.data.get(key);
        if (dataList) {
            dataList.push(...values);
        }
    }

    public getData(key: string): T[] | undefined {
        return this.data.get(key);
    }

    public complexcalcperformancetest(arr: number[]): number {
        return arr.reduce((acc, curr, index) => acc + curr * (index + 1), 0);
    }

    public generatefibonaccisequence(limit: number): number[] {
        const fibonacci: number[] = [0, 1];
        while (fibonacci[fibonacci.length - 1] + fibonacci[fibonacci.length - 2] <= limit) {
            fibonacci.push(fibonacci[fibonacci.length - 1] + fibonacci[fibonacci.length - 2]);
        }
        return fibonacci;
    }

    public stringoperationperformancetest(str: string): string {
        return str
            .split('')
            .map((char) => (char.match(/[a-zA-Z]/) ? String.fromCharCode(char.charCodeAt(0) + 1) : char))
            .join('');
    }
}

 
class exception01 extends Error {
    constructor(message: string) {
        super(message);
        this.name = 'exception01';
    }
}


class datastructure01<T extends number | string> {
    private utility: Utility<T>;

    constructor() {
        this.utility = new Utility<T>();
    }

    public addData(key: string, values: T[]): void {
        this.utility.addData(key, values);
    }

    public performComplexOperation(key: string): number {
        try {
            const arr = this.utility.getData(key) || [];
            if (arr.every((val) => typeof val === 'number')) {
                return this.utility.complexcalcperformancetest(arr as number[]);
            } else {
                throw new exception01('data is not of type number');
            }
        } catch (error) {
            throw new exception01('key not found in the data structure');
        }
    }
}


const dataStructure = new datastructure01<number>();


dataStructure.addData('key1', [1, 2, 3, 4, 5]);
dataStructure.addData('key2', [6, 7, 8, 9, 10]);

try {
    
    const result = dataStructure.performComplexOperation('key1');
    console.log('result of the operation:', result);
} catch (error) {
    console.error('an error occurred:', error.message);
}


const fibonaccisequence = new Utility<number>().generatefibonaccisequence(50);
console.log('fibonacci sequence up to 50:', fibonaccisequence);


const inputString = 'hello world';
const modifiedString = new Utility<string>().stringoperationperformancetest(inputString);
console.log('Modified String:', modifiedString);

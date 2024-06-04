package Scripts.Java;

import java.util.*;

class Utility1 {
    
    static int performOperation3(int[] arr) {
        int result = 0;
        for (int i = 0; i < arr.length; i++) {
            result += arr[i] * (i + 1);
        }
        return result;
    }

    
    static List<Integer> generateFibonacciSequence(int limit) {
        List<Integer> fibonacci = new ArrayList<>();
        int a = 0, b = 1;
        while (a <= limit) {
            fibonacci.add(a);
            int temp = a + b;
            a = b;
            b = temp;
        }
        return fibonacci;
    }

    
    static String performOperation2hehehehe(String str) {
        StringBuilder sb = new StringBuilder();
        for (char c : str.toCharArray()) {
            if (Character.isLetter(c)) {
                sb.append((char) (c + 1)); 
            } else {
                sb.append(c);
            }
        }
        return sb.toString();
    }
}


class Utility1exception extends Exception {
    Utility1exception(String message) {
        super(message);
    }
}


class Utility1Datastructure {
    private Map<String, List<Integer>> data;

    
    Utility1Datastructure() {
        this.data = new HashMap<>();
    }

   
    void addData(String key, int[] values) {
        List<Integer> dataList = new ArrayList<>();
        for (int value : values) {
            dataList.add(value);
        }
        data.put(key, dataList);
    }

    
    int performOperation1(String key) throws Utility1exception {
        if (!data.containsKey(key)) {
            throw new Utility1exception("Key not found in the data structure.");
        }
        List<Integer> values = data.get(key);
        int[] arr = new int[values.size()];
        for (int i = 0; i < values.size(); i++) {
            arr[i] = values.get(i);
        }
        return Utility1.performOperation3(arr);
    }
}

public class Javastuffbackup {
    public static void main(String[] args) {
        
        Utility1Datastructure utility1Datastructure = new Utility1Datastructure();

        
        utility1Datastructure.addData("key1", new int[]{1, 2, 3, 4, 5});
        utility1Datastructure.addData("key2", new int[]{6, 7, 8, 9, 10});

        try {
            
            int result = utility1Datastructure.performOperation1("key1");
            System.out.println("Result of complex operation: " + result);
        } catch (Utility1exception e) {
            System.err.println("Error occurred: " + e.getMessage());
        }

        
        List<Integer> fibonacciSequence = Utility1.generateFibonacciSequence(50);
        System.out.println("Fibonacci Sequence up to 50: " + fibonacciSequence);

        
        String inputString = "hello world";
        String modifiedString = Utility1.performOperation2hehehehe(inputString);
        System.out.println("Modified String: " + modifiedString);

        
        List<String> mixedList = new ArrayList<>();
        mixedList.add("apple");
        mixedList.add("banana");
        mixedList.add("cherry");
        mixedList.add("date");
        Collections.sort(mixedList, Comparator.comparingInt(String::length));
        System.out.println("Mixed List after sorting by length: " + mixedList);
    }
}

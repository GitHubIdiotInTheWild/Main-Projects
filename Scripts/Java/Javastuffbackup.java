package Scripts.Java;

import java.util.*;

class Utility {
    
    static int operation3performancetest(int[] arr) {
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

    
    static String operation2performancetest(String str) {
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


class UtilityException extends Exception {
    UtilityException(String message) {
        super(message);
    }
}


class MainDataStructure01 {
    private Map<String, List<Integer>> data;

    
    MainDataStructure01() {
        this.data = new HashMap<>();
    }

   
    void addData(String key, int[] values) {
        List<Integer> dataList = new ArrayList<>();
        for (int value : values) {
            dataList.add(value);
        }
        data.put(key, dataList);
    }

    
    int operation1performancetest(String key) throws UtilityException {
        if (!data.containsKey(key)) {
            throw new UtilityException("Key not found in the data structure");
        }
        List<Integer> values = data.get(key);
        int[] arr = new int[values.size()];
        for (int i = 0; i < values.size(); i++) {
            arr[i] = values.get(i);
        }
        return Utility.operation3performancetest(arr);
    }
}

public class Javastuffbackup {
    public static void main(String[] args) {
        
        MainDataStructure01 maindatastructure01 = new MainDataStructure01();

        
        maindatastructure01.addData("key1", new int[]{1, 2, 3, 4, 5});
        maindatastructure01.addData("key2", new int[]{6, 7, 8, 9, 10});

        try {
            
            int result = maindatastructure01.operation1performancetest("key1");
            System.out.println("Result of a complex operation: " + result);
        } catch (UtilityException e) {
            System.err.println("An error occurred: " + e.getMessage());
        }

        
        List<String> list = new ArrayList<>();
        list.add("test01");
        list.add("test02");
        list.add("test03");
        list.add("test04");
        Collections.sort(list, Comparator.comparingInt(String::length));
        System.out.println("List after sorting by length: " + list);

        
        List<Integer> fibonacciSequence = Utility.generateFibonacciSequence(50);
        System.out.println("Fibonacci Sequence up to 50: " + fibonacciSequence);

        
        String inputString = "hello world";
        String modifiedString = Utility.operation2performancetest(inputString);
        System.out.println("Modified String: " + modifiedString);
    }
}

### Using C/C++ from Python

Creating dynamically linked libraries in C/C++: <http://www.cs.swarthmore.edu/~newhall/unixhelp/howto_C_libraries.html>  

Basically put multiple `.o` files into one `.so` file (shared object, or `.dylib` for Mac), which can then be linked using `-l`, and `-L`.  

Using C++ libraries within Python without 3rd party dependencies:    
<http://stackoverflow.com/questions/145270/calling-c-c-from-python>
<http://stackoverflow.com/questions/23713949/how-to-expose-c-class-to-python-without-using-boost>
<https://www.safaribooksonline.com/library/view/c-cookbook/0596007612/ch01s05.html>

Using this `.so` file to contain the library, the library can then be imported to Python using `extern "C"` functions, a C interface to communicate with these C++ objects. Once the interface is written and the `.so` file is compiled, wrapper Python classes/function can be written using Python's "natural" `ctypes`.

Example `hello.h` with C interface:

```C++

	#include <iostream>
	
	std::string* makeHelloWorld();
	
	extern "C" {
	
		std::string* externFunction() {
			return makeHelloWorld();
		}
	
	}
	
	
```

`hello.cpp` file with `makeHelloWorld()` definition:

```C++

	#include "hello.h"
	
	std::string* makeHelloWorld() {
			std::string* result = new std::string("Hello World!");
			return result;
	}
	
```



Python script that uses the C++ code:

```Python     
	# Get cdll and other C data types for Python
	from ctypes import *  
    # Open library, either `.so` or `.dylib` file (Linux or Mac)
   	library = cdll.LoadLibrary('path to .so file')   
     
    # Use extern "C" function, must declare it's C return type  
    library.externFunction.restype = c_void_p  
    library.externFunction()   
```
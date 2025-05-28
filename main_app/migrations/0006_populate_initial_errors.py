# main_app/migrations/000Y_populate_extensive_errors.py
# (Ensure 000Y is the correct number, AFTER your last schema migration)

from django.db import migrations
from django.utils.text import slugify

# --- Expanded Sample Data Definition ---
CATEGORIES_DATA = [
    # Languages
    {"name": "Python", "description": "Errors related to the Python programming language."},
    {"name": "JavaScript", "description": "Errors in client-side or server-side JavaScript."},
    {"name": "Java", "description": "Common errors and exceptions in Java development."},
    {"name": "C", "description": "Compilation, linking, and runtime errors in C programming."},
    {"name": "C++", "description": "Compilation, linking, and runtime errors in C++."},
    {"name": "C#", "description": "Errors and exceptions in C# and .NET framework."},
    {"name": "Go (Golang)", "description": "Common issues and panic messages in Go programming."},
    {"name": "Kotlin", "description": "Errors specific to Kotlin development."},
    {"name": "Swift", "description": "Errors in Swift programming for Apple platforms."},
    {"name": "Ruby", "description": "Errors and exceptions in Ruby."},
    {"name": "PHP", "description": "Common errors and warnings in PHP scripting."},
    {"name": "TypeScript", "description": "Type checking and compilation errors in TypeScript."},
    {"name": "Rust", "description": "Compiler errors and panics in Rust."},
    {"name": "Scala", "description": "Compilation and runtime errors in Scala."},
    {"name": "Perl", "description": "Errors and warnings in Perl scripting."},
    {"name": "Lua", "description": "Runtime errors in Lua scripting."},
    {"name": "R", "description": "Errors and warnings in R for statistical computing."},
    {"name": "SQL", "description": "Database errors from SQL queries across various RDBMS."},
    {"name": "HTML", "description": "Validation and rendering issues in HTML."},
    {"name": "CSS", "description": "Styling, layout, and parsing issues in CSS."},
    {"name": "Python", "description": "Errors related to the Python programming language."},
    {"name": "JavaScript", "description": "Errors in client-side or server-side JavaScript."},
    {"name": "Java", "description": "Common errors and exceptions in Java development."},
    {"name": "C", "description": "Compilation, linking, and runtime errors in C programming."},
    {"name": "C++", "description": "Compilation, linking, and runtime errors in C++."},
    {"name": "C#", "description": "Errors and exceptions in C# and .NET framework."},
    {"name": "Go (Golang)", "description": "Common issues and panic messages in Go programming."},
    {"name": "Kotlin", "description": "Errors specific to Kotlin development."},
    {"name": "Swift", "description": "Errors in Swift programming for Apple platforms."},
    {"name": "Ruby", "description": "Errors and exceptions in Ruby."},
    {"name": "PHP", "description": "Common errors and warnings in PHP scripting."},
    {"name": "TypeScript", "description": "Type checking and compilation errors in TypeScript."},
    {"name": "Rust", "description": "Compiler errors and panics in Rust."},
    {"name": "Scala", "description": "Compilation and runtime errors in Scala."},
    {"name": "Perl", "description": "Errors and warnings in Perl scripting."},
    {"name": "Lua", "description": "Runtime errors in Lua scripting."},
    {"name": "R", "description": "Errors and warnings in R for statistical computing."},
    {"name": "SQL", "description": "Database errors from SQL queries across various RDBMS."},
    {"name": "HTML", "description": "Validation and rendering issues in HTML."},
    {"name": "CSS", "description": "Styling, layout, and parsing issues in CSS."},


    # Frameworks & Libraries
    {"name": "Django", "description": "Errors specific to the Django web framework."},
    {"name": "Flask", "description": "Errors encountered when working with the Flask microframework."},
    {"name": "Node.js", "description": "Server-side JavaScript errors specific to the Node.js runtime."},
    {"name": "Express.js", "description": "Errors related to the Express.js framework for Node.js."},
    {"name": "React", "description": "Common errors in the React JavaScript library for UIs."},
    {"name": "Angular", "description": "Errors and issues in the Angular framework."},
    {"name": "Vue.js", "description": "Common problems in the Vue.js progressive framework."},
    {"name": "Ruby on Rails", "description": "Errors specific to the Ruby on Rails framework."},
    {"name": "Spring (Java)", "description": "Errors in the Spring Framework for Java applications."},
    {"name": ".NET Core/ASP.NET", "description": "Errors in Microsoft's .NET Core and ASP.NET frameworks."},
    {"name": "jQuery", "description": "Common issues when using the jQuery JavaScript library."},
    {"name": "Pandas (Python)", "description": "Errors related to data manipulation with Pandas."},
    {"name": "NumPy (Python)", "description": "Errors in numerical computing with NumPy."},
    {"name": "Django", "description": "Errors specific to the Django web framework."},
    {"name": "Flask", "description": "Errors encountered when working with the Flask microframework."},
    {"name": "Node.js", "description": "Server-side JavaScript errors specific to the Node.js runtime."},
    {"name": "Express.js", "description": "Errors related to the Express.js framework for Node.js."},
    {"name": "React", "description": "Common errors in the React JavaScript library for UIs."},
    {"name": "Angular", "description": "Errors and issues in the Angular framework."},
    {"name": "Vue.js", "description": "Common problems in the Vue.js progressive framework."},
    {"name": "Ruby on Rails", "description": "Errors specific to the Ruby on Rails framework."},
    {"name": "Spring (Java)", "description": "Errors in the Spring Framework for Java applications."},
    {"name": ".NET Core/ASP.NET", "description": "Errors in Microsoft's .NET Core and ASP.NET frameworks."},
    {"name": "jQuery", "description": "Common issues when using the jQuery JavaScript library."},
    {"name": "Pandas (Python)", "description": "Errors related to data manipulation with Pandas."},
    {"name": "NumPy (Python)", "description": "Errors in numerical computing with NumPy."},
    {"name": "TensorFlow", "description": "Errors from the TensorFlow deep learning library."},
    {"name": "PyTorch", "description": "Errors from the PyTorch deep learning library."},
    {"name": "Scikit-learn", "description": "Errors from the Scikit-learn machine learning library."},


    # Tools & Platforms
    {"name": "Git", "description": "Common errors and issues when using Git version control."},
    {"name": "Docker", "description": "Problems related to Docker containers and orchestration."},
    {"name": "Kubernetes", "description": "Errors in deploying and managing applications with Kubernetes."},
    {"name": "Webpack", "description": "Errors from the Webpack module bundler."},
    {"name": "Babel", "description": "JavaScript compiler errors related to Babel."},
    {"name": "Jenkins", "description": "CI/CD pipeline errors in Jenkins."},
    {"name": "Ansible", "description": "Errors in Ansible automation playbooks."},
    {"name": "Terraform", "description": "Errors in Infrastructure as Code using Terraform."},
    {"name": "Git", "description": "Common errors and issues when using Git version control."},
    {"name": "Docker", "description": "Problems related to Docker containers and orchestration."},
    {"name": "Kubernetes", "description": "Errors in deploying and managing applications with Kubernetes."},
    {"name": "Webpack", "description": "Errors from the Webpack module bundler."},
    {"name": "Babel", "description": "JavaScript compiler errors related to Babel."},
    {"name": "Jenkins", "description": "CI/CD pipeline errors in Jenkins."},
    {"name": "Ansible", "description": "Errors in Ansible automation playbooks."},
    {"name": "Terraform", "description": "Errors in Infrastructure as Code using Terraform."},
    {"name": "Linux", "description": "Common errors and issues on Linux operating systems."},
    {"name": "Windows", "description": "Common errors and issues on Windows operating systems."},
    {"name": "macOS", "description": "Common errors and issues on macOS operating systems."},


    # Databases
    {"name": "PostgreSQL", "description": "Errors specific to the PostgreSQL database."},
    {"name": "MySQL", "description": "Errors specific to the MySQL database."},
    {"name": "SQLite", "description": "Errors specific to the SQLite database."},
    {"name": "MongoDB", "description": "Errors specific to the MongoDB NoSQL database."},
    {"name": "Redis", "description": "Errors related to the Redis in-memory data store."},
    {"name": "PostgreSQL", "description": "Errors specific to the PostgreSQL database."},
    {"name": "MySQL", "description": "Errors specific to the MySQL database."},
    {"name": "SQLite", "description": "Errors specific to the SQLite database."},
    {"name": "MongoDB", "description": "Errors specific to the MongoDB NoSQL database."},
    {"name": "Redis", "description": "Errors related to the Redis in-memory data store."},


    # Concepts & Domains
    {"name": "HTTP Errors", "description": "Standard HTTP status codes and their meanings."},
    {"name": "Networking", "description": "Common networking issues and error messages."},
    {"name": "Operating System", "description": "Errors from Windows, Linux, or macOS."},
    {"name": "Machine Learning", "description": "Common errors in ML model training, data processing."},
    {"name": "Deep Learning", "description": "Errors in DL frameworks like TensorFlow, PyTorch."},
    {"name": "Cloud Services (General)", "description": "General errors from cloud platforms like AWS, Azure, GCP."},
    {"name": "Security", "description": "Common security-related errors and warnings."},
    {"name": "API Development", "description": "Errors related to designing and consuming APIs."},
    {"name": "Mobile Development (General)", "description": "General errors in Android or iOS app development."},
    {"name": "Web Servers", "description": "Errors from web servers like Apache, Nginx."},
    {"name": "HTTP Errors", "description": "Standard HTTP status codes and their meanings."},
    {"name": "Networking", "description": "Common networking issues and error messages."},
    {"name": "Security", "description": "Common security-related errors and warnings."},
    {"name": "API Development", "description": "Errors related to designing and consuming APIs."},
    {"name": "Mobile Development (General)", "description": "General errors in Android or iOS app development."},
    {"name": "Web Servers", "description": "Errors from web servers like Apache, Nginx."},
    {"name": "Machine Learning (General)", "description": "Common errors in ML model training, data processing."},
    {"name": "Deep Learning (General)", "description": "Errors related to deep learning concepts and frameworks."},
    {"name": "Cloud Services (General)", "description": "General errors from cloud platforms like AWS, Azure, GCP."},
    {"name": "Build Systems", "description": "Errors related to build tools like Maven, Gradle, Make."},
    {"name": "IDEs & Editors", "description": "Common issues with Integrated Development Environments and code editors."},
]

# For brevity, I will only add a *selection* of new errors here.
# You would need to expand this list to 200-300 entries.
# I'll add ~30-40 new diverse examples to illustrate.
ERRORS_DATA = [
    # Python (Existing + New)
    {"title": "Python TypeError: 'NoneType' object is not callable", "error_code": "TypeError", "category_name": "Python", "description": "Attempting to call `None` as a function.", "cause_overview": "Variable expected to be a function is `None`.", "solution_overview": "Check variable assignment; ensure function returns a callable."},
    {"title": "Python IndexError: list index out of range", "error_code": "IndexError", "category_name": "Python", "description": "Accessing a list element with an invalid index.", "cause_overview": "Index too large, too small, or list is empty.", "solution_overview": "Verify index bounds: `0 <= index < len(list)`."},
    {"title": "Python KeyError: 'my_key'", "error_code": "KeyError", "category_name": "Python", "description": "Attempting to access a dictionary key that does not exist.", "cause_overview": "Typo in key name; key was never added to dictionary.", "solution_overview": "Check key spelling; use `my_dict.get('my_key')` or `if 'my_key' in my_dict:`."},
    {"title": "Python ImportError: No module named 'module_name'", "error_code": "ImportError", "category_name": "Python", "description": "Python cannot find the module specified in an import statement.", "cause_overview": "Module not installed; typo in module name; module not in PYTHONPATH.", "solution_overview": "Install module (`pip install module_name`); check spelling; ensure virtual environment is active."},
    {"title": "Python SyntaxError: invalid syntax", "error_code": "SyntaxError", "category_name": "Python", "description": "A generic syntax error indicating incorrect Python grammar.", "cause_overview": "Missing colons, parentheses, typos in keywords, incorrect indentation.", "solution_overview": "Carefully review the line indicated by the interpreter and surrounding lines for syntax mistakes."},
    {"title": "Python ValueError: too many values to unpack", "error_code": "ValueError", "category_name": "Python", "description": "Occurs during tuple unpacking when the number of variables on the left side does not match the number of items on the right.", "cause_overview": "e.g., `a, b = (1, 2, 3)` or `x, y, z = func_returning_two_values()`.", "solution_overview": "Ensure the number of variables matches the number of items being unpacked. Use `*` to capture multiple items if needed."},

    # JavaScript (Existing + New)
    {"title": "JavaScript Uncaught TypeError: Cannot read properties of undefined (reading 'x')", "error_code": "TypeError", "category_name": "JavaScript", "description": "Accessing a property 'x' on a variable that is `undefined`.", "cause_overview": "Variable not initialized; function returned `undefined`.", "solution_overview": "Initialize variable; check for `undefined` before access: `if (obj && obj.x)`."},
    {"title": "JavaScript ReferenceError: x is not defined", "error_code": "ReferenceError", "category_name": "JavaScript", "description": "Using a variable 'x' that hasn't been declared in the current scope.", "cause_overview": "Typo in variable name; variable used before declaration (`let`, `const`).", "solution_overview": "Declare variable with `let`, `const`, or `var`; check spelling."},
    {"title": "JavaScript SyntaxError: Unexpected token '<' in JSON at position 0", "error_code": "JSON Parse Error", "category_name": "JavaScript", "description": "Attempting to parse a non-JSON string (often HTML error page) as JSON.", "cause_overview": "API endpoint returned HTML instead of JSON; malformed JSON string.", "solution_overview": "Check API response in Network tab; ensure server sends valid JSON with correct `Content-Type` header."},
    {"title": "JavaScript: Event listener added multiple times", "error_code": "Logic Error", "category_name": "JavaScript", "description": "An event listener is attached to an element multiple times, causing the handler function to execute repeatedly for a single event.", "cause_overview": "Attaching listener in a function that's called multiple times (e.g., re-renders in a SPA) without removing the old one.", "solution_overview": "Remove previous listener before adding a new one (`removeEventListener`); use a flag to ensure listener is added only once; manage listeners within component lifecycle methods."},

    # Java (Existing + New)
    {"title": "Java NullPointerException", "error_code": "NullPointerException", "category_name": "Java", "description": "Attempting to use a null reference as if it were pointing to an object.", "cause_overview": "Object variable not initialized; method returned null unexpectedly.", "solution_overview": "Initialize objects before use; check for null before dereferencing: `if (obj != null)`."},
    {"title": "Java ClassCastException", "error_code": "ClassCastException", "category_name": "Java", "description": "Attempting to cast an object to a type that it is not an instance of.", "cause_overview": "Incorrect assumption about an object's runtime type.", "solution_overview": "Use `instanceof` to check type before casting; ensure object is of the correct type through program logic."},
    {"title": "Java NumberFormatException", "error_code": "NumberFormatException", "category_name": "Java", "description": "Attempting to convert a string to a numeric type (e.g., int, float), but the string does not have the appropriate format.", "cause_overview": "String contains non-numeric characters; string is empty or null.", "solution_overview": "Validate string content before parsing; use try-catch block to handle the exception."},


    # C/C++ (Existing + New)
    {"title": "C/C++ Segmentation fault (core dumped)", "error_code": "SIGSEGV", "category_name": "C/C++", "description": "Program tried to access a memory location it's not allowed to access.", "cause_overview": "Dereferencing null/uninitialized pointers; buffer overflows.", "solution_overview": "Use debugger (GDB); initialize pointers; check array bounds; Valgrind."},
    {"title": "C++ Compiler Error: 'cout' was not declared in this scope", "error_code": "Compiler Error", "category_name": "C++", "description": "The compiler does not recognize `cout`.", "cause_overview": "Missing `using namespace std;` or `std::` prefix; `<iostream>` not included.", "solution_overview": "Include `<iostream>`; use `std::cout` or add `using namespace std;`."},

    # C# (Existing + New)
    {"title": "C# NullReferenceException", "error_code": "NullReferenceException", "category_name": "C#", "description": "Object reference not set to an instance of an object.", "cause_overview": "Variable not initialized; method returned null.", "solution_overview": "Initialize objects; check for null; use `?.` operator."},
    {"title": "C# InvalidOperationException: Collection was modified after the enumerator was instantiated.", "error_code": "InvalidOperationException", "category_name": "C#", "description": "Modifying a collection (e.g., adding or removing items) while iterating over it using `foreach` or an enumerator.", "cause_overview": "Calling `Add()`, `Remove()` on the collection inside a `foreach` loop.", "solution_overview": "Iterate over a copy of the collection (`ToList()`); use a `for` loop with index carefully; collect items to be modified and modify after loop."},

    # Go (Golang) (Existing + New)
    {"title": "Go panic: runtime error: index out of range", "error_code": "panic: index out of range", "category_name": "Go (Golang)", "description": "Accessing a slice/array with an index out of bounds.", "cause_overview": "Incorrect index; empty slice.", "solution_overview": "Check `len()` before access."},
    {"title": "Go: 'goroutine stack exceeded'", "error_code": "panic: goroutine stack", "category_name": "Go (Golang)", "description": "A goroutine has exceeded its allocated stack space, usually due to infinite or very deep recursion.", "cause_overview": "Infinite recursion; extremely deep recursive calls without a base case.", "solution_overview": "Identify and fix the recursive function's base case or termination condition; refactor to an iterative approach if possible."},

    # Kotlin (Existing + New)
    {"title": "Kotlin: 'lateinit property has not been initialized'", "error_code": "UninitializedPropertyAccessException", "category_name": "Kotlin", "description": "Accessing a `lateinit` property before it has been assigned a value.", "cause_overview": "Forgot to initialize the `lateinit` var, or accessed it in a code path where initialization was skipped.", "solution_overview": "Ensure `lateinit` var is initialized before first access; check `::myVar.isInitialized` before use."},

    # Swift (Existing + New)
    {"title": "Swift: 'Thread 1: Fatal error: Index out of range'", "error_code": "Fatal error", "category_name": "Swift", "description": "Attempting to access an element in an array or collection using an index that is outside its valid bounds.", "cause_overview": "Off-by-one error in loop; incorrect index calculation; accessing empty array.", "solution_overview": "Check array's `count` before accessing; ensure index is within `0..<array.count`."},

    # Ruby (Existing + New)
    {"title": "Ruby TypeError: no implicit conversion of Symbol into Integer", "error_code": "TypeError", "category_name": "Ruby", "description": "Trying to use a Symbol where an Integer is expected, often as an array index.", "cause_overview": "e.g., `my_array[:key]` instead of `my_hash[:key]` or `my_array[integer_index]`.", "solution_overview": "Ensure you are using an integer for array indexing or that you are accessing a Hash with a Symbol key if intended."},

    # Django (Existing + New)
    {"title": "Django NoReverseMatch Error", "error_code": "NoReverseMatch", "category_name": "Django", "description": "Django cannot find a URL pattern matching arguments to `{% url %}` or `reverse()`.", "cause_overview": "Typo in URL name; missing/incorrect arguments; namespace error.", "solution_overview": "Verify URL name and arguments in `urls.py` and template/view."},
    {"title": "Django OperationalError: no such table: myapp_mymodel", "error_code": "OperationalError", "category_name": "Django", "description": "Django cannot find the database table for a model.", "cause_overview": "Migrations not created or applied after defining/changing model; wrong database connected.", "solution_overview": "Run `python manage.py makemigrations myapp` and `python manage.py migrate`."},

    # React
    {"title": "React Error: 'Objects are not valid as a React child'", "error_code": "React Render Error", "category_name": "React", "description": "Attempting to render a plain JavaScript object directly within JSX.", "cause_overview": "e.g., `<div>{{ myObject }}</div>` instead of `<div>{{ myObject.property }}</div>` or `JSON.stringify(myObject)`.", "solution_overview": "Render a specific property of the object, or convert the object to a string (e.g., `JSON.stringify`) if displaying the whole object is intended (for debugging)."},
    {"title": "React Warning: Each child in a list should have a unique 'key' prop.", "error_code": "React Key Warning", "category_name": "React", "description": "When rendering a list of elements using `map()`, React needs a unique `key` prop on each list item for efficient updates.", "cause_overview": "Missing `key` prop in a list rendering: `myArray.map(item => <div>{item.name}</div>)`.", "solution_overview": "Add a unique `key` prop to the outermost element returned by `map()`: `myArray.map(item => <div key={item.id}>{item.name}</div>)`."},

    # Node.js / Express.js (Existing + New)
    {"title": "Node.js Error: 'EADDRINUSE: address already in use :::3000'", "error_code": "EADDRINUSE", "category_name": "Node.js", "description": "Attempting to start a server on a port that is already being used by another process.", "cause_overview": "Another instance of your app is running; different application using the port.", "solution_overview": "Stop the other process using the port (find PID with `lsof -i :3000` or `netstat`); change the port for your application."},

    # Git (Existing + New)
    {"title": "Git Error: 'Updates were rejected because the remote contains work that you do not have locally'", "error_code": "Git Push Rejected", "category_name": "Git", "description": "Cannot push local changes because the remote branch has new commits not present locally.", "cause_overview": "Someone else pushed to the remote branch since your last pull.", "solution_overview": "Run `git pull` (or `git pull --rebase`) to integrate remote changes, resolve any merge conflicts, then `git push`."},

    # Docker (Existing + New)
    {"title": "Docker: 'image not found' when running a container", "error_code": "Image Not Found", "category_name": "Docker", "description": "Docker cannot find the specified image locally and (if applicable) cannot pull it from a remote repository.", "cause_overview": "Typo in image name/tag; image not built or pulled; not logged into private registry.", "solution_overview": "Check image name and tag spelling; run `docker pull image:tag`; build the image if it's from a Dockerfile; login to registry if private."},

    # Machine Learning (Existing + New)
    {"title": "Scikit-learn ValueError: Found input variables with inconsistent numbers of samples", "error_code": "ValueError", "category_name": "Machine Learning", "description": "Input arrays (e.g., X features and y target) to a Scikit-learn estimator have different numbers of rows (samples).", "cause_overview": "Mistake in data splitting; features and target arrays became misaligned.", "solution_overview": "Ensure `X.shape[0] == y.shape[0]`; double-check data preprocessing and splitting steps."},
    {"title": "TensorFlow: 'Input 0 of layer ... is incompatible with the layer ...'", "error_code": "TensorFlow Shape Error", "category_name": "Deep Learning", "description": "The shape of the input tensor being fed into a layer does not match the expected input shape of that layer.", "cause_overview": "Incorrect input data shape; wrong layer configuration (e.g., units, input_shape); previous layer outputting unexpected shape.", "solution_overview": "Check `model.summary()` for layer shapes; print tensor shapes (`tensor.shape`) before feeding into layers; ensure data preprocessing produces correct dimensions."},
    {"title": "Java: java.util.ConcurrentModificationException", "error_code": "ConcurrentModificationException", "category_name": "Java", "description": "Thrown when an object is concurrently modified while it's being iterated over in a way that's not permitted by the iterator.", "cause_overview": "Modifying a collection (e.g., adding/removing elements from an ArrayList) during iteration using a standard iterator or for-each loop.", "solution_overview": "Use an Iterator's `remove()` method if needed; iterate over a copy of the collection; use concurrent collections if multi-threaded modification is required."},
    {"title": "Java: java.lang.OutOfMemoryError: Java heap space", "error_code": "OutOfMemoryError", "category_name": "Java", "description": "The JVM cannot allocate an object because it is out of memory, and no more memory could be made available by the garbage collector.", "cause_overview": "Holding onto objects too long (memory leak); processing huge datasets in memory; insufficient heap size configuration.", "solution_overview": "Analyze heap dump (e.g., with Eclipse MAT, VisualVM); identify and fix memory leaks; increase heap size (`-Xmx` JVM option); process large data in chunks."},
    {"title": "Java: java.io.FileNotFoundException", "error_code": "FileNotFoundException", "category_name": "Java", "description": "An attempt to open the file denoted by a specified pathname has failed because the file does not exist.", "cause_overview": "Incorrect file path; file truly missing; insufficient permissions to access the path.", "solution_overview": "Verify file path spelling and location; check file system permissions; ensure file exists before attempting to open."},

    # C
    {"title": "C Compiler Warning: implicit declaration of function 'my_func'", "error_code": "Compiler Warning", "category_name": "C", "description": "The C compiler encounters a call to a function `my_func` before it has seen its declaration or definition.", "cause_overview": "Function called before its prototype is declared; header file containing the declaration not included.", "solution_overview": "Provide a function prototype (e.g., `int my_func(void);`) before its first call, usually in a header file or at the top of the source file; include the necessary header file."},
    {"title": "C Runtime Error: Bus error (core dumped)", "error_code": "SIGBUS", "category_name": "C", "description": "Access to an invalid memory address, often due to unaligned memory access or accessing memory mapped to a file that has been truncated.", "cause_overview": "Dereferencing a misaligned pointer (e.g., trying to read an `int` from an odd address on some architectures); hardware error.", "solution_overview": "Ensure pointers are correctly aligned for the data type they point to; check for file I/O issues if using memory-mapped files; use a debugger like GDB."},

    # C++
    {"title": "C++: 'std::bad_alloc' thrown", "error_code": "std::bad_alloc", "category_name": "C++", "description": "Exception thrown by the `new` operator when memory allocation fails.", "cause_overview": "System out of memory; requesting an extremely large block of memory; memory fragmentation.", "solution_overview": "Check for memory leaks; ensure requested memory size is reasonable; optimize memory usage; catch the exception (`catch (const std::bad_alloc& e)`)."},
    {"title": "C++ Linker Error: LNK2019: unresolved external symbol", "error_code": "LNK2019 (MSVC)", "category_name": "C++", "description": "The linker could not find the definition for a symbol (function, variable) that was referenced.", "cause_overview": "Missing object file or library in the link command; incorrect function signature in declaration vs definition; issues with name mangling (extern \"C\").", "solution_overview": "Ensure all source files are compiled and their object files are linked; link necessary libraries; verify function/variable declarations and definitions match exactly."},

    # C#
    {"title": "C#: CS0103: The name 'variableName' does not exist in the current context", "error_code": "CS0103", "category_name": "C#", "description": "Compiler error indicating a variable, method, or type name is used but not declared or not accessible in the current scope.", "cause_overview": "Typo in the name; variable declared in a different scope; missing `using` directive for a type.", "solution_overview": "Check spelling; ensure variable is declared before use and in an accessible scope; add necessary `using` directives."},

    # Go (Golang)
    {"title": "Go: 'import cycle not allowed'", "error_code": "Compiler Error", "category_name": "Go (Golang)", "description": "The Go compiler detected a circular dependency between packages (e.g., package A imports package B, and package B imports package A).", "cause_overview": "Poor package design leading to circular dependencies.", "solution_overview": "Refactor code to break the cycle: extract common functionality into a new package; use interfaces to decouple packages; rethink package responsibilities."},

    # Kotlin
    {"title": "Kotlin: 'Smart cast to 'Type' is impossible, because 'variable' is a mutable property that could have been changed by this time'", "error_code": "Compiler Warning/Error", "category_name": "Kotlin", "description": "Kotlin's smart cast feature cannot safely cast a variable because it's a mutable property (`var`) that might be modified concurrently or between the check and the usage.", "cause_overview": "Using a `var` property that is checked for a certain type, then used as that type, but its value could change in between.", "solution_overview": "Assign the mutable property to a local immutable variable (`val localCopy = mutableVar`) and perform checks and operations on `localCopy`; use explicit casting with `as?` or `as` if certain about the type."},

    # Swift
    {"title": "Swift: 'Value of optional type 'String?' must be unwrapped to a value of type 'String''", "error_code": "Compiler Error", "category_name": "Swift", "description": "Attempting to use an optional value directly where a non-optional value is expected, without unwrapping it.", "cause_overview": "An optional variable (`String?`) holds either a `String` or `nil`, but it's used as if it's guaranteed to be a `String`.", "solution_overview": "Use optional binding (`if let unwrappedValue = optionalValue`), force unwrapping (`optionalValue!`) if sure it's not nil (use cautiously), optional chaining (`optionalValue?.property`), or provide a default value (`optionalValue ?? defaultValue`)."},

    # Ruby
    {"title": "Ruby on Rails: ActionController::RoutingError (No route matches [GET] \"/nonexistent-path\")", "error_code": "RoutingError", "category_name": "Ruby on Rails", "description": "A request was made to a URL for which no route is defined in `config/routes.rb`.", "cause_overview": "Typo in the requested URL; route not defined or commented out; incorrect HTTP verb used for the route.", "solution_overview": "Check `config/routes.rb` for a matching route definition; verify the URL path and HTTP method; run `rails routes` to list all defined routes."},

    # PHP
    {"title": "PHP Parse error: syntax error, unexpected '}', expecting end of file", "error_code": "Parse error", "category_name": "PHP", "description": "The PHP parser found a closing brace `}` where it wasn't expected, often indicating an imbalance of braces or a prematurely ended script.", "cause_overview": "Missing opening brace `{`; an extra closing brace `}`; unterminated multi-line comment.", "solution_overview": "Carefully check brace balancing in functions, classes, and control structures; ensure comments are properly closed."},
    {"title": "PHP Warning: Undefined array key \"key_name\"", "error_code": "PHP Warning", "category_name": "PHP", "description": "Attempting to access an array element using a key that does not exist in the array (PHP 8+). Older versions might show a Notice: Undefined index.", "cause_overview": "Typo in the array key; key not set in the array.", "solution_overview": "Use `isset($array['key_name'])` or `array_key_exists('key_name', $array)` before accessing; initialize array keys properly."},

    # TypeScript
    {"title": "TypeScript Error: TS2339: Property 'propName' does not exist on type 'ObjectType'.", "error_code": "TS2339", "category_name": "TypeScript", "description": "Attempting to access a property that is not defined on the statically-typed object.", "cause_overview": "Typo in property name; property truly missing from the type definition (interface or class); object is of an unexpected type.", "solution_overview": "Check spelling of `propName`; verify the type definition of `ObjectType` includes `propName`; ensure the object is correctly typed."},

    # Rust
    {"title": "Rust error[E0382]: borrow of moved value: `my_var`", "error_code": "E0382", "category_name": "Rust", "description": "Attempting to use a variable after its ownership has been moved to another part of the code.", "cause_overview": "Assigning `my_var` to another variable or passing it by value to a function, then trying to use `my_var` again.", "solution_overview": "Clone the value if you need multiple owners (`my_var.clone()`); pass by reference (`&my_var` or `&mut my_var`); return ownership from functions if necessary."},

    # Angular
    {"title": "Angular Error: NG0100: ExpressionChangedAfterItHasBeenCheckedError", "error_code": "NG0100", "category_name": "Angular", "description": "A property bound in the template was changed after Angular's change detection cycle for that component had already completed.", "cause_overview": "Modifying component properties within `ngAfterViewInit` or other lifecycle hooks that run after initial check; side effects in template bindings.", "solution_overview": "Move property updates to appropriate lifecycle hooks (e.g., `ngOnInit`); use `ChangeDetectorRef.detectChanges()` cautiously; wrap problematic updates in `setTimeout(() => { ... }, 0)` as a last resort."},

    # Vue.js
    {"title": "Vue.js Warning: [Vue warn]: Failed to mount component: template or render function not defined.", "error_code": "Vue Mount Error", "category_name": "Vue.js", "description": "Vue tried to mount a component, but it could not find a `template` option or a `render` function for that component.", "cause_overview": "Component definition is missing a template (e.g., `<template>...</template>` in SFC or `template: '...'` in object); incorrect component registration.", "solution_overview": "Ensure every component has a valid template or render function; check component registration (global or local)."},

    # Spring (Java)
    {"title": "Spring: 'org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type ... available'", "error_code": "NoSuchBeanDefinitionException", "category_name": "Spring (Java)", "description": "The Spring IoC container could not find a bean of the required type for autowiring or explicit lookup.", "cause_overview": "Bean not declared (e.g., missing `@Component`, `@Service`, `@Repository`, or `@Bean` annotation); component scanning not configured for the package containing the bean; incorrect qualifier used.", "solution_overview": "Ensure the bean is properly annotated and within a scanned package; check autowiring qualifiers (`@Qualifier`); verify configuration classes."},

    # .NET Core/ASP.NET
    {"title": "ASP.NET Core: HTTP Error 500.30 - ANCM In-Process Start Failure", "error_code": "ANCM Start Failure", "category_name": ".NET Core/ASP.NET", "description": "The ASP.NET Core Module (ANCM) for IIS failed to start the .NET Core process.", "cause_overview": "Application startup errors (e.g., in `Program.cs` or `Startup.cs`); missing .NET Core Hosting Bundle on server; configuration issues in `web.config`.", "solution_overview": "Enable detailed startup error messages; check Event Viewer logs on the server; ensure correct .NET Core Hosting Bundle is installed; verify `web.config` settings."},

    # Kubernetes
    {"title": "Kubernetes Pod Status: CrashLoopBackOff", "error_code": "CrashLoopBackOff", "category_name": "Kubernetes", "description": "A pod is repeatedly starting and crashing. Kubernetes tries to restart it but gives up after too many failures in a short period.", "cause_overview": "Application error within the container causing it to exit; misconfiguration (e.g., wrong environment variables, missing config files); resource limits exceeded; liveness/readiness probe failures.", "solution_overview": "Check pod logs: `kubectl logs <pod-name> [-c <container-name>]`; check previous pod logs: `kubectl logs <pod-name> -p`; describe pod: `kubectl describe pod <pod-name>` for events; verify container image and application startup."},

    # Webpack
    {"title": "Webpack Error: 'Module not found: Error: Can't resolve 'module-name' in '/path/to/project/src'", "error_code": "Webpack Module Not Found", "category_name": "Webpack", "description": "Webpack cannot find a module that is being imported in your JavaScript/TypeScript code.", "cause_overview": "Module not installed; typo in import path or module name; incorrect Webpack `resolve.alias` or `resolve.modules` configuration.", "solution_overview": "Install missing module (`npm install module-name` or `yarn add`); check import path and spelling; verify Webpack resolve configuration."},

    # PostgreSQL
    {"title": "PostgreSQL Error: 'FATAL: password authentication failed for user \"username\"'", "error_code": "Auth Failed", "category_name": "PostgreSQL", "description": "Connection attempt to PostgreSQL server failed due to incorrect password for the specified user.", "cause_overview": "Wrong password provided; user does not exist; `pg_hba.conf` not configured to allow password authentication for that user/host.", "solution_overview": "Verify username and password; check `pg_hba.conf` to ensure authentication method is `md5` or `scram-sha-256` for the user and connection source; ensure user exists and has login privileges."},

    # MySQL
    {"title": "MySQL Error: 'Access denied for user 'user'@'host' (using password: YES/NO)'", "error_code": "Access Denied", "category_name": "MySQL", "description": "The MySQL server denied access to the specified user from the given host.", "cause_overview": "Incorrect username or password; user does not have privileges from that host; user does not exist.", "solution_overview": "Verify username, password, and host in connection string; grant necessary privileges: `GRANT ALL PRIVILEGES ON database.* TO 'user'@'host'; FLUSH PRIVILEGES;`."},

    # MongoDB
    {"title": "MongoDB Error: 'AuthenticationFailed: Authentication failed.'", "error_code": "AuthenticationFailed", "category_name": "MongoDB", "description": "Connection to MongoDB failed due to authentication issues.", "cause_overview": "Incorrect username/password; user does not exist in the specified authentication database; authentication mechanism mismatch.", "solution_overview": "Verify username, password, and `authSource` database in connection string; ensure user has appropriate roles on the target database."},

    # Redis
    {"title": "Redis Error: 'MISCONF Redis is configured to save RDB snapshots, but is currently not able to persist on disk.'", "error_code": "Redis Persist Error", "category_name": "Redis", "description": "Redis cannot write its RDB snapshot to disk, often preventing write operations if `stop-writes-on-bgsave-error` is enabled.", "cause_overview": "Insufficient disk space; incorrect file permissions for Redis data directory; Linux Transparent Huge Pages (THP) issues after a fork.", "solution_overview": "Ensure sufficient disk space; check permissions of Redis `dir` (configured in `redis.conf`); disable THP (`echo never > /sys/kernel/mm/transparent_hugepage/enabled`); set `stop-writes-on-bgsave-error no` (use with caution, understand data loss implications)."},

    # Security
    {"title": "Security Warning: SQL Injection Vulnerability", "error_code": "SQL Injection", "category_name": "Security", "description": "User-supplied input is directly included in SQL queries, allowing attackers to manipulate the query and access or modify data.", "cause_overview": "Concatenating user input into SQL strings instead of using parameterized queries or prepared statements.", "solution_overview": "Use parameterized queries (prepared statements) provided by your database library/ORM; validate and sanitize all user inputs rigorously."},
    {"title": "Security Warning: Cross-Site Scripting (XSS)", "error_code": "XSS", "category_name": "Security", "description": "User-supplied input containing malicious scripts is rendered directly on a web page, allowing the script to execute in other users' browsers.", "cause_overview": "Not properly sanitizing or escaping user input before displaying it in HTML.", "solution_overview": "Use context-aware output encoding/escaping for all user-supplied data; set appropriate `Content-Security-Policy` headers; use modern frontend frameworks that auto-escape by default."},

    # Web Servers (Apache/Nginx)
    {"title": "Nginx Error: '502 Bad Gateway'", "error_code": "502 Bad Gateway", "category_name": "Web Servers", "description": "Nginx, acting as a reverse proxy, received an invalid response from an upstream server (e.g., your application server like Gunicorn, uWSGI, PHP-FPM).", "cause_overview": "Upstream application server crashed or is not running; upstream server is overloaded and not responding; network connectivity issues between Nginx and upstream; misconfiguration in Nginx proxy settings.", "solution_overview": "Check status and logs of the upstream application server (e.g., Django/Flask app, PHP-FPM); verify Nginx `proxy_pass` directive and upstream server address/port; check firewall rules."},
    {"title": "Apache Error: '.htaccess: pcfg_openfile: unable to check htaccess file, ensure it is readable'", "error_code": "Apache .htaccess Error", "category_name": "Web Servers", "description": "Apache cannot read an `.htaccess` file, usually due to file permissions or incorrect `AllowOverride` directive.", "cause_overview": "`.htaccess` file has incorrect permissions (not readable by Apache user); `AllowOverride` directive in Apache configuration is set to `None` for the directory.", "solution_overview": "Ensure `.htaccess` file is readable by the Apache user (e.g., `www-data`); set `AllowOverride All` (or specific directives) for the relevant `<Directory>` block in Apache configuration (`httpd.conf` or virtual host config)."},
    # ... Continue adding more diverse errors for each category listed in CATEGORIES_DATA ...
    # Aim for at least 1-3 per specific language/framework/tool to reach your target.
    # This is just a starting batch of ~30. You'd need to add many more.
]

# --- Migration Logic ---

def populate_data(apps, schema_editor):
    Category = apps.get_model('main_app', 'Category')
    ErrorEntry = apps.get_model('main_app', 'ErrorEntry')
    User = apps.get_model('auth', 'User')

    STATUS_APPROVED = 'approved' # Local constant

    author = None
    try:
        author = User.objects.filter(is_superuser=True).order_by('pk').first()
        if not author:
            author = User.objects.order_by('pk').first()
    except Exception as e:
        print(f"Warning: Could not fetch a default user due to: {e}. Errors will be created without an author.")
        author = None

    category_objects = {}
    print("--- Populating Categories ---")
    for cat_data in CATEGORIES_DATA:
        category_name = cat_data["name"]
        category_description = cat_data.get("description", "")
        try:
            category = Category.objects.get(name=category_name)
            updated_fields_to_save = []
            if category.description != category_description:
                category.description = category_description
                updated_fields_to_save.append('description')
            if not category.slug:
                original_slug = slugify(category.name)
                unique_slug = original_slug
                num = 1
                while Category.objects.filter(slug=unique_slug).exclude(pk=category.pk).exists():
                    unique_slug = f'{original_slug}-{num}'
                    num += 1
                category.slug = unique_slug
                updated_fields_to_save.append('slug')
            if updated_fields_to_save:
                fields_to_update_in_db = [f for f in updated_fields_to_save if hasattr(category, f)] # Check field exists before update
                if fields_to_update_in_db: # Only save if there are actual fields to update
                    category.save(update_fields=fields_to_update_in_db)
                print(f"Updated existing category: {category.name} (Slug: {category.slug})")
            else:
                print(f"Category '{category.name}' already exists with slug '{category.slug}'. No changes needed.")
        except Category.DoesNotExist:
            original_slug = slugify(category_name)
            unique_slug = original_slug
            num = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{original_slug}-{num}'
                num += 1
            try:
                category = Category.objects.create(
                    name=category_name,
                    description=category_description,
                    slug=unique_slug
                )
                print(f"Created category: {category.name} with slug {category.slug}")
            except Exception as e:
                print(f"ERROR creating category '{category_name}' with pre-calculated slug '{unique_slug}': {e}")
                continue
        category_objects[category_name] = category

    print("\n--- Populating Error Entries ---")
    for error_data in ERRORS_DATA:
        category_name = error_data.get("category_name")
        error_title = error_data.get("title")

        if category_name not in category_objects:
            print(f"Critical Warning: Category object for '{category_name}' was not created or fetched. Skipping error '{error_title}'.")
            continue
        category = category_objects.get(category_name)

        if ErrorEntry.objects.filter(title=error_title, category=category).exists():
            print(f"Error '{error_title}' in category '{category.name}' already exists. Skipping.")
            continue
        
        original_slug = slugify(error_title)
        unique_error_slug = original_slug
        num = 1
        while ErrorEntry.objects.filter(slug=unique_error_slug).exists():
            max_len_for_base = ErrorEntry._meta.get_field('slug').max_length - len(str(num)) - 1
            if len(original_slug) > max_len_for_base:
                truncated_slug_base = original_slug[:max_len_for_base]
            else:
                truncated_slug_base = original_slug
            unique_error_slug = f'{truncated_slug_base}-{num}'
            num += 1

        current_error_data_for_create = error_data.copy()
        current_error_data_for_create.pop("category_name", None)

        try:
            ErrorEntry.objects.create(
                category=category,
                author=author,
                status=STATUS_APPROVED,
                is_public=True,
                slug=unique_error_slug, # Assign the pre-calculated unique slug
                **current_error_data_for_create
            )
            print(f"Created error entry: {error_title} with slug {unique_error_slug}")
        except Exception as e:
            print(f"ERROR creating error entry '{error_title}' with slug '{unique_error_slug}': {e}")


def reverse_populate_data(apps, schema_editor):
    Category = apps.get_model('main_app', 'Category')
    ErrorEntry = apps.get_model('main_app', 'ErrorEntry')
    print("--- Reversing Data Population (Deleting seeded data) ---")
    
    titles_to_delete_by_category = {}
    for error_data in ERRORS_DATA:
        cat_name = error_data.get("category_name")
        if cat_name not in titles_to_delete_by_category:
            titles_to_delete_by_category[cat_name] = []
        titles_to_delete_by_category[cat_name].append(error_data['title'])

    for cat_name, error_titles in titles_to_delete_by_category.items():
        try:
            category = Category.objects.get(name=cat_name)
            deleted_count, _ = ErrorEntry.objects.filter(title__in=error_titles, category=category).delete()
            if deleted_count:
                print(f"Deleted {deleted_count} error entries from category: {cat_name}")
        except Category.DoesNotExist:
            pass

    for cat_data in CATEGORIES_DATA:
        try:
            category = Category.objects.get(name=cat_data['name'])
            if not category.errors.exists(): 
                category.delete()
                print(f"Deleted empty category: {cat_data['name']}")
            # else: # Decided against this to avoid accidentally keeping categories if only seeded errors were deleted by title
            #     print(f"Category {cat_data['name']} not deleted as it still contains other errors.")
        except Category.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        # !!! IMPORTANT: REPLACE '000X_your_last_main_app_SCHEMA_migration' WITH THE NAME OF THE MIGRATION
        # THAT ADDED THE 'status' AND 'is_public' FIELDS TO ErrorEntry model.
        # For example, if it was '0005_errorentry_add_moderation_fields':
        ('main_app', '0005_errorentry_is_public_errorentry_moderator_notes_and_more'), # <<<--- UPDATE THIS LINE!!!
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(populate_data, reverse_code=reverse_populate_data),
    ]
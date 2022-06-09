# Rules for contributing code

## Documentation style
This project is using [doxygen](https://doxygen.nl/) for in-line documentation of the Python code. The configuration file for a doxygen run is shared in the repository. So please keep this in mind if you share code!

### What to document?

For an easier access to your code please document the following:
 1. every function/class method with all used parameters right after the header line:
    - purpose of the function/class method in the `@brief` section
    - more detailed how the function/class method is working in the `detailed` section.
    - the purpose (and type) of each parameter given (if not clear by given default values).
    - same with returned data if any.
 2. add a `@todo` section separated with `----` if the function/class method/class is not complete or you have plans on additional features.
 3. add a `@bug` section separated with `----` if you know of certain bug(s) in that function/class method/class you have not fixed yet.
 4. document each important variable/class attribute with it's data type and purpose.
 5. put in-line documentations in a separate line and **not** at the end of a line of code.
 6. if you are using a "one line comment" for optical separation of the code please use `#----- ` as prefix.

## Arranging the code

For better readability,  please note the following:

- 2 empty lines between classes/functions/class methods
- 1 empty line before each header of a block containing comand like `if`, `for`, `try` etc.
- 1 empty line after each (even logical) block.
- **avoid compact code** like one-liner `for`-blocks for better readability!

# Numeric Converter - cs1060-hw2-base

A web-based application that converts numbers between different formats including:
- English text (e.g., "one hundred twenty-three")
- Binary
- Octal
- Decimal
- Hexadecimal
- Base64

## Setup

1. Install the required dependencies. We recommend following the best Python practice of a virtual environment. (This assumes Python3.)
```bash
python3 -m venv "hw2-env"
. hw2-env/bin/activate
pip3 install -r requirements.txt
```

2. Run the application:
```bash
python api/index.py
```

3. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Enter your input value in the text box
2. Select the input format from the dropdown menu
3. Select the desired output format from the second dropdown menu
4. Click "Convert" to see the result

## Bug Fixes

1. **Negative Number Handling**
   - Fixed issue where negative numbers in text format (e.g., "negative forty-two") were not being properly parsed
   - Both "negative" and "minus" prefixes are now supported

2. **Number to Text Conversion**
   - Improved formatting of large numbers (e.g., 1000000 now correctly converts to "one million")
   - Fixed handling of compound numbers (e.g., "one hundred twenty-three")
   - Ensured consistent spacing and hyphenation in output text

3. **Base64 Conversion**
   - Fixed endianness issues in base64 number conversion
   - Added proper handling of negative numbers in base64 format
   - Improved error handling for invalid base64 inputs

4. **Input Validation**
   - Added better error messages for invalid inputs
   - Improved handling of edge cases (e.g., zero, very large numbers)
   - Fixed issues with numeric strings containing special characters

## Examples

- Convert decimal to binary: Input "42" with input type "decimal" and output type "binary"
- Convert text to decimal: Input "forty two" with input type "text" and output type "decimal"
- Convert negative numbers: Input "negative one hundred" with input type "text" and output type "decimal"
- Convert large numbers: Input "1234567" with input type "decimal" and output type "text"

# Deploying
The application should deploy to [Vercel](https://vercel.com?utm_source=github&utm_medium=readme&utm_campaign=vercel-examples)
out of the box.

Just Add New... > Project, import the Git repository, and off you go.
Note that Vercel's Hobby plan means your private repository needs to be
in your personal GitHub account, not the organizational account.

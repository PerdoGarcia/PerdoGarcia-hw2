from flask import Flask, render_template, request, jsonify
from num2words import num2words
from text2digits import text2digits
import base64
import re

app = Flask(__name__)

def text_to_number(text):
    """Convert English text number to integer"""
    if not isinstance(text, (str, int, float)):
        raise ValueError("Input must be a string or number")

    # First, try to convert if it's already a number string
    if isinstance(text, (int, float)):
        return int(text)

    text = str(text).lower().strip()
    if not text:
        raise ValueError("Empty input")

    # Try direct conversion first for numeric strings
    try:
        return int(text)
    except ValueError:
        pass

    # Special cases
    if text in ['zero', 'nil']:
        return 0

    # Dictionary for number words
    number_words = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
        'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
        'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
        'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
    }

    # Handle hyphenated numbers (e.g., twenty-one, forty-two)
    if '-' in text:
        parts = text.split('-')
        try:
            return sum(text_to_number(part) for part in parts if part)
        except ValueError:
            pass  # Try other methods if hyphen parsing fails

    # Handle simple numbers
    if text in number_words:
        return number_words[text]

    # Try using text2digits for more complex numbers
    try:
        t2d = text2digits.TextToDigits()
        result = t2d.convert(text)
        if result != text:  # If conversion happened
            return int(result)
    except:
        pass  # Fall through to manual parsing

    # Manual parsing for compound numbers (e.g., one hundred five)
    words = [w for w in re.findall(r'\w+', text) if w not in ['and', 'a']]
    if not words:
        raise ValueError("No valid number words found")

    # Check for invalid words
    valid_words = set(number_words.keys()) | {'hundred', 'thousand', 'million', 'billion'}
    for word in words:
        if word not in valid_words:
            raise ValueError(f"Invalid number word: {word}")

    # Convert words to numbers
    result = 0
    current = 0

    for word in words:
        if word == 'hundred':
            current *= 100
        elif word == 'thousand':
            current *= 1000
            result += current
            current = 0
        elif word == 'million':
            current *= 1000000
            result += current
            current = 0
        elif word == 'billion':
            current *= 1000000000
            result += current
            current = 0
        else:
            current += number_words[word]

    result += current

    if result == 0:
        raise ValueError("Unable to convert text to number")

    return result

def number_to_text(number):
    """Convert integer to English text"""
    try:
        # Convert string input to integer
        if isinstance(number, str):
            try:
                number = int(number)
            except ValueError:
                raise ValueError("Invalid number format")

        # Use num2words and replace 'minus' with 'negative' for consistency
        text = num2words(number)
        return text.replace('minus', 'negative')
    except Exception as e:
        raise ValueError(f"Unable to convert number to text: {str(e)}")

def base64_to_number(b64_str):
    """Convert base64 to integer using little-endian byte order"""
    try:
        decoded_bytes = base64.b64decode(b64_str)
        return int.from_bytes(decoded_bytes, byteorder='little', signed=True)
    except:
        raise ValueError("Invalid base64 input")

def number_to_base64(number):
    """Convert integer to base64 using little-endian byte order"""
    try:
        # Handle zero case
        if number == 0:
            return base64.b64encode(b'\x00').decode('utf-8')

        # Calculate minimum number of bytes needed
        byte_count = (number.bit_length() + 7) // 8
        # Ensure at least 1 byte for small numbers
        byte_count = max(1, byte_count)

        # Convert to bytes with little-endian and signed=True to handle negatives
        number_bytes = number.to_bytes(byte_count, byteorder='little', signed=True)
        return base64.b64encode(number_bytes).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Unable to convert to base64: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        if not data or 'input' not in data or 'inputType' not in data or 'outputType' not in data:
            return jsonify({'error': 'Missing required fields: input, inputType, outputType'}), 400
            
        input_value = data['input']
        input_type = data['inputType']
        output_type = data['outputType']
        
        # Validate input value is not empty
        if input_value is None or (isinstance(input_value, str) and not input_value.strip()):
            return jsonify({'error': 'Input value cannot be empty'}), 200
        
        # Convert input to number
        try:
            if input_type == 'text':
                number = text_to_number(input_value)
            elif input_type == 'decimal':
                number = int(input_value)
            elif input_type == 'binary':
                number = int(str(input_value), 2)
            elif input_type == 'octal':
                number = int(str(input_value), 8)
            elif input_type == 'hex':
                number = int(str(input_value), 16)
            elif input_type == 'base64':
                number = base64_to_number(input_value)
            else:
                return jsonify({'error': 'Invalid input type'}), 400
        except ValueError as e:
            # Return 200 with error message as per test expectations
            return jsonify({'error': str(e)}), 200
        
        # Convert number to output type
        try:
            if output_type == 'text':
                result = number_to_text(number)
            elif output_type == 'decimal':
                result = str(number)
            elif output_type == 'binary':
                result = bin(int(number))[2:]  # Convert to int first to handle negative numbers
            elif output_type == 'octal':
                result = oct(int(number))[2:]  # Convert to int first to handle negative numbers
            elif output_type == 'hex':
                result = hex(int(number))[2:].lower()  # Convert to lowercase for consistency
            elif output_type == 'base64':
                result = number_to_base64(number)
            else:
                return jsonify({'error': 'Invalid output type'}), 400
        except Exception as e:
            return jsonify({'error': f'Error converting to {output_type}: {str(e)}'}), 200
        
        return jsonify({'result': result})
        
    except Exception as e:
        # Catch any unexpected errors
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

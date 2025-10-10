#!/usr/bin/env python
"""
Command-line interface for soft404 package.

Usage:
    python -m soft404 <html_file>
    python -m soft404 --help
"""
import argparse
import sys


def main():
    from soft404 import probability

    parser = argparse.ArgumentParser(
        description='Predict probability that an HTML page is a soft 404 page.',
        epilog='For training and data conversion, use soft404-train and soft404-convert commands.'
    )
    parser.add_argument(
        'html_file',
        nargs='?',
        help='Path to HTML file to analyze (or use --html for inline HTML)'
    )
    parser.add_argument(
        '--html',
        help='HTML content as a string'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.5,
        help='Probability threshold for classification (default: 0.5)'
    )
    
    args = parser.parse_args()

    # Get HTML content
    if args.html:
        html = args.html
    elif args.html_file:
        try:
            with open(args.html_file, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.html_file}' not found", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 1
    else:
        parser.print_help()
        return 1

    # Predict
    try:
        prob = probability(html)
        is_soft_404 = prob >= args.threshold
        
        print(f"Probability: {prob:.4f}")
        print(f"Classification: {'Soft 404' if is_soft_404 else 'Valid page'}")
        
        return 0 if not is_soft_404 else 1
    except Exception as e:
        print(f"Error during prediction: {e}", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())

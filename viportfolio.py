#!/usr/bin/env python3

import argparse

def create_portfolio(args):
    """
    Сreate an optimal portfolio of assets and print it to stdout
    :param args:
    :return: 0 - Ok, 1- Error
    """
    print(args)
    pass

def analyze_portfolio(args):
    """
    Analyze mutual fund portfolios and print report to stdout
    :param args:  arguments for analyze portfolios
    :return: 0 - Ok, 1- Error
    """
    print(args)
    pass

def describe_(args):
    """
    Describe assets of universe and covered mutual funds and print report to stdout
    :param args:  arguments for describe
    :return: 0 - Ok, 1- Error
    """
    print(args)
    pass


def main():

    parser = argparse.ArgumentParser(description="Viportfolio help to analyze and create optimal portfolio \
                                                    (\'Markowitz porfolio\') of assets",
                                     prog='Viportfolio')

    # setup universe
    parser.add_argument('u', type=str, default='ru',
                       choices=['ru', 'em', 'us', 'cn', 'eu', 'all'],
                       help='universe of assets to analyze  (default: %(default)s)')

    subparsers = parser.add_subparsers() # required=True

    # create subcommand

    parser_create = subparsers.add_parser('create', help='calculate asset weights for portfolio')
    parser_create.add_argument('-t','--type', type=str,
                               choices=['optimal', 'maxsharpe'],
                               default='optimal',
                               help='type of creating portfolio (default: %(default)s)) ')
    parser_create.add_argument('-r','--return', type=float, default=0.2,
                               help='expected return for \'Markowitz portfolio\' (default: %(default)s))',  metavar='X.XX')

    parser_create.add_argument('-p','--period', type=int, default=12,
                               help='observation period in months  (default: %(default)s))', metavar='XX'
                               )

    parser_create.add_argument('-d','--depo', type=float, default=1000000,  metavar='XXX',
                                help='deposit value (default: %(default)s))')

    parser_create.set_defaults(func=create_portfolio)

    # analyze subcommand
    parser_analyze = subparsers.add_parser('analyze', help='analyze asset weights in mutual fund portfolios')
    parser_analyze.add_argument('-m','--mutualfund', type=str,
                                default='all',
                                help='mutual funds to analyze',
                                metavar='fund')
    parser_analyze.add_argument('-f','--file', nargs=2, help='files to analize',
                                metavar=('fileXXX.csv','fileYYY.csv'))
    parser_analyze.add_argument('-p','--period', type=int, default=1,
                                help='period fo analize in months (default: %(default)s)',
                                 metavar='X')
    parser_analyze.set_defaults(func=analyze_portfolio)

    # describe subcommand
    parser_describe = subparsers.add_parser('describe', help='desribe assets and mutual funds for current universe')

    parser_describe.set_defaults(func=describe_)


    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        print( "usage: \n\tviportfolio [-h] {ru,em,us,cn,eu,all} {create,analyze,describe}\n\
        (choose from 'create', 'analyze', 'describe')")

if __name__ == "__main__":
    main()

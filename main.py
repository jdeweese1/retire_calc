import locale
from argparse import ArgumentParser, Namespace
from typing import Union

from config import Config
from finance_models import (compound_interest, get_savings_through_retirement,
                            tvm_factor)

locale.setlocale(locale.LC_ALL, 'en_US')


def to_currency(n: int):
    return locale.currency(n, grouping=True)


def run_retirement_simulation(parsed_args: Union[None, Namespace]):
    cfg = Config()
    cfg.overwrite_with_cli_args(parsed_args)  # If parsed_args is populated, it holds the cli args, which should supersede those read in by the Config constructor
    print(
        f'Config\nRetiring at : {cfg.retirement_age}\nyearly salary to be {to_currency(cfg.cur_yearly_salary)}\nannual contribution {to_currency(cfg.yearly_retirement_contribution_ratio)}')
    print('\n')

    print(
        f'TVM of $1 today is {tvm_factor(r=cfg.yearly_investment_return_during_career, years=cfg.years_until_retirement, periods_per_year=4)}')

    yearly_retirement_contribution_gen = cfg.get_yearly_retirement_contribution_gen()
    money_saved_at_end_of_career = compound_interest(
        p=cfg.upfront_investment, rate=cfg.yearly_investment_return_during_career, years=cfg.years_until_retirement,
        annual_addition=yearly_retirement_contribution_gen)
    print(
        f'With {to_currency(money_saved_at_end_of_career)} you could live until age of {cfg.retirement_age + money_saved_at_end_of_career / cfg.yearly_retirement_stipend}')

    print(
        f'''Amount of money saved by age {cfg.retirement_age} would be {to_currency(
            compound_interest(
                p=cfg.upfront_investment,
                rate=cfg.yearly_investment_return_during_career,
                years=cfg.years_until_retirement,
                periods_per_year=4,
                annual_addition=cfg.get_yearly_retirement_contribution_gen()))} with annual addition of {cfg.yearly_retirement_contribution_ratio} for {cfg.years_until_retirement} years, so total money put in would be''')
    counter = range(0, cfg.years_until_retirement)
    g = cfg.get_yearly_retirement_contribution_gen()
    cost_basis_saved = 0
    for _ in counter:
        cost_basis_saved += next(g)

    print(f'''{to_currency(cost_basis_saved)} + init of {cfg.upfront_investment}''')

    print(
        f'If you entered retirement with {to_currency(money_saved_at_end_of_career)}')
    for item in get_savings_through_retirement(savings_beginning_retirement=money_saved_at_end_of_career, cfg=cfg):
        print(
            f'At age {item.age} money in bank will be {to_currency(item.savings)} which is {round(item.pct_of_original, 2)}% of original')


parser = ArgumentParser()
parser.add_argument('--config-file', '-cf', type=str, help='The config file to read settings for the retirement calculation. Defaults to config.yaml')
parser.add_argument('--write-default-config-to', '-wct', help='Writes a sample config file for the retirement calculator to the specified file.')
parser.add_argument('--birth_year', '-by', type=int, help='Birth year of the individual')
parser.add_argument('--life_span', '-ls', type=int, help='How long the individual expects to live ex. 100')
parser.add_argument('--retirement_age', '-ra', type=int, help='The age at which the individual expects to retire at')
parser.add_argument('--cur_yearly_salary', '-cys', type=float, help='The current yearly income of the individual')
parser.add_argument('--yearly_salary_increase_pct', '-ysip', type=float, help='Percent at which the individual expects their income to increase each year. To denote a 1%% increase in income, enter .01')
parser.add_argument('--yearly_investment_return_during_career', '-yirdc', type=float, help='Percent return the individual expects investments to appreciate each year during their career. An 8%% return would be denoted as .08')
parser.add_argument('--yearly_investment_return_during_retirement', '-yirdr', type=float, help='Percent return the individual expects investments to appreciate each year during retirement. A 4%% return would be denoted as .04')
parser.add_argument('--upfront_investment', '-ui', type=float, help='The amount in investments the individual currently holds.')
parser.add_argument('--yearly_retirement_contribution_ratio', '-yrcr', type=float, help='The portion of the individual\'s income that is saved for retirement during their career. Saving 1/3 of income would be denoted by .33')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.write_default_config_to:
        Config.write_default_config(filepath=args.write_default_config_to)
    else:
        run_retirement_simulation(args)

import locale
from argparse import ArgumentParser

from config import Config
from finance_models import (compound_interest, get_savings_through_retirement,
                            tvm_factor)

locale.setlocale(locale.LC_ALL, 'en_US')


def to_currency(n: int):
    return locale.currency(n, grouping=True)


def run_retirement_simulation():
    cfg = Config()
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
parser.add_argument('--config-file', type=str)
parser.add_argument('--write-default-config-to', help='Writes a sample config file for the retirement calculator to the specified file.')
if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    if args.write_default_config_to:
        Config.write_default_config(filepath=args.write_default_config_to)
    else:
        run_retirement_simulation()

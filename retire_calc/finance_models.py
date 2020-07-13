import itertools
import locale
from argparse import Namespace
from collections import namedtuple
from typing import Iterable, Union

from config import Config


def get_savings_through_retirement(savings_beginning_retirement, cfg: Config) -> None:
    stipend = cfg.yearly_retirement_stipend

    tmp_age = cfg.retirement_age
    tmp_money = savings_beginning_retirement
    SavingsObj = namedtuple(typename='SavingsObj', field_names=(
        'age', 'savings', 'pct_of_original'))
    while tmp_age < cfg.life_span:
        yield SavingsObj(age=tmp_age, savings=tmp_money, pct_of_original=100 * tmp_money / savings_beginning_retirement)
        tmp_money -= stipend
        tmp_money *= 1 + cfg.yearly_investment_return_during_retirement
        tmp_age += 1


# https://stackoverflow.com/a/21544322
def compound_interest(p: int, rate: float, years: int, periods_per_year: int = 4, annual_addition: Union[int, Iterable[int]] = 0) -> float:
    """

    Calculates compound interest, roughly according to the formula 𝐴=𝑃(1+𝑟/𝑛)**(𝑛𝑡)
    :param p: Principal amount of money the investment begins it's life with.
    :param rate: Annual appreciation interest rate of investment. This should be positive and between 0 and 1. 10% interest would be denoted as .1
    :param years: How many years until the investment matures.
    :param periods_per_year: The number of periods per year that the interest will be compounded. Once every quarter would be denoted as 4
    :param annual_addition: The amount of money that will be added to the portfolio on a yearly basis. This may be an number, or it could be a iterator like object that will that yields the amount of money that will be added for the corresponding year. This is useful, because as you get further in your career, you will likely add a different amount of money to your portfolio.
    :return: Float that denotes the final value of the investment.
    """

    assert 0 <= rate <= 1
    assert periods_per_year >= 1
    r_div_n = rate / periods_per_year
    nt = periods_per_year * years

    # TODO Not sure if annual addition formula is correct
    base_wo_annual_addition = p * ((1 + r_div_n) ** nt)

    if type(annual_addition) in [int, float]:
        assert annual_addition >= 0
        if annual_addition == 0:
            return base_wo_annual_addition
        annual_contribution_gen = itertools.repeat(annual_addition)
    elif isinstance(annual_addition, Iterable):
        annual_contribution_gen = annual_addition
    else:
        raise Exception

    contribution_per_period_gen = (
        this_year_contribution / periods_per_year for this_year_contribution in annual_contribution_gen)
    monthly_contribution_iter = iter(
        next(contribution_per_period_gen) * (1 + r_div_n) ** i for i in range(0, nt))
    with_annual_addition = sum(monthly_contribution_iter)
    return base_wo_annual_addition + with_annual_addition


def tvm_factor(r, years, periods_per_year):
    return compound_interest(p=1, rate=r, years=years, periods_per_year=periods_per_year)


def to_currency(n: int):
    return locale.currency(n, grouping=True)


def run_retirement_simulation(parsed_args: Union[None, Namespace]):
    cfg = Config()
    cfg.overwrite_with_cli_args(parsed_args)  # If parsed_args is populated, it holds the cli args, which should supersede those read in by the Config constructor
    print(
        f'Config\nRetiring at : {cfg.retirement_age}\nyearly salary to be {to_currency(cfg.cur_yearly_salary)}\nannual contribution {to_currency(cfg.yearly_retirement_contribution_ratio)}')
    print('\n')

    print(
        f'TVM of $1 today is {tvm_factor(r=cfg.yearly_investment_return_during_career, years=cfg.years_until_retirement, periods_per_year=4)} with {cfg.years_until_retirement} years to grow')

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
        if item.age % 5 ==0:

            print(f'At age {item.age} money in bank will be {to_currency(item.savings)} which is {round(item.pct_of_original, 2)}% of what it was at the beginning of retirement.')

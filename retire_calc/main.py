import locale
from argparse import ArgumentParser

from retire_calc import Config
from finance_models import (run_retirement_simulation)

am_locale = locale.getlocale()
locale.setlocale(category=locale.LC_ALL, locale=am_locale)

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
        cfg = Config()
        if args.config_file:
            cfg = Config.from_yaml(args.config_file)

        cfg.overwrite_with_cli_args(args)
        run_retirement_simulation(cfg)
